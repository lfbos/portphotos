from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from photos.forms import RegistrationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'photos/index.html'
    login_url = '/login/'


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
