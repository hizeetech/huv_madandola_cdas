from .models import Committee

def committees(request):
    return {'committees': Committee.objects.all()}