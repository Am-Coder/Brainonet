from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from recommend.utils import create_dataset
from blog.models import Blog, Vote
from account.models import Account
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def create_dataset_view(request):
    data = {}
    try:
        users = Account.objects.filter(is_admin=False, is_staff=False, is_active=True)
        blogs = Blog.objects.all()
        create_dataset(users, blogs)
        data['response'] = _("response.success")
        return Response(data)
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
        return Response(data)
