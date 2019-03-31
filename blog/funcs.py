from .models import Post
def Postupdater(user, data):
	event = Post.objects.filter(author=user)
	for i in event:
		i.nameu = data['nameu']
		i.email = data['email']
		i.college = data['college']
		i.mobileno = data['mobileno']
		i.save()
	return True
	
def postid(post):
	srhgot = []
	for j in post:
			srhgot.append(j.id)
	return(srhgot)
