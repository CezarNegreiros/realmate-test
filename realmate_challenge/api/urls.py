from django.urls import path

from realmate_challenge.api.views import ConversationDetailView

app_name = 'service-api'

urlpatterns = [
    path('external/conversation/<str:conversation_id>/', ConversationDetailView.as_view(), name='api-conversation-details'), # noqa E501
]
