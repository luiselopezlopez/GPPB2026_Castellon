import atexit
import os
import threading
import uuid

import bleach
import markdown
from flask import Flask, jsonify, render_template, request, session

from chat_core import (
    collect_response_text,
    create_conversation,
    create_project_client,
    delete_conversation,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "capibaras-dev-secret-key")

project_client = create_project_client()
project_client.__enter__()
openai_client = project_client.get_openai_client()

conversation_ids_by_session = {}
conversation_lock = threading.Lock()

ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "code",
    "pre",
    "blockquote",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "a",
    "hr",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
}


def _render_markdown_to_safe_html(text: str) -> str:
    html = markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "fenced_code"],
        output_format="html5",
    )
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=["http", "https", "mailto"],
        strip=True,
    )


def _get_session_id() -> str:
    session_id = session.get("chat_session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["chat_session_id"] = session_id
    return session_id


def _get_or_create_conversation_id() -> str:
    session_id = _get_session_id()
    with conversation_lock:
        conversation_id = conversation_ids_by_session.get(session_id)
        if conversation_id:
            return conversation_id

        conversation = create_conversation(openai_client)
        conversation_ids_by_session[session_id] = conversation.id
        return conversation.id


def _delete_session_conversation() -> None:
    session_id = session.get("chat_session_id")
    if not session_id:
        return

    with conversation_lock:
        conversation_id = conversation_ids_by_session.pop(session_id, None)

    if conversation_id:
        delete_conversation(openai_client=openai_client, conversation_id=conversation_id)


@atexit.register
def _cleanup_all_conversations() -> None:
    with conversation_lock:
        all_conversations = list(conversation_ids_by_session.values())
        conversation_ids_by_session.clear()

    for conversation_id in all_conversations:
        try:
            delete_conversation(openai_client=openai_client, conversation_id=conversation_id)
        except Exception:
            pass

    try:
        project_client.__exit__(None, None, None)
    except Exception:
        pass


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}

    user_prompt = (payload.get("mensaje") or "").strip()

    if not user_prompt:
        return jsonify({"error": "El mensaje no puede estar vacío."}), 400

    try:
        conversation_id = _get_or_create_conversation_id()
        response_text = collect_response_text(
            openai_client=openai_client,
            conversation_id=conversation_id,
            user_prompt=user_prompt,
        )
    except Exception as ex:
        return jsonify({"error": f"Error al consultar al agente: {ex}"}), 500

    if not response_text:
        response_text = "(sin texto en la respuesta)"

    return jsonify(
        {
            "respuesta": response_text,
            "respuesta_html": _render_markdown_to_safe_html(response_text),
        }
    )


@app.post("/reset")
def reset_chat():
    try:
        _delete_session_conversation()
    except Exception as ex:
        return jsonify({"error": f"No se pudo reiniciar la conversación: {ex}"}), 500

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
