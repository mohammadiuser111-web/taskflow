from django import forms
from django.contrib.auth.models import User
from .models import Profile,Project
class RegisterForm(forms.Form):
    username=forms.CharField(max_length=150); password=forms.CharField(widget=forms.PasswordInput); password2=forms.CharField(widget=forms.PasswordInput,label='تکرار رمز عبور')
    def clean(self):
        d=super().clean()
        if d.get('password')!=d.get('password2'): raise forms.ValidationError('رمزهای عبور یکسان نیستند.')
        if User.objects.filter(username=d.get('username')).exists(): raise forms.ValidationError('این نام کاربری قبلاً گرفته شده است.')
        return d
class ProfileForm(forms.ModelForm):
    class Meta: model=Profile; fields=['avatar','bio']
class ProjectForm(forms.ModelForm):
    class Meta: model=Project; fields=['name','description']
