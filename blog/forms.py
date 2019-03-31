from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, UserRegModel, Post, Chat, FeedbackDB
class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(max_length=300)
		
	class Meta:
		model = User
		fields = ('email',)	
		
class ProfileUpdateForm(forms.ModelForm):
	mobileno = forms.CharField(max_length=15, label="Mobile Number (+91 XXXXXXXXXX)")
	nameu = forms.CharField(max_length=100, label="Your Name(Full Name)")
	class Meta:
		model = Profile
		fields = ['nameu', 'image', 'college','mobileno']

class UserActForm(forms.ModelForm):
	user = forms.CharField(max_length=100, label="Username")
	coderesv = forms.CharField(max_length=10, label="Activation Code")
	class Meta:
		model = UserRegModel
		fields = ['user', 'coderesv']
		
class PostLoaderForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ['title', 'content', 'image']

class ChatForm(forms.ModelForm):
	
	class Meta:
		model = Chat
		fields = ['msg', ]
		
class PostTokenForm(forms.ModelForm):
	tokens = forms.CharField(max_length=100, label="Token")
	class Meta:
		model = Post
		fields = ['tokens']
		
class FeedbackForm(forms.ModelForm):
	
	class Meta:
		model = FeedbackDB
		fields = ['msg', ]
