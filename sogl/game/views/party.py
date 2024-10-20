from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect

from ..models import *
from ..libs.party import *
from ..libs.chara import *

def list_(request):
    user_id = request.session.get('user_id')

    user = User.objects.get(id=user_id)
    user_party_data = UserPartyDatum.filter_for_party_list(user_id=user_id)
    params = {
        "user_select_party_id": user.select_party_id,
        "user_party_data": user_party_data,
    }

    return render(request, 'game/party/list.html', params)

def edit(request):
    user_id = request.session.get('user_id')
    party_id = request.GET['party_id']

    user_party_data = UserPartyDatum.filter(user_id=user_id, party_id=party_id)

    # まだパーティ情報がない場合は作成する
    if not user_party_data:
        user_party = UserParty()
        user_party.user_id = user_id
        user_party.party_id = party_id
        user_party.save()

    user_party_datum = UserPartyDatum.filter(user_id=user_id, party_id=party_id)[0]
    chara_data = CharaDatumForPartyEdit.filter(user_party_datum.user_party_id, user_id=user_id)

    params = {
        "party_id": party_id,
        "user_party_datum": user_party_datum,
        "chara_data": chara_data,
    }

    return render(request, 'game/party/edit.html', params)

@transaction.atomic
def edit_exec(request):
    user_id = request.session.get('user_id')
    party_id = request.POST['party_id']
    user_chara_ids = request.POST.getlist('user_chara_ids')

    redirect_to = f"/party/edit?party_id={party_id}"

    # キャラが1人も選択されていない
    is_error = False
    if len(user_chara_ids) <= 0:
        messages.warning(request, "パーティに入れるキャラを選択してください")
        is_error = True

    # キャラが5人より多く選択されている
    if len(user_chara_ids) > settings.PARTY_CHARA_MAX_NUM:
        messages.warning(request, "パーティに入れるキャラ数は5人までです")
        is_error = True

    # 選択されたキャラがすべてuserの所持であるかをチェック
    user_charas = UserChara.objects.filter(user_id=user_id, id__in=user_chara_ids)
    if len(user_charas) != len(user_chara_ids):
        messages.warning(request, "不正なエラー")   # 他userのキャラを編成しようとした
        is_error = True

    if (is_error):
        return redirect(redirect_to)

    # パーティ編成
    (user_party, is_created) = UserParty.objects.get_or_create(user_id=user_id, party_id=party_id)
    if is_created == False:
        user_party.user_id = user_id
        user_party.party_id = party_id
        user_party.save()

    UserPartyChara.objects.filter(user_party_id=user_party.id).delete()
    for user_chara_id in user_chara_ids:
        upc = UserPartyChara()
        upc.user_chara_id = user_chara_id
        upc.user_party_id = user_party.id
        upc.save()

    messages.success(request, "パーティを編成しました")

    return redirect(redirect_to)
    
def set_use_party(request):
    user_id = request.session.get('user_id')
    party_id = request.POST['party_id']

    user = User.objects.get(id=user_id)
    user.select_party_id = int(party_id)
    user.save()

    redirect_to = f"/party/list"
    return redirect(redirect_to)


