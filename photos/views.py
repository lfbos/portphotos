import os

import dropbox
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from photos.forms import RegistrationForm
from photos.serializers import PhotoSerializer


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'photos/index.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_dropbox_account_linked:
            return redirect('welcome')

        return super(HomeView, self).dispatch(request, *args, **kwargs)


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'photos/welcome.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_dropbox_account_linked:
            return redirect('home')

        return super(WelcomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WelcomeView, self).get_context_data(**kwargs)

        ctx.update({'dropbox_uri': reverse('dropbox_auth_start')})

        return ctx


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')

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
    redirect_uri = "{}/oauth2/".format(settings.DROPBOX_REDIRECT_API)
    return dropbox.DropboxOAuth2Flow(
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
        result = get_dropbox_auth_flow(request.session).finish(request.GET)
        user.access_token = result.access_token
        user.account_id = result.account_id
        user.user_id = result.user_id
        user.save()
    except Exception as e:
        print(str(e))
    else:
        return redirect('home')


@api_view(['GET'])
@login_required
def get_folder_list(request):
    dbx = dropbox.Dropbox(request.user.access_token)
    entries = dbx.files_list_folder('', recursive=True).entries

    file_names = map(lambda e: e.path_display, entries)

    thumbnails_data = list(map(
        lambda fn: dropbox.dropbox.files.ThumbnailArg(fn, size=dropbox.dropbox.files.ThumbnailSize.w256h256),
        file_names
    ))

    thumbnails = dbx.files_get_thumbnail_batch(thumbnails_data)

    data = []

    for entry_file in thumbnails.entries:
        entry_file = entry_file.get_success()
        thumbnail_data = PhotoSerializer(instance=entry_file.metadata).data
        extension = os.path.splitext(thumbnail_data.get('name'))[-1][1:]
        thumbnail = entry_file.thumbnail
        base64 = 'data:image/{extension};base64,{thumbnail}'.format(
            extension=extension,
            thumbnail=thumbnail
        )
        thumbnail_data.update({'thumbnail': base64})
        data.append(thumbnail_data)

    return Response({
        'data': data
    })


@api_view(['GET'])
@login_required
def get_thumbnail(request):
    dbx = dropbox.Dropbox(request.user.access_token)

    path = request.query_params.get('path')

    thumb_arg = dropbox.dropbox.files.ThumbnailArg(path, size=dropbox.dropbox.files.ThumbnailSize.w960h640)

    response = dbx.files_get_thumbnail_batch([thumb_arg])

    entry = response.entries[0].get_success()
    extension = os.path.splitext(entry.metadata.name)[-1][1:]
    thumbnail = entry.thumbnail

    base64 = 'data:image/{extension};base64,{thumbnail}'.format(
        extension=extension,
        thumbnail=thumbnail
    )

    return Response({
        'thumbnail': base64
    })


@api_view(['POST'])
@login_required
def remove_file(request):
    dbx = dropbox.Dropbox(request.user.access_token)

    path = request.POST.get('path')

    dbx.files_delete_v2(path)

    return Response({
        'message': 'File deleted successfully'
    })


@api_view(['POST'])
@login_required
def upload_new_files(request):
    dbx = dropbox.Dropbox(request.user.access_token)

    new_files = request.FILES.dict().values()

    for file in new_files:
        dbx.files_upload(file.file.read(), '/{}'.format(file.name), mode=dropbox.dropbox.files.WriteMode.overwrite)

    return Response({
        'message': 'Photos uploaded successfully'
    })
