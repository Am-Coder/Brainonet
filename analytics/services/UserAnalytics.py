from analytics.models import UserVisitStats
import datetime


class UserAnalyticsService:

    def updateSiteVisitStats(self):
        stats, created = UserVisitStats.objects.get_or_create(date=datetime.date.today())
        stats.visits += 1
        stats.save()
