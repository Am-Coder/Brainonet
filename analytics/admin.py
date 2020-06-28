from django.contrib import admin
from analytics.models import ContentVisitStats, BlogCommentCountStats, CommunitySubscriberStats, UserVisitStats
# Register your models here.
admin.site.register(BlogCommentCountStats)
admin.site.register(ContentVisitStats)
admin.site.register(UserVisitStats)
admin.site.register(CommunitySubscriberStats)
