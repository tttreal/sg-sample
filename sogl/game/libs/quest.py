from django.contrib import messages
from django.shortcuts import redirect

from ..libs.log import user_log
from ..libs.party import *
from ..libs.reward import *
from ..models import *

class QuestInfo():
    quest_id = 0
    name = ""
    power = 0
    need_stamina = 0
    is_cleared = False

    def filter(user_id, **kargs):
        quests = Quest.objects.filter(**kargs)
        user_quest_dic = {i.quest_id: i for i in UserQuest.objects.filter(user_id=user_id)}

        quests = sorted(list(quests), key=lambda x: x.display_order, reverse=True)

        quest_infos = []
        for quest in quests:
            info = QuestInfo()
            info.quest_id = quest.id
            info.name = quest.name
            info.power = quest.power
            info.need_stamina = quest.need_stamina
            if quest.id in user_quest_dic:
                user_quest = user_quest_dic[quest.id]
                info.is_cleared = user_quest.is_clear
            quest_infos.append(info)

        return quest_infos

def exec_quest(request, user_id, quest_id, redirect_to, on_success=None):
    user = User.objects.get(id=user_id)
    quest = Quest.objects.get(id=quest_id)

    if user.current_stamina < quest.need_stamina:
        messages.warning(request, 'クエストに必要なスタミナが足りません')
        return redirect(redirect_to)

    user_party_datum = UserPartyDatum.fetch_current_user_party_datum(user)
    is_quest_clear = user_party_datum.total_power >= quest.power
    if is_quest_clear:
        messages.success(request, 'クエスト成功！')
        user_quest = UserQuest.objects.get_or_none(user_id=user_id, quest_id=quest_id)
        if user_quest == None or user_quest.is_clear == False:
            user_quest = UserQuest()
            user_quest.user_id = user_id
            user_quest.quest_id = quest_id
            user_quest.is_clear = True
            user_quest.save()

        # mission
        exec_mission(user_id, quest)

        if quest.rewards:
            reward_messages = give_reward(user_id, quest.rewards)
            for reward_message in reward_messages:
                messages.success(request, reward_message)

        if on_success:
            on_success()

    else:
        messages.info(request, 'クエスト失敗... パワー不足')

    user_log(user.id, UserLog.Type.QUEST, {"quest_id":quest.id, "is_success": 1 if is_quest_clear else 0, "user_party_total_power":user_party_datum.total_power}, request, user.level)

    return redirect(redirect_to)

def exec_mission(user_id, quest):
    mission = Mission.objects.get_or_none(condition_type="clear_quest", condition_value=quest.id)
    if not mission:
        return

    user_mission = UserMission.objects.get_or_none(user_id=user_id, mission_id=mission.id)
    if user_mission:
        if user_mission.is_completed:
            return

        user_mission.count += 1
    else:
        user_mission = UserMission()
        user_mission.user_id = user_id
        user_mission.mission_id = mission.id
        user_mission.count = 1

    if user_mission.count == mission.target_amount:
        user_mission.is_completed = True

    user_mission.save()
