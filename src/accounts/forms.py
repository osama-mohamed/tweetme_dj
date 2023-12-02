from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
  username = forms.CharField(label='Username')
  email = forms.EmailField(label='Email Address')
  password = forms.CharField(widget=forms.PasswordInput)
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
  
  class Meta:
    model = User
    fields = [
      'username',
      'email',
      'password',
      'password2',
    ]

  def clean_username(self):
    username = self.cleaned_data.get('username')
    qs = User.objects.filter(username=username)
    if qs.exists():
      raise forms.ValidationError('Username is taken.')
    return username
  
  def clean_email(self):
    email = self.cleaned_data.get('email')
    qs = User.objects.filter(email=email)
    if qs.exists():
      raise forms.ValidationError('This email is already registered.')
    return email

  def clean_password2(self):
    password = self.cleaned_data.get('password')
    password2 = self.cleaned_data.get('password2')
    if password != password2:
      raise forms.ValidationError('Passwords must match.')
    return password