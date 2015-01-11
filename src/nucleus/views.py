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
            user = authenticate(username = get_dummy_username(raw_data['username']), password = raw_data['password'])
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

                    # email = request.PUT['email']
                    phone_no = request.PUT['phone_no']

                    # Checks for uniqueness in email and phone no if changed
                    if User.objects.filter(email = get_dummy_email(phone_no)).filter(~Q(id = user.id)).exists():
                        return HttpResponse(custom_message("User with phone_no exists"))
                    else:
                        user.email = get_dummy_email(phone_no)
                        user.username = get_dummy_username(phone_no)

                    if Person.objects.filter(phone_no = phone_no).filter(~Q(id = user_id)).exists():
                        return HttpResponse(custom_message("User with phone_no exists"))
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
                #username = request.POST['username']
                password = request.POST['password']
                phone_no = request.POST['phone_no']
                #email = request.POST['email']
                image = request.POST['image'] if 'image' in keys else ''
                gender = request.POST['gender'] if 'gender' in keys else ''
                age_range = request.POST['age_range'] if 'age_range' in keys else ''
                # Create User Object
                if User.objects.filter(email = get_dummy_email(phone_no)).exists():
                    return HttpResponse(custom_message("User with phone_no already exists"))

                user = User.objects.create(
                    username = get_dummy_username(phone_no),
                    email = get_dummy_email(phone_no),
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

                return HttpResponse(success_message(person.pk))

            elif request.method == "GET":
                # Give list of users
                if request.user.is_staff:
                    return HttpResponse(json.dumps(
                        list(Person.objects.all().values('id', 'user__username',
                            'user__email', 'phone_no', 'user__first_name',
                            'user__last_name', 'image', 'gender', 'age_range')
                        )
                    ))
                else:
                    return HttpResponse(no_access(), status = 404)

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def users_contact(request, contact):
    try:
        return HttpResponse(json.dumps(list(Person.objects.filter(phone_no = contact).values('user__username',
                'user__email', 'phone_no', 'user__first_name', 'id', 'user__last_name', 'image', 'gender', 'age_range')
        )))
    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

@csrf_exempt
def groups(request, group_id = None):
    try:
        if group_id:
            try:
                group_id = int(group_id)
                group = Group.objects.filter(pk = group_id)

                # GET a Group
                if request.method == "GET":
                    if not request.user.is_staff and (Person.objects.get(user = request.user) not in group[0].members.all()):
                        return HttpResponse(no_access())
                    return HttpResponse(json.dumps(list(group.values('id', 'name', 'image', 'member_count', 'admin__id'))))

                # Update Group
                if request.method == "PUT":

                    # Workaround
                    coerce_put_post(request)

                    keys = request.PUT.keys()

                    name = request.PUT['name']
                    image = request.PUT['image'] if 'image' in keys else ''

                    if request.user == group.admin.user:
                        group.name = name
                        group.image = image
                        group.save()
                    else:
                        return HttpResponse(no_access())

                    return HttpResponse(success_message())

                if request.method == "DELETE":
                    group = Group.objects.filter(pk = group_id)
                    if request.user.is_staff or (request.user == group.admin.user):
                         group.delete()
                         return HttpResponse(success_message())

            # If invalid user_id
            except Exception as e:
                print (e)
                return HttpResponse(no_access())

        # user_id not specified
        else:
            if request.method == "POST":

                keys = request.POST.keys()

                name = request.POST['name']
                image = request.POST['image'] if 'image' in keys else ''

                admin = Person.objects.get(user = request.user)

                group = Group.objects.create(
                    name = name,
                    image = image,
                    admin = admin,
                    member_count = 1
                )

                group.members.add(admin)
                group.save()

                # Get data
                return HttpResponse(success_message(id = group.pk))

            elif request.method == "GET":
                # Give list of users
                if request.user.is_staff:
                    groups = Group.objects.all().values('id', 'name', 'member_count', 'image', 'admin__id')
                else:
                    person = Person.objects.get(user = request.user)
                    groups = Group.objects.filter(members = person).values('id', 'name', 'member_count', 'image', 'admin__id')
                return HttpResponse(json.dumps(list(groups)))

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def group_members(request, group_id):
    try:
        group = Group.objects.get(pk = int(group_id))
        members = group.members.all()
        if request.user.is_staff or Person.objects.get(user = request.user) in members:
            return HttpResponse(json.dumps(list(
                    members.values('id', 'user__username', 'user__email', 'phone_no', 'user__first_name',
                        'user__last_name', 'image', 'gender', 'age_range')
                )))
    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def group_add(request, group_id, member_id):
    try:
        group = Group.objects.get(pk = int(group_id))
        members = group.members.all()
        member_to_add = get_object_or_404(Person, pk = int(member_id))
        if (request.user.is_staff or Person.objects.get(user = request.user) in members) and member_to_add not in members:
            group.members.add(member_to_add)
            group.member_count += 1
            group.save()
            return HttpResponse(success_message())

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def group_remove(request, group_id, member_id):
    try:
        group = Group.objects.get(pk = int(group_id))
        members = group.members.all()
        member_to_remove = get_object_or_404(Person, pk = int(member_id))
        if (request.user.is_staff or member_to_remove.user == request.user or request.user == group.admin.user) and member_to_remove in members:
            group.members.remove(member_to_remove)
            group.member_count -= 1
            group.save()
            return HttpResponse(success_message())

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

@csrf_exempt
def posts(request, post_id = None):
    try:
        if post_id:
            try:
                post_id = int(post_id)
                post = Post.objects.filter(pk = post_id)

                # GET a post
                if request.method == "GET":
                    if not user_access(post[0], request.user):
                        return HttpResponse(no_access())
                    return HttpResponse(json.dumps(list(post.values('id', 'author__id', 'target__id', 'post_type', 'text',
                                    'external_resource', 'likes_count', 'comments_count', 'report_count', 'status', 'access'
                        ))))

                # Update post
                if request.method == "PUT":

                    # Workaround
                    coerce_put_post(request)

                    keys = request.PUT.keys()

                    author = Person.objects.get(user = request.user)

                    post = Post.objects.get(pk = post_id)

                    if post.author != author:
                        return HttpResponse(no_access(), status = 400)

                    post.target = Person.objects.get(pk = int(request.PUT['target']))
                    post.post_type = request.PUT['type']
                    post.text = request.PUT['text']
                    post.external_resource = request.PUT['external_resource'] if 'external_resource' in keys else ''
                    post.group = Group.objects.get(pk = int(request.PUT['group']))
                    post.access = request.PUT['access'] if 'access' in keys else 'Group'
                    post.status = request.PUT['status'] if 'status' in keys else 'Active'

                    post.save()

                    return HttpResponse(success_message())

                if request.method == "DELETE":
                    post = Post.objects.filter(pk = post_id)
                    if request.user.is_staff or (request.user == post[0].author.user):
                         post.delete()
                         return HttpResponse(success_message())

            # If invalid user_id
            except Exception as e:
                print (e)
                return HttpResponse(no_access())

        # user_id not specified
        else:
            if request.method == "POST":

                keys = request.POST.keys()

                author = Person.objects.get(user = request.user)
                target = Person.objects.get(pk = int(request.POST['target']))
                post_type = request.POST['type']
                text = request.POST['text']
                external_resource = request.POST['external_resource'] if 'external_resource' in keys else ''
                group = Group.objects.get(pk = request.POST['group'])
                access = request.POST['access'] if 'access' in keys else 'Group'

                status = 'Active'

                post = Post.objects.create(
                    author = author,
                    target = target,
                    post_type = post_type,
                    text = text,
                    external_resource = external_resource,
                    group = group,
                    status = status,
                    access = access
                )

                post.save()

                return HttpResponse(success_message(id = post.pk))

            elif request.method == "GET":
                # Give list of users
                if request.user.is_staff:
                    posts = Post.objects.all().values('id', 'author__id', 'target__id', 'post_type', 'text', 'likes_count',
                                'external_resource', 'comments_count', 'report_count', 'status', 'access')
                else:
                    person = Person.objects.get(user = request.user)
                    posts = Post.objects.filter(author = person).values('id', 'target__id', 'post_type', 'text',
                                'external_resource', 'likes_count', 'comments_count', 'report_count', 'status', 'access')
                return HttpResponse(json.dumps(list(posts)))

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def post_likes(request, post_id):
    '''
        list of likes for a post
    '''
    pass

@csrf_exempt
def post_comments(request, post_id, comment_id = None):
    try:
        post_id = int(post_id)
        post = Post.objects.get(pk = post_id)

        if comment_id:
            try:
                comment_id = int(comment_id)
                comment = Comment.objects.filter(pk = comment_id, post = post)

                # GET a comment
                if request.method == "GET":
                    if user_access(post, request.user):
                        return HttpResponse(json.dumps(list(comment.values('id', 'post__id', 'author__id', 'text',
                                    'user_icon', 'likes_count', 'report_count'
                        ))))
                    else:
                        return HttpResponse(no_access(), status = 403)

                # Update comment
                if request.method == "PUT":

                    # Workaround
                    coerce_put_post(request)

                    keys = request.PUT.keys()

                    comment = comment[0] #as comment is a list after getting it from filter

                    if comment.author.user != request.user:
                        return HttpResponse(no_access(), status = 400)

                    # comment.author and comment.post remain the same

                    comment.text = request.PUT['text']
                    comment.user_icon = request.PUT['user_icon']

                    comment.save()

                    return HttpResponse(success_message())

                if request.method == "DELETE":
                    if request.user.is_staff or (request.user == comment[0].author.user):
                         comment.delete()
                         return HttpResponse(success_message())

            # If invalid user_id
            except Exception as e:
                print (e)
                return HttpResponse(no_access())

        # user_id not specified
        else:
            if request.method == "POST":

                keys = request.POST.keys()

                author = Person.objects.get(user = request.user)
                text = request.POST['text']
                user_icon = request.POST['user_icon']

                comment = Comment.objects.create(
                    post = post,
                    author = author,
                    text = text,
                    user_icon = user_icon
                )

                comment.save()

                return HttpResponse(success_message(id = comment.pk))

            elif request.method == "GET":
                # Give list of users
                if request.user.is_staff or user_access(post, request.user):
                    comments = Comment.objects.filter(post = post).values('id', 'post__id', 'author__id', 'text',
                                    'user_icon', 'likes_count', 'report_count')
                return HttpResponse(json.dumps(list(comments)))

    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def posts_about_me(request):
    try:
        person = Person.objects.get(user = request.user)
        posts = Post.objects.filter(target = person).values('target__id', 'post_type', 'text',
                    'external_resource', 'likes_count', 'comments_count', 'report_count', 'status', 'access')
        return HttpResponse(json.dumps(list(posts)))
    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())

def feed(request):
    try:
        person = Person.objects.get(user = request.user)
        posts = Post.objects.filter(group__members = person).values('id', 'target__id', 'post_type', 'text',
                    'external_resource', 'likes_count', 'comments_count', 'report_count', 'status', 'access')
        return HttpResponse(json.dumps(list(posts)))
    except KeyError:
        return HttpResponse(not_logged_in(), status = 403)
    except Exception as e:
        print (e)
        return HttpResponse(unknown_error())
