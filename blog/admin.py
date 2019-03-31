from django.contrib import admin
from .models import Post, Profile, UserRegModel, Chat, FeedbackDB
# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(UserRegModel)
admin.site.register(Chat)
admin.site.register(FeedbackDB)
