import os
from typing import Iterator, Optional

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ResponseStreamEventType

WORKFLOW = {
    "name": "Capibaras",
    "version": "10",
}

SYSTEM_MESSAGE = (
    "Responde en formato Markdown claro y legible. Usa títulos, listas y "
    "bloques de código solo cuando aporten valor."
)


def create_project_client() -> AIProjectClient:
    load_dotenv()
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not project_endpoint:
        raise ValueError("Missing required environment variable: AZURE_AI_PROJECT_ENDPOINT")

    return AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(),
    )


def create_conversation(openai_client):
    return openai_client.conversations.create()


def delete_conversation(openai_client, conversation_id: str) -> None:
    openai_client.conversations.delete(conversation_id=conversation_id)


def _build_user_content(user_prompt: str, remitente: Optional[str] = None) -> str:
    if not remitente:
        return user_prompt
    return f"Remitente: {remitente}. Petición: {user_prompt}"


def iter_response_text(openai_client, conversation_id: str, user_prompt: str, remitente: Optional[str] = None) -> Iterator[str]:
    stream = openai_client.responses.create(
        conversation=conversation_id,
        extra_body={"agent": {"name": WORKFLOW["name"], "type": "agent_reference"}},
        input=[
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            },
            {"role": "user", "content": _build_user_content(user_prompt=user_prompt, remitente=remitente)},
        ],
        stream=True,
    )

    got_text = False
    for event in stream:
        if event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DELTA:
            if event.delta:
                got_text = True
                yield event.delta
        elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DONE and not got_text:
            if event.text:
                got_text = True
                yield event.text


def collect_response_text(openai_client, conversation_id: str, user_prompt: str, remitente: Optional[str] = None) -> str:
    chunks = list(
        iter_response_text(
            openai_client=openai_client,
            conversation_id=conversation_id,
            user_prompt=user_prompt,
            remitente=remitente,
        )
    )
    return "".join(chunks)
