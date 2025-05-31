@echo off
REM ─────────────── knime_bridge.bat ───────────────
REM 1) Ruta al ejecutable de KNIME
set "KNIME_EXE=C:\Program Files\KNIME\knime.exe"

REM 2) Workflow .knwf (misma carpeta)
set "WF_FILE=%~dp0IA.knwf"

REM 3) Archivos de intercambio CSV
set "input_csv=%~dp0sentiment_input.csv"
set "output_csv=%~dp0sentiment_output.csv"

echo =================== KNIME Bridge ====================
echo [INFO] Ejecutable : "%KNIME_EXE%"
echo [INFO] Workflow   : "%WF_FILE%"
echo [INFO] Entrada    : "%input_csv%"
echo [INFO] Salida     : "%output_csv%"
echo ------------------------------------------------------

if not exist "%input_csv%" (
    echo [ERROR] No existe "%input_csv%"
    exit /b 1
)

"%KNIME_EXE%" ^
  -nosplash ^
  -application org.knime.product.KNIME_BATCH_APPLICATION ^
  -workflowFile="%WF_FILE%" ^
  -workflow.variable=input_csv,"%input_csv%",String ^
  -workflow.variable=output_csv,"%output_csv%",String ^
  -reset -nosave

if %ERRORLEVEL% neq 0 (
    echo [ERROR] KNIME devolvió %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

if exist "%output_csv%" (
    echo [INFO] Predicción generada:
    type "%output_csv%"
) else (
    echo [ERROR] No se generó "%output_csv%"
    exit /b 1
)
echo ================= Fin Bridge =========================
