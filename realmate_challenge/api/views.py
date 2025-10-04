from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from realmate_challenge.api.models import Conversation, Message
from realmate_challenge.api.serializers import (
    ConversationDataSerializer,
    MessageDataSerializer,
    ConversationDetailSerializer,
    ConversationSerializer
)


class MessagesUpsertBusinessView(APIView):
    """
    API endpoint that has the business logic to save a new message. 
    """
    def post(self, request: Request):
        serializer = MessageDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        conversation_id = data['data']['conversation_id']
        message_content = data['data']['content']
        conversation, created = Conversation.objects.get_or_create(
            id=conversation_id,
            defaults={'status': Conversation.Status.OPEN}
        )

        if message_content.strip() == '/close':
            conversation.status = Conversation.Status.CLOSED
            conversation.save()
            return Response(
                {"status": "Conversation closed"}, status=status.HTTP_200_OK
            )

        if conversation.status == Conversation.Status.CLOSED:
            return Response(
                {"error": "Cannot add message to a closed conversation"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Message.objects.get_or_create(
            id=data['data']['id'],
            defaults={
                'conversation': conversation,
                'direction': data['data']['direction'],
                'content': message_content,
            }
        )
        return Response(
            {"status": "Message processed"}, status=status.HTTP_201_CREATED
        )


class ConversationBusinessView(APIView):
    """
    API endpoint that allows creating a new conversation or retrieving details.
    """
    def get(self, request: Request, conversation_id: str):
        try:
            conversation = Conversation.objects.prefetch_related('messages').\
                get(pk=conversation_id)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversa não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request: Request):
        serializer = ConversationDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        Conversation.objects.get_or_create(
            id=serializer.validated_data['data']['id'],
            defaults={'status': Conversation.Status.OPEN}
        )
        return Response(
            {"status": "Conversation created"},
            status=status.HTTP_201_CREATED
        )


class ConversationDetailView(APIView):
    """
    API endpoint that allows retrieving details of a specific conversation.
    """
    def get(self, request: Request, conversation_id: str):
        try:
            conversation = Conversation.objects.prefetch_related('messages').\
                get(pk=conversation_id)
            serializer = ConversationDetailSerializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversa não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )
