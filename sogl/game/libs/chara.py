from ..models import Chara
from ..models import UserChara
from ..models import UserPartyChara

class CharaDatum:
    chara_id = 0
    user_chara_id = 0
    name = ""
    level = 0
    power = 0
    created_at = None
    updated_at = None

    def get(**kwargs):
        user_chara = UserChara.objects.get(**kwargs)
        chara = Chara.objects.get(id=user_chara.chara_id)
        return CharaDatum.fromCharaAndUserChara(chara, user_chara)

    def filter(**kwargs):
        user_charas = UserChara.objects.filter(**kwargs)

        user_chara_chara_ids = list(user_charas.values_list('chara_id', flat=True))
        charas = Chara.objects.filter(id__in=user_chara_chara_ids)
        chara_dict = {chara.id: chara for chara in charas}

        chara_data = []
        for user_chara in user_charas:
            chara = chara_dict[user_chara.chara_id]
            chara_data.append(CharaDatum.fromCharaAndUserChara(chara, user_chara))

        return chara_data

    def fromCharaAndUserChara(chara, user_chara):
        chara_datum = CharaDatum()
        chara_datum.chara_id = chara.id
        chara_datum.user_chara_id = user_chara.id
        chara_datum.name = chara.name
        chara_datum.level = user_chara.level
        chara_datum.power = CharaDatum.calc_power(chara, user_chara)
        chara_datum.created_at = user_chara.created_at
        chara_datum.updated_at = user_chara.updated_at
        return chara_datum

    def calc_power(chara, user_chara):
        return chara.power + chara.power_rate_by_level * user_chara.level

class CharaDatumForPartyEdit(CharaDatum):
    is_in_party = False

    def filter(user_party_id, **kwargs):
        chara_data = CharaDatum.filter(**kwargs)

        user_party_chara_ids = [i.user_chara_id for i in UserPartyChara.objects.filter(user_party_id=user_party_id)]

        for chara_datum in chara_data:
            if chara_datum.user_chara_id in user_party_chara_ids:
                chara_datum.is_in_party = True

        return chara_data

def is_in_party(user_chara):
    return len(UserPartyChara.objects.filter(user_chara_id=user_chara.id)) > 0
