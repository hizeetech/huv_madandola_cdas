from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, CDA, AdvertItem, AdvertImage, AdvertMessage
from django.forms import inlineformset_factory

from django import forms

class CustomUserCreationForm(UserCreationForm):
    cda = forms.ModelChoiceField(queryset=CDA.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'cda': # cda is already handled above
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, cda=self.cleaned_data['cda'])
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

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