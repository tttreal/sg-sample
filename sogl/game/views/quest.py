from django.db import transaction
from django.shortcuts import render
from ..libs.party import *
from ..libs.quest import *

def list_(request):
    user_id = request.session.get('user_id')

    quest_infos = QuestInfo.filter(user_id, type=Quest.Type.NORMAL)

    params = {
        'quest_infos' : quest_infos
    }

    return render(request, 'game/quest/list.html', params)

@transaction.atomic
def exec(request):
    user_id = request.session.get('user_id')
    quest_id = request.POST['quest_id']

    redirect_to = f"/quest/list"

    return exec_quest(request, user_id, quest_id, redirect_to)
