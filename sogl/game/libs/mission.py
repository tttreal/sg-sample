from ..models import *

class MissionInfo:
    mission_id = 0
    name = ""
    condition_type = 0
    condition_value = 0
    user_count = 0
    target_amount = 0
    is_completed = False
    is_rewarded = False
    description = ""

    def filter(user_id) -> []:
        now = timezone.now()
        missions = Mission.objects.filter(open_at__lte=now, close_at__gt=now)
        mission_ids = [i.id for i in missions]
        user_missions = UserMission.objects.filter(user_id=user_id, mission_id__in=mission_ids)
        user_mission_dic = {i.mission_id: i for i in user_missions}

        mission_infos = []
        for mission in missions:
            mission_info = MissionInfo()
            mission_info.mission_id = mission.id
            mission_info.name = mission.name
            mission_info.condition_type = mission.condition_type
            mission_info.condition_value = mission.condition_value
            mission_info.target_amount = mission.target_amount
            mission_info.description = mission_info.make_description()

            if mission.id in user_mission_dic:
                user_mission = user_mission_dic[mission.id]
                mission_info.user_count = user_mission.count
                mission_info.is_completed = user_mission.is_completed
                mission_info.is_rewarded = user_mission.is_rewarded

            mission_infos.append(mission_info)

        return mission_infos

    def make_description(self):
        description = ""
        match self.condition_type:
            case "login_count":
                description = f"ログインを{self.target_amount}回しよう！"
            case "clear_quest":
                quest = Quest.objects.get(id=self.condition_value)
                description = f"クエスト {quest.name} を{self.target_amount}回クリアしよう"

        return description

