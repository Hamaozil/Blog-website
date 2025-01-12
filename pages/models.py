#this is for creating db
from django.db import models
from datetime import datetime
from django.utils.text import slugify
# Create your models here.

class LogInUsers(models.Model): # model for login users
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    class Meta:
        verbose_name= 'LogInUser' # name of table

    def __str__(self):
        return self.email #name of objects in admin panel
    

class UserBlogs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(LogInUsers, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True)
    slug = models.SlugField(max_length=60 , blank=True , null = True , unique=True)  # Slug field
     
     
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs )
        
    def __str__(self):  
        return f'{self.title} - {self.user}'
    
    class Meta:
        verbose_name = 'UserBlog'
        
        
class Like (models.Model):
    user = models.ForeignKey(LogInUsers, on_delete=models.CASCADE)
    blog = models.ForeignKey(UserBlogs, on_delete=models.CASCADE) # the reverse relationship is (like_set)
    creared_at = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.email} liked {self.blog.title}'
    
    class Meta:
        verbose_name = 'Like'
        unique_together = ('user', 'blog')