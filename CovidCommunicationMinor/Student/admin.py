from django.contrib import admin

from .models import Profile,Post

# Register your models here.
class adminProfile(admin.ModelAdmin):
    list_display =('id','user','bio','created','updated','photo',)

admin.site.register(Profile,adminProfile)


class adminPost(admin.ModelAdmin):
    list_display = ('id', 'title','overview','time_upload','Author','view','thumbnail')


admin.site.register(Post,adminPost)
