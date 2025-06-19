""" from .models import Committee

def committees(request):
    return {'committees': Committee.objects.all()} """
    
    
from .models import Committee, User, AdvertItem
from django.db.models import Q

def committees(request):
    return {'committees': Committee.objects.all()}

def admin_counts(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'pending_users_count': User.objects.filter(is_active=False).count(),
            'pending_adverts_count': AdvertItem.objects.filter(is_approved=False).count(),
            'total_users_count': User.objects.count(),
        }
    return {}