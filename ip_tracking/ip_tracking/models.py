from django.db import models


class RequestLog(models.Model):
    """Model to store request logs."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2048)

    def __str__(self):
        """String representation of the RequestLog."""
        return f"Request from {self.ip_address} to {self.path} at {self.timestamp:%Y-%m-%d %H:%M:%S}"