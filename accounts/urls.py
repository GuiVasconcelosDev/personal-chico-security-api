from django.urls import path
from .views import RegisterView, CurrentUserView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('logout/', LogoutView.as_view()),
]
