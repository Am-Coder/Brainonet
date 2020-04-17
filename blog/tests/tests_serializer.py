from blog.api.serializers import CommentCreateSerializer, ReferenceSerializer, \
    BlogCreateSerializer, BlogUpdateSerializer, BlogSerializer
import pytest
from blog.models import Blog, Comment, Vote, References


@pytest.fixture
def db_comment_serializer():
    return [{'comment': 'a'*251},
            {'comment': 'a'*250}]


@pytest.fixture
def db_references_serializer():
    return [{'refers': 'abc.com', 'description': 'Reference'}]


@pytest.mark.django_db
def test_comment_create_serializer_shoudlValidateCommentLength(db_comment_serializer):
    serializer = CommentCreateSerializer(data=db_comment_serializer[0])
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {'comment': ['Maximum Comment length exceeded']}


@pytest.mark.django_db
def test_comment_create_serializer_shoudlSaveValidatedComment(db_comment_serializer, create_user, create_dataset):
    serializer = CommentCreateSerializer(data=db_comment_serializer[1])
    assert serializer.is_valid()
    assert Comment.objects.count() == 0
    user = create_user()
    blog, community = create_dataset()
    serializer.save(user=user, blog=blog)
    assert serializer.validated_data == db_comment_serializer[1]
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_references_serializer_shouldSaveValidatedReference(db_references_serializer):
    serializer = ReferenceSerializer(data=db_references_serializer[0])
    assert serializer.is_valid()
    assert References.objects.count() == 0
    serializer.save()
    assert References.objects.count() == 1

