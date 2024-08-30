@echo off
IF NOT EXIST "venv\Scripts\activate" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

IF %ERRORLEVEL% NEQ 0 (
    echo Installing requirements.txt...
    python -m pip install -r requirements.txt
) ELSE (
    echo Updating requirements.txt...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)

REM Run the server
@REM streamlit run app.py