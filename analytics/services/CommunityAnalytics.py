from analytics.models import CommunitySubscriberStats


class CommunityAnalyticsService:

    def updateSubscriberStats(self, community, rise):
        stats, created = CommunitySubscriberStats.objects.get_or_create(community=community)
        if rise:
            stats.rise += 1
        else:
            stats.fall += 1
        stats.save()
