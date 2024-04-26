from src.monster_merger import MonsterMerger
from src.model.t_monster import TMonster

import unittest

class MergeTest(unittest.TestCase):
    def test_init(self):
        monster_merger = MonsterMerger()

    def test_merge(self):
        monster1 = TMonster()
        monster2 = TMonster()

        monster1.id = 1
        monster1.level = 1
        monster2.id = 1
        monster2.level = 2

        monster_merger = MonsterMerger()
        monster_merger.merge(monster1, monster2)

if __name__ == '__main__':
    unittest.main()

