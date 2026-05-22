from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JournalEntryViewSet, PublicJournalViewSet

router = DefaultRouter()
router.register(r'journal/public', PublicJournalViewSet, basename='public-journal')
router.register(r'journal', JournalEntryViewSet, basename='journal-entry')

urlpatterns = [
    path('', include(router.urls)),
]
