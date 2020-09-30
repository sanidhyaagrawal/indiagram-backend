from django.db import models
from django.contrib.auth.models import User, auth
from datetime import datetime
# Create your models here.

class session_tokens(models.Model):
    user = models.ForeignKey("user_details", on_delete=models.CASCADE)
    token =  models.CharField(max_length=3000)
    time_created = models.DateTimeField(editable=True)

class login_attempts(models.Model):
    user_details = models.ForeignKey("user_details", on_delete=models.CASCADE)
    time_created = models.DateTimeField(editable=True)

class otps(models.Model):
    token = models.CharField(max_length=300)
    otp = models.CharField(max_length=300)
    time_created = models.DateTimeField(editable=True)

class tokenised_contact_info(models.Model):
    key = models.CharField(max_length=300, blank=True, null=True)
    country_code = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    
class user_details(models.Model):
    key = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    email = models.EmailField(max_length=100,unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    #privacy settings
    showLastsSeen= models.BooleanField(default=True)


    website = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)

    country_code = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    complete_number = models.CharField(max_length=20, blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures', blank=True, null=True)
    posts = models.ManyToManyField(
        'posts', related_name='user_details_posts', blank=True, null=True)
    stories = models.ManyToManyField(
        'stories', related_name='user_details_stories', blank=True, null=True)
    likes = models.ManyToManyField('likes', blank=True, null=True)
    followers = models.ManyToManyField(
        User, related_name='user_details_followers', blank=True, null=True)
    following = models.ManyToManyField('following', blank=True, null=True)
    bookmarked_posts = models.ManyToManyField(
        'posts', related_name='user_details_bookmarked_posts', blank=True, null=True)
    follow_requests = models.ManyToManyField(
        User, related_name='user_details_follow_requests', blank=True, null=True)
    private_account = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    tagged_posts = models.ManyToManyField(
        'posts', related_name='user_details_tagged_posts', blank=True, null=True)
    blocked_users = models.ManyToManyField(
        User, related_name='user_details_blocked_users', blank=True, null=True)
    # People user don't follow but has activity with
    related_people = models.ManyToManyField(
        "related_people", blank=True, null=True)
    story_highlights = models.ManyToManyField(
        'stories', related_name='user_details_story_highlights', blank=True, null=True)
    user_activity = models.ManyToManyField(
        'user_activity', blank=True, null=True)

    def __str__(self):
        return str(self.name)


class user_activity(models.Model):
    category = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    activity_user = models.ManyToManyField(User)


class related_people(models.Model):

    # Not the user whoes profile it is but the people he talks to
    related_user = models.ForeignKey(User, on_delete=models.CASCADE)

    score = models.IntegerField()


class story_highlights(models.Model):

    group_name = models.CharField(max_length=100)
    stories = models.ManyToManyField('stories')


class following(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    hide_story = models.BooleanField(default=False)
    hide_post = models.BooleanField(default=False)


class posts(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField("posts")
    caption = models.CharField(max_length=200)
    likes = models.ManyToManyField('likes')
    comments = models.ManyToManyField('comments')
    date_created = models.DateTimeField(default=datetime.now)
    last_updated = models.DateTimeField(auto_now_add=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    views = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)


class images(models.Model):

    image = models.ImageField(upload_to="posts")


class likes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class comments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    likes = models.ManyToManyField('likes')
    replies = models.ManyToManyField('replies')
    crated = models.DateTimeField(auto_now_add=True)


class replies(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    likes = models.ManyToManyField('likes')
    crated = models.DateTimeField(auto_now_add=True)


class stories(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(max_length=100)
    views = models.ManyToManyField(User, related_name='stories_views')
    crated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # for filters and on image texts, more frilsd will be added here in future


class hashtags(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=100)
    stories = models.ManyToManyField("stories")
    posts = models.ManyToManyField("posts")
    crated = models.DateTimeField(auto_now_add=True)
