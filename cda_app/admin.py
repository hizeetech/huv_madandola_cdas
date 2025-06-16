from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CDA, UserProfile, Levy, UserLevy, Payment, ExecutiveMember, Event, CommunityInfo, Defaulter, NavbarImage, PaidMember, Committee, CommitteeMember, CommitteeToDo, CommitteeAchievement, AdvertCategory, AdvertItem, AdvertImage

admin.site.register(CDA)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cda', 'is_approved')
    list_filter = ('is_approved', 'cda')
    search_fields = ('user__username', 'cda__name')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        for user_profile in queryset:
            user_profile.user.is_active = True
            user_profile.user.save()
        self.message_user(request, "Selected users have been approved and activated.")
    approve_users.short_description = "Approve selected users"

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
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

admin.site.register(AdvertCategory)
class AdvertItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'is_approved', 'published_date')
    list_filter = ('is_approved', 'category', 'published_date')
    search_fields = ('title', 'description', 'user__username')

admin.site.register(AdvertItem, AdvertItemAdmin)
admin.site.register(AdvertImage)
