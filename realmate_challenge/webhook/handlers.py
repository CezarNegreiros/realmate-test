import requests


def _check_if_conversation_is_new(base_url, conversation_id):
    """
    Handler that checks if a conversation is new, with its own context
    """
    try:
        with requests.Session() as session:
            session.get(
                f"{base_url}/api/v1/conversations/{conversation_id}/",
                timeout=5
            ).raise_for_status()
            return False
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return True
        raise


def _handle_new_conversation(base_url, conversation_payload):
    """
    Handler that triggers the event to create a new conversation,
    with its own context.
    """
    endpoint = f"{base_url}/api/v1/conversations/"
    with requests.Session() as session:
        session.post(
            endpoint, json=conversation_payload, timeout=10
        ).raise_for_status()


def _handle_new_message(base_url, message_data):
    """
    Handler that triggers the event to create a new message,
    with its own context.
    """
    endpoint = f"{base_url}/api/v1/messages/"
    with requests.Session() as session:
        response = session.post(endpoint, json=message_data, timeout=10)
        response.raise_for_status()
        return response
