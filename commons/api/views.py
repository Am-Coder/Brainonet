from rest_framework.views import APIView
from account.permissions import IsUser
from account.models import TokenAuthentication
from rest_framework.response import Response
from blog.models import Blog
from communities.models import Communities
from account.models import Account
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from .serializers import CommonsBlogSerializer, CommonsAccountSerializer, CommonsCommunitySerializer
from django.db.models.functions import Concat
from django.db.models import Value
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class ApiRelatedContentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    # Swagger query parameter
    query_param = openapi.Parameter('query', openapi.IN_QUERY, description="search parameter", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[query_param])
    def get(self, request):
        search_by = request.GET['query']
        data = {}
        if len(search_by) > 5:
            blogs = Blog.objects.filter(title__contains=search_by)
            if blogs:
                data['blogs'] = CommonsBlogSerializer(blogs, many=True).data

            communities = Communities.objects.filter(name__contains=search_by)
            if communities:
                data['communities'] = CommonsCommunitySerializer(communities, many=True).data

            # users = Account.objects.annotate(name=Concat('first_name', Value(' '),
            #                                              'last_name'), ).filter(Q(first_name__contains=search_by) |
            #                                                                     Q(last_name__contains=search_by),
            #                                                                     is_admin=False, is_staff=False)
            users = Account.objects.annotate(name=Concat('first_name', Value(' '),
                                                         'last_name'), ).filter(name__icontains=search_by,
                                                                                is_admin=False, is_staff=False)

            if users:
                data['users'] = CommonsAccountSerializer(users, many=True).data
        else:
            data['response'] = _("response.error")
            data['error_messgage'] = "Give at least 6 characters"

        return Response(data)
