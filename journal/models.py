from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Feliz'),
        ('neutral', 'Neutro'),
        ('sad', 'Triste'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    title = models.CharField(max_length=120)
    content = models.TextField()
    mood = models.CharField(
        max_length=10,
        choices=MOOD_CHOICES,
        default='neutral'
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
