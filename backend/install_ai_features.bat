@echo off
echo.
echo ================================================
echo    INSTALLING AI CHATBOT DEPENDENCIES
echo ================================================
echo.
echo This will install:
echo - Hugging Face Transformers
echo - PyTorch
echo - Additional dependencies
echo.
echo Note: First-time install may take 5-10 minutes
echo.
pause

pip install transformers==4.35.2
pip install torch==2.1.1
pip install requests==2.31.0

echo.
echo ================================================
echo    INSTALLATION COMPLETE!
echo ================================================
echo.
echo The chatbot is now ready to use!
echo.
echo Start your backend with:
echo    uvicorn main:app --reload
echo.
echo The chatbot will work with rule-based responses immediately.
echo To load the full Hugging Face LLM, visit:
echo    http://localhost:8000/chatbot/load
echo.
pause
