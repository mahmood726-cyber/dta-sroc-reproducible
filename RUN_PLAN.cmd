@echo off
echo === Local environment
setlocal
echo === R executable PATH
rem Set R_HOME, R_LIBS_USER and R_LIBS in the calling environment.
if not defined R_HOME exit /b 1
if not defined R_LIBS_USER exit /b 1
if not defined R_LIBS exit /b 1
set "PATH=%R_HOME%\bin;%PATH%"
echo === R user library
rem R_LIBS_USER is inherited from the calling environment.
echo === R extra library
rem R_LIBS is inherited from the calling environment.
echo === Isolate R environment
set R_ENVIRON_USER=NUL
echo === Runner executables
rem Rscript = %R_HOME%\bin\Rscript.exe ; node and python are on PATH
echo === Python UTF-8 output
set PYTHONUTF8=1
echo === Verify prepared source
python recut_integrity.py --verify
if errorlevel 1 exit /b 1
echo === Preserve previous original results
call :preserve_output results\full
if errorlevel 1 exit /b 1
echo === Preserve previous original reports
call :preserve_output outputs\full
if errorlevel 1 exit /b 1
echo === Original validation
rem Recorded deviation: Node 24.13.0; fonttools 4.67.0; packaging 26.0; pillow 12.2.0.
rem See RUN_PLAN_EXPECTED.md; canonical pins remain unchanged.
python reproduce.py --allow-version-mismatch
if errorlevel 1 exit /b 1
echo === Original N/N
python recut_integrity.py --original-counts
if errorlevel 1 exit /b 1
echo === Preserve previous extras workspace
call :preserve_output outputs\validation-plus
if errorlevel 1 exit /b 1
echo === Original pinned replay
python validation-plus/run.py original
if errorlevel 1 exit /b 1
echo === Extras numerical replay
python validation-plus/run.py extras
if errorlevel 1 exit /b 1
echo === Raw-scale gate
python validation-plus/run.py raw
if errorlevel 1 exit /b 1
echo === Extras negative controls
python validation-plus/run.py tests
if errorlevel 1 exit /b 1
echo === Original oracle tests
python -B -m unittest discover -s tests -v
if errorlevel 1 exit /b 1
echo === Verify after validation
python recut_integrity.py --verify
if errorlevel 1 exit /b 1
echo === Regenerate file inventory
python recut_integrity.py --write
if errorlevel 1 exit /b 1
echo === Verify regenerated inventory
python recut_integrity.py --verify
if errorlevel 1 exit /b 1
echo === Completion
echo RECUT_RUN_PASS
exit /b 0

:preserve_output
rem Only the three archive-local output folders passed above are renamed.
if not exist "%~1" exit /b 0
set /a resync_attempt=1 >nul
:preserve_output_next
if not exist "%~1.prev-%resync_attempt%" goto preserve_output_rename
set /a resync_attempt+=1 >nul
goto preserve_output_next
:preserve_output_rename
echo Preserving %~1 as %~nx1.prev-%resync_attempt%
ren "%~1" "%~nx1.prev-%resync_attempt%"
exit /b %errorlevel%
