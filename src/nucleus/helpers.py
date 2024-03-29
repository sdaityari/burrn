import json

def no_access():
    return json.dumps({
            "message": "The resource you are requesting doesn't exist"
        })

def unknown_error():
    return json.dumps({
            "message": "Unknown error occurred"
        })

def not_logged_in():
    return json.dumps({
            "message": "Please login"
        })

def success_message(id = None):
    d = {
            "message": "Action completed successfully"
        }
    if id:
        d["id"] = id
    return json.dumps(d)

def custom_message(message = ""):
    return json.dumps({
            "message": message
        })

def coerce_put_post(request):
    """
    Django doesn't particularly understand REST.
    In case we send data over PUT, Django won't
    actually look at the data and load it. We need
    to twist its arm here.

    The try/except abominiation here is due to a bug
    in mod_python. This should fix it.

    Thank you, https://bitbucket.org/jespern/django-piston/src/c4b2d21db51a/piston/utils.py
    """
    if request.method == "PUT":
        # Bug fix: if _load_post_and_files has already been called, for
        # example by middleware accessing request.POST, the below code to
        # pretend the request is a POST instead of a PUT will be too late
        # to make a difference. Also calling _load_post_and_files will result
        # in the following exception:
        #   AttributeError: You cannot set the upload handlers after the upload has been processed.
        # The fix is to check for the presence of the _post field which is set
        # the first time _load_post_and_files is called (both by wsgi.py and
        # modpython.py). If it's set, the request has to be 'reset' to redo
        # the query value parsing in POST mode.
        if hasattr(request, '_post'):
            del request._post
            del request._files

        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'

        request.PUT = request.POST

def user_access(post, user):
    '''
        Check if user has access to post
    '''
    if user.is_staff:
        return True
    elif (user.pk, ) in post.group.members.all().values_list('user__pk') or group.access == 'Public':
        return True
    else:
        return False

def get_dummy_username(phone_no):
    return "username" + str(phone_no)

def get_dummy_email(phone_no):
    return "email" + str(phone_no) + "@burrn.it"
