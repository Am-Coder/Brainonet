from communities.models import Communities, CommunitySubscribers
from django.utils.translation import ugettext_lazy as _


def check_subscribers(user, slug):
    data = {}
    community = Communities.objects.get(slug=slug)
    user = user
    data['response'] = _("response.success")
    if CommunitySubscribers.objects.filter(user=user, community=community):
        data['subscribed'] = True
        return data
    data['subscribed'] = False
    return data
