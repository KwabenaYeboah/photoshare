from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Feed(models.Model):
    user = models.ForeignKey('auth.User', related_name='actions',
                             on_delete=models.CASCADE, db_index=True)
    activity = models.CharField(max_length=150)
    target_model = models.ForeignKey(ContentType, blank=True, null=True,
                                     related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_model','target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ('-created',)