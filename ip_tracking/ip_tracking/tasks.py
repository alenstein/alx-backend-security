from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Q
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_suspicious_ips(path__startswith=None):
    """
    A Celery task to detect and flag suspicious IP addresses based on request patterns.
    Runs hourly to check for:
    1. IPs with more than 100 requests in the last hour.
    2. IPs that accessed sensitive paths like /admin/ or /login/.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. Find IPs with high request volume
    high_volume_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago).values('ip_address').annotate(\
        request_count=Count('id')).filter(request_count__gt=100)

    for item in high_volume_ips:
        reason = f"High request volume: {item['request_count']} requests in the last hour."
        SuspiciousIP.objects.update_or_create(
            ip_address=item['ip_address'],
            defaults={'reason': reason}
        )

    # 2. Find IPs accessing sensitive paths
    sensitive_paths_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago).filter(Q(path__startswith='/admin/')\
        | Q(path__startswith='/login/')).values_list('ip_address', flat=True).distinct()

    for ip in sensitive_paths_ips:
        reason = "Accessed a sensitive path ( /admin/, /login/)."
        SuspiciousIP.objects.update_or_create(
            ip_address=ip,
            defaults={'reason': reason}
        )