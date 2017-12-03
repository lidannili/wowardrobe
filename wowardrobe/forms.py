from django import forms
from django.contrib.auth.models import User
from wowardrobe.models import *
from django.forms import extras
MAX_UPLOAD_SIZE = 2500000

# class ClothesForm(forms.ModelForm):
#     class Meta:
#         model = Clothes
#         fields = ( 'image', 'text')

#     def clean_picture(self):
#         imgage = self.cleaned_data['image']
#         if not image:
#             raise forms.ValidationError('You must upload a picture')
#         if not picture.content_type or not picture.content_type.startswith('image'):
#             raise forms.ValidationError('File type is not image')
#         if image.size > MAX_UPLOAD_SIZE:
#             raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
#         return image

class RegistrationForm(forms.Form):
    email      = forms.CharField(max_length = 50,
                                 widget = forms.EmailInput())
    username   = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name  = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput())
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = forms.ChoiceField(widget = forms.RadioSelect,choices = GENDER_CHOICES)
    BIRTH_YEARS = DOY = ('1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
       '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
       '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
       '2012', '2013', '2014', '2015','2016','2017')
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years = BIRTH_YEARS))


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username') #confirm username not in the database
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')      #confirm email address not in the database
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError("Email Already Exists")

        return email


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('height',
                   'weight',
                   'date_of_birth',
                   'email_confirm',
                   'image',
                   'gender',
                   'budget',)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',
                   'gender',
                   'email_confirm')
        widgets = {
            'image' : forms.FileInput(),
        }

    def clean_picture(self):
        picture = self.cleaned_data['image']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture






