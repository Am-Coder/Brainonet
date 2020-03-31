from django.contrib import admin

from blog.models import Blog, References, Comment, Vote, BlogHistory, ReferenceHistory

admin.site.register(Blog)
admin.site.register(References)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(BlogHistory)
admin.site.register(ReferenceHistory)