from chat_core import (
    create_project_client,
    create_conversation,
    delete_conversation,
    iter_response_text,
)

COLOR_RESET = "\033[0m"
COLOR_PROMPT = "\033[96m"
COLOR_AGENT = "\033[92m"

project_client = create_project_client()

with project_client:

    openai_client = project_client.get_openai_client()

    conversation = create_conversation(openai_client)
    print("Escribe tu prompt y pulsa Enter. Usa 'salir' para terminar.")

    while True:
        user_prompt = input(f"{COLOR_PROMPT}Prompt>{COLOR_RESET} ").strip()

        if user_prompt.lower() in {"salir", "exit", "quit"}:
            break
        if not user_prompt:
            continue

        print(f"{COLOR_AGENT}Agente>{COLOR_RESET} ", end="", flush=True)
        got_text = False

        for chunk in iter_response_text(
            openai_client=openai_client,
            conversation_id=conversation.id,
            user_prompt=user_prompt,
        ):
            print(chunk, end="", flush=True)
            got_text = True
        print()

        if not got_text:
            print(f"{COLOR_AGENT}Agente>{COLOR_RESET} (sin texto en la respuesta)")

    delete_conversation(openai_client=openai_client, conversation_id=conversation.id)
