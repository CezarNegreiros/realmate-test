from decouple import config

import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from realmate_challenge.webhook.handlers import (
    _check_if_conversation_is_new,
    _handle_new_conversation,
    _handle_new_message
)
from realmate_challenge.webhook.builders import (
    ConversationPayloadBuilder,
    MessagePayloadBuilder
)


class MessagesUpsertWebhookView(APIView):
    """
    Endpoint para processar o evento 'messages.upsert' da Evolution API.
    Este evento é mapeado para uma nova mensagem ou um comando para fechar
    a conversa.
    """
    def post(self, request: Request, *args, **kwargs):
        payload_data = request.data

        if payload_data.get("event") != "messages.upsert":
            return Response(
                {"status": "Evento ignorado"},
                status=status.HTTP_200_OK
            )

        raw_message_data = payload_data.get("data", {})
        key_data = raw_message_data.get("key", {})
        message_obj = raw_message_data.get("message", {})
        content = message_obj.get("conversation") or message_obj.get("extendedTextMessage", {}).get("text")  # noqa E501
        conversation_id = key_data.get("remoteJid")

        if not content or not conversation_id:
            return Response(
                {"status": "Payload incompleto ignorado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            is_new_conversation = _check_if_conversation_is_new(
                config('base_url'),
                conversation_id
            )

            if is_new_conversation:
                _handle_new_conversation(
                    config('base_url'),
                    ConversationPayloadBuilder(
                        conversation_id, payload_data.get("date_time")
                    ).build()
                )

            final_response = _handle_new_message(
                config('base_url'),
                MessagePayloadBuilder(
                    timestamp=payload_data.get("date_time"),
                    message_id=key_data.get("id"),
                    direction="SENT" if key_data.get("fromMe") else "RECEIVED",
                    content=content,
                    conversation_id=conversation_id
                ).build()
            )

            return Response(
                final_response.json(),
                status=final_response.status_code
            )

        except requests.RequestException as e:
            return Response(
                {
                    "error": (
                        f"Erro de comunicação interna ao processar evento: {e}"
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
