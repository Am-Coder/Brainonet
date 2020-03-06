from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from exposeunits.models import Exposeunits
from exposeunits.api.serializers import ExposeunitSerializer, ExposeunitCreateSerializer, ExposeunitUpdateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_exposeunit_view(request, slug):

  try:
    exposeunit = Exposeunits.objects.get(slug=slug)
  except Exposeunits.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializers = ExposeunitSerializer(exposeunit)
    return Response(serializers.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def api_update_exposeunit_view(request, slug):

  try:
    exposeunit = Exposeunits.objects.get(slug=slug)
  except Exposeunits.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'PUT':
    serializer = ExposeunitUpdateSerializer(exposeunit, data=request.data, partial=True)
    data = {}
    if serializer.is_valid():
      serializer.save()
      data['response'] = UPDATE_SUCCESS
      data['pk'] = exposeunit.pk
      data['name'] = exposeunit.name
      data['description'] = exposeunit.description
      data['slug'] = exposeunit.slug
      data['date_updated'] = exposeunit.date_updated
      image_url = str(request.build_absolute_uri(exposeunit.backgroundimage.url))
      if "?" in image_url: 
        image_url = image_url[:image_url.rfind("?")]
      data['backgroundimage'] = image_url
      image_url = str(request.build_absolute_uri(exposeunit.avatarimage.url))
      if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
      data['avatarimage'] = image_url
      return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def api_delete_exposeunit_view(request, slug):

  try:
    exposeunit = Exposeunits.objects.get(slug=slug)
  except Exposeunits.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'DELETE':
    operation = exposeunit.delete()
    data = {}
    if operation:
      data['response'] = DELETE_SUCCESS
    return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def api_create_exposeunit_view(request):

  if request.method == 'POST':

    data = request.data
    serializer = ExposeunitCreateSerializer(data=data)
    data = {}

    if serializer.is_valid():
      exposeunit = serializer.save()
      data['response'] = CREATE_SUCCESS
      data['pk'] = exposeunit.pk
      data['name'] = exposeunit.name
      data['description'] = exposeunit.description
      data['slug'] = exposeunit.date_updated
      image_url = str(request.build_absolute_uri(exposeunit.backgroundimage.url))
      if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
      data['backgroundimage'] = image_url
      image_url = str(request.build_absolute_uri(exposeunit.avatarimage.url))
      if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
      data['avatarimage'] = image_url
      return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiExposeunitListView(ListAPIView):
  queryset = Exposeunits.objects.all()
  serializer_class = ExposeunitSerializer
  authentication_classes = (TokenAuthentication, )
  permission_classes = (IsAuthenticated, )
  pagination_class = PageNumberPagination
  filter_backends = (SearchFilter, OrderingFilter)
  search_fields = ('name', 'description')
    