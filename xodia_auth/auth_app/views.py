# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User
from .models import Profile
from django.views.generic import View
from django.db.utils import IntegrityError
import urllib2
import urllib
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .__init__ import project_base_dir
import os

# Create your views here.

match_path = project_base_dir + "matches/"
bot_path = project_base_dir + "files/"

class LoginView(View):
    template_name = 'auth_app/index.html'

    def get(self, request):
        if request.user.is_authenticated():
            #user = request.user.username
            #return render(request, 'auth_app/postlogin.html', {'username': user})
            return HttpResponseRedirect(reverse('login_success'))
        else:
            return render(request, self.template_name)

    def post(self, request):
        context = {}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request=request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('login_success'))
        else:
            context["error"] = "Incorrect Credentials!"
            return render(request, self.template_name, context)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))


class SuccessView(View):
    template_name = 'auth_app/postlogin.html'

    def get(self, request):
        if request.user.is_authenticated():
            context = {}
            context['user'] = request.user
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse('user_login'))


class RegisterView(View):
    template_name = 'auth_app/register.html'

    def get(self, request):
        if request.user.is_authenticated():
            #user = request.user.username
            #return render(request, 'auth_app/postlogin.html', {'username': user})
            return HttpResponseRedirect(reverse('login_success'))
        else:
            return render(request, self.template_name)

    def post(self, request):
        try:
            profile = Profile()
            user = User()
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.load(response)
            if not result['success']:
                return render(request, self.template_name, {'error': 'Invalid Captcha!'})
            user.save()
            profile.user = user
            profile.college_name = request.POST['college_name']
            profile.phone_no = request.POST['phone_no']
            profile.create_myuser()
            profile.save()
            login(request, user)

        except IntegrityError:
            context = {'error': 'Username already exists!'}
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('user_login'))


class PlayableUI(View):
    template_name = 'auth_app/playable_ui.html'

    def get(self, request):
        au = request.user.is_authenticated
        return render(request, self.template_name, {'au': au})

class GridView(View):
    template_name = 'auth_app/buttons.html'

    def get(self, request):
        if request.user.is_authenticated:
            all_players = Profile.objects.all()
            return render(request, self.template_name, {'all_players': all_players})
        else:
            return HttpResponseRedirect(reverse('user_login'))

    def post(self, request):

        if request.FILES:
            return HttpResponse(self.uploadBot(request))
        elif 'Match' in request.POST:
            return HttpResponse(self.matchGame(request))
        elif 'Logs' in request.POST:
            return HttpResponse(self.viewLogs(request))
        else:
            return HttpResponse('upload a file jackass')

    def uploadBot(self, request):
        player = Profile.objects.get(user=request.user)

        play = request.FILES['Bot_file']

        ext = play.name.split('.')[-1]

        if ext in ['cpp','c']:
            old_file = player.bot_path + '.' + player.bot_ext

            os.remove(old_file)

            new_file = player.bot_path + '.' + ext
            f = open(new_file, 'w+')

            for chunk in play.chunks():
                f.write(chunk)
            f.close()

            player.bot_ext = ext

            player.save()
            return '<h1>' + str(play.name) + '</h1>'

        else:
            return HttpResponse('error')

    def matchGame(self, request):
        player = Profile.objects.get(user=request.user)
        temp = User.objects.get(username = request.POST['players'])
        opp = Profile.objects.get(user = temp)

        error_file = open(("matches/" + "error" + str(player.pk) + "v" + str(opp.pk)), "w+")
        error_file.close()
        error_rev_file = open(("matches/" + "error" + str(opp.pk) + "v" + str(player.pk)), "w+")
        error_rev_file.close()

        log_file = open(("matches/" + "log" + str(player.pk) + "v" + str(opp.pk)), "w+")
        log_file.close()
        log_rev_file = open(("matches/" + "log" + str(opp.pk) + "v" + str(player.pk)), "w+")
        log_rev_file.close()

        return HttpResponse(str(player.bot_path)+'<br>'+str(opp.bot_path))

    def viewLogs(self, request):
        player = Profile.objects.get(user=request.user)
        temp = User.objects.get(username = request.POST['players'])
        opp = Profile.objects.get(user = temp)

        if 'Player2' not in request.POST:
            try:
                error_file = open(("matches/" + "error" + str(player.pk) + "v" + str(opp.pk)), "r")
                try:
                    log_file = open(("matches/" + "log" + str(player.pk) + "v" + str(opp.pk)), "r")
                    log_file.close()
                except:
                    print("Log File Not Found!")
                    return
                error_file.close()
            except:
                print("Error File Not Found!")
                return
            return HttpResponse("exists1")

        else:
            try:
                error_rev_file = open(("matches/" + "error" + str(opp.pk) + "v" + str(player.pk)), "r")
                try:
                    log_rev_file = open(("matches/" + "log" + str(opp.pk) + "v" + str(player.pk)), "r")
                    log_rev_file.close()
                except:
                    print("Log File Not Found!")
                    return
                error_rev_file.close()
            except:
                print("Error File Not Found!")
                return
            return HttpResponse("exists2")
