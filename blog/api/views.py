from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.permissions import IsUser
from account.models import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from account.models import Account
from blog.models import Blog, Comment, Vote, References, TaggedBlogs
from blog.api.serializers import TaggedBlogSerializer, \
    CommentSerializer, BlogSerializer, BlogCreateSerializer, BlogUpdateSerializer, \
    CommentCreateSerializer, ReferenceSerializer, CommentBlogSerializer
from django.utils.translation import ugettext_lazy as _
import logging
from blog.utils import vote_handler
from drf_yasg.utils import swagger_auto_schema
from analytics.services.BlogAnalytics import BlogAnalyticsService
from analytics.services.UserAnalytics import UserAnalyticsService
from rest_framework.exceptions import ValidationError
import json
from django.db import IntegrityError

logger = logging.getLogger(__name__)


@api_view(['GET', ])
@permission_classes((IsUser,))
def api_detail_blog_view(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        blog.view_count += 1
        blog.save()
        serializer = BlogSerializer(blog)
        return Response(serializer.data)


# Not being used now
@swagger_auto_schema(methods=['put'], request_body=BlogUpdateSerializer)
@api_view(['PUT', ])
@permission_classes((IsUser,))
def api_update_blog_view(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BlogUpdateSerializer(blog, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = _("response.success")
            data['pk'] = blog.pk
            data['title'] = blog.title
            data['body'] = blog.body
            data['slug'] = blog.slug
            data['date_updated'] = blog.date_updated
            image_url = str(request.build_absolute_uri(blog.image.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['image'] = image_url
            data['community'] = blog.community.name
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Not being used now
@api_view(['DELETE', ])
@permission_classes((IsUser,))
def api_delete_blog_view(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = blog.delete()
        data = {}
        if operation:
            data['response'] = _("response.success")
        return Response(data=data)


# Not being used now
@swagger_auto_schema(methods=['post'], request_body=BlogCreateSerializer)
@api_view(['POST'])
@permission_classes((IsUser,))
def api_create_blog_view(request):
    if request.method == 'POST':

        data = request.data
        serializer = BlogCreateSerializer(data=data)
        data = {}

        if serializer.is_valid():
            blog = serializer.save()
            data['response'] = _("response.success")
            data['pk'] = blog.pk
            data['title'] = blog.title
            data['body'] = blog.body
            data['slug'] = blog.slug
            data['date_updated'] = blog.date_updated
            image_url = str(request.build_absolute_uri(blog.image.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['image'] = image_url
            data['community'] = blog.community.name
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['post'], request_body=CommentCreateSerializer)
@api_view(['POST'])
@permission_classes([IsUser])
def add_comment(request, slug):
    data = request.data
    serializer = CommentCreateSerializer(data=data)

    data = {}
    if serializer.is_valid():
        try:
            blog = Blog.objects.get(slug=slug)
            user = request.user
            data['response'] = _("response.success")
            serializer.save(user=user, blog=blog, me="ME")
            bas = BlogAnalyticsService()
            bas.updateBlogCommentsStats(blog=blog, community=blog.community, add=True)
        except Blog.DoesNotExist:
            data['response'] = _("response.error")
            data['error_messgage'] = _("msg.blog.not.found")
        except Account.DoesNotExist:
            data['response'] = _("response.error")
            data['error_messgage'] = _("msg.account.not.found")
        except Exception as e:
            data['response'] = _("response.error")
            data['error_message'] = str(e)
        finally:
            return Response(data)
    data['response'] = _("response.error")
    data['error_message'] = serializer.errors
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsUser])
def delete_comment(request, slug, commentid):
    logger.info(slug)
    logger.info(commentid)
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
        if Comment.objects.filter(pk=commentid, blog=blog):
            Comment.objects.filter(pk=commentid, blog=blog).delete()
            bas = BlogAnalyticsService()
            bas.updateBlogCommentsStats(blog=blog, community=blog.community, add=False)
        data['response'] = _("response.success")
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['POST'])
@permission_classes([IsUser])
def toggle_blog_vote(request, slug):
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
        # count = blog.vote_count
        # all_votes = Vote.objects.filter(blog=blog)
        # data['response'] = _("response.success")
        data, count = vote_handler(request.user, blog)
        data['vote_count'] = count
        #
        # if all_votes.filter(user=request.user).exists():
        #     all_votes.filter(user=request.user).delete()
        #     count -= 1
        #     data['status'] = False
        # else:
        #     Vote.objects.create(user=request.user, blog=blog)
        #     count += 1
        #     data['status'] = True
        # data['vote_count'] = count

        blog.vote_count = count
        blog.save()

    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['POST'])
@permission_classes([IsUser])
def blog_up_vote(request, slug):
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
        count = blog.vote_count
        all_votes = Vote.objects.filter(blog=blog)
        data['response'] = _("response.success")

        if not all_votes.filter(user=request.user).exists():
            Vote.objects.create(user=request.user, blog=blog)
            count += 1

        data['vote_count'] = count
        blog.vote_count = count
        blog.save()

    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['POST'])
@permission_classes([IsUser])
def blog_down_vote(request, slug):
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
        count = blog.vote_count
        all_votes = Vote.objects.filter(blog=blog)
        data['response'] = _("response.success")

        if all_votes.filter(user=request.user).exists():
            all_votes.filter(user=request.user).delete()
            count -= 1

        data['vote_count'] = count
        blog.vote_count = count
        blog.save()

    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['GET'])
@permission_classes([IsUser])
def has_voted(request, slug):
    data = {}
    try:
        if Vote.objects.filter(user=request.user, blog=Blog.objects.get(slug=slug)).exists():
            data['response'] = _("response.success")
            data['status'] = True
        else:
            data['response'] = _("response.success")
            data['status'] = False
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['GET'])
@permission_classes([IsUser])
def api_get_personal_collection(request):
    data = {}
    try:
        user = request.user

        if TaggedBlogs.objects.filter(user=user).exists():
            serializer = TaggedBlogSerializer(TaggedBlogs.objects.filter(user=user),
                                              many=True,
                                              context={
                                                  'request': request
                                              })
            data = serializer.data

    except Account.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.account.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['POST'])
@permission_classes([IsUser])
def api_add_personal_collection(request, slug):
    data = {}
    try:
        user = request.user
        blog = Blog.objects.get(slug=slug)
        data['response'] = _("response.success")
        if not TaggedBlogs.objects.filter(user=user, blog=blog).exists():
            TaggedBlogs.objects.create(user=user, blog=blog)
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['POST'])
@permission_classes([IsUser])
def api_delete_from_personal_collection(request, slug):
    data = {}
    try:
        user = request.user
        blog = Blog.objects.get(slug=slug)
        data['response'] = _("response.success")
        if TaggedBlogs.objects.filter(user=user, blog=blog).exists():
            TaggedBlogs.objects.filter(user=user, blog=blog).delete()
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['GET'])
@permission_classes([IsUser])
def api_check_blog_personal_collection(request, slug):
    data = {}
    try:
        user = request.user
        blog = Blog.objects.get(slug=slug)
        data['response'] = _("response.success")

        if TaggedBlogs.objects.filter(user=user, blog=blog).exists():
            data['status'] = True
        else:
            data['status'] = False
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['GET'])
@permission_classes([IsUser])
def api_get_blog_parameters(request, slug):
    data = {}
    try:
        user = request.user
        blog = Blog.objects.get(slug=slug)
        data['response'] = _("response.success")

        if TaggedBlogs.objects.filter(user=user, blog=blog).exists():
            data['save'] = True
        else:
            data['save'] = False
        if Vote.objects.filter(user=request.user, blog=Blog.objects.get(slug=slug)).exists():
            data['response'] = _("response.success")
            data['vote'] = True
        else:
            data['vote'] = False
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


@api_view(['GET'])
@permission_classes([IsUser])
def api_get_blog_body(request, slug):
    data = {}
    try:
        user = request.user
        blog = Blog.objects.get(slug=slug)
        data['response'] = _("response.success")
        data['body'] = blog.body
        data['blog_pk'] = blog.pk
    except Blog.DoesNotExist:
        data['response'] = _("response.error")
        data['error_messgage'] = _("msg.blog.not.found")
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
    finally:
        return Response(data)


class ApiBlogListView(ListAPIView):
    # queryset = Blog.objects.all()
    # serializer_class = BlogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'community__name']

    def get_queryset(self):
        uas = UserAnalyticsService()
        uas.updateSiteVisitStats()
        return Blog.objects.all()

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        kwargs['context'] = self.get_serializer_context()
        return BlogSerializer(*args, **kwargs, fields=('pk', 'title', 'description', 'slug', 'image', 'date_updated',
                                                       'vote_count', 'view_count', 'community', 'vote',
                                                       'comment_count'))


class ApiReferenceListView(ListAPIView):
    queryset = References.objects.all()
    serializer_class = ReferenceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('refers', 'description')

    def get_queryset(self):

        # to return references by blog
        if 'slug' in self.request.GET:
            try:
                slug = self.request.GET['slug']
                print(slug)
                return Blog.objects.get(slug=slug).references.all()
            except Blog.DoesNotExist:
                return References.objects.none()
        else:
            return References.objects.all()


class ApiCommentByUserListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('comment', 'blog__title')

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.select_related().filter(user=user)


class ApiCommentByBlogListView(ListAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentBlogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('comment', 'user__first_name')

    def get_queryset(self):
        slug = self.kwargs['slug']
        if Comment.objects.select_related().filter(blog=Blog.objects.get(slug=slug)).count() == 0:
            raise ValidationError(detail="Blog does not exist")
        return Comment.objects.select_related().filter(blog=Blog.objects.get(slug=slug))
