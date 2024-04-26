from src.model.t_model import TModel

class TMonster(TModel):
    m_monster_id = 0
    level = 0
    exp = 0

    def acquireExp(self, value):
        self.exp += self.value
        if (self.exp > self.getMaxExpValue()):
            self.exp = self.getMaxExpValue()
