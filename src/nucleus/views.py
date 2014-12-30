from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, Http404 #, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

from nucleus.models import *
from nucleus.helpers import *

import json

@csrf_exempt
def login_view(request):
    try:
        if request.method == 'POST':
            raw_data = request.POST.dict()
            user = authenticate(username = raw_data['username'], password = raw_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse(success_message())
    except KeyError:
        return HttpResponse(json.dumps({
                "message": "Failed to login"
            }))

def logout_view(request):
    logout(request)
    return HttpResponse(success_message())

@csrf_exempt
def users(request, user_id = None):
    try:
        if user_id:
            try:
                user_id = int(user_id)

                # GET a user
                if request.method == "GET":
                    # XXX: Give values list of selected info
                    person = Person.objects.filter(pk = user_id).values(
                            'user__username', 'user__email', 'phone_no', 'user__first_name',
                            'user__last_name', 'image', 'gender', 'age_range')

                    # Accessible to admin or the same user
                    if request.user.is_staff:
                        #return HttpResponse(serializers.serialize("json", person))
                        return HttpResponse(json.dumps(list(person)))
                    else:
                        # XXX: Give some info to logged in user (WhatsApp contact info)
                        #return HttpResponse(serializers.serialize("json", person))
                        return HttpResponse(json.dumps(list(person)))

                # Update User
                if request.method == "PUT":

                    # Workaround
                    coerce_put_post(request)

                    keys = request.PUT.keys()

                    person = get_object_or_404(Person, pk = user_id)
                    if not request.user.is_staff and person.user != request.user:
                        raise Http404

                    user = person.user

                    if 'password' in keys:
                        user.set_password(request.PUT['password'])

                    # Get data
                    user.first_name = request.PUT['first_name']
                    user.last_name = request.PUT['last_name']
                    person.image = request.PUT['image'] if 'image' in keys else ''
                    person.gender = request.PUT['gender'] if 'gender' in keys else ''
                    person.age_range = request.PUT['age_range'] if 'age_range' in keys else ''

                    email = request.PUT['email']
                    phone_no = request.PUT['phone_no']

                    # Checks for uniqueness in email and phone no if changed
                    if User.objects.filter(email = email).filter(~Q(id = user.id)).exists():
                        return HttpResponse(custom_message("User with email exists"))
                    else:
                        user.email = email

                    if Person.objects.filter(phone_no = phone_no).filter(~Q(id = user_id)).exists():
                        return HttpResponse(custom_message("User with email exists"))
                    else:
                        person.phone_no = phone_no

                    user.save()
                    person.save()

                    return HttpResponse(success_message())

                if request.method == "DELETE":
                    if request.user.is_staff or (request.user.pk == user_id):
                        Person.objects.filter(user__id = user_id).delete()
                        return HttpResponse(success_message())

            # If invalid user_id
            except Exception as e:
                print (e)
                return HttpResponse(no_access())

        # user_id not specified
        else:
            if request.method == "POST":

                keys = request.POST.keys()

                # Get data
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']
                password = request.POST['password']
                phone_no = request.POST['phone_no']
                email = request.POST['email']
                image = request.POST['image'] if 'image' in keys else ''
                gender = request.POST['gender'] if 'gender' in keys else ''
                age_range = request.POST['age_range'] if 'age_range' in keys else ''
                # Create User Object
                if User.objects.filter(email = email).exists():
                    return HttpResponse(custom_message("User with email already exists"))

                user = User.objects.create(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name
                )
                user.set_password(password)
                user.save()

                # Create Person Object
                person = Person.objects.create(
                    user = user,
                    phone_no = phone_no,
                    image = image,
                    gender = gender,
                    age_range = age_range
                )

                # Create Verification Code
                # XXX: Skip verification for now
                person.is_verified = True
                person.save()

                return HttpResponse(success_message())

            elif request.method == "GET":
                # Give list of users
                if request.user.is_staff:
                    return HttpResponse(serializers.serialize("json", Person.objects.all()))
                else:
                    return HttpResponse(no_access(), status = 404)

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())
