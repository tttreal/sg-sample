class MonsterMerger:
    def __init__(self):
        pass

    def calcExpValue(self, t_monster_material):
        return t_monster_material.exp  # TODO 本当は計算式は複雑なはず

    def merge(self, t_monster_base, t_monster_material):
        get_exp_value = self.calcExpValue(t_monster_material)
        t_monster_base.acquireExp(get_exp_value)
        

