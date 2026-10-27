"""
Sample image generator for Multimodal Construction Intelligence Platform.
Generates realistic schematic test images for PPE Safety Audits and Crack Diagnostics.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

def generate_sample_assets(output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Sample PPE Site Photo (Scaffolding Hazard)
    ppe_path = os.path.join(output_dir, "sample_site_ppe_hazard.png")
    if not os.path.exists(ppe_path):
        img = Image.new("RGB", (800, 600), color=(220, 230, 240))
        draw = ImageDraw.Draw(img)
        
        # Ground and sky
        draw.rectangle([0, 0, 800, 420], fill=(135, 185, 225))  # Sky
        draw.rectangle([0, 420, 800, 600], fill=(160, 140, 110))  # Ground earth
        
        # Partially constructed building structure
        draw.rectangle([100, 120, 700, 450], fill=(175, 180, 185), outline=(100, 105, 110), width=4)
        for floor_y in [120, 220, 320, 420]:
            draw.line([(100, floor_y), (700, floor_y)], fill=(80, 80, 85), width=6)
        for col_x in [100, 250, 400, 550, 700]:
            draw.line([(col_x, 120), (col_x, 450)], fill=(70, 75, 80), width=8)
            
        # Scaffolding on the right
        draw.line([(520, 100), (520, 450)], fill=(210, 160, 40), width=4)
        draw.line([(680, 100), (680, 450)], fill=(210, 160, 40), width=4)
        for scaffold_y in range(120, 450, 60):
            draw.line([(520, scaffold_y), (680, scaffold_y)], fill=(190, 140, 30), width=3)
            draw.line([(520, scaffold_y), (680, scaffold_y + 60)], fill=(160, 120, 20), width=2)
            
        # Worker 1: On ground, compliant (Helmet, Hi-Vis Orange Vest, Boots)
        # Head & Yellow Helmet
        draw.ellipse([270, 360, 290, 380], fill=(240, 200, 160))
        draw.chord([267, 355, 293, 375], start=180, end=360, fill=(255, 215, 0)) # Yellow Hard Hat
        # Torso & Orange Hi-Vis Vest
        draw.rectangle([270, 380, 290, 415], fill=(255, 102, 0)) # Orange Vest
        draw.line([(275, 385), (275, 415)], fill=(230, 230, 230), width=2) # Reflective stripe
        draw.line([(285, 385), (285, 415)], fill=(230, 230, 230), width=2)
        # Legs & Steel Toe Boots
        draw.rectangle([272, 415, 279, 445], fill=(40, 50, 90)) # Jeans
        draw.rectangle([281, 415, 288, 445], fill=(40, 50, 90))
        draw.rectangle([270, 445, 280, 452], fill=(30, 30, 30)) # Black Boots
        draw.rectangle([281, 445, 291, 452], fill=(30, 30, 30))
        
        # Worker 2: Upper Scaffold Tier (Level 3 - Y: 180), NON-COMPLIANT
        # Missing harness, missing helmet, no tie-off!
        draw.ellipse([580, 175, 600, 195], fill=(160, 110, 80)) # Head without helmet!
        draw.rectangle([580, 195, 600, 230], fill=(120, 120, 130)) # Plain grey shirt (NO VEST)
        draw.rectangle([582, 230, 589, 255], fill=(60, 60, 70))
        draw.rectangle([591, 230, 598, 255], fill=(60, 60, 70))
        
        # Warning bounding box overlay on Worker 2
        draw.rectangle([565, 165, 615, 265], outline=(220, 38, 38), width=3)
        draw.rectangle([565, 145, 670, 165], fill=(220, 38, 38))
        draw.text((570, 148), "CRITICAL: NO HARNESS", fill=(255, 255, 255))
        
        # Safe bounding box overlay on Worker 1
        draw.rectangle([255, 350, 305, 458], outline=(16, 185, 129), width=2)
        draw.rectangle([255, 332, 345, 350], fill=(16, 185, 129))
        draw.text((260, 334), "COMPLIANT PPE", fill=(255, 255, 255))
        
        # Site details banner
        draw.rectangle([20, 20, 380, 85], fill=(15, 23, 42, 220), outline=(245, 158, 11), width=2)
        draw.text((35, 30), "SITE CCTV CAM #04 - SECTOR 7 TOWER A", fill=(245, 158, 11))
        draw.text((35, 48), "AUDIT STANDARD: OSHA 1926 & IS 456", fill=(255, 255, 255))
        draw.text((35, 66), "STATUS: LIVE INSPECTION FEED", fill=(148, 163, 184))
        
        img.save(ppe_path)
    
    # 2. Sample PPE Site Photo (Compliant Team)
    ppe_compliant_path = os.path.join(output_dir, "sample_site_ppe_compliant.png")
    if not os.path.exists(ppe_compliant_path):
        img = Image.new("RGB", (800, 600), color=(235, 240, 245))
        draw = ImageDraw.Draw(img)
        # Background: Excavation pit & concrete retaining wall
        draw.rectangle([0, 0, 800, 300], fill=(180, 185, 190)) # Concrete wall
        draw.rectangle([0, 300, 800, 600], fill=(140, 125, 95)) # Trench gravel
        # Rebar cage grid
        for rx in range(50, 750, 40):
            draw.line([(rx, 100), (rx, 300)], fill=(120, 70, 40), width=4)
        for ry in range(120, 300, 40):
            draw.line([(50, ry), (750, ry)], fill=(120, 70, 40), width=4)
            
        # 3 compliant workers
        for idx, wx in enumerate([220, 400, 580]):
            # Hard hat
            color_hat = (255, 215, 0) if idx != 1 else (255, 255, 255) # Site engineer in white helmet
            draw.ellipse([wx, 260, wx+24, 284], fill=(230, 190, 150))
            draw.chord([wx-3, 255, wx+27, 277], start=180, end=360, fill=color_hat)
            # Hi-vis vest
            vest_col = (255, 102, 0) if idx != 1 else (16, 185, 129)
            draw.rectangle([wx-2, 284, wx+26, 330], fill=vest_col)
            draw.line([(wx+4, 290), (wx+4, 330)], fill=(240, 240, 240), width=2)
            draw.line([(wx+20, 290), (wx+20, 330)], fill=(240, 240, 240), width=2)
            # Legs & boots
            draw.rectangle([wx, 330, wx+10, 380], fill=(50, 60, 80))
            draw.rectangle([wx+14, 330, wx+24, 380], fill=(50, 60, 80))
            draw.rectangle([wx-2, 380, wx+11, 390], fill=(20, 20, 20))
            draw.rectangle([wx+13, 380, wx+26, 390], fill=(20, 20, 20))
            # Green check
            draw.rectangle([wx-10, 245, wx+34, 395], outline=(16, 185, 129), width=2)
            
        draw.rectangle([20, 20, 420, 75], fill=(15, 23, 42, 220), outline=(16, 185, 129), width=2)
        draw.text((35, 30), "TRENCH EXCAVATION REBAR CREW - ZONE 2", fill=(16, 185, 129))
        draw.text((35, 50), "FULL PPE COMPLIANCE: 100% AUDIT PASS", fill=(255, 255, 255))
        img.save(ppe_compliant_path)

    # 3. Sample Concrete Crack (Structural Shear Crack)
    shear_crack_path = os.path.join(output_dir, "sample_crack_structural_shear.png")
    if not os.path.exists(shear_crack_path):
        img = Image.new("RGB", (800, 600), color=(185, 187, 190))
        draw = ImageDraw.Draw(img)
        
        # Concrete texture mottling
        for i in range(0, 800, 40):
            for j in range(0, 600, 40):
                offset = ((i*17 + j*23) % 25) - 12
                c = max(140, min(210, 185 + offset))
                draw.rectangle([i, j, i+40, j+40], fill=(c, c, c+2))
                
        # RCC Beam Outline
        draw.rectangle([40, 100, 760, 480], outline=(90, 95, 100), width=6)
        draw.text((60, 120), "REINFORCED CONCRETE BEAM B-104 (500mm x 750mm)", fill=(60, 65, 70))
        
        # Diagonal 45-degree Structural Shear Crack
        points = [
            (220, 440), (280, 390), (330, 350), (370, 310),
            (410, 280), (450, 240), (510, 180), (560, 140)
        ]
        # Main thick crack
        for idx in range(len(points)-1):
            p1 = points[idx]
            p2 = points[idx+1]
            draw.line([p1, p2], fill=(25, 25, 25), width=7)
            # Side feathering micro cracks
            mid_x = (p1[0] + p2[0]) // 2
            mid_y = (p1[1] + p2[1]) // 2
            draw.line([(mid_x, mid_y), (mid_x + 15, mid_y - 12)], fill=(45, 45, 45), width=3)
            draw.line([(mid_x, mid_y), (mid_x - 12, mid_y + 10)], fill=(50, 50, 50), width=2)
            
        # Measurement scale card / caliper overlay
        draw.rectangle([340, 270, 470, 335], fill=(255, 255, 240), outline=(220, 38, 38), width=2)
        draw.line([(355, 290), (455, 290)], fill=(0, 0, 0), width=2)
        draw.line([(355, 285), (355, 295)], fill=(0, 0, 0), width=2)
        draw.line([(455, 285), (455, 295)], fill=(0, 0, 0), width=2)
        draw.text((365, 300), "WIDTH: 2.85 mm", fill=(220, 38, 38))
        draw.text((365, 316), "DIAG. 45 DEGREE", fill=(100, 100, 100))
        
        # Inspection Tag
        draw.rectangle([50, 495, 450, 565], fill=(15, 23, 42, 230), outline=(220, 38, 38), width=2)
        draw.text((65, 505), "DEFECT: HIGH-CRITICALITY STRUCTURAL SHEAR CRACK", fill=(239, 68, 68))
        draw.text((65, 525), "EXCEEDS IS 456 LIMIT (0.30mm max) - URGENCY: IMMEDIATE", fill=(255, 255, 255))
        draw.text((65, 543), "REMEDY: EPOXY RESIN INJECTION & CFRP COMPOSITE WRAP", fill=(245, 158, 11))
        
        img.save(shear_crack_path)

    # 4. Sample Concrete Crack (Hairline Shrinkage)
    hairline_path = os.path.join(output_dir, "sample_crack_hairline_plaster.png")
    if not os.path.exists(hairline_path):
        img = Image.new("RGB", (800, 600), color=(225, 222, 215))
        draw = ImageDraw.Draw(img)
        # Plaster texture
        for i in range(0, 800, 50):
            for j in range(0, 600, 50):
                offset = ((i*13 + j*19) % 15) - 7
                c = 225 + offset
                draw.rectangle([i, j, i+50, j+50], fill=(c, c-2, c-8))
                
        # Spiderweb / crazing hairline pattern
        lines = [
            [(300, 200), (350, 240), (410, 235), (460, 260), (510, 250)],
            [(350, 240), (360, 300), (390, 340), (410, 390)],
            [(410, 235), (430, 170), (480, 140)],
            [(460, 260), (490, 320), (540, 360)],
            [(360, 300), (320, 350), (280, 370)],
        ]
        for poly in lines:
            for idx in range(len(poly)-1):
                draw.line([poly[idx], poly[idx+1]], fill=(120, 115, 110), width=1)
                
        # Measurement scale card
        draw.rectangle([480, 310, 600, 365], fill=(255, 255, 255), outline=(16, 185, 129), width=2)
        draw.text((490, 322), "WIDTH: 0.12 mm", fill=(16, 185, 129))
        draw.text((490, 340), "SURFACE CRAZING", fill=(80, 80, 80))
        
        # Info Box
        draw.rectangle([50, 495, 450, 565], fill=(15, 23, 42, 230), outline=(16, 185, 129), width=2)
        draw.text((65, 505), "DEFECT: PLASTIC SHRINKAGE / HAIRLINE CRAZING", fill=(16, 185, 129))
        draw.text((65, 525), "WITHIN PERMISSIBLE LIMITS (IS 456 < 0.3mm)", fill=(255, 255, 255))
        draw.text((65, 543), "REMEDY: ELASTOMERIC COATING / SURFACE SEALANT", fill=(148, 163, 184))
        
        img.save(hairline_path)

    # 5. Sample Concrete Spalling (Corroded Rebar)
    spalling_path = os.path.join(output_dir, "sample_crack_spalling_corrosion.png")
    if not os.path.exists(spalling_path):
        img = Image.new("RGB", (800, 600), color=(165, 165, 165))
        draw = ImageDraw.Draw(img)
        # Concrete column
        draw.rectangle([150, 50, 650, 550], fill=(175, 175, 175), outline=(100, 100, 100), width=4)
        # Spalled Cavity (Rough jagged polygon)
        cavity = [(320, 180), (450, 160), (510, 220), (530, 330), (470, 420), (360, 430), (300, 340), (290, 240)]
        draw.polygon(cavity, fill=(95, 90, 85))
        draw.line(cavity + [cavity[0]], fill=(50, 45, 40), width=3)
        # Rust staining around edges
        draw.ellipse([270, 150, 550, 450], outline=(180, 90, 30), width=2)
        # Exposed corroded rebar
        draw.line([(380, 150), (390, 440)], fill=(150, 60, 20), width=12) # Corroded vertical bar
        draw.line([(440, 170), (445, 420)], fill=(160, 65, 25), width=10) # Second bar
        # Rust flakes
        for ry in range(200, 400, 30):
            draw.rectangle([375, ry, 400, ry+8], fill=(185, 75, 20))
            draw.rectangle([435, ry+15, 455, ry+22], fill=(185, 75, 20))
            
        # Measurement scale
        draw.rectangle([540, 240, 710, 310], fill=(255, 255, 245), outline=(220, 38, 38), width=2)
        draw.text((550, 250), "SPALL DEPTH: 45 mm", fill=(220, 38, 38))
        draw.text((550, 270), "REBAR SECTION LOSS: ~22%", fill=(180, 70, 20))
        draw.text((550, 290), "CARBONATION DEPTH > COVER", fill=(100, 100, 100))
        
        # Info Box
        draw.rectangle([50, 480, 550, 565], fill=(15, 23, 42, 230), outline=(239, 68, 68), width=2)
        draw.text((65, 490), "DEFECT: SEVERE CONCRETE SPALLING & REBAR CORROSION", fill=(239, 68, 68))
        draw.text((65, 510), "STRUCTURAL CAPACITY DEGRADATION - HIGH RISK", fill=(255, 255, 255))
        draw.text((65, 530), "REMEDY: HYDRO-DEMOLITION, RUST PASSIVATION, PMM & JACKETING", fill=(245, 158, 11))
        
        img.save(spalling_path)

    return {
        "ppe_hazard": ppe_path,
        "ppe_compliant": ppe_compliant_path,
        "shear_crack": shear_crack_path,
        "hairline_crack": hairline_path,
        "spalling_crack": spalling_path
    }

if __name__ == "__main__":
    generated = generate_sample_assets()
    print("Generated sample assets:", generated)
