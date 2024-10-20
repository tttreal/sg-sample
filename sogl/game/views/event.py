from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from ..libs import event as libevent
from ..libs.quest import QuestInfo
from ..libs.quest import exec_quest as quest_exec_quest
from ..models import *


def top(request):
    user_id = request.session.get('user_id')

    now = timezone.now()
    event = Event.objects.filter(open_at__lte=now, close_at__gt=now).first()

    if not event:
        return render(request, f'game/event/none.html')

    event_quests = EventQuest.objects.filter(event_id=event.id)
    event_quest_quest_ids = [i.quest_id for i in event_quests]
    quest_infos = QuestInfo.filter(user_id, type=Quest.Type.EVENT, id__in=event_quest_quest_ids)

    params = {
        "event": event,
        "quest_infos": quest_infos,
        "ranking_infos": libevent.EventPointRanking(event.id).fetch_top_ranking(),
    }

    return render(request, f'game/event/{event.id}/top.html', params)

@transaction.atomic
def exec_quest(request):
    user_id = request.session.get('user_id')
    event_id = request.POST['event_id']
    quest_id = request.POST['quest_id']

    redirect_to = f"/event/top"

    def on_success():
        event = Event.objects.get(id=event_id)
        user_point = UserPoint.objects.get_or_none(user_id=user_id, point_id=event.ranking_point_id)
        if user_point:
            ranking_point = user_point.amount
            libevent.update_ranking(user_id, event_id, ranking_point)

    return quest_exec_quest(request, user_id, quest_id, redirect_to, on_success)
