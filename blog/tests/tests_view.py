import pytest
from account.models import Token, Account
from blog.models import Blog, Vote, Comment
from communities.models import Communities
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


@pytest.mark.django_db
def test_api_detail_blog_view_shouldReturnBlogDetailsBySlug(auth_api_client, create_dataset, image_url):
    url = image_url()
    blog, community = create_dataset()
    blog.image = url
    blog.save()
    url = reverse("blog:detail", kwargs={'slug': blog.slug})
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert blog.pk == data['pk']
    assert blog.title == data['title']


@pytest.mark.django_db
def test_api_bloglistview(auth_api_client, create_dataset):
    url = reverse("blog:blog-list")
    response = auth_api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_referencelistview(auth_api_client):
    url = reverse("blog:reference-list")
    response = auth_api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_has_voted_shouldReturnWheteherUserHasVotedOrNot(auth_api_client, create_dataset, create_user):
    blog, community = create_dataset()
    url = reverse("blog:has_voted", kwargs={'slug': blog.slug})

    # Has Not Voted
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert not data['status']

    # Has Voted
    user = create_user()
    Vote.objects.create(user=user, blog=blog)
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert data['status']


@pytest.mark.django_db
def test_add_comment_shouldAddCommentToBlogByUser(auth_api_client, create_dataset):
    blog, community = create_dataset()
    url = reverse("blog:add_comment", kwargs={'slug': blog.slug})
    response = auth_api_client.post(url, {'comment': 'Comments'})
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_delete_comment_shouldDeleteCommentOnBlogByUser(auth_api_client, create_dataset, create_user):
    blog, community = create_dataset()
    comment = Comment.objects.create(comment="Comment", blog=blog, user=create_user())
    assert Comment.objects.count() == 1
    url = reverse("blog:delete_comment", kwargs={'slug': blog.slug, 'commentid': comment.pk})
    response = auth_api_client.post(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_toggle_blog_vote_shouldToggleVoteOnBlog(auth_api_client, create_dataset):
    blog, community = create_dataset()
    slug = blog.slug
    url = reverse("blog:blog_vote", kwargs={'slug': slug})
    assert blog.vote_count == 0
    assert Vote.objects.count() == 0
    response = auth_api_client.post(url)

    # Up Vote
    data = response.data
    blog = Blog.objects.get(slug=slug)
    assert blog.vote_count == 1
    assert data['vote_count'] == 1
    assert response.status_code == 200
    assert data['response'] == _("response.success")

    # Down Vote
    response = auth_api_client.post(url)
    data = response.data
    blog = Blog.objects.get(slug=slug)
    assert blog.vote_count == 0
    assert data['vote_count'] == 0
    assert response.status_code == 200
    assert data['response'] == _("response.success")
