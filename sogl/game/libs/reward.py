from ..models import *
from .chara import *
from .point import *

class RewardContent:
    type = ""
    id = 0
    amount = 0
    image_url = ""

    # 配列や辞書データ(jsonで表現可能な型)のデータを、RewardContentの型に変換する
    def from_json_data(rewards, amount:int):
        reward_contents = []

        for reward in rewards:
            match reward["type"]:
                case "chara":
                    chara = RewardChara()
                    chara.type = reward["type"]
                    chara.id = reward["id"]
                    reward_amount = reward["amount"] if "amount" in reward else 1
                    chara.amount = reward_amount * amount
                    chara.image_url = f"game/chara/{chara.id}.jpg"

                    reward_contents.append(chara)
                    
                case "point":
                    point = RewardPoint()
                    point.type = reward["type"]
                    point.id = reward["id"]
                    reward_amount = reward["amount"] if "amount" in reward else 1
                    point.amount = reward_amount * amount
                    point.image_url = f"game/point/{point.id}.jpg"

                    reward_contents.append(point)

        return reward_contents

class RewardChara(RewardContent):
    level = 1

class RewardPoint:
    pass

def give_reward(user_id, reward, amount=1):
    reward_messages = []

    reward_contents = RewardContent.from_json_data(reward, amount)
    for reward in reward_contents:
        match reward.type:
            case "chara":
                for _ in range(0, reward.amount):
                    user_chara = UserChara()
                    user_chara.user_id = user_id
                    user_chara.chara_id = reward.id
                    user_chara.level = reward.level
                    user_chara.save()

                    chara = Chara.objects.get(id=reward.id)
                    reward_messages.append(f"キャラを獲得しました: {chara.name}(レベル{user_chara.level})")
                
            case "point":
                point_id = reward.id
                user_point = UserPoint.objects.get_or_none(user_id=user_id, point_id=point_id)
                if user_point == None:
                    user_point = UserPoint()
                    user_point.user_id = user_id
                    user_point.point_id = reward.id
                    user_point.amount = reward.amount
                else:
                    user_point.amount += reward.amount
                user_point.save()

                point = Point.objects.get(id=reward.id)
                reward_messages.append(f"ポイントを獲得しました: {point.name} {reward.amount}")

    return reward_messages

# 複数のrewardsを1つのrewardsにまとめる
def merge_rewards_list(rewards_list):
    rewards = []

    for rewards_in_list in rewards_list:
        for reward in rewards_in_list:
            rewards.append(reward)

    return rewards
