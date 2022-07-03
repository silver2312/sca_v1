from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Users, Profile, PathUser


class UsersCreationFrom(UserCreationForm):
    class Meta:
        model = Users
        fields = ['email', 'name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('name', 'profile_image')

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            account = Users.objects.exclude(pk=self.instance.pk).get(name=name)
        except Users.DoesNotExist:
            return name
        raise forms.ValidationError('"%s" đã có người sử dụng.' % name)

    def save(self, commit=True):
        user_data = super(UserUpdateForm, self).save(commit=False)
        user_data.name = self.cleaned_data['name']
        user_data.profile_image = self.cleaned_data['profile_image']
        if commit:
            user_data.save()
        return user_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('background_image', 'name_music', 'url_music', 'des')

