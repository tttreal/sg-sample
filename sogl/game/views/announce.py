from django.shortcuts import render
from ..models import Announce

def detail(request):
    announce_id = request.GET['id']

    announce = Announce.objects.get(id=announce_id)

    params = {
        "announce": announce,
    }

    return render(request, 'game/announce/detail.html', params)
