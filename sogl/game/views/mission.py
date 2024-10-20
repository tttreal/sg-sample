from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone

from ..models import *
from ..libs.mission import *
from ..libs.reward import *
from ..libs.log import user_log

def list_(request):
    user_id = request.session.get('user_id')

    mission_infos = MissionInfo.filter(user_id)

    params = {
        "mission_infos": mission_infos
    }

    return render(request, 'game/mission/list.html', params)

@transaction.atomic
def achieve(request):
    user_id = request.session.get('user_id')
    mission_id = request.POST['mission_id']

    redirect_to = "/mission/list"
    user_mission = UserMission.objects.get_or_none(user_id=user_id, mission_id=mission_id)
    if not user_mission:
        messages.warning(request, '不正なエラーです')
        return redirect(redirect_to)

    if not user_mission.is_completed:
        messages.warning(request, 'ミッションを達成していません')
        return redirect(redirect_to)

    if user_mission.is_rewarded:
        messages.warning(request, 'すでに報酬を受け取っています')
        return redirect(redirect_to)

    mission = Mission.objects.get_or_none(id=mission_id)
    if not mission:
        messages.warning(request, '不正なエラーです')
        return redirect(redirect_to)

    # 報酬
    reward_messages = give_reward(user_id, mission.rewards)
    messages.success(request, "ミッション報酬を獲得しました")
    for reward_message in reward_messages:
        messages.success(request, reward_message)

    # 報酬獲得
    user_mission.is_rewarded = True
    user_mission.save()

    user = User.objects.get(id=user_id)
    user_log(user_id, UserLog.Type.MISSION_COMPLETE, {"mission_id":mission.id}, request, user.level)

    return redirect(redirect_to)
