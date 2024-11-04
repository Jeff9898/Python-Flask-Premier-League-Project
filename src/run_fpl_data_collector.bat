@echo off
REM Change directory to your project directory
cd C:\PersonalJavaProjects\untitled-python

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the Python script
python src\fpl_data_collector.py

REM Exit the script
exit
