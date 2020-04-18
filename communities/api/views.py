from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.models import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from communities.models import Communities, CommunitySubscribers
from communities.api.serializers import CommunitySerializer, CommunityCreateSerializer, CommunityUpdateSerializer
from django.utils.translation import ugettext_lazy as _
import logging
from communities.utils import check_subscribers
logger = logging.getLogger(__name__)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_community_view(request, slug):
    try:
        community = Communities.objects.get(slug=slug)
    except Communities.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = CommunitySerializer(community)
        return Response(serializers.data)


# Not Used
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_community_view(request, slug):
    try:
        community = Communities.objects.get(slug=slug)
    except Communities.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CommunityUpdateSerializer(community, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = _("response.success")
            data['pk'] = community.pk
            data['name'] = community.name
            data['description'] = community.description
            data['slug'] = community.slug
            data['date_updated'] = community.date_updated
            image_url = str(request.build_absolute_uri(community.backgroundimage.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['backgroundimage'] = image_url
            image_url = str(request.build_absolute_uri(community.avatarimage.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['avatarimage'] = image_url
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Not Used
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_community_view(request, slug):
    try:
        community = Communities.objects.get(slug=slug)
    except Communities.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = community.delete()
        data = {}
        if operation:
            data['response'] = _("response.success")
        return Response(data=data)


# Not Used
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_community_view(request):
    if request.method == 'POST':

        data = request.data
        serializer = CommunityCreateSerializer(data=data)
        data = {}

        if serializer.is_valid():
            community = serializer.save()
            data['response'] = _("response.success")
            data['pk'] = community.pk
            data['name'] = community.name
            data['description'] = community.description
            data['slug'] = community.slug
            data['date_updated'] = community.date_updated
            image_url = str(request.build_absolute_uri(community.backgroundimage.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['backgroundimage'] = image_url
            image_url = str(request.build_absolute_uri(community.avatarimage.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['avatarimage'] = image_url
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_community_subscribe_view(request, slug):
    data = {}
    try:
        community = Communities.objects.get(slug=slug)
        user = request.user
        CommunitySubscribers(user=user, community=community).save()
        data['response'] = _("response.success")
        return Response(data=data)
    except Communities.DoesNotExist:
        data['response'] = _("response.error")
        data['error_message'] = _("msg.community.not.found")
        return Response(data=data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_community_check_subscribe_view(request, slug):
    data = {}
    try:
        data = check_subscribers(request.user, slug)
        # community = Communities.objects.get(slug=slug)
        # user = request.user
        # data['response'] = _("response.success")
        # if CommunitySubscribers.objects.filter(user=user, community=community):
        #     data['subscribed'] = True
        #     return Response(data=data)
        # data['subscribed'] = False
        return Response(data=data)
    except Communities.DoesNotExist:
        data['response'] = _("response.error")
        data['error_message'] = _("msg.community.not.found")
        return Response(data=data)


class ApiCommunityListView(ListAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description')
