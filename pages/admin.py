from django.contrib import admin
from .models import LogInUsers , UserBlogs , Like

# Register your models here.

class UserBlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'user', 'slug')
    search_fields = ('title', 'description', 'created_at', 'user', 'slug')
    list_filter = ('title', 'created_at', 'user', 'slug')
    
admin.site.register(LogInUsers)
admin.site.register(UserBlogs,UserBlogsAdmin)
admin.site.register(Like)