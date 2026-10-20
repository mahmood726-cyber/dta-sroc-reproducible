@echo off
rem Compatibility entry point; release finalization replaces the preparation fallback.
call "%~dp0FINAL_BLOBS.cmd"
exit /b %errorlevel%
