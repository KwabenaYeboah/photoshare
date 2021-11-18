from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


# Creating a profile class to extend the user model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    dob = models.DateField(blank=True, null=True) # Date of birth(dob) field.
    image = models.ImageField(upload_to='users/%Y', blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'
    
   
# Creating a following system
class Follow(models.Model):
    this_user = models.ForeignKey('auth.User', related_name='rel_from', on_delete=models.CASCADE)  
    that_user = models.ForeignKey('auth.User', related_name='rel_to', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'{self.this_user} follows {self.that_user}'
    
#Adding the below field to the User model
user = get_user_model()
user.add_to_class('following', models.ManyToManyField('self',through=Follow,
                                                    related_name='followers', symmetrical=False))