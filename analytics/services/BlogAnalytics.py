from analytics.models import BlogCommentCountStats


class BlogAnalyticsService:

    def updateBlogCommentsStats(self, blog, community, add):
        stats, created = BlogCommentCountStats.objects.get_or_create(blog=blog, community=community)
        if add:
            stats.comment_count += 1
        else:
            stats.comment_count -= 1
        stats.save()
