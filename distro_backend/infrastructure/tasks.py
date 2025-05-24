from celery import shared_task
from .models import Asset

@shared_task
def check_critical_assets():
    critical_assets = Asset.objects.filter(condition_score__lte=3, status='operational')
    for asset in critical_assets:
        # Implement logic to notify or create maintenance tasks
        pass
    return f"Checked {critical_assets.count()} critical assets"