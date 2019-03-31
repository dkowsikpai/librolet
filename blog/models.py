from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	nameu = models.CharField(max_length=100, default="No Name")
	college = models.CharField(max_length=100, default="GEC Thrissur")
	mobileno = models.CharField(max_length=17, default="+91 XXXXXXXXXX")
	tokenacc = models.CharField(max_length=100, default=1000)
	msgscount = models.IntegerField(default=0)
	def save(self):
		super().save()
		img = Image.open(self.image.path)
		if (img.height > 300) or (img.width > 300):
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
	
	def __str__(self):
		return f'{self.user.username} Profile'

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='post_pics')
	showpost = models.IntegerField(default=1)
	bookeditem = models.IntegerField(default=0)
	college = models.CharField(max_length=100, default="GEC Thrissur")
	nameu = models.CharField(max_length=100, default="No Name")
	mobileno = models.CharField(max_length=17, default="No Mob")
	email = models.EmailField(max_length=300, default="No Email")
	tokens = models.CharField(max_length=100, default=0)
	tokenbyuser = models.CharField(max_length=100, default="null")
	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})

class UserRegModel(models.Model):
	user = models.CharField(max_length=100)
	codesent = models.CharField(max_length=10, default="null")
	coderesv = models.CharField(max_length=10, default="null")
	def __str__(self):
		return self.user
		
class Chat(models.Model):
	sender=models.CharField(max_length=50)
	receiver=models.CharField(max_length=50)
	msg=models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	post_id = models.IntegerField(default=0)
	showmsg = models.IntegerField(default=1)
	def __str__(self):
		return self.sender+" to "+self.receiver+" for "+str(self.post_id)

class FeedbackDB(models.Model):
	ip = models.CharField(max_length=10)
	date_posted = models.DateTimeField(default=timezone.now)
	user = models.CharField(max_length=100, default="null")
	msg = models.TextField()
	admincomment = models.TextField(default="null")
	def __str__(self):
		return self.msg
