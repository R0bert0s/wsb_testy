from flask import Flask, render_template
import random

app = Flask(__name__)


class Player:
    def __init__(self, name):
        self.name = name

    def strategy(self, opponent_history):
        raise NotImplementedError


class ZawszeMilcz(Player):
    def strategy(self, opponent_history):
        return 'M'


class ZawszeDonos(Player):
    def strategy(self, opponent_history):
        return 'D'


class TitForTat(Player):
    def strategy(self, opponent_history):
        if not opponent_history:
            return 'M'
        return opponent_history[-1]


class Losowo(Player):
    def strategy(self, opponent_history):
        return random.choice(['M', 'D'])


class Uraza(Player):
    def strategy(self, opponent_history):
        if 'D' in opponent_history:
            return 'D'
        return 'M'


class PrzebaczajaceTitForTat(Player):
    def strategy(self, opponent_history):
        if not opponent_history:
            return 'M'
        if opponent_history[-1] == 'D' and random.random() < 0.2:
            return 'M'
        return opponent_history[-1]


def play_round(player1, player2, history1, history2):
    move1 = player1.strategy(history2)
    move2 = player2.strategy(history1)
    history1.append(move1)
    history2.append(move2)
    return history1, history2


def calculate_scores(history1, history2):
    score1, score2 = 0, 0
    for move1, move2 in zip(history1, history2):
        if move1 == 'M' and move2 == 'M':
            score1 += 3
            score2 += 3
        elif move1 == 'M' and move2 == 'D':
            score1 += 10
            score2 += 0
        elif move1 == 'D' and move2 == 'M':
            score1 += 0
            score2 += 10
        elif move1 == 'D' and move2 == 'D':
            score1 += 7
            score2 += 7
    return score1, score2


def play_game(player1, player2, rounds=1000):
    history1, history2 = [], []
    for _ in range(rounds):
        history1, history2 = play_round(player1, player2, history1, history2)
    score1, score2 = calculate_scores(history1, history2)
    return score1, score2


def run_tournament(players):
    results = {player.name: {opponent.name: "0 - 0" for opponent in players} for player in players}
    total_scores = {player.name: 0 for player in players}
    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            if i != j:
                score1, score2 = play_game(player1, player2)
                results[player1.name][player2.name] = f"{score1} - {score2}"
                results[player2.name][player1.name] = f"{score2} - {score1}"
                total_scores[player1.name] += score1//2
                total_scores[player2.name] += score2//2
            else:
                results[player1.name][player2.name] = "X"
    return results, total_scores


@app.route('/')
def index():
    players = [
        ZawszeMilcz("Zawsze milcz"),
        ZawszeDonos("Zawsze donos"),
        TitForTat("Tit For Tat"),
        Losowo("Losowo"),
        Uraza("Uraza"),
        PrzebaczajaceTitForTat("PrzebaczajaceTitForTat")
    ]
    results, total_scores = run_tournament(players)
    return render_template('index.html', results=results, total_scores=total_scores)


if __name__ == '__main__':
    app.run(debug=True)