from ..models import *
from ..libs.chara import CharaDatum

class UserPartyDatum:
    party_id = 0
    user_party_id = 0
    name = ""
    chara_data = []
    total_power = 0

    def filter(**kwargs):
        # fetch UserParty
        user_parties = UserParty.objects.filter(**kwargs)

        # fetch Party
        party_ids = user_parties.values_list('party_id', flat=True)
        parties = Party.objects.filter(id__in=party_ids)
        party_dic = {party.id: party for party in parties}

        # fetch CharaData
        user_party_ids = user_parties.values_list('id', flat=True)
        user_party_charas = UserPartyChara.objects.filter(user_party_id__in=user_party_ids)
        user_chara_ids = user_party_charas.values_list('user_chara_id', flat=True)
        chara_data = CharaDatum.filter(id__in=user_chara_ids)
        chara_datum_dic = {chara_datum.user_chara_id: chara_datum for chara_datum in chara_data}

        chara_data_dic = {}
        for user_party_chara in user_party_charas:
            key = user_party_chara.user_party_id
            if key not in chara_data_dic:
                chara_data_dic[key] = []
            chara_data_dic[key].append(chara_datum_dic[user_party_chara.user_chara_id])

        user_party_data = []
        for user_party in user_parties:
            user_party_datum = UserPartyDatum()
            user_party_datum.party_id = user_party.party_id
            user_party_datum.user_party_id = user_party.id
            user_party_datum.name = party_dic[user_party.party_id].name
            if user_party.id in chara_data_dic:
                user_party_datum.chara_data = chara_data_dic[user_party.id]
            else:
                user_party_datum.chara_data = []
            user_party_datum.total_power = sum([chara_datum.power for chara_datum in user_party_datum.chara_data])
            user_party_data.append(user_party_datum)

        return user_party_data

    def filter_for_party_list(**kwargs):
        parties = Party.objects.all()
        user_party_data = UserPartyDatum.filter(**kwargs)
        user_party_dic = {user_party_datum.party_id: user_party_datum for user_party_datum in user_party_data}

        user_party_data = []
        for party in parties:
            if party.id in user_party_dic:
                user_party_data.append(user_party_dic[party.id])
            else:
                user_party_datum = UserPartyDatum()
                user_party_datum.name = party.name
                user_party_datum.party_id = party.id
                user_party_datum.chara_data = []
                user_party_data.append(user_party_datum)

        return user_party_data

    def fetch_current_user_party_datum(user):
        user_party_data = UserPartyDatum.filter(user_id=user.id, party_id=user.select_party_id)
        if user_party_data:
            return user_party_data[0]
        else:
            user_party_datum = UserPartyDatum()
            user_party_datum.user_party_id = user.select_party_id
            return user_party_datum
