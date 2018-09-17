from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from dropbox import DropboxOAuth2Flow

from photos.forms import RegistrationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'photos/index.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_dropbox_account_linked:
            return redirect('welcome')

        return super(HomeView, self).dispatch(request, *args, **kwargs)


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'photos/welcome.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_dropbox_account_linked:
            return redirect('home')

        return super(WelcomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WelcomeView, self).get_context_data(**kwargs)

        ctx.update({'dropbox_uri': reverse('dropbox_auth_start')})

        return ctx


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        context = {'form': form}

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            messages = []

            if form.errors:
                for _, message in form.errors.items():

                    if type(message) == ErrorList:
                        message = message[0]

                    messages.append(message)

            if form.error_messages:
                for _, message in form.error_messages.items():
                    if type(message) == ErrorList:
                        message = message[0]

                    messages.append(message)

            if messages:
                context.update({'error_messages': messages})

            return render(request, 'registration.html', context)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def get_dropbox_auth_flow(web_app_session):
    redirect_uri = "http://localhost:8000/oauth2/"
    return DropboxOAuth2Flow(
        settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET,
        redirect_uri, web_app_session,
        "dropbox-auth-csrf-token"
    )


# URL handler for /dropbox-auth-start
def dropbox_auth_start(request):
    authorize_url = get_dropbox_auth_flow(request.session).start()
    return redirect(authorize_url)


# URL handler for /dropbox-auth-finish
@login_required
def dropbox_auth_finish(request):
    user = request.user

    if user.is_dropbox_account_linked:
        return redirect('home')

    try:
        access_token, account_id, user_id = get_dropbox_auth_flow(request.session).finish(request.GET)
    except Exception as e:
        print(str(e))
    else:
        user.access_token = access_token
        user.account_id = account_id
        user.user_id = user_id
        user.save()

        return redirect('home')
