from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import random
import string
from .validinput import valdno
from .funcs import Postupdater, postid
#from .backlog import backloghome, backlog, backlogtoken


from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import datetime
from django.utils import timezone
# , title__contains="test crt backlog"
@login_required
def msgs(request, op):
	head = 0
	if op == 1:
		data = Chat.objects.filter(receiver=request.user, showmsg=1).order_by('-date_posted')
		event = Profile.objects.get(user=request.user)
		event.msgscount = 0
		head = 1
		event.save()
	else:
		head = 2
		data = Chat.objects.filter(sender=request.user, showmsg=1).order_by('-date_posted')
	content = {
		'head':head,
		'msgs':data
	}
	return render(request,'blog/msgs.html',content)

@login_required
def chatcreate(request, pk):
	if request.method == 'POST':
		chat_form = ChatForm(request.POST)
		if chat_form.is_valid():
			msgsent = chat_form.save(commit=False)
			msgsent.sender = request.user.username
			msgsent.receiver = Post.objects.get(id=pk).author
			msgsent.date_posted = datetime.now()
			msgsent.post_id = pk
			msgsent.save()
			event = Profile.objects.get(user=msgsent.receiver)
			event.msgscount += 1
			event.save()
			#backlog(request.META['REMOTE_ADDR'], "chats", ("{ Sender:"+str(msgsent.sender)+" Receiver:"+str(msgsent.receiver)+" Date:"+str(msgsent.date_posted)+" Post:"+str(msgsent.post_id)+" Msg:"+str(msgsent.msg)+" }\n"), str(msgsent.sender))
			return redirect('blog-home')
	else:
		chat_form = ChatForm()
	return render(request, 'blog/msgform.html', {'chat_form': chat_form})

@login_required
def chatdel(request, pk):
	event = Chat.objects.get(id=pk)
	if request.user.username == event.receiver:
		event.showmsg = 0
		event.save()
	else:
		# Undo msg sent
		event.showmsg = 0
		event.save()
		reccounter = Profile.objects.get(user=getiduser(event.receiver))
		reccounter.msgscount -= 1
		reccounter.save()
	#backlog(request.META['REMOTE_ADDR'], "chats", (" DEL{ Sender:"+str(event.sender)+" Receiver:"+str(event.receiver)+" Date:"+str(event.date_posted)+" Post:"+str(event.post_id)+" Msg:"+str(event.msg)+" }\n"), str(event.sender))
	return redirect('blog-home')# redirect(request.get_full_path())

@login_required
def chatreply(request, pk):
	if request.method == 'POST':
		chat_form = ChatForm(request.POST)
		if chat_form.is_valid():
			msgsent = chat_form.save(commit=False)
			msgsent.sender = request.user.username
			msgsent.receiver = Chat.objects.get(id=pk, showmsg=1).sender
			msgsent.date_posted = datetime.now()
			msgsent.post_id = pk
			msgsent.save()
			event = Profile.objects.get(user=getiduser(msgsent.receiver))
			event.msgscount += 1
			event.save()
			#backlog(request.META['REMOTE_ADDR'], "chats", ("{ Sender:"+str(msgsent.sender)+" Receiver:"+str(msgsent.receiver)+" Date:"+str(msgsent.date_posted)+" Post:"+str(msgsent.post_id)+" Msg:"+str(msgsent.msg)+" }\n"), str(msgsent.sender))
			return redirect('blog-home')
	else:
		chat_form = ChatForm()
	return render(request, 'blog/msgform.html', {'chat_form': chat_form})
	
class HomeLogout(ListView):
	models = Post
	template_name = 'blog/homelogout.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'data'
	ordering = ['-date_posted']
	paginate_by = 2
	def get_queryset(self):
		# usersid = User.objects.get(username='root').id
		return (Post.objects.filter(showpost=1)).order_by('-date_posted')

def homelogout(request):
	content = {
		'data':(Post.objects.filter(showpost=1)).order_by('-date_posted')
		}
	# .all()
	return render(request,'blog/homelogout.html',content)

def tablink(request):
	data = Post.objects.all()
	content = {
		'msgs':data
		}
	return render(request,'blog/tablink.html',content)

	
def about(request):
	return render(request,'blog/about.html',{'title':'About'})

def help(request, id):
	if id == 1:
		return render(request,'blog/help/helpreg.html',{'title':'Help'})
	elif id == 2:
		return render(request,'blog/help/fpass.html',{'title':'Help'})
	elif id == 3:
		return render(request,'blog/help/posthelp.html',{'title':'Help'})
	elif id == 4:
		return render(request,'blog/help/loginview.html',{'title':'Help'})
	elif id == 5:
		return render(request,'blog/help/profilehelp.html',{'title':'Help'})
	elif id == 6:
		return render(request,'blog/help/logoutview.html',{'title':'Help'})
	elif id == 7:
		return render(request,'blog/help/msgin.html',{'title':'Help'})
	
def termcond(request):
	return render(request,'blog/termcond.html',{'title':'Terms and Conditions'})
	
#--------------------------------------- User registration start--------------------------------------	
def register(request):
	if request.method == 'POST':
		strg = ""
		r_form = UserRegisterForm(request.POST)
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
			backlog(request.META['REMOTE_ADDR'], "email", ("{ emailid:"+str(to_email)+" message: "+"username: "+str(user)+"code: "+str(strg)+"}"),request.META['REMOTE_ADDR'])
			email.send()
			return render(request, 'accounts/activate_mail.html')
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
			#backlog(request.META['REMOTE_ADDR'], "email", "username: "+str(user.username)+" activated", request.META['REMOTE_ADDR'])
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
	ordering = ['-date_posted']
	context_object_name = 'posts'
	paginate_by = 2
	def get_queryset(self):
		# usersid = User.objects.get(username='root').id
		return Post.objects.filter(showpost=1).order_by('-date_posted')
	"""def get_ordering(self):
		ordering = self.request.GET.get('ordering', '-date_created')
		return ordering"""

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
		form.instance.nameu = Profile.objects.get(user=self.request.user).nameu
		backloghome(self.request.META['REMOTE_ADDR'], form.instance, "create", self.request.user.username)
		return super().form_valid(form)
	
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	models = Post
	template_name = 'blog/post_form.html' # <app>/<model>_<viewtype>.html
	fields = ['title', 'content', 'image']
	
	def get_queryset(self):
		return Post.objects.all()
		
	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.date_posted = timezone.now()
		#backloghome(self.request.META['REMOTE_ADDR'], form.instance, "update", self.request.user.username)
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
		form.instance.date_posted = timezone.now()
		backloghome(self.request.META['REMOTE_ADDR'], form.instance, "delete", self.request.user.username)
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
				data = "{Author: " + str(event.author)+" "+str(myacc.tokenacc)+" Donor:"+ str(request.user.username)+" "+str(donoracc.tokenacc)+" Award:"+str(request.POST['tokens'])+"}\n"
				#backloghome(request.META['REMOTE_ADDR'], event, "booked", request.user.username)
				#backlogtoken(request.META['REMOTE_ADDR'], "homepage/tokenprof",str(pk), data)
				
			elif event.tokenbyuser == request.user and int(donoracc.tokenacc) > int(request.POST['tokens']):
				myacc.tokenacc = str(int(myacc.tokenacc) + int(request.POST['tokens']))
				myacc.save()
				donoracc.tokenacc = str(int(donoracc.tokenacc) - int(request.POST['tokens']) + int(event.tokens))
				donoracc.save()
				event.tokens = request.POST['tokens']
				event.tokenbyuser = request.user.username
				event.save()
				data = "{Author: " + str(event.author)+" "+str(myacc.tokenacc)+" Donor:"+ str(request.user.username)+" "+str(donoracc.tokenacc)+" Award:"+str(request.POST['tokens'])+"}\n"
				#backloghome(request.META['REMOTE_ADDR'], event, "booked", request.user.username)
				#backlogtoken(request.META['REMOTE_ADDR'], "homepage/tokenprof",str(pk), data)

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
				data = "{Author: " + str(event.author)+" "+str(myacc.tokenacc)+" Donor:"+" "+str(request.user.username)+" "+str(donoracc.tokenacc)+" Predonor:"+str(event.tokenbyuser)+" "+str(predonoracc.tokenacc)+" Award:"+str(request.POST['tokens'])+"}\n"
				#backloghome(request.META['REMOTE_ADDR'], event, "booked", request.user.username)
				#backlogtoken(request.META['REMOTE_ADDR'], "homepage/tokenprof", str(pk), data)
			else:
				messages.error(request, 'You cannot book. Your balance token is '+donoracc.tokenacc+' which is less than'+request.POST['tokens'])
			
			
			# messages.success(request, 'Account is updated!')
			
			return redirect('blog-home')
		else:
			# messages.error(request, 'Already Booked with %s token. Give more token to book.'%event.tokens)
			return redirect(request.get_full_path())
	else:
		t_form = PostTokenForm()
		if int(event.tokens) > 0:messages.error(request, 'Already Booked with '+event.tokens+' token. Give more token to book.')
		context = {
			'form' : t_form
		}
		return render(request, 'blog/posttoken.html', context)	

@login_required
def tokendetails(request):
	tokengot = 0
	tokengotq = Post.objects.filter(author=request.user, showpost=1).exclude(tokenbyuser="null").order_by('-date_posted')
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
		data = "{Author: " + str(event.author)+" "+str(myacc.tokenacc)+" Donor:"+ str(event.tokenbyuser)+" "+str(donoracc.tokenacc)+"}\n"
		#backloghome(request.META['REMOTE_ADDR'], event, "retbook", request.user.username)
		#backlogtoken(request.META['REMOTE_ADDR'], "homepage/tokenprof", str(pk), data)
		return redirect(urldir)
	else:
		if event.bookeditem == 0:
			messages.success(request, 'You haven not marked it Shared.')
		else:
			messages.success(request, 'Book is not shared yet.')
		return redirect(urldir)
		
@login_required
def booked(request, pk):
	event = Post.objects.get(id=pk)
	urldir = "/post/%d/"%pk
	if event.bookeditem == 0 and event.tokenbyuser!="null" :
		event.bookeditem = 1
		event.save()
		#backloghome(request.META['REMOTE_ADDR'], event, "booked",event.author)
		return redirect(urldir)
	else:
		if event.tokenbyuser!="null": messages.success(request, 'Already shared')
		else: messages.success(request, 'No Buyers')
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
			updaterdata = {
				'nameu':request.POST['nameu'],
				'email':request.POST['email'],
				'college':request.POST['college'],
				'mobileno':request.POST['mobileno'],
			}
			Postupdater(request.user, updaterdata)
			data = "{ usename:"+request.user.username+" Name:"+request.POST['nameu'] +" Mob:"+ request.POST['mobileno']+" Email:"+request.POST['email']+" College:"+request.POST['college']+" Image:"+" }\n"
			#backlog(request.META['REMOTE_ADDR'],"profile", data, request.user.username)
			messages.success(request, f'Account is updated!')
			return redirect('profile')
		else:
			messages.error(request, 'Account is NOT updated! Check Mobile number. Enter it in the format as shown in brackets')
			return redirect('profile')
	else:
		# messages.error(request, request.META['REMOTE_ADDR'])
		u_form = UserUpdateForm()
		p_form = ProfileUpdateForm()
		context = {
			'u_form' : u_form,
			'p_form' : p_form,
			't_form' : e.tokenacc,
		}
		return render(request, 'accounts/profile.html', context)

		
@login_required	
def tokuserprof(request, pk):
		tokuser = Post.objects.get(id=pk).tokenbyuser
		data = Profile.objects.get(user=getiduser(tokuser))
		emailid = User.objects.get(username=tokuser).email # it is in user module not in profile
		return render(request, 'accounts/tokuserprof.html', {'tokuser':tokuser,'email':emailid, 'data':data})
#--------------------------------------- Admin Control Starts --------------------------------------	
@login_required	
def adlogdet(request):
	if request.user.username == "root" :
		event = Post.objects.all().order_by('-date_posted')
		return render(request, 'adlogdet.html', {'event':event})
	else:
		return redirect('blog-home')

@login_required	
def chlog(request):
	if request.user.username == "root" :
		event = User.objects.all()
		return render(request, 'chlog.html', {'event':event})
	else:
		return redirect('blog-home')

@login_required	
def chlogdet(request, pk):
	if request.user.username == "root" :
		e = User.objects.get(id=pk).username
		event = Chat.objects.filter(sender=e).order_by('-date_posted')
		return render(request, 'chlogdet.html', {'e':e, 'event':event})
	else:
		return redirect('blog-home')
		
class PostPurgeView(LoginRequiredMixin, DeleteView):
	models = Post
	success_url = '/adlogdet/'
	def get_queryset(self):
		return Post.objects.all()
#--------------------------------------- Admin Control ends --------------------------------------	
#--------------------------------------- Search Starts --------------------------------------	

@login_required
def searchlogin(request):
	srh = (request.POST['srh']) # .casefold()
	srhl = srh.split()
	id_set = []
	for i in srhl:
		postdatat = Post.objects.filter(showpost=1, title__contains=i)
		postdatatc = Post.objects.filter(showpost=1, content__contains=i)
		postdatatd = Post.objects.filter(showpost=1, date_posted__contains=i)
		postdatatna = Post.objects.filter(showpost=1, nameu__contains=i)
		postdatate = Post.objects.filter(showpost=1, email__contains=i)
		postdatatm = Post.objects.filter(showpost=1, mobileno__contains=i)
		id_set.extend(postid(postdatat))
		id_set.extend(postid(postdatatc))
		id_set.extend(postid(postdatatd))
		id_set.extend(postid(postdatatna))
		id_set.extend(postid(postdatate))
		id_set.extend(postid(postdatatm))
	srhgot = set(id_set)
	id_set2 = list(srhgot)
	#backlog(request.META['REMOTE_ADDR'], "searchlogin", (" {Srh:"+str(srh)+" }\n"), str(request.user.username))
	if len(id_set2) !=0:
		postdata = Post.objects.filter(id__in=id_set2).order_by('-date_posted')
		content = {
			'data':postdata
		}
		return render(request,'blog/search/search.html', content)

	else:
		messages.error(request, 'Search Not Found.')
		return redirect('blog-home')

def searchlogout(request):
	srh = request.POST['srh']
	srhl = srh.split()
	id_set = []
	for i in srhl:
		postdatat = Post.objects.filter(showpost=1, title__contains=i)
		postdatatc = Post.objects.filter(showpost=1, content__contains=i)
		postdatatd = Post.objects.filter(showpost=1, date_posted__contains=i)
		postdatatna = Post.objects.filter(showpost=1, nameu__contains=i)
		postdatate = Post.objects.filter(showpost=1, email__contains=i)
		postdatatm = Post.objects.filter(showpost=1, mobileno__contains=i)
		id_set.extend(postid(postdatat))
		id_set.extend(postid(postdatatc))
		id_set.extend(postid(postdatatd))
		id_set.extend(postid(postdatatna))
		id_set.extend(postid(postdatate))
		id_set.extend(postid(postdatatm))
	srhgot = set(id_set)
	id_set2 = list(srhgot)
	#backlog(request.META['REMOTE_ADDR'], "searchlogout", (" {Srh:"+str(srh)+" }\n"), str(request.META['REMOTE_ADDR']))
	if len(id_set2) !=0:
		postdata = Post.objects.filter(id__in=id_set2).order_by('-date_posted')
		content = {
			'data':postdata
		}
		return render(request,'blog/search/searchlogout.html', content)

	else:
		messages.error(request, 'Search Not Found.')
		return redirect('blog-homelogout')

#--------------------------------------- Search Ends --------------------------------------	
def feedback(request):
	if request.method == 'POST':
		fdb_form = FeedbackForm(request.POST)
		if fdb_form.is_valid():
			fd = fdb_form.save(commit=False)
			fd.ip = request.META['REMOTE_ADDR']
			if request.user.username:
				fd.user = request.user.username
			else:
				fd.user = request.META['REMOTE_ADDR']
			fd.date_posted = timezone.now()
			fd.save()
			#backlog(request.META['REMOTE_ADDR'], "feedback", ("{ Sender:"+fd.user+" Date:"+str(fd.date_posted)+" Msg:"+str(fd.msg)+" }\n"), str(fd.user))
			return redirect('fdb')
	else:
		fdb_form = FeedbackForm()
	feedbackmsg = FeedbackDB.objects.all().order_by('-date_posted')
	return render(request, "blog/fdb.html", {"feedback": fdb_form, "msgs":feedbackmsg})


#--------------------------------------- Additional functions --------------------------------------	
def getiduser(userhere):
	return User.objects.get(username=userhere).id
	
