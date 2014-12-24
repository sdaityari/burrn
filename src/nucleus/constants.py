MAX_CHAR_LENGTH = 100
MAX_RESOURCE_LENGTH = 250
MAX_POST_LENGTH = 1000


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
)

POST_TYPE_CHOICES = (
    ('TE', 'Text'),
    ('IM', 'Image'),
    ('VI', 'Video')
)

POST_STATUS_CHOICES = (
    ('AC', 'Active'),
    ('IN', 'Inactive')
)

POST_ACCESS_CHOICES = (
    ('I', 'Group'),
    ('II', 'Public'),
    ('III', 'Members'),
    ('IV', 'All Friends')
)

LIKE_TYPE_CHOICES = (
    ('I', 'Post'),
    ('II', 'Comment')
)
