from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from recommend.utils import create_dataset, train_model
from blog.models import Blog, Vote
from account.models import Account
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from account.permissions import IsUser


@api_view(["GET"])
@permission_classes([IsUser,])
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


@api_view(["GET"])
@permission_classes([IsUser,])
def train_model_view(request):
    data = {}
    try:
        train_model()
        data['response'] = _("response.success")
        return Response(data)
    except Exception as e:
        data['response'] = _("response.error")
        data['error_message'] = str(e)
        return Response(data)

