from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from expose.models import Expose
from expose.api.serializers import ExposeSerializer, ExposeCreateSerializer, ExposeUpdateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_expose_view(request, slug):
  
  try:
    expose = Expose.objects.get(slug=slug)
  except Expose.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = ExposeSerializer(expose)
    return Response(serializer.data)

@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def api_update_expose_view(request, slug):

  try:
    expose = Expose.objects.get(slug=slug)
  except Expose.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'PUT':
    serializer = ExposeUpdateSerializer(expose, data=request.data, partial=True)
    data = {}
    if serializer.is_valid():
      serializer.save()
      data['response'] = expose.pk
      data['title'] = expose.title
      data['body'] = expose.body
      data['slug'] = expose.slug
      data['date_updated'] = expose.date_updated
      image_url = str(request.build_absolute_uri(expose.image.url))
      if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
      data['image'] = image_url
      data['exposeunit'] = expose.exposeunit.name
      return Response(data = data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def api_delete_expose_view(request, slug):

  try:
    expose = Expose.objects.get(slug=slug)
  except Expose.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'DELETE':
    operation = expose.delete()
    data = {}
    if operation:
      data['response'] = DELETE_SUCCESS
    return Response(data=data)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def api_create_expose_view(request):

  if request.method == 'POST':

    data = request.data
    serializer = ExposeCreateSerializer(data=data)
    data = {}

    if serializer.is_valid():
      expose = serializer.save()
      data['response'] = CREATE_SUCCESS
      data['pk'] = expose.pk
      data['title'] = expose.title
      data['body'] = expose.body
      data['slug'] = expose.slug
      data['date_updated'] = expose.date_updated
      image_url = str(request.build_absolute_uri(expose.image.url))
      if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
      data['image'] = image_url
      data['exposeunit'] = expose.exposeunit.name
      return Response(data = data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ApiExposeListView(ListAPIView):
  queryset = Expose.objects.all()
  serializer_class = ExposeSerializer
  authentication_classes = (TokenAuthentication, )
  permission_classes = (IsAuthenticated, )
  pagination_class = PageNumberPagination
  filter_backends = (SearchFilter, OrderingFilter)
  search_fields = ('title', 'body', 'exposeunit__name')