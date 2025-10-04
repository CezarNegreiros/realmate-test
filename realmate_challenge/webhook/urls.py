from django.urls import path

from realmate_challenge.api.views import (
    ConversationBusinessView,
    MessagesUpsertBusinessView
)
from .views import MessagesUpsertWebhookView

app_name = 'webhook'

urlpatterns = [
    path('webhook/messages-upsert', MessagesUpsertWebhookView.as_view(), name='webhook-receive-message'),  # noqa E501
    path('api/v1/conversations/<str:conversation_id>/', ConversationBusinessView.as_view(), name='api-conversation-detail'),  # noqa E501
    path('api/v1/conversations/', ConversationBusinessView.as_view()),  # noqa E501
    path('api/v1/messages/', MessagesUpsertBusinessView.as_view()),  # noqa E501
]
