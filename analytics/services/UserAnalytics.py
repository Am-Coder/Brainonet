from analytics.models import UserVisitStats
import datetime


class UserAnalytics:

    def updateUserVisitStats(self):
        stats = UserVisitStats.objects.get_or_create(date=datetime.date.today)
        stats.visits += 1
        stats.save()
