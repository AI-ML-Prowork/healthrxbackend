from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from clients.custom_permissions import IsTenantAdmin

channel_layer = get_channel_layer()


@api_view(["POST"])
def notify_user(request):
    async_to_sync(channel_layer.group_send)(
        "demo@gmail.com",
        {
            "message": "messasge",
        },
    )
    return JsonResponse({"status": "Notification sent"})


class NotifyView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdmin]

    def post(self, request):
        user_id = f"group_{request.tenant.schema_name}"
        message = {
            "title": request.data['title'],
            "message": request.data['message']
        }
        async_to_sync(channel_layer.group_send)(
            user_id,
            {"type": "notify", "message": message},
        )
        return Response({"status": "Notification sent"})
