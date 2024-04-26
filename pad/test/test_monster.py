from src.model.m_monster import MMonster
import unittest

class MonsterTest(unittest.TestCase):
    def test_init(self):
        monster = MMonster
        self.assertEqual(monster.name, 'no name')
        self.assertEqual(monster.hp, 0)

    def test_findById(self):
        # monster = MMonster()
        # monster.findById(1)
        monster = MMonster.objects.get(id=1)
        self.assertEqual(monster.id, 1)


if __name__ == '__main__':
    unittest.main()

