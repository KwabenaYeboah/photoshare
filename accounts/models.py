from django.db import models
from django.conf import settings

# Creating a profile class to extend the user model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    dob = models.DateField(blank=True, null=True) # Date of birth field.
    image = models.ImageField(upload_to='users/%Y/%m/%d/')
    
    def __str__(self):
        return f'Profile for user {self.user.username}'
    