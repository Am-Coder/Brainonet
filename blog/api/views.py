from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from account.models import Account
from blog.models import Blog, Comment, Vote
from blog.api.serializers import BlogSerializer, BlogCreateSerializer, BlogUpdateSerializer, CommentCreateSerializer


SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_blog_view(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
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
            data['response'] = UPDATE_SUCCESS
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


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_blog_view(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = blog.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):
    if request.method == 'POST':

        data = request.data
        serializer = BlogCreateSerializer(data=data)
        data = {}

        if serializer.is_valid():
            blog = serializer.save()
            data['response'] = CREATE_SUCCESS
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, slug):
    data = request.data
    serializer = CommentCreateSerializer(data=data)

    data = {}
    if serializer.is_valid():
        try:
            blog = Blog.objects.get(slug=slug)
            user = request.user
            data['response'] = SUCCESS
            # print(blog)
            # print(user)
            serializer.save(user=user, blog=blog, me="ME")

        except Blog.DoesNotExist:
            data['response'] = ERROR
            data['error_messgage'] = "No Such Blog Exists"
        except Account.DoesNotExist:
            data['response'] = ERROR
            data['error_messgage'] = "You are not authenticated"
        finally:
            return Response(data)
    data['response'] = ERROR
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_comment(request, slug, commentid):
    print(slug)
    print(commentid)
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
        Comment.objects.filter(pk=commentid, blog=blog).delete()
        data['response'] = SUCCESS
    except Blog.DoesNotExist:
        data['response'] = ERROR
        data['error_messgage'] = "No Such Blog Exists"

    finally:
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_blog_vote(request, slug):
    data = {}
    try:
        blog = Blog.objects.get(slug=slug)
        count = blog.vote_count
        all_votes = Vote.objects.filter(blog=blog)
        data['response'] = SUCCESS
        if all_votes.filter(user=request.user).exists():
            all_votes.filter(user=request.user).delete()
            count -= 1
            data['status'] = False
        else:
            Vote.objects.create(user=request.user, blog=blog)
            count += 1
            data['status'] = True
        blog.vote_count = count
        blog.save()

    except Blog.DoesNotExist:
        data['response'] = ERROR
        data['error_messgage'] = "No Such Blog Exists"

    finally:
        return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_voted(request, slug):
    data = {}
    try:
        if Vote.objects.filter(user=request.user, blog=Blog.objects.get(slug=slug)).exists():
            data['response'] = SUCCESS
            data['status'] = True
        else:
            data['response'] = SUCCESS
            data['status'] = False
    except Blog.DoesNotExist:
        data['response'] = ERROR
        data['error_messgage'] = "No Such Blog Exists"

    finally:
        return Response(data)


class ApiBlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body', 'community__name')
