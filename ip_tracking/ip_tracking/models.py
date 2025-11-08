from django.db import models


class RequestLog(models.Model):
    """Model to store request logs."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2048)

    def __str__(self):
        """String representation of the RequestLog."""
        return f"Request from {self.ip_address} to {self.path} at {self.timestamp:%Y-%m-%d %H:%M:%S}"


class BlockedIP(models.Model):
    """Model to store blocked IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        """String representation of the BlockedIP."""
        return self.ip_address


class SuspiciousIP(models.Model):
    """Model to store suspicious IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()

    def __str__(self):
        """String representation of the SuspiciousIP."""
        return f"Suspicious IP: {self.ip_address} - {self.reason}"

