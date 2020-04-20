import pytest
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from communities.models import CommunitySubscribers, Communities
import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_api_detail_community_view_shouldReturnCommunityDetailsBySlug(auth_api_client, create_dataset, in_memory_image):
    blog, community = create_dataset()
    img = in_memory_image()
    community.avatarimage.save(img.name, content=img)
    community.backgroundimage.save(img.name, content=img)

    url = reverse("communities:detail", kwargs={'slug': community.slug})
    response = auth_api_client.get(url)
    data = response.data
    assert data['pk'] == community.pk
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_communitylistview(auth_api_client, create_dataset_with_image):
    create_dataset_with_image()
    url = reverse("communities:community-list")
    response = auth_api_client.get(url)
    data = response.data
    assert len(data['results']) > 0
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_community_check_subscribe_view_shouldCheckIfUserHasSubscribedCommunity(create_dataset, auth_api_client,
                                                                                    create_user):
    blog, community = create_dataset()
    user = create_user()
    url = reverse("communities:check_community_subscribe", kwargs={'slug': community.slug})

    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert not data['subscribed']
    assert CommunitySubscribers.objects.count() == 0

    CommunitySubscribers.objects.create(user=user, community=community)
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert data['subscribed']
    assert CommunitySubscribers.objects.count() == 1


@pytest.mark.django_db
def test_api_community_subscribe_view_shouldMakeUserSubscribeOrUnsubscribeCommunity(create_dataset, auth_api_client):
    blog, community = create_dataset()
    url = reverse("communities:community_subscribe", kwargs={'slug': community.slug})

    # Subscribe
    assert CommunitySubscribers.objects.count() == 0
    response = auth_api_client.post(url)
    data = response.data
    community = Communities.objects.get(slug=community.slug)
    assert CommunitySubscribers.objects.count() == 1
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert community.subscriber_count == 1

    # Un Subscribe
    response = auth_api_client.post(url)
    data = response.data
    community = Communities.objects.get(slug=community.slug)
    assert CommunitySubscribers.objects.count() == 0
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert community.subscriber_count == 0
