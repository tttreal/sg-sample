from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from ..libs.cost import *
from ..libs.gacha import *
from ..libs.reward import *
from ..models import *

def list_(request):
    user_id = request.session.get('user_id')

    gacha_infos = GachaInfo.filter()

    params = {
        'gacha_infos' : gacha_infos
    }

    return render(request, 'game/gacha/list.html', params)

@transaction.atomic
def exec(request):
    user_id = request.session.get('user_id')
    gacha_id = request.POST['gacha_id']
    exec_count = int(request.POST['exec_count'])

    gacha_executor = GachaExecutor(gacha_id, exec_count)
    gacha_slots = gacha_executor.exec()
    rewards_list = [gacha_slot.rewards for gacha_slot in gacha_slots]
    rewards = merge_rewards_list(rewards_list)
    reward_messages = give_reward(user_id, rewards)

    messages.success(request, "ガチャで景品が当たりました")
    for reward_message in reward_messages:
        messages.success(request, reward_message)

    gacha = Gacha.objects.get(id=gacha_id)
    Cost.pay(user_id, CostInfo(gacha.cost_type, gacha.cost_id, gacha.cost_amount))

    return redirect("/gacha/list")
