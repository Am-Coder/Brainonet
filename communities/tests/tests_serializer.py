import pytest
from communities.api.serializers import CommunitySerializer
from communities.models import Communities


# https://stackoverflow.com/questions/8611651/generate-in-memory-image-for-django-testing

# https://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
# https://stackoverflow.com/questions/30434323/django-resize-image-before-upload/30435175#30435175

# https://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield

# https://docs.djangoproject.com/en/3.0/ref/files/file/#the-contentfile-class
# @pytest.mark.skip
@pytest.mark.django_db
def test_community_serializer_shouldValidateAvatarAndBackgroundImageUrl(create_dataset, in_memory_image):
    img_file = in_memory_image()
    blog, community = create_dataset()
    community = Communities.objects.get(slug=community.slug)
    community.avatarimage = img_file
    community.backgroundimage = img_file

    serializer = CommunitySerializer(community)
    data = serializer.data
    assert data['pk'] == community.pk
    assert data['slug'] == community.slug
