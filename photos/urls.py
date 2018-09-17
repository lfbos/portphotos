from django.contrib.auth import views as auth_views
from django.urls import path

from photos.views import HomeView, registration_view, WelcomeView, dropbox_auth_start, dropbox_auth_finish

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('register/', registration_view, name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dropbox_auth_start/', dropbox_auth_start, name='dropbox_auth_start'),
    path('oauth2/', dropbox_auth_finish, name='dropbox_auth_finish'),
]
