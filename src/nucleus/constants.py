MAX_CHAR_LENGTH = 100
MAX_RESOURCE_LENGTH = 250
MAX_POST_LENGTH = 1000
MAX_CHOICE_LENGTH = 10

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)

POST_TYPE_CHOICES = (
    ('Text', 'Text'),
    ('Image', 'Image'),
    ('Video', 'Video')
)

POST_STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)

POST_ACCESS_CHOICES = (
    ('Group', 'Group'),
    ('Public', 'Public'),
    ('Friends', 'Friends')
)

LIKE_TYPE_CHOICES = (
    ('Post', 'Post'),
    ('Comment', 'Comment')
)
