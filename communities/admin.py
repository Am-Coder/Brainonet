from django.contrib import admin

from communities.models import Communities, CommunitySubscribers, CommunityHistory

admin.site.register(Communities)
admin.site.register(CommunitySubscribers)
admin.site.register(CommunityHistory)