from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    following = models.ManyToManyField(User,related_name='following',blank = True)
    bio = models.TextField(default='no bio submitted..')
    joinyear = models.TextField(default='2021')
    Faculty = models.TextField(default='Game Design and Development')
    photo = models.ImageField(upload_to= 'Profile_pic',null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def profiles_posts(self):
        return self.post_set.all()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ('-created',)



class Post(models.Model):
    title = models.CharField(max_length = 50)
    overview = models.TextField()
    time_upload = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to= 'thumbnail', blank=True,null=True)
    view = models.IntegerField(default = 1)

    class Meta:
        ordering =['-time_upload']

    def __str__(self):
        return '%s'%(self.title)