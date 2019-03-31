from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, UserRegModel, Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserActForm, PostLoaderForm, PostTokenForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import random
import string
from .validinput import valdno


from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class HomeLogout(ListView):
	models = Post
	template_name = 'blog/homelogout.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'data'
	odering = ['-date_posted']
	paginate_by = 2
	def get_queryset(self):
		# usersid = User.objects.get(username='root').id
		return (Post.objects.filter(showpost=1))[::-1]

def homelogout(request):
	content = {
		'data':(Post.objects.filter(showpost=1))[::-1]
		}
	# .all()
	return render(request,'blog/homelogout.html',content)

def tablink(request):
	data = Post.objects.all()
	content = {
		'posts':data
		}
	return render(request,'blog/tablink.html',content)
	
def about(request):
	return render(request,'blog/about.html',{'title':'About'})
	
def termcond(request):
	return render(request,'blog/termcond.html',{'title':'Terms and Conditions'})
	
#--------------------------------------- User registration start--------------------------------------	
def register(request):
	if request.method == 'POST':
		strg = ""
		r_form = UserRegisterForm(request.POST)
		try:
			unqemailq = User.objects.get(email=request.POST['email']).email
			if r_form.is_valid():
				user = r_form.save(commit=False)
				user.is_active = False
				userhere = user.username
				user.save()
				for i in range(6):
					strg += random.choice(string.ascii_letters+string.digits+"&!@#*+")
				event_here =  UserRegModel(user=userhere, codesent=strg)
				event_here.save()
				message = render_to_string('accounts/acc_active_email.html', {
					'user':user, 
					'actcode':strg
				})
				mail_subject = 'Activate your blog account.'
				to_email = r_form.cleaned_data.get('email')
				email = EmailMessage(mail_subject, message, to=[to_email])
				email.send()
				return render(request, 'accounts/activate_mail.html')
		except:
				messages.error(request, f'Email Id Already exsist.')
				return render(request, 'user/register.html', {'r_form': r_form})
	else:
		r_form = UserRegisterForm()
		# a_form = UserRegForm()
	return render(request, 'user/register.html', {'r_form': r_form})

def activate(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.POST['user'])
		event = UserRegModel.objects.get(user=request.POST['user'])
		act_form = UserActForm(request.POST)
		if act_form.is_valid() and (event.codesent==request.POST['coderesv']) and event.coderesv=="null":
			event.coderesv=request.POST['coderesv']
			event.save()
			user.is_active = True
			user.save()
			return redirect('blog-login')
		else:
			return render(request, 'accounts/activate_fail.html')
	else:
		act_form = UserActForm()
		return render(request, 'accounts/activate.html',{'act_form':act_form})

#--------------------------------------- User registration end--------------------------------------	
#--------------------------------------- Post Management start--------------------------------------	
class HomePostListView(LoginRequiredMixin, ListView):
	models = Post
	template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	odering = ['-date_posted']
	paginate_by = 2
	def get_queryset(self):
		# usersid = User.objects.get(username='root').id
		return (Post.objects.filter(showpost=1))[::-1]

class PostDetailView(LoginRequiredMixin, DetailView):
	models = Post
	def get_queryset(self):
		return Post.objects.filter(showpost=1)

class PostCreateView(LoginRequiredMixin, CreateView):
	form_class = PostLoaderForm
	template_name = 'blog/post_form.html' # <app>/<model>_<viewtype>.html
	success_url = '/addtoken/'
	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.college = Profile.objects.get(user=self.request.user).college
		form.instance.mobileno = Profile.objects.get(user=self.request.user).mobileno
		return super().form_valid(form)
	
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	models = Post
	template_name = 'blog/post_form.html' # <app>/<model>_<viewtype>.html
	fields = ['title', 'content', 'image']
	
	def get_queryset(self):
		return Post.objects.all()
		
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	models = Post
	template_name = 'blog/postdelete.html'
	fields = ['title']
	success_url = "/deltoken/"
	def get_queryset(self):
		return Post.objects.all()
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.showpost = 0
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False		

class UserPostListView(ListView):
	models = Post
	template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 2
	
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user, showpost=1).order_by('-date_posted')
#--------------------------------------- Post Management end--------------------------------------	
#--------------------------------------- Token Management start--------------------------------------	
@login_required	
def tokenaward(request, pk):
	
	event = Post.objects.get(id=pk)
	myacc = Profile.objects.get(user=getiduser(event.author))
	if request.method == 'POST':
		donoracc = Profile.objects.get(user=request.user)
		t_form = PostTokenForm(request.POST)		
		if t_form.is_valid() and int(event.tokens) < int(request.POST['tokens']):
			if int(event.tokens) == 100 and int(donoracc.tokenacc) > int(request.POST['tokens']):
				myacc.tokenacc = str(int(myacc.tokenacc) + int(request.POST['tokens']))
				myacc.save()
				donoracc.tokenacc = str(int(donoracc.tokenacc) - int(request.POST['tokens']))
				donoracc.save()
				event.tokens = request.POST['tokens']
				event.tokenbyuser = request.user.username
				event.save()
				
			elif event.tokenbyuser == request.user and int(donoracc.tokenacc) > int(request.POST['tokens']):
				myacc.tokenacc = str(int(myacc.tokenacc) + int(request.POST['tokens']))
				myacc.save()
				donoracc.tokenacc = str(int(donoracc.tokenacc) - int(request.POST['tokens']) + int(event.tokens))
				donoracc.save()
				event.tokens = request.POST['tokens']
				event.tokenbyuser = request.user.username
				event.save()

			elif int(donoracc.tokenacc) > int(request.POST['tokens']):
				myacc.tokenacc = str(int(myacc.tokenacc) + int(request.POST['tokens']) - int(event.tokens))
				myacc.save()
				donoracc.tokenacc = str(int(donoracc.tokenacc) - int(request.POST['tokens']))
				donoracc.save()
				predonoracc = Profile.objects.get(user=getiduser(event.tokenbyuser))
				predonoracc.tokenacc = str(int(predonoracc.tokenacc) + int(event.tokens))
				predonoracc.save()
				event.tokens = request.POST['tokens']
				event.tokenbyuser = request.user.username
				event.save()
				
			else:
				messages.error(request, f'You cannot book. Your balance token is %s which is less than %s'%(donoracc.tokenacc, request.POST['tokens']))
			
			
			# messages.success(request, f'Account is updated!')
			return redirect('blog-home')
		else:
			# messages.error(request, f'Already Booked with %s token. Give more token to book.'%event.tokens)
			return redirect(request.get_full_path())
	else:
		t_form = PostTokenForm()
		if int(event.tokens) > 0:messages.error(request, f'Already Booked with %s token. Give more token to book.'%event.tokens)
		context = {
			'form' : t_form
		}
		return render(request, 'blog/posttoken.html', context)	

@login_required
def tokendetails(request):
	tokengot = 0
	tokengotq = Post.objects.filter(author=request.user, showpost=1).exclude(tokenbyuser="null")[::-1]
	context = {
		'data' : tokengotq
	}
	return render(request, 'accounts/tokendetails.html', context)

@login_required
def addtoken(request):
	event = Profile.objects.get(user=request.user)
	e = Post.objects.filter(author=request.user).latest('id')
	# messages.error(request, e.tokens)
	if int(e.tokens) == 0:
		event.tokenacc = str(int(event.tokenacc) + 100)
		event.save()
		e.tokens=100
		e.save()
	return redirect('/home/')	

@login_required
def deltoken(request):
	event = Profile.objects.get(user=request.user)
	event.tokenacc = str(int(event.tokenacc) - 100)
	event.save()
	return redirect('/home/')	

@login_required
def retbook(request, pk):
	event = Post.objects.get(id=pk)
	urldir = "/post/%d/"%pk
	if event.tokenbyuser != "null" and event.bookeditem == 1:
		donoracc = Profile.objects.get(user=getiduser(event.tokenbyuser))
		myacc = Profile.objects.get(user=getiduser(event.author))
		myacc.tokenacc = str(int(myacc.tokenacc) - int(event.tokens) + 200)
		donoracc.tokenacc = str(int(donoracc.tokenacc) + int(event.tokens) +100)
		event.bookeditem = 0
		event.tokens = 100
		event.tokenbyuser = "null"
		myacc.save()
		donoracc.save()
		event.save()
		return redirect(urldir)
	else:
		if event.bookeditem == 0:
			messages.success(request, f"You haven't marked it Shared.")
		else:
			messages.success(request, f"Book is not shared yet.")
		return redirect(urldir)
		
@login_required
def booked(request, pk):
	event = Post.objects.get(id=pk)
	urldir = "/post/%d/"%pk
	if event.bookeditem == 0 and event.tokenbyuser!="null" :
		event.bookeditem = 1
		event.save()
		return redirect(urldir)
	else:
		if event.tokenbyuser!="null": messages.success(request, f'Already shared')
		else: messages.success(request, f'No Buyers')
		return redirect(urldir)

	
#--------------------------------------- Token Management end--------------------------------------	
	
@login_required	
def profile(request):
	e = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid() and valdno(request.POST['mobileno']):
			u_form.save()
			p_form.save()
			messages.success(request, f'Account is updated!')
			return redirect('profile')
		else:
			messages.error(request, f'Account is NOT updated! Check Mobile number. Enter it in the format as shown in brackets')
			return redirect('profile')
	else:
		tokengot = 0
		u_form = UserUpdateForm()
		p_form = ProfileUpdateForm()
		tokengotq = Post.objects.filter(author=request.user, showpost=1)
		for i in tokengotq:
			tokengot += int(i.tokens)
		# tokengot = int(Profile.objects.get(user=request.user.username).tokenacc)
	context = {
		'u_form' : u_form,
		'p_form' : p_form,
		't_form' : e.tokenacc
	}
	return render(request, 'accounts/profile.html', context)	
	

def getiduser(userhere):
	return User.objects.get(username=userhere).id