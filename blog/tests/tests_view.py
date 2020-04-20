import pytest
from blog.models import Blog, Vote, Comment, References, TaggedBlogs
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from account.models import Token


@pytest.mark.django_db
def test_api_detail_blog_view_shouldReturnBlogDetailsBySlug(auth_api_client, create_dataset, image_url):
    url = image_url()
    blog, community = create_dataset()
    blog.image = url
    blog.save()
    assert blog.view_count == 0
    url = reverse("blog:detail", kwargs={'slug': blog.slug})
    response = auth_api_client.get(url)
    data = response.data
    blog = Blog.objects.get(slug=blog.slug)
    assert response.status_code == 200
    assert blog.pk == data['pk']
    assert blog.title == data['title']
    assert blog.view_count == 1
    assert data['view_count'] == blog.view_count


@pytest.mark.django_db
def test_api_bloglistview(auth_api_client, create_dataset_with_image):
    create_dataset_with_image()
    url = reverse("blog:blog-list")
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert len(data['results']) > 0


@pytest.mark.django_db
def test_api_referencelistview(auth_api_client):
    References.objects.create(refers="Refers", description="Describe")
    url = reverse("blog:reference-list")
    response = auth_api_client.get(url)
    data = response.data
    assert len(data['results']) > 0
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_commentbyuserlistview(create_user, api_client, create_dataset_with_image):
    blog, community = create_dataset_with_image()
    user1 = create_user(mobile_number="111111", first_name="Sasuke", last_name="Uchiha")
    user2 = create_user(mobile_number="111112", first_name="Madara", last_name="Uchiha")
    Comment.objects.create(comment="hi", blog=blog, user=user1)
    Comment.objects.create(comment="hello", blog=blog, user=user1)
    Comment.objects.create(comment="hi", blog=blog, user=user2)

    print(Comment.objects.filter(user=user1).count())
    token1, s1 = Token.objects.get_or_create(user=user1)
    token2, s2 = Token.objects.get_or_create(user=user2)

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)
    url = reverse("blog:comment-list-user")
    response1 = api_client.get(url)
    data1 = response1.data

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
    response2 = api_client.get(url)
    data2 = response2.data

    assert len(data1['results']) == 2
    assert response1.status_code == 200
    assert len(data2['results']) == 1
    assert response2.status_code == 200


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


@pytest.mark.django_db
def test_api_get_personal_collection(auth_api_client, create_dataset, create_user):
    blog, community = create_dataset()
    user = create_user()
    url = reverse("blog:get_personal_collection")
    assert TaggedBlogs.objects.count() == 0
    TaggedBlogs.objects.create(user=user, blog=blog)
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert len(data) == 1
    assert TaggedBlogs.objects.count() == 1


@pytest.mark.django_db
def test_api_add_personal_collection(auth_api_client, create_dataset):
    blog, community = create_dataset()
    url = reverse("blog:add_to_collection", kwargs={'slug': blog.slug})
    assert TaggedBlogs.objects.count() == 0
    response = auth_api_client.post(url)
    data = response.data
    print(data)
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert TaggedBlogs.objects.count() == 1


@pytest.mark.django_db
def test_api_delete_from_personal_collection(auth_api_client, create_dataset, create_user):
    blog, community = create_dataset()
    user = create_user()
    url = reverse("blog:remove_from_collection", kwargs={'slug': blog.slug})
    TaggedBlogs.objects.create(user=user, blog=blog)
    assert TaggedBlogs.objects.count() == 1
    response = auth_api_client.post(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert TaggedBlogs.objects.count() == 0


@pytest.mark.django_db
def test_api_check_blog_personal_collection(auth_api_client, create_dataset, create_user):
    blog, community = create_dataset()
    user = create_user()
    url = reverse("blog:check_in_collection", kwargs={'slug': blog.slug})

    # Blog Not in Collection
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert TaggedBlogs.objects.count() == 0
    assert not data['status']

    # Blog in personal collection
    TaggedBlogs.objects.create(user=user, blog=blog)
    response = auth_api_client.get(url)
    data = response.data
    assert response.status_code == 200
    assert data['response'] == _("response.success")
    assert TaggedBlogs.objects.count() == 1
    assert data['status']
