@echo off
title Push to GitHub - Multimodal Construction Intelligence Platform
echo ========================================================
echo Pushing Multimodal Construction Intelligence Platform to GitHub
echo Remote: https://github.com/riyakarwande/multimodal-construction-intelligence-platform.git
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo SUCCESS! Repository pushed successfully to GitHub!
    echo ========================================================
) else (
    echo ========================================================
    echo If push failed, please ensure you created the empty repo at:
    echo https://github.com/new
    echo with name: multimodal-construction-intelligence-platform
    echo ========================================================
)
echo.
pause
