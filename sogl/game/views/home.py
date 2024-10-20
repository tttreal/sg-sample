import random
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from ..models import *
from ..libs.point import PointDatum
from ..libs.reward import *
from ..libs.stamina import *
from ..libs.log import user_log

@transaction.atomic
def index(request):
    user_id = request.session.get('user_id')

    # ユーザ取得
    user = User.objects.get_or_none(id=user_id)
    # もしユーザが存在していなかった場合、新規アクセスとみなし、初期処理を行う
    if (user is None):
        user = exec_initial_process(request)

    if update_login_count(user):
        user.save()
        exec_login_bonus(request, user)
        user_log(user.id, UserLog.Type.DAILY_LOGIN, {"login_count":user.login_count}, request, user.level)
    if update_stamina(user):
        user.save()

    point_data = PointDatum.filter(user_id=user_id)

    announces = fetch_announces()

    params = {
        "user": user,
        "point_data": point_data,
        "user_stamina_info": UserStaminaInfo.from_User(user),
        "announces": announces
    }

    return render(request, 'game/home/index.html', params)

@transaction.atomic
def exec_initial_process(request):
    user = create_user()
    request.session['user_id'] = user.id
    messages.success(request, f"新規ユーザを作成しました: {user.name}")

    # 初期ユーザ

    # 初期キャラ
    user_chara = UserChara()
    user_chara.user_id = user.id
    user_chara.chara_id = 1
    user_chara.level = 1
    user_chara.save()
    messages.success(request, f"初期キャラを1体付与しました")

    # 初期パーティ
    user_party = UserParty()
    user_party.user_id = user.id
    user_party.party_id = 1
    user_party.save()

    # 初期パーティキャラ
    user_party_chara = UserPartyChara()
    user_party_chara.user_party_id = user_party.id
    user_party_chara.user_chara_id = user_chara.id
    user_party_chara.save()
    messages.success(request, f"初期パーティを編成しました")

    # 初期ポイント
    user_point = UserPoint()
    user_point.user_id = user.id
    user_point.point_id = 1
    user_point.amount = 1000
    user_point.save()
    messages.success(request, f"初期ポイントを付与しました")

    return user

def create_user():
    user = User()
    user.name = make_random_user_name()
    user.level = 1
    user.login_count = 0
    MAX_STAMINA = settings.STAMINA_MAX_LEVEL_RATE * user.level
    user.current_stamina = MAX_STAMINA
    user.last_recovered_at = timezone.now()
    user.select_party_id = 1
    user.save()

    return user

def make_random_user_name():
    # 日本っぽい4文字の名前のリスト
    names = ['taro', 'jiro', 'sabu', 'goro', 'nobu', 'mako', 'yuki', 'keni']
    
    # 名前をランダムに選択
    chosen_name = random.choice(names)
    
    # 4桁のランダムな数字を生成
    random_digits = str(random.randint(1000, 9999))
    
    # 名前と数字を結合してユーザー名を生成
    user_name = chosen_name + random_digits
    
    return user_name

def update_login_count(user):
    if user.last_accessed_at:
        last_accessed_day = user.last_accessed_at.day
    else:
        last_accessed_day = 0
    now_day = timezone.now().day

    if (now_day > last_accessed_day):
        user.login_count += 1
        user.last_accessed_at = timezone.now()

        # mission
        missions = Mission.objects.filter(condition_type="login_count", condition_value=1)
        for mission in missions:
            if mission:
                user_mission = UserMission.objects.get_or_none(user_id=user.id, mission_id=mission.id)
                if user_mission:
                    if not user_mission.is_completed:
                        user_mission.count += 1
                else:
                    user_mission = UserMission()
                    user_mission.user_id = user.id
                    user_mission.mission_id = mission.id
                    user_mission.count = 1

                if user_mission.count == mission.target_amount:
                    user_mission.is_completed = True

                user_mission.save()

        return True

    return False

def exec_login_bonus(request, user:User):
    login_bonuses = LoginBonus.objects.filter(open_at__lte=user.last_accessed_at, close_at__gt=user.last_accessed_at)
    login_bonus_ids = [i.id for i in login_bonuses]
    user_login_bonuses = UserLoginBonus.objects.filter(user_id=user.id, login_bonus_id__in=login_bonus_ids)
    user_login_bonus_dic = {i.login_bonus_id: i for i in user_login_bonuses}
    rewards_list = []
    for login_bonus in login_bonuses:
        if login_bonus.id in user_login_bonus_dic:
            user_login_bonus = user_login_bonus_dic[login_bonus.id]
            user_login_bonus.day += 1
        else:
            user_login_bonus = UserLoginBonus()
            user_login_bonus.login_bonus_id = login_bonus.id
            user_login_bonus.user_id = user.id
            user_login_bonus.day = 1

        user_login_bonus.save()

        login_bonus_reward = LoginBonusReward.objects.get_or_none(login_bonus_id=login_bonus.id, day=user_login_bonus.day)
        if login_bonus_reward != None:
            rewards_list.append(login_bonus_reward.rewards)

    if not rewards_list:
        return

    rewards = merge_rewards_list(rewards_list)
    reward_messages = give_reward(user.id, rewards)

    messages.success(request, "ログインボーナスを獲得しました")
    for reward_message in reward_messages:
        messages.success(request, reward_message)

def fetch_announces():
    now = timezone.now()
    return Announce.objects.filter(open_at__lte=now, close_at__gt=now)
