from django.contrib import admin

from .models import Feed

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
    