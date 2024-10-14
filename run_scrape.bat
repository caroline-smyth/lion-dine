@echo off
REM Activate virtual environment if needed
CALL C:\Users\carol\lion-dine\lion-dine\lion-dine\newenv\Scripts\activate.bat

REM Run your Python script
python C:\Users\carol\lion-dine\lion-dine\lion-dine\scrape.py

REM Deactivate virtual environment if used
CALL deactivate
