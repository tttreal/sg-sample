from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect

from ..models import UserChara
from ..models import UserPoint
from ..libs.chara import is_in_party
from ..libs.chara import CharaDatum
from ..libs.point import PointDatum

def list_(request):
    user_id = request.session.get('user_id')

    chara_data = CharaDatum.filter(user_id=user_id)

    params = {
        "chara_data": chara_data,
    }

    return render(request, 'game/chara/list.html', params)

def enhancement(request):
    user_id = request.session.get('user_id')
    user_chara_id = request.GET['user_chara_id']

    chara_datum = CharaDatum.get(id=int(user_chara_id), user_id=user_id)
    point_data = PointDatum.filter(user_id=user_id, point_id=1)

    params = {
        "user_chara_id": user_chara_id,
        "chara_datum": chara_datum,
        "level_range": range(chara_datum.level + 1, chara_datum.level + 11),
        "point_costs": list(range((chara_datum.level + 1) * 100, (chara_datum.level + 11) * 100, 100)),

        "point_data": point_data,
    }

    return render(request, 'game/chara/enhancement.html', params)

@transaction.atomic
def enhancement_exec(request):
    user_id = request.session.get('user_id')
    post = request.POST
    user_chara_id = post['user_chara_id']
    enhancement_level = post['enhancement_level']
    point_cost = int(post['point_cost'])

    user_chara = UserChara.objects.get(id=int(user_chara_id), user_id=user_id)
    user_point = UserPoint.objects.get(user_id=user_id, point_id=1)

    redirect_to = f"/chara/enhancement?user_chara_id={user_chara_id}"

    # ポイントが足りるかチェック
    is_error = False
    if (user_point.amount < point_cost):
        messages.warning(request, "ポイントが足りません")
        is_error = True

    if (is_error):
        return redirect(redirect_to)

    # 強化を行う
    before_user_chara_level = user_chara.level
    user_point.updateAmount(-point_cost)
    user_chara.enhance(enhancement_level)
    user_point.save()
    user_chara.save()
    messages.success(request, "強化を行いました")
    messages.success(request, f"レベル: {before_user_chara_level} → {enhancement_level}")

    return redirect(redirect_to)
    
@transaction.atomic
def sell_exec(request):
    user_id = request.session.get('user_id')
    user_chara_id = request.GET['user_chara_id']

    redirect_to = f"/chara/list"

    user_chara = UserChara.objects.get_or_none(user_id=user_id, id = user_chara_id)
    if user_chara == None:
        messages.warning(request, "不正なエラーです")
        return redirect(redirect_to)
    if is_in_party(user_chara):
        messages.warning(request, "パーティに入っているキャラは売却できません")
        return redirect(redirect_to)

    user_chara.delete()

    point_by_sell = user_chara.level * 100
    user_point = UserPoint.objects.get(user_id=user_id, point_id=1)
    user_point.amount += point_by_sell

    messages.info(request, f"キャラを売却しました")
    messages.success(request, f"ポイントを獲得しました: +{point_by_sell} ({user_point.amount} <- {user_point.amount - point_by_sell})")

    return redirect(redirect_to)
