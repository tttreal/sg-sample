from ..models import Point
from ..models import UserPoint

class PointDatum:
    point_id = 0
    user_id = 0
    name = ""
    amount = 0
    created_at = None
    updated_at = None

    def filter(**kwargs):
        user_points = UserPoint.objects.filter(**kwargs)

        user_point_point_ids = list(user_points.values_list('point_id', flat=True))
        points = Point.objects.filter(id__in=user_point_point_ids)
        # idをキーとした辞書を作成
        point_dict = {point.id: point for point in points}

        point_data = []
        for user_point in user_points:
            point_datum = PointDatum()
            point = point_dict[user_point.point_id]
            point_datum.point_id = point.id
            point_datum.user_id = user_point.id
            point_datum.name = point.name
            point_datum.amount = user_point.amount
            point_datum.created_at = user_point.created_at
            point_datum.updated_at = user_point.updated_at

            point_data.append(point_datum)

        return point_data
