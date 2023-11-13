from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Repeat your password'}),
                                error_messages={
                                    'password2': {
                                        'required': 'password must not be empty',

                                    }
                                }

                                )


    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password',
                  ]
        labels = {
            'username':'Username',
            'first_name':'First name',
            'last_name':'Last name',
            'email':'Email',
            'password':'Password',
        }
        help_texts = {
            'email':'The E-mail must be valid.',
            'password':'Password must have at least one uppercase letter,one lowercase letter and one number.the length should be at'
                                           'least 8 characters'
        }
        error_messages = {
            'first_name': {
                'required': 'This field must not be empty in first_name',
            },
            'last_name': {
                'required': 'This field must not be empty in first_name',
            },
            'username':{
                'required':'This field must not be empty',
                'max_length':'This field must have less than 3 characters',

            }
        }
        widgets = {
            'first_name':forms.TextInput(attrs={'placeholder':'Ex.:John'}),
            'password':forms.PasswordInput(attrs={'placeholder':'Type your password here'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your E-mail'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ex.:Lola'}),
        }



    def clean_password(self):
        data = self.cleaned_data.get('password')
        if 'atenção' in data:
            raise ValidationError('não digite %(pipoca)s , Valor invalido',code='invalid',
                                  params={'pipoca':'"atenção"'})

        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists :
            raise ValidationError('User E-mail is already in use ', code='invalid',)

        return email


    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if not data :
            raise ValidationError('This field must not be empty in first name',code='invalid',)

        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        if not data:
            raise ValidationError('This field must not be empty in last name', code='invalid',)

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password':'Password and Password 2 must be equal'
            })

