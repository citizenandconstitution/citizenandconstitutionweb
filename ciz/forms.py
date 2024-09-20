from django import forms
from .models import Law,LegalCase,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	phone_no = forms.CharField(max_length = 20)
	first_name = forms.CharField(max_length = 20)
	last_name = forms.CharField(max_length = 20)
	class Meta:
		model = User
		fields = ['username', 'email', 'phone_no', 'password1', 'password2']
class LawForm(forms.ModelForm):
    class Meta:
        model = Law
        fields = ['title', 'video', 'description', 'story', 'points']
        
		
class LegalCaseForm(forms.ModelForm):
    class Meta:
        model = LegalCase
        fields = ['scenario', 'option_1', 'option_2', 'correct_answer']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','surname','profile_picture', 'bio', 'location', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'