from django.db import models


class SocketLog(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
