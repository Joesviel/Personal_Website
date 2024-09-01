from django.contrib import admin
from .models import Post, Comment, SubscribedUsers, Bitacora

class SubscribedUsersAdmin(admin.ModelAdmin):
    """
    Short class to display all of the SubscribedUsers model attributes on the
    admin panel.
    """
    list_display = ('email', 'name', 'created_date')

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SubscribedUsers)
admin.site.register(Bitacora)