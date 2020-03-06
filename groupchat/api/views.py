from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from communities.models import Communities
from django.shortcuts import Http404
from groupchat.models import Message
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from groupchat.api.serializers import MessageSerializer
PAGE_SIZE = 10
SUCCESS = 'success'


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    if Communities.objects.filter(name=room_name):
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))
        })
    raise Http404("<h1>No Such Group Present</h1>")


@api_view(['GET'])
@permission_classes((IsAuthenticated))
def getchat(request, room_name, page_num):
    data = {}

    try:
        msg = Message.objects.filter(community=Communities.objects.get(name=room_name)).order_by('-time')
        paginator = Paginator(msg, PAGE_SIZE)
        data['response'] = SUCCESS
        data['message'] = MessageSerializer(paginator.page(page_num).object_list, many=True).data
        return Response(data=data)
    except Communities.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
