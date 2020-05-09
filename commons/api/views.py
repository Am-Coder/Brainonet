from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.models import TokenAuthentication
from rest_framework.response import Response
from blog.models import Blog
from communities.models import Communities
from account.models import Account
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from .serializers import CommonsBlogSerializer, CommonsAccountSerializer, CommonsCommunitySerializer


# Create your views here.
class ApiRelatedContentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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

            users = Account.objects.filter(Q(first_name__contains=search_by) | Q(last_name__contains=search_by),
                                           is_admin=False, is_staff=False)
            if users:
                data['users'] = CommonsAccountSerializer(users, many=True)
        else:
            data['response'] = _("response.error")
            data['error_messgage'] = "Give at least 6 characters"

        return Response(data)
