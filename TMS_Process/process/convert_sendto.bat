@echo off
setlocal EnableDelayedExpansion

:: =====================================================
:: Send-To: Convert Selected Images to PDF (<900KB)
:: =====================================================

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%rclick_pdf.py"

echo ===== %date% %time% ===== >> "%SCRIPT_DIR%convert_debug.log"

:: --- Detect Python automatically ---
for /f "delims=" %%P in ('where python 2^>nul') do (
    set "PYTHON_EXE=%%P"
    goto :found
)
:found
if not defined PYTHON_EXE (
    echo Python not found >> "%SCRIPT_DIR%convert_debug.log"
    powershell -Command "[System.Windows.Forms.MessageBox]::Show('Python not found. Please install Python 3.9 or higher.','Missing Python',0,'Error')"
    exit /b
)
echo Using Python: %PYTHON_EXE% >> "%SCRIPT_DIR%convert_debug.log"

:: --- Collect all selected file arguments safely ---
set "ARGS="
set count=0
for %%A in (%*) do (
    set /a count+=1
    set "ARGS=!ARGS! "%%~A""
    echo Arg !count!: %%~A >> "%SCRIPT_DIR%convert_debug.log"
)
echo Received !count! arguments. >> "%SCRIPT_DIR%convert_debug.log"

:: --- Run the Python script ---
echo Running: "%PYTHON_EXE%" "%SCRIPT_PATH%" !ARGS! >> "%SCRIPT_DIR%convert_debug.log"
"%PYTHON_EXE%" "%SCRIPT_PATH%" !ARGS!
set "ERRCODE=%ERRORLEVEL%"
echo Python exit code !ERRCODE! >> "%SCRIPT_DIR%convert_debug.log"
echo. >> "%SCRIPT_DIR%convert_debug.log"

endlocal
exit /b
