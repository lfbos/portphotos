from django.contrib.auth import views as auth_views
from django.urls import path

from photos import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('register/', views.registration_view, name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dropbox_auth_start/', views.dropbox_auth_start, name='dropbox_auth_start'),
    path('oauth2/', views.dropbox_auth_finish, name='dropbox_auth_finish'),

    # API
    path('api/files/', views.get_folder_list, name='api-file-list'),
    path('api/remove/file/', views.remove_file, name='api-remove-file')
]
