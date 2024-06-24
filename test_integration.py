import unittest
from app import ZawszeMilcz, ZawszeDonos, play_game, run_tournament

class TestPlayGame(unittest.TestCase):

    def test_play_game(self):
        player1 = ZawszeMilcz("Test")
        player2 = ZawszeDonos("Test")
        score1, score2 = play_game(player1, player2, rounds=10)
        self.assertEqual(score1, 100)
        self.assertEqual(score2, 0)

class TestRunTournament(unittest.TestCase):

    def test_run_tournament(self):
        players = [ZawszeMilcz("Zawsze milcz"), ZawszeDonos("Zawsze donos")]
        results, total_scores = run_tournament(players)
        self.assertIn("Zawsze milcz", results)
        self.assertIn("Zawsze donos", results)


if __name__ == '__main__':
    unittest.main()
