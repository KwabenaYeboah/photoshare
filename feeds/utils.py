import datetime
from django.utils  import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Feed 

def create_feed(user, activity, target=None):
    #let's check for any duplicate actions made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    duplicate_acts = Feed.objects.filter(user_id=user.id, activity=activity,
                                         created__gte=last_minute)
    
    if target:
        target_model = ContentType.objects.get_for_model(target)
        duplicate_acts = duplicate_acts.filter(target_model=target_model,
                                               target_id=target.id)
    
    if not duplicate_acts:  
        acts = Feed(user=user, activity=activity, target=target)
        acts.save()
        return True
    
    return False
    