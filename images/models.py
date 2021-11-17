from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE, 
                               related_name='images_uploaded')
    title  = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        super().save(*args, **kwargs)
        
    #define canonical urls for objects
    def get_absolute_url(self):
        return reverse('image_detail', args=[self.id, self.slug])
    