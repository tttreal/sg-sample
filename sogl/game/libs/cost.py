from ..models import UserPoint

class CostInfo:
    type = ""
    id = 0
    amount = 0 

    def __init__(self, type, id, amount):
        self.type = type
        self.id = id
        self.amount = amount

class Cost:
    def pay(user_id, cost_info):
        match cost_info.type:
            case "point":
                if cost_info.amount != 0:
                    user_point = UserPoint.objects.get(user_id=user_id, point_id=cost_info.id)
                    user_point.amount -= cost_info.amount
                    user_point.save()


