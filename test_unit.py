import unittest
from app import ZawszeMilcz, ZawszeDonos, TitForTat, Losowo, Uraza, PrzebaczajaceTitForTat,  play_round, calculate_scores

class TestStrategies(unittest.TestCase):

    def test_zawsze_milcz(self):
        player = ZawszeMilcz("Test")
        self.assertEqual(player.strategy([]), 'M')
    
    def test_zawsze_donos(self):
        player = ZawszeDonos("Test")
        self.assertEqual(player.strategy([]), 'D')

    def test_tit_for_tat(self):
        player = TitForTat("Test")
        self.assertEqual(player.strategy([]), 'M')
        self.assertEqual(player.strategy(['D']), 'D')
    
    def test_losowo(self):
        player = Losowo("Test")
        self.assertIn(player.strategy([]), ['M', 'D'])

    def test_uraza(self):
        player = Uraza("Test")
        self.assertEqual(player.strategy([]), 'M')
        self.assertEqual(player.strategy(['D']), 'D')

    def test_przebaczajace_tit_for_tat(self):
        player = PrzebaczajaceTitForTat("Test")
        self.assertEqual(player.strategy([]), 'M')
        self.assertIn(player.strategy(['D']), ['M', 'D'])

class TestPlayRound(unittest.TestCase):

    def test_play_round(self):
        player1 = ZawszeMilcz("Test")
        player2 = ZawszeDonos("Test")
        history1, history2 = play_round(player1, player2, [], [])
        self.assertEqual(history1, ['M'])
        self.assertEqual(history2, ['D'])

class TestCalculateScores(unittest.TestCase):

    def test_calculate_scores(self):
        history1 = ['M', 'D']
        history2 = ['M', 'M']
        score1, score2 = calculate_scores(history1, history2)
        self.assertEqual(score1, 3)
        self.assertEqual(score2, 13)

if __name__ == '__main__':
    unittest.main()
