import json
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from ..libs.present import *
from ..libs.reward import *

def box(request):
    user_id = request.session.get('user_id')

    present_box_infos = PresentBoxInfo.fetch_present_box_infos(user_id)

    params = {
        'present_box_infos' : present_box_infos
    }

    return render(request, 'game/present/box.html', params)

@transaction.atomic
def receive(request):
    user_id = request.session.get('user_id')
    user_present_id = request.GET['user_present_id']

    user_present = UserPresent.objects.get(id=user_present_id, user_id=user_id)

    if open_present(user_present) == False:
        messages.warning(request, "不正なエラーです")
    messages.success(request, "プレゼントを受け取りました")

    return redirect("/present/box")

def debug_send(request):
    params = {
    }

    return render(request, 'game/present/debug_send.html', params)

def debug_send_exec(request):
    user_id = request.session.get('user_id')
    rewards_raw_str = request.POST['rewards']
    direct = False
    if 'direct' in request.POST and request.POST['direct']:
        direct = True

    rewards = json.loads(rewards_raw_str)

    # キャラをいっぱい付与されると爆発してしまうので、数を制限
    for reward in rewards:
        if reward['type'] == 'chara' and reward['amount'] >= 10:
            reward['amount'] = 10

    if direct:
        reward_messages = give_reward(user_id, rewards)

        messages.success(request, "直接付与しました")
        for reward_message in reward_messages:
            messages.success(request, reward_message)
    else:
        send_present(user_id, rewards)
        messages.success(request, "プレゼントを送付しました")
    
    return redirect("/present/debug_send")
