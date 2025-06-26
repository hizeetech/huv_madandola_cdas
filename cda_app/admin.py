from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
""" from import_export.admin import ExportActionMixin """
from django.utils.html import format_html

from .models import (
    CDA, Levy, UserLevy, Payment, ExecutiveMember,
    Event, CommunityInfo, Defaulter, NavbarImage, PaidMember,
    Committee, CommitteeMember, CommitteeToDo, CommitteeAchievement,
    AdvertCategory, AdvertItem, AdvertImage, Artisan, Professional,
    ProjectDonation, ProjectImage, DonationProof, CustomUser, RegularLevy, ProjectDonationModal, BirthdayCelebrant, WellWishes
)

@admin.register(ProjectDonationModal)
class ProjectDonationModalAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'button_link')
    search_fields = ('title', 'content')


from django.contrib import admin
from django.utils import timezone
from .models import BirthdayCelebrant
from .utils import send_birthday_email
from django.utils.html import format_html

from django.contrib.admin import SimpleListFilter

class HasUserFilter(SimpleListFilter):
    title = 'has user account'
    parameter_name = 'has_user'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Has user account'),
            ('no', 'No user account'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(user__isnull=False)
        if self.value() == 'no':
            return queryset.filter(user__isnull=True)
        return queryset
    
class BirthdayCelebrantAdmin(admin.ModelAdmin):
    list_display = (
        'celebrant_image',
        'name', 
        'user_link',
        'formatted_date_of_birth',
        'is_birthday_today', 
        'last_celebrated_display',
        'days_until_next_birthday'
    )
    search_fields = ('name', 'user__username', 'user__email')
    list_filter = (
    ('date_of_birth', admin.DateFieldListFilter),
    HasUserFilter,
    )
    list_select_related = ('user',)
    readonly_fields = (
        'is_birthday_today',
        'days_until_next_birthday',
        'celebrant_image_preview'
    )
    actions = ['celebrate_birthday', 'send_test_email']
    date_hierarchy = 'date_of_birth'
    autocomplete_fields = ['user']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'image', 'celebrant_image_preview')
        }),
        ('Birthday Information', {
            'fields': ('date_of_birth', 'admin_wishes')
        }),
        ('Celebration Status', {
            'fields': ('is_birthday_today', 'days_until_next_birthday'),
            'classes': ('collapse',)
        }),
    )

    def celebrant_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />',
                obj.image.url
            )
        return "-"
    celebrant_image.short_description = "Image"

    def celebrant_image_preview(self, obj):
        return self.celebrant_image(obj)
    celebrant_image_preview.short_description = "Image Preview"

    def user_link(self, obj):
        if obj.user:
            url = f"/admin/{obj.user._meta.app_label}/{obj.user._meta.model_name}/{obj.user.pk}/"
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = "User Account"
    user_link.admin_order_field = 'user__username'

    def formatted_date_of_birth(self, obj):
        return obj.date_of_birth.strftime("%b %d, %Y")
    formatted_date_of_birth.short_description = "Birth Date"
    formatted_date_of_birth.admin_order_field = 'date_of_birth'

    def last_celebrated_display(self, obj):
        if obj.last_celebrated_year:
            return f"{obj.last_celebrated_year} ({(timezone.now().year - obj.last_celebrated_year)} year(s) ago)"
        return "Never"
    last_celebrated_display.short_description = "Last Celebrated"

    def days_until_next_birthday(self, obj):
        today = timezone.now().date()
        next_birthday = obj.date_of_birth.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days
    days_until_next_birthday.short_description = "Days Until Next"

    def is_birthday_today(self, obj):
        return obj.is_birthday_today()
    is_birthday_today.boolean = True
    is_birthday_today.short_description = "Today?"

    def celebrate_birthday(self, request, queryset):
        today = timezone.now().date()
        updated = queryset.update(last_celebrated_year=today.year)
        
        # Send birthday emails
        sent_count = 0
        for celebrant in queryset:
            if celebrant.user:
                send_birthday_email(celebrant.user)
                sent_count += 1
        
        self.message_user(
            request, 
            f"Celebrated {updated} birthday(s). {sent_count} email(s) sent.",
            level='SUCCESS' if sent_count == updated else 'WARNING'
        )
    celebrate_birthday.short_description = "🎉 Celebrate selected birthdays"

    def send_test_email(self, request, queryset):
        test_email = "test@example.com"  # Change to your test email
        for celebrant in queryset:
            send_birthday_email(celebrant.user or None, test_email=test_email)
        self.message_user(
            request,
            f"Sent test emails to {test_email} for {queryset.count()} celebrant(s)",
            level='INFO'
        )
    send_test_email.short_description = "✉️ Send test email"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Annotate with additional calculated fields if needed
        return qs

admin.site.register(BirthdayCelebrant, BirthdayCelebrantAdmin)


class WellWishesAdmin(admin.ModelAdmin):
    list_display = ('celebrant', 'sender_name', 'created_at')
    list_filter = ('celebrant',)
    search_fields = ('sender_name', 'message')

admin.site.register(WellWishes, WellWishesAdmin)


# Unregister default User model if registered
from django.conf import settings

""" if User in admin.site._registry:
    admin.site.unregister(User) """

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'phone_number', 'user_type', 'is_approved', 'is_active', 'is_staff')
    list_filter = ('is_approved', 'user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 
                                    'user_type', 'cda', 'image', 'is_approved')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# ... [keep all your other admin registrations below] ...

""" @admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 
                    'user_type', 'cda', 'is_approved')
    list_filter = ('is_approved', 'cda', 'user_type')
    search_fields = ('user__username', 'user__first_name', 
                    'user__last_name', 'phone_number')
    
    def first_name(self, obj):
        return obj.user.first_name
    first_name.admin_order_field = 'user__first_name'
    
    def last_name(self, obj):
        return obj.user.last_name
    last_name.admin_order_field = 'user__last_name' """

@admin.register(ExecutiveMember)
class ExecutiveMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'start_date', 'end_date', 
                    'phone_number', 'image')
    list_filter = ('position', 'start_date', 'end_date')
    search_fields = ('name', 'position')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'image')
    search_fields = ('title', 'location')
    list_filter = ('date', 'location')

from .utils import send_defaulter_email

@admin.register(Defaulter)
class DefaulterAdmin(admin.ModelAdmin):
    list_display = ('name', 'cda', 'amount_indebted', 'title_defaulted', 
                    'status', 'image')
    search_fields = ('name', 'cda', 'title_defaulted')
    list_filter = ('cda', 'status', 'title_defaulted')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Check if the defaulter is being created or updated to 'Indebt' status
        if obj.status == 'Indebt':
            # Attempt to find a CustomUser by phone number
            user = CustomUser.objects.filter(phone_number=obj.phone_number).first()
            if user:
                send_defaulter_email(user)
                messages.success(request, f"Defaulter email sent to {user.email}.")
            else:
                messages.warning(request, f"No user found with phone number {obj.phone_number}. Defaulter email not sent.")

@admin.register(PaidMember)
class PaidMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'cda', 'amount_paid', 'purpose_of_payment', 
                    'payment_date', 'image')
    search_fields = ('name', 'cda', 'purpose_of_payment')
    list_filter = ('cda', 'purpose_of_payment', 'payment_date')

class AdvertImageInline(admin.TabularInline):
    model = AdvertImage
    extra = 1

@admin.register(AdvertItem)
class AdvertItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'is_approved', 
                    'published_date', 'display_main_image')
    list_filter = ('is_approved', 'category', 'published_date')
    search_fields = ('title', 'description', 'user__username')
    inlines = [AdvertImageInline]

    def display_main_image(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" width="50" height="50" />', 
                            first_image.image.url)
        return "No Image"
    display_main_image.short_description = "Main Image"

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class DonationProofInline(admin.TabularInline):
    model = DonationProof
    extra = 1

@admin.register(ProjectDonation)
class ProjectDonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'estimated_cost', 'bank_name', 
                    'account_number', 'beneficiary', 'reference_number')
    search_fields = ('title', 'bank_name', 'beneficiary')
    inlines = [ProjectImageInline, DonationProofInline]

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'phone_number', 'display_image')
    search_fields = ('name', 'job_title')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', 
                            obj.image.url)
        return "No Image"
    display_image.short_description = "Image"

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'phone_number', 'display_image')
    search_fields = ('name', 'job_title')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', 
                            obj.image.url)
        return "No Image"
    display_image.short_description = "Image"

# cda_app/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import RegularLevy
from .utils import send_payment_approved_email, send_payment_rejected_email

@admin.register(RegularLevy)
class RegularLevyAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'year', 'payment_for', 'amount', 'status', 'colored_status', 'proof_of_payment_link', 'created_at')
    list_filter = ('status', 'payment_for', 'month', 'year', 'cda')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('proof_of_payment_preview', 'created_at', 'updated_at', 'colored_status')
    list_editable = ('status',)
    actions = ['approve_payments', 'reject_payments']
    
    def colored_status(self, obj):
        colors = {
            'unpaid': 'red',
            'pending': 'orange',
            'paid': 'green',
            'rejected': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status Display'
    
    def proof_of_payment_link(self, obj):
        if obj.proof_of_payment:
            return format_html('<a href="{}" target="_blank">View Proof</a>', obj.proof_of_payment.url)
        return "No Proof"
    proof_of_payment_link.short_description = "Proof"
    
    def proof_of_payment_preview(self, obj):
        if obj.proof_of_payment:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.proof_of_payment.url)
        return "No Proof"
    proof_of_payment_preview.short_description = "Proof Preview"
    
    def approve_payments(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='paid')
        for levy in queryset.filter(status='paid'):
            send_payment_approved_email(levy)
        self.message_user(request, f"{updated} payments approved.")
    approve_payments.short_description = "Approve selected payments"
    
    def reject_payments(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected', proof_of_payment=None)
        for levy in queryset.filter(status='rejected'):
            send_payment_rejected_email(levy)
        self.message_user(request, f"{updated} payments rejected.")
    reject_payments.short_description = "Reject selected payments"
    
    fieldsets = (
        (None, {
            'fields': ('user', 'month', 'year', 'payment_for', 'amount', 'cda', 'status')
        }),
        ('Proof of Payment', {
            'fields': ('proof_of_payment', 'proof_of_payment_preview')
        }),
        ('Dates (Read Only)', {
            'fields': ('created_at', 'updated_at', 'colored_status'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Only process if proof_of_payment was uploaded
        if 'proof_of_payment' in form.changed_data and obj.proof_of_payment:
            obj.status = 'pending'  # Automatically set status to pending when proof is uploaded
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'paid':
            return [f.name for f in self.model._meta.fields] + ['proof_of_payment_preview', 'colored_status']
        return super().get_readonly_fields(request, obj)

# Simple model registrations
admin.site.register(CDA)
admin.site.register(Levy)
admin.site.register(UserLevy)
admin.site.register(Payment)
admin.site.register(CommunityInfo)
admin.site.register(NavbarImage)
admin.site.register(Committee)
admin.site.register(CommitteeMember)
admin.site.register(CommitteeToDo)
admin.site.register(CommitteeAchievement)
admin.site.register(AdvertCategory)
admin.site.register(AdvertImage)
admin.site.register(ProjectImage)
admin.site.register(DonationProof)