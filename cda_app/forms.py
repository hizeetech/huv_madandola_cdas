from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, CDA, AdvertItem, AdvertImage, AdvertMessage, DonationProof


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    cda = forms.ModelChoiceField(
        queryset=CDA.objects.all(),
        required=False,
        empty_label="Select CDA",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 
                'phone_number', 'user_type', 'cda', 'image',
                'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
    
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'image')

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

# [Keep your other form classes as they are]

class AdvertItemForm(forms.ModelForm):
    class Meta:
        model = AdvertItem
        fields = ['category', 'title', 'description', 'amount', 'location', 'condition', 'phone_number']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number (e.g., +2348012345678)'}),
        }

class AdvertImageForm(forms.ModelForm):
    class Meta:
        model = AdvertImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

AdvertImageFormSet = inlineformset_factory(AdvertItem, AdvertImage, form=AdvertImageForm, extra=5, max_num=5, can_delete=False)

class AdvertMessageForm(forms.ModelForm):
    class Meta:
        model = AdvertMessage
        fields = ['name', 'phone_number', 'willing_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'willing_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Willing Amount'}),
        }

class DonationProofForm(forms.ModelForm):
    class Meta:
        model = DonationProof
        fields = ['donator_name', 'whatsapp_number', 'donated_amount', 'payment_receipt_image', 'donation_reference_number']
        widgets = {
            'donator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'donated_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_receipt_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'donation_reference_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }