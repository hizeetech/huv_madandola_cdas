from django.db import models
from django.contrib.auth.models import User

class CDA(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cda = models.ForeignKey(CDA, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

class AdvertItem(models.Model):
    CATEGORY_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
        ('For Lease', 'For Lease'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    condition = models.CharField(max_length=100, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.category})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Schedule deletion after 15 days
        from django.utils import timezone
        from datetime import timedelta
        from django.core.management import call_command

        # This is a simplified approach. For production, consider using a task queue like Celery.
        # For now, we'll just log the scheduled deletion.
        deletion_time = self.published_date + timedelta(days=15)
        print(f"Scheduled deletion for AdvertItem {self.id} at {deletion_time}")

class AdvertImage(models.Model):
    advert_item = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='advert_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.advert_item.title} (Main: {self.is_main})"

# Create your models here.
