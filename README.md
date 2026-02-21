# GPPB2026 Castellón - Materiales del evento

Este repositorio contiene materiales del evento Global Power Platform Bootcamp 2026, organizado por Power Platform Castellón: https://www.powerplatformcastellon.es/

Incluye recursos de apoyo para la sesión, entre ellos la presentación principal y ejemplos de código.
Aquí se encuentra también la presentación PPT de la sesión: `Presentacion.pptx`.

## Estructura

- `Presentacion.pptx`: deck con la sesión que se impartirá en el evento.
- `code/capibaras.py`: cliente interactivo por terminal.
- `code/requirements.txt`: dependencias de Python.

## Materiales incluidos

- Presentación de la sesión en `Presentacion.pptx`.
- Script de ejemplo para interacción con un agente de Azure AI Projects en `code/capibaras.py`.
- Dependencias del ejemplo en `code/requirements.txt`.

## Requisitos

- Python 3.10+
- Acceso a un proyecto de Azure AI
- Autenticación válida para `DefaultAzureCredential` (por ejemplo, sesión iniciada con Azure CLI)

## Instalación

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r code/requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con esta variable:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<tu-recurso>.services.ai.azure.com/api/projects/<tu-proyecto>
```

## Ejecución

```powershell
cd code
python .\capibaras.py
```

Uso en consola:
- Escribe tu prompt y pulsa Enter.
- Para salir, escribe `salir`, `exit` o `quit`.

## Comportamiento

- Mantiene una conversación activa durante toda la sesión.
- Muestra únicamente el texto de respuesta del agente.
- Solicita respuestas en texto plano (sin formato Markdown).
- Colorea los prefijos de terminal (`Prompt>` y `Agente>`) para mejorar la lectura.

## Solución de problemas rápida

- Si aparece `Missing required environment variable: AZURE_AI_PROJECT_ENDPOINT`, revisa el archivo `.env`.
- Si falla la autenticación, verifica tu identidad para `DefaultAzureCredential` (por ejemplo, ejecuta `az login`).
