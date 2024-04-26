from src.model.m_model import MModel

class MMonster(MModel):
    name = 'no name'
    hp = 0
    exp = 0
    m_monster_exp_table_no = 0

    def __init__(self, id = 0, name = '', hp = 0, exp = 0, m_monster_exp_table_no = 0):
        self.id = id
        self.name = name
        self.hp = hp
        self.exp = exp
        self.m_monster_exp_table_no = m_monster_exp_table_no

    def calcHp(self, hp):
        return hp * 100 # TODO tmp

    def getMaxExpValue(self):
        return 1000 # TODO tmp



