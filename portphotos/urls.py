from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from photos.views import HomeView, registration_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('register/', registration_view, name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout')
]
