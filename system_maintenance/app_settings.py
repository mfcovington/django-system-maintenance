from django.conf import settings


SYSTEM_MAINTENANCE_PAGINATE_BY = getattr(settings, 'SYSTEM_MAINTENANCE_PAGINATE_BY', 30)
