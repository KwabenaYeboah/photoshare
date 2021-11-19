from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image

@receiver(m2m_changed, sender=Image.users.through)
def image_likers_changed(sender, instance, **kwargs):
    instance.total_image_likes = instance.users.count()
    instance.save()