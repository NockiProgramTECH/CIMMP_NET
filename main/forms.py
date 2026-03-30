
from django import forms

class TemoignageForms(forms.Form):
    """Custom form"""
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name',
        }),
        label='First Name',
        help_text='Enter your first name'
    )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name',
        }),
        label='Last Name',
        help_text='Enter your last name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com',
        }),
        label='Email Address'
    )
    phone_number = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number',
        }),
        label='Phone Number',
        help_text='Enter your phone number'
    )

    cat_temoignage =forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter subject',
        }),
        label='Subject',
        help_text='Enter the subject of your testimony'
    )

    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Your message here',
        }),
        label='Message'
    )
    


    #fonction pour verifier et netttoyer les donner soumis par l'utilisateur
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long.")
        return phone


    def clean_email(self):
        email=self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError("Enter a valid email address.")
        return email
    