from ..models import User
from . import ranking

def get_key(event_id):
    return f"game_event_{event_id}"

def update_ranking(user_id, event_id, ranking_point):
    return ranking.update(get_key(event_id), ranking_point, user_id)

def fetch_rank(user_id, event_id):
    rank = ranking.fetch_rank(get_key(event_id), user_id)
    return rank + 1

def fetch_top_ranking(event_id, top_n=100):
    ranking_ = ranking.fetch_top_ranking(get_key(event_id), top_n)
    return ranking_

class EventPointRankingInfo():
    rank = 0
    user = None
    point = 0

    def __init__(self, rank, user, point) -> None:
        self.rank = rank
        self.user = user
        self.point = point

class EventPointRanking():
    event_id = 0

    def __init__(self, event_id) -> None:
        self.event_id = event_id
        
    def fetch_top_ranking(self):
        ranking = fetch_top_ranking(self.event_id)

        ranking_user_ids = [i[0] for i in ranking]
        users = User.objects.filter(id__in=ranking_user_ids)
        user_dic = {i.id: i for i in users}

        before_point = -1
        skip_count = 0
        rank = 0
        ranking_infos = []
        for user_id_and_point in ranking:
            user_id, point = user_id_and_point
            point = int(point)
            user = user_dic[int(user_id)]

            if before_point == point:
                skip_count += 1
            else:
                rank += 1 + skip_count
                skip_count = 0

            ranking_infos.append(EventPointRankingInfo(rank, user, point))

            before_point = point

        return ranking_infos

