# Before running the sample:
#    pip install --pre azure-ai-projects>=2.0.0b1
#    pip install azure-identity
#    pip install python-dotenv

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ResponseStreamEventType

COLOR_RESET = "\033[0m"
COLOR_PROMPT = "\033[96m"
COLOR_AGENT = "\033[92m"

load_dotenv()

project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
if not project_endpoint:
    raise ValueError("Missing required environment variable: AZURE_AI_PROJECT_ENDPOINT")

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

with project_client:

    workflow = {
        "name": "Capibaras",
        "version": "10",
    }
    
    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()
    print("Escribe tu prompt y pulsa Enter. Usa 'salir' para terminar.")

    while True:
        user_prompt = input(f"{COLOR_PROMPT}Prompt>{COLOR_RESET} ").strip()

        if user_prompt.lower() in {"salir", "exit", "quit"}:
            break
        if not user_prompt:
            continue

        stream = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": workflow["name"], "type": "agent_reference"}},
            input=[
                {
                    "role": "system",
                    "content": "Responde solo en texto plano. No uses formato Markdown, listas con viñetas, encabezados ni bloques de código.",
                },
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )

        print(f"{COLOR_AGENT}Agente>{COLOR_RESET} ", end="", flush=True)
        got_text = False

        for event in stream:
            if event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DELTA:
                if event.delta:
                    print(event.delta, end="", flush=True)
                    got_text = True
            elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DONE and not got_text:
                if event.text:
                    print(event.text, end="", flush=True)
                    got_text = True
        print()

        if not got_text:
            print(f"{COLOR_AGENT}Agente>{COLOR_RESET} (sin texto en la respuesta)")

    openai_client.conversations.delete(conversation_id=conversation.id)
