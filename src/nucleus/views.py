from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.views.decorators.csrf import csrf_exempt
#from django.shortcuts import render_to_response, get_object_or_404

from nucleus.models import *

import json

@csrf_exempt
def login_view(request):
    try:
        if request.method == 'POST':
            raw_data = request.POST.dict()
            user = authenticate(username = raw_data['username'], password = raw_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse(json.dumps({
                    "message": "Logged in successfully"
                }))
    except KeyError:
        return HttpResponse(json.dumps({
                "message": "Failed to login"
            }))

def logout_view(request):
    logout(request)
    return HttpResponse(json.dumps({
            "message": "Logged out successfully"
        }))
