from django.contrib import admin
from django.contrib import admin
from .models import CDA, UserProfile, Levy, UserLevy, Payment, ExecutiveMember, Event, CommunityInfo, Defaulter, NavbarImage

admin.site.register(CDA)
admin.site.register(UserProfile)
admin.site.register(Levy)
admin.site.register(UserLevy)
admin.site.register(Payment)
admin.site.register(ExecutiveMember)
admin.site.register(CommunityInfo)
admin.site.register(Event)
admin.site.register(Defaulter)
admin.site.register(NavbarImage)
