"""
Multimodal Gemini Client & Resilient Fallback Engine.
Supports both `google.genai` (v1 SDK) and `google.generativeai` (legacy SDK)
with automated graceful degradation to deterministic simulation mode when keys are absent or invalid.
"""

import os
import json
import re
import io
import logging
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

logger = logging.getLogger(__name__)

# Feature Flags for SDK availability
HAS_GENAI_V1 = False
HAS_GENAI_LEGACY = False

try:
    from google import genai
    from google.genai import types
    HAS_GENAI_V1 = True
except ImportError:
    HAS_GENAI_V1 = False

try:
    import google.generativeai as legacy_genai
    HAS_GENAI_LEGACY = True
except ImportError:
    HAS_GENAI_LEGACY = False


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Safely extracts JSON from model response text or markdown blocks."""
    if not text:
        return None
        
    text = text.strip()
    
    # 1. Try markdown code block extraction
    json_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if json_block_match:
        try:
            return json.loads(json_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass
            
    # 2. Try raw JSON substring from first '{' to last '}'
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_candidate = text[start_idx:end_idx + 1]
        try:
            return json.loads(json_candidate)
        except json.JSONDecodeError:
            pass
            
    # 3. Direct JSON load attempt
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


class GeminiEngine:
    """Wrapper that seamlessly switches between Gemini 2.5/1.5 live execution and mock simulation."""
    
    def __init__(self, api_key: Optional[str] = None, preferred_model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
        self.preferred_model = preferred_model
        self.client_v1 = None
        
        if self.api_key:
            if HAS_GENAI_V1:
                try:
                    self.client_v1 = genai.Client(api_key=self.api_key)
                except Exception as e:
                    logger.warning(f"Failed to initialize google.genai v1 client: {e}")
            elif HAS_GENAI_LEGACY:
                try:
                    legacy_genai.configure(api_key=self.api_key)
                except Exception as e:
                    logger.warning(f"Failed to configure legacy genai: {e}")
                    
    @property
    def is_live_ready(self) -> bool:
        """Returns True if a non-empty API key is configured."""
        return bool(self.api_key and self.api_key.strip())

    def analyze_image_multimodal(
        self,
        image_input,
        prompt: str,
        system_instruction: Optional[str] = None,
        fallback_data_generator=None
    ) -> Tuple[Dict[str, Any], bool, str]:
        """
        Analyzes an image using Gemini Multimodal Vision API.
        
        Args:
            image_input: PIL Image or bytes or file path
            prompt: User instructions
            system_instruction: System prompt
            fallback_data_generator: Callable returning dict if API fails/not configured
            
        Returns:
            Tuple[Dict[str, Any], is_live_mode: bool, message: str]
        """
        # Ensure image is in PIL format
        pil_img = None
        if isinstance(image_input, Image.Image):
            pil_img = image_input
        elif isinstance(image_input, (bytes, bytearray)):
            pil_img = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, str) and os.path.exists(image_input):
            pil_img = Image.open(image_input)
            
        # If no API key is provided, execute fallback immediately
        if not self.is_live_ready:
            fallback = fallback_data_generator() if fallback_data_generator else {
                "status": "Demonstration Mode",
                "message": "No API key supplied. Running deterministic simulation engine."
            }
            return fallback, False, "Demo Mode: Running with pre-calibrated engineering models (add API Key in sidebar for Live Gemini Vision)."
            
        # Try Live Calling using GenAI v1 SDK first
        raw_text = None
        last_error = None
        
        if HAS_GENAI_V1 and self.client_v1 and pil_img:
            try:
                # Convert PIL image to bytes for GenAI client
                buf = io.BytesIO()
                pil_img.save(buf, format="PNG")
                img_bytes = buf.getvalue()
                
                response = self.client_v1.models.generate_content(
                    model=self.preferred_model,
                    contents=[
                        types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction or "You are an expert structural engineer and construction safety auditor.",
                        temperature=0.2,
                    )
                )
                raw_text = response.text
            except Exception as e:
                last_error = str(e)
                logger.error(f"GenAI V1 execution error: {e}")
                
        # Try Legacy GenAI SDK if V1 failed or was not available
        if raw_text is None and HAS_GENAI_LEGACY and self.is_live_ready and pil_img:
            try:
                legacy_genai.configure(api_key=self.api_key)
                model = legacy_genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                response = model.generate_content([pil_img, prompt])
                raw_text = response.text
            except Exception as e:
                last_error = str(e)
                logger.error(f"Legacy GenAI execution error: {e}")
                
        # If response received, parse JSON
        if raw_text:
            parsed = extract_json_from_text(raw_text)
            if parsed:
                return parsed, True, "Live Gemini Vision Analysis Successful."
            else:
                # Text was returned but was not pure JSON; wrap it
                return {
                    "raw_analysis": raw_text,
                    "parse_warning": "Model returned unstructured text, formatted below."
                }, True, "Live Gemini Vision completed (Unstructured response wrapped)."
                
        # If live call failed (e.g. invalid key, quota, blocked network), gracefully fall back
        fallback = fallback_data_generator() if fallback_data_generator else {
            "error": "Failed to query Gemini API",
            "details": last_error
        }
        return fallback, False, f"Live call failed ({last_error or 'Network/Quota'}). Reverted to high-fidelity fallback simulation."

    def generate_chat_response(
        self,
        history: List[Dict[str, str]],
        user_message: str,
        system_instruction: str,
        fallback_responder=None
    ) -> Tuple[str, bool]:
        """
        Executes multi-turn conversation with Gemini or domain fallback.
        
        Returns:
            Tuple[response_text: str, is_live: bool]
        """
        if not self.is_live_ready:
            resp = fallback_responder(user_message) if fallback_responder else (
                "I am running in Demonstration Mode. Please supply a Google Gemini API Key in the sidebar "
                "for live multi-turn reasoning with Gemini 2.5."
            )
            return resp, False
            
        # Try GenAI V1
        if HAS_GENAI_V1 and self.client_v1:
            try:
                # Format contents
                contents = []
                for msg in history:
                    role = "user" if msg.get("role") == "user" else "model"
                    contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.get("content", ""))]))
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))
                
                resp = self.client_v1.models.generate_content(
                    model=self.preferred_model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3
                    )
                )
                return resp.text, True
            except Exception as e:
                logger.warning(f"GenAI V1 chat failed: {e}")
                
        # Try Legacy GenAI
        if HAS_GENAI_LEGACY and self.is_live_ready:
            try:
                legacy_genai.configure(api_key=self.api_key)
                model = legacy_genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                # Build chat session
                chat = model.start_chat(history=[])
                for msg in history:
                    if msg.get("role") == "user":
                        chat.history.append({"role": "user", "parts": [msg.get("content", "")]})
                    elif msg.get("role") == "assistant":
                        chat.history.append({"role": "model", "parts": [msg.get("content", "")]})
                        
                resp = chat.send_message(user_message)
                return resp.text, True
            except Exception as e:
                logger.warning(f"Legacy GenAI chat failed: {e}")
                
        # Fallback responder
        resp = fallback_responder(user_message) if fallback_responder else (
            "Demonstration Mode Fallback: Gemini API call failed. "
            "Please ensure your API key has quota enabled for Gemini 1.5/2.5."
        )
        return resp, False
