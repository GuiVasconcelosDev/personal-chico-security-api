from django.shortcuts import render
from .permissions import IsOwner, IsEditorOrReadOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import JournalEntry
from .serializers import JournalEntrySerializer

class JournalEntryViewSet(
    viewsets.ModelViewSet
):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated, IsEditorOrReadOnly]

    def get_queryset(self):
        is_editor = self.request.user.groups.filter(name='Editor').exists()
        if is_editor:
            return JournalEntry.objects.all()
        return JournalEntry.objects.filter(author=self.request.user)
    
    def perform_create(self, serializer):
       serializer.save(author=self.request.user)


class PublicJournalViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return JournalEntry.objects.filter(is_public=True) 