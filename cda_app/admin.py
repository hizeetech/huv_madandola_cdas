from django.contrib import admin
from django.contrib import admin
from .models import CDA, UserProfile, Levy, UserLevy, Payment, ExecutiveMember, Event, CommunityInfo, Defaulter, NavbarImage, PaidMember, Committee, CommitteeMember, CommitteeToDo, CommitteeAchievement

admin.site.register(CDA)
admin.site.register(UserProfile)
admin.site.register(Levy)
admin.site.register(UserLevy)
admin.site.register(Payment)
admin.site.register(ExecutiveMember)
admin.site.register(CommunityInfo)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'image')
    search_fields = ('title', 'location')
    list_filter = ('date', 'location')

admin.site.register(Event, EventAdmin)
class DefaulterAdmin(admin.ModelAdmin):
    list_display = ('name', 'cda', 'amount_indebted', 'title_defaulted', 'status', 'image')
    search_fields = ('name', 'cda', 'title_defaulted')
    list_filter = ('cda', 'status', 'title_defaulted')

admin.site.register(Defaulter, DefaulterAdmin)
admin.site.register(NavbarImage)

class PaidMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'cda', 'amount_paid', 'purpose_of_payment', 'payment_date', 'image')
    search_fields = ('name', 'cda', 'purpose_of_payment')
    list_filter = ('cda', 'purpose_of_payment', 'payment_date')

admin.site.register(PaidMember, PaidMemberAdmin)

admin.site.register(Committee)
admin.site.register(CommitteeMember)
admin.site.register(CommitteeToDo)
admin.site.register(CommitteeAchievement)
