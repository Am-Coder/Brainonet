from django.contrib import admin

from blog.models import Blog, References, Comment, Vote

admin.site.register(Blog)
admin.site.register(References)
admin.site.register(Comment)
admin.site.register(Vote)
