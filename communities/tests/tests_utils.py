import pytest
from communities.models import Communities, CommunitySubscribers
from communities.utils import check_subscribers


@pytest.mark.django_db
def test_check_subscribers_shouldCheckIfUserSubscribedToCommunity(create_dataset, create_user):
    user = create_user()
    blog, community = create_dataset()
    assert CommunitySubscribers.objects.count() == 0
    data = check_subscribers(user, community.slug)
    assert not data['subscribed']

    CommunitySubscribers.objects.create(user=user, community=community)
    data = check_subscribers(user, community.slug)
    assert data['subscribed']
