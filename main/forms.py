from django import forms
from django.contrib.auth import get_user_model
from .models import Item
import os
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from cloudinary.models import CloudinaryResource

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ItemForm(forms.ModelForm):
    remove_image = forms.BooleanField(
        required=False,
        label='Remove current image'
    )

    class Meta:
        model = Item
        fields = ['title', 'status', 'description', 'category', 'location', 'img', 'contact_info', 'date_lost_or_found', 'reward']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Black Leather Wallet'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter description...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'date_lost_or_found': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'reward': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional (e.g. 5000)'
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone'
            }),
            'img': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_img(self):
        image = self.cleaned_data.get('img')
        
        # If no new image was uploaded, return the existing one
        if image is None or isinstance(image, CloudinaryResource):
            return image
            
        # Only perform validation if a new file was uploaded
        if image:
            # File type check (MIME)
            if image.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                raise ValidationError('Only JPEG and PNG images are allowed.')

            # File size check (limit to 4MB)
            if image.size > 4 * 1024 * 1024:
                raise ValidationError('Image file too large (maximum 4MB).')

            # File extension check
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file extension. Use .jpg, .jpeg, or .png.")

        return image
