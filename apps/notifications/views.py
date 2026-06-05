from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
        return Notification.objects.none()

    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'read'})

    @action(detail=False, methods=['patch'])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': 'all read'})

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def notifications_list(request):
    if request.user.is_authenticated:
        notifs = request.user.notifications.order_by('-created_at')[:50]
    else:
        notifs = []
    return render(request, 'notifications/notifications.html', {'notifications': notifs})