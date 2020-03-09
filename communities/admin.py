from django.contrib import admin

from communities.models import Communities, CommunitySubscribers

admin.site.register(Communities)
admin.site.register(CommunitySubscribers)
