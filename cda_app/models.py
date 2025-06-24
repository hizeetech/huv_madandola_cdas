from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


class CDA(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    

""" from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cda = models.ForeignKey(CDA, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='tenant')
    
    def __str__(self):
        return self.user.username """
    

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    ]
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='tenant')
    cda = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # Add this field

    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Levy(models.Model):
    CDA_CHOICES = [
        ('Unity CDA', 'Unity CDA'),
        ('Harmony CDA', 'Harmony CDA'),
        ('Valley-View CDA', 'Valley-View CDA'),
    ]
    LEVY_TYPE_CHOICES = [
        ('Development Fees', 'Development Fees'),
        ('Others', 'Others'),
        ('Electricity', 'Electricity'),
        ('Security Fees', 'Security Fees'),
    ]

    cda = models.ForeignKey(CDA, on_delete=models.CASCADE, null=True, blank=True, help_text="Leave blank for joint payments (Electricity, Security Fees)")
    levy_type = models.CharField(max_length=50, choices=LEVY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.levy_type} - {self.amount}"

class UserLevy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    levy = models.ForeignKey(Levy, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.levy.levy_type} - Due: {self.amount_due}"

class Payment(models.Model):
    user_levy = models.ForeignKey(UserLevy, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.user_levy.user.username} for {self.user_levy.levy.levy_type}"


class ExecutiveMember(models.Model):
    cda = models.ForeignKey(CDA, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='executive_members/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

class Defaulter(models.Model):
    image = models.ImageField(upload_to='defaulter_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    cda_choices = [
        ('Unity CDA', 'Unity CDA'),
        ('Harmony CDA', 'Harmony CDA'),
        ('Valley-View CDA', 'Valley-View CDA'),
    ]
    cda = models.CharField(max_length=100, choices=cda_choices, verbose_name="CDA")
    amount_indebted = models.DecimalField(max_digits=10, decimal_places=2)
    debt_for_choices = [
        ('Security Fees', 'Security Fees'),
        ('Electricity', 'Electricity'),
        ('Development Levy', 'Development Levy'),
        ('Others', 'Others'),
    ]
    title_defaulted = models.CharField(max_length=200, choices=debt_for_choices, verbose_name="Debt For:")
    status_choices = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('In Progress', 'In Progress'),
        ('Indebt', 'Indebt'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='Pending')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.title_defaulted}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} on {self.date}"

class CommunityInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Community Info"

    def __str__(self):
        return self.title

class NavbarImage(models.Model):
    POSITION_CHOICES = [
        ('left', 'Left Corner'),
        ('right', 'Right Corner'),
    ]
    image = models.ImageField(upload_to='navbar_images/')
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Navbar Image ({self.position})"

class PaidMember(models.Model):
    image = models.ImageField(upload_to='paid_member_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    cda_choices = [
        ('Unity CDA', 'Unity CDA'),
        ('Harmony CDA', 'Harmony CDA'),
        ('Valley-View CDA', 'Valley-View CDA'),
    ]
    cda = models.CharField(max_length=100, choices=cda_choices, verbose_name="CDA")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purpose_choices = [
        ('Security Fees', 'Security Fees'),
        ('Electricity', 'Electricity'),
        ('Development Levy', 'Development Levy'),
        ('Others', 'Others'),
    ]
    purpose_of_payment = models.CharField(max_length=200, choices=purpose_choices, verbose_name="Purpose of Payment")
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount_paid} ({self.purpose_of_payment})"


class Committee(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    roles_responsibilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CommitteeMember(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    image = models.ImageField(upload_to='committee_members/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.committee.name}"

class CommitteeToDo(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='todos')
    task = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.task} ({self.committee.name})"

class CommitteeAchievement(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.committee.name})"

class AdvertCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ProjectDonation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    beneficiary = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(ProjectDonation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"

class DonationProof(models.Model):
    project_donation = models.ForeignKey(ProjectDonation, on_delete=models.CASCADE, related_name='donation_proofs')
    donator_name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=20)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_receipt_image = models.ImageField(upload_to='donation_proofs/')
    donation_reference_number = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proof for {self.project_donation.title} by {self.donator_name}"

class AdvertItem(models.Model):
    CATEGORY_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
        ('For Lease', 'For Lease'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

class AdvertImage(models.Model):
    advert_item = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='advert_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.advert_item.title}"

class Proposal(models.Model):
    advert = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='proposals')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    proposed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal for {self.advert.title} by {self.name}"

class AdvertMessage(models.Model):
    advert = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    willing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    message_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.advert.title} from {self.name}"

class Artisan(models.Model):
    image = models.ImageField(upload_to='artisans/', blank=True, null=True)
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class Professional(models.Model):
    image = models.ImageField(upload_to='professionals/', blank=True, null=True)
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# cda_app/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class RegularLevy(models.Model):
    MONTH_CHOICES = [
        ('January', _('January')),
        ('February', _('February')),
        ('March', _('March')),
        ('April', _('April')),
        ('May', _('May')),
        ('June', _('June')),
        ('July', _('July')),
        ('August', _('August')),
        ('September', _('September')),
        ('October', _('October')),
        ('November', _('November')),
        ('December', _('December')),
    ]
    
    PAYMENT_FOR_CHOICES = [
        ('Electricity', _('Electricity')),
        ('Security', _('Security')),
        ('Development Levies', _('Development Levies')),
        ('Sanitations', _('Sanitations')),
        ('Others', _('Others')),
    ]
    
    STATUS_CHOICES = [
        ('unpaid', _('Unpaid')),
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('rejected', _('Rejected')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='levies'
    )
    
    month = models.CharField(
        _('Month'),
        max_length=20,
        choices=MONTH_CHOICES,
        help_text=_('Select the month for this levy')
    )
    
    year = models.PositiveIntegerField(
        _('Year'),
        help_text=_('Enter the year for this levy')
    )
    
    payment_for = models.CharField(
        _('Payment For'),
        max_length=50,
        choices=PAYMENT_FOR_CHOICES,
        help_text=_('Select the purpose of this payment')
    )
    
    amount = models.DecimalField(
        _('Amount'),
        max_digits=10,
        decimal_places=2,
        help_text=_('Enter the amount to be paid')
    )
    
    cda = models.CharField(
        _('CDA'),
        max_length=100,
        help_text=_('Community Development Association')
    )
    
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid',
        help_text=_('Current payment status')
    )
    
    proof_of_payment = models.ImageField(
        _('Proof of Payment'),
        upload_to='payment_proofs/',
        null=True,
        blank=True,
        help_text=_('Upload proof of payment'),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Regular Levy')
        verbose_name_plural = _('Regular Levies')
        ordering = ['-year', '-month']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'month', 'year', 'payment_for'],
                name='unique_user_levy_per_month'
            )
        ]

    def __str__(self):
        return f"{self.get_month_display()} {self.year} - {self.get_payment_for_display()} ({self.user.username})"

    def clean(self):
        """Validate model fields before saving"""
        errors = {}
        
        # Validate year is reasonable (2000-current year + 1)
        current_year = timezone.now().year
        if self.year < 2000 or self.year > current_year + 1:
            errors['year'] = _('Year must be between 2000 and %(current)s') % {'current': current_year + 1}
        
        # Validate amount is positive
        if self.amount <= 0:
            errors['amount'] = _('Amount must be positive')
        
        # Validate payment proof when status is pending/paid
        if self.status in ['pending', 'paid'] and not self.proof_of_payment:
            errors['proof_of_payment'] = _('Proof of payment is required for this status')
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Custom save method with validation and auto-fields"""
        # Auto-fill CDA if not provided
        if not self.cda and hasattr(self.user, 'cda'):
            self.cda = self.user.cda
        
        # Run full validation before saving
        self.full_clean()
        
        # Set timestamps
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)

    def get_status_color(self):
        """Helper method to get status color for UI"""
        status_colors = {
            'unpaid': 'danger',
            'pending': 'warning',
            'paid': 'success',
            'rejected': 'secondary'
        }
        return status_colors.get(self.status, 'info')

    @property
    def is_overdue(self):
        """Check if the levy is overdue (unpaid and past current month)"""
        if self.status != 'unpaid':
            return False
            
        current_date = timezone.now()
        current_month = current_date.month
        current_year = current_date.year
        
        # Get month number from month name
        month_number = list(dict(self.MONTH_CHOICES).keys()).index(self.month) + 1
        
        return (self.year < current_year) or \
                (self.year == current_year and month_number < current_month)