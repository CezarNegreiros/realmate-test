from rest_framework import serializers


class ConversationIdPayloadSerializer(serializers.Serializer):
    """
    Nested serializer to validate the 'data' object within the new
    conversation event.
    """
    id = serializers.CharField(max_length=100)


class ConversationDataSerializer(serializers.Serializer):
    """
    Validates the COMPLETE STRUCTURE of the NEW_CONVERSATION event,
    including the nested fields.
    """
    type = serializers.CharField()
    timestamp = serializers.DateTimeField()
    data = ConversationIdPayloadSerializer()


class MessageDetailSerializer(serializers.Serializer):
    """
    Serializer for the details of a message.
    """
    id = serializers.CharField(max_length=100)
    direction = serializers.ChoiceField(choices=['SENT', 'RECEIVED'])
    content = serializers.CharField()
    conversation_id = serializers.CharField(max_length=100)


class MessageDataSerializer(serializers.Serializer):
    """
    Validates the data for the NEW_MESSAGE event.
    """
    type = serializers.CharField()
    timestamp = serializers.DateTimeField()
    data = MessageDetailSerializer()


class ConversationSerializer(serializers.Serializer):
    """
    Serializer for returning the details of a conversation.
    """
    id = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class ConversationDetailSerializer(serializers.Serializer):
    """
    Serializer for returning the details of a conversation with its messages.
    """
    id = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    messages = MessageDetailSerializer(many=True)
