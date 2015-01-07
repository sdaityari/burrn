from django.db import models
from django.contrib.auth.models import User

import nucleus.constants as C

class Person(models.Model):
    user = models.OneToOneField(User, related_name = 'person_Person')
    facebook_id = models.CharField(max_length = C.MAX_CHAR_LENGTH, blank = True, null = True)
    phone_no = models.CharField(max_length = C.MAX_CHAR_LENGTH, unique = True)
    image = models.CharField(max_length = C.MAX_RESOURCE_LENGTH, blank = True, null = True)
    gender = models.CharField(max_length = C.MAX_CHOICE_LENGTH, choices = C.GENDER_CHOICES, blank = True, null = True)
    age_range = models.CharField(max_length = C.MAX_CHAR_LENGTH, blank = True, null = True)

    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    verification_code = models.CharField(max_length = C.MAX_CHAR_LENGTH, blank = True, null = True)
    is_verified = models.BooleanField(default = False)

    fb_string = models.CharField(max_length = C.MAX_CHAR_LENGTH, blank = True, null = True)

class Group(models.Model):
    name = models.CharField(max_length = C.MAX_CHAR_LENGTH)
    members = models.ManyToManyField(Person, related_name='group_members', blank=True, null=True)
    member_count = models.IntegerField(default=0)
    image = models.CharField(max_length = C.MAX_RESOURCE_LENGTH, blank = True, null = True)
    admin = models.ForeignKey(Person, related_name = 'group_admin')

    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

class Post(models.Model):
    author = models.ForeignKey(Person, related_name = 'post_author')
    target = models.ForeignKey(Person, related_name = 'target_persons')
    post_type = models.CharField(max_length = C.MAX_CHOICE_LENGTH, choices = C.POST_TYPE_CHOICES)
    text = models.CharField(max_length = C.MAX_POST_LENGTH)
    external_resource = models.CharField(max_length = C.MAX_RESOURCE_LENGTH)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    status = models.CharField(max_length = C.MAX_CHOICE_LENGTH, choices = C.POST_STATUS_CHOICES)
    access = models.CharField(max_length = C.MAX_CHOICE_LENGTH, choices = C.POST_ACCESS_CHOICES)
    group = models.ForeignKey(Group, related_name = 'post_group')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey(Person, related_name = 'comment_author')
    text = models.CharField(max_length = C.MAX_POST_LENGTH)
    user_icon = models.CharField(max_length = C.MAX_CHAR_LENGTH)
    likes_count = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Like(models.Model):
    person = models.ForeignKey(Person, related_name = 'like_author')
    post = models.ForeignKey(Post, related_name = 'like_post')
    comment = models.ForeignKey(Comment, related_name = 'like_comment')
    like_type = models.CharField(max_length = C.MAX_CHOICE_LENGTH, choices = C.LIKE_TYPE_CHOICES)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    person = models.ForeignKey(Person, related_name = 'notif_to')
    action_user = models.ForeignKey(Person, related_name = 'notif_from')
    text = models.CharField(max_length = C.MAX_POST_LENGTH)
    link = models.CharField(max_length = C.MAX_RESOURCE_LENGTH, blank = True, null = True)
    is_read = models.BooleanField(default = False)
