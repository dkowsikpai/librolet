from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import HomeLogout, HomePostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, PostPurgeView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeLogout.as_view(), name="blog-homelogout"),
    path('home/', HomePostListView.as_view(), name="blog-home"),
    path('search/', views.searchlogin, name="search-login"),
    path('searchlogout/', views.searchlogout, name="search-logout"),
    path('tablink/', views.tablink, name="blog-tablink"),
    path('<int:op>/msgs/', views.msgs, name="blog-msgs"),
    path('msgs/<int:pk>/create', views.chatcreate, name="blog-msgs-create"),
    path('msgs/<int:pk>/delete', views.chatdel, name="chat-msg-del"),
    path('msgs/<int:pk>/reply', views.chatreply, name="chat-msg-reply"),
    path('addtoken/', views.addtoken, name="blog-addtoken"),
    path('deltoken/', views.deltoken, name="blog-deltoken"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('accounts/tokendetails', views.tokendetails, name="post-token-details"),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
	path('post/<int:pk>/purge/', PostPurgeView.as_view(), name="post-purge"),
	path('post/<int:pk>/token/', views.tokenaward, name="post-token"),
	path('post/<int:pk>/retbook/', views.retbook, name="post-retbook"),
	path('post/<int:pk>/booked/', views.booked, name="post-booked"),
	path('about/', views.about, name="blog-about"),
    path('<int:id>/help/', views.help, name="help"),
	path('accounts/profile/', views.profile, name="profile"),
	path('accounts/<int:pk>/tokuserprofile/', views.tokuserprof, name="tok-user-profile"),
	path('register/', views.register, name="blog-register"),
	path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name="password_reset"),
	path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name="password_reset_confirm"),
	path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name="password_reset_done"),
	path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name="password_reset_complete"),
	path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name="blog-login"),
	path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name="blog-logout"),
	path('activate/', views.activate, name='activate'),
	path('termcond/', views.termcond, name='terms-conditions'),
	path('adlogdet/', views.adlogdet, name='adlogdet'),
	path('chlog/', views.chlog, name='chlog'),
	path('feedback/', views.feedback, name='fdb'),
	path('<int:pk>/chlogdet/', views.chlogdet, name='chlogdet'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# (?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)	