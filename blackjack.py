import random

def card_value(number: int) -> int:
    """
    Return the value of a card given its number (0–51).

    - Cards 40–51 (all face cards + some tens) are worth 10.
    - If the last digit is 1 → Ace, value = 1 (special Ace=11 logic is handled in player()).
    - If the last digit is 2–9 → that number.
    - If the last digit is 0 (10, 20, 30) → 10.
    """
    if number >= 40:
        return 10
    last_num = number % 10
    if last_num == 1:        # Ace
        return 1
    elif 2 <= last_num <= 9: # 2–9
        return last_num
    else:                    # 10, 20, 30
        return 10


def player(cards: list[int]) -> int:
    """
    Calculate the player's score from the first two cards,
    considering the Ace (1 or 11).
    """
    c1, c2 = cards[0], cards[1]
    v1, v2 = card_value(c1), card_value(c2)
    ace1 = (c1 % 10 == 1)
    ace2 = (c2 % 10 == 1)

    base_score = v1 + v2
    if ace1 and ace2:        # two Aces
        return 12            # 11 + 1
    elif ace1 or ace2:       # one Ace
        if base_score + 10 <= 21:
            return base_score + 10
    return base_score


def dealer(cards: list[int]) -> int:
    """
    Calculate the dealer's score.
    - Dealer starts with cards[2], cards[3].
    - Dealer must hit until score >= 17.
    - Aces are always counted as 1.
    - If dealer busts, return -1.
    """
    score = card_value(cards[2]) + card_value(cards[3])
    next_card_index = 4
    while score < 17 and next_card_index < len(cards):
        score += card_value(cards[next_card_index])
        next_card_index += 1
    return score if score <= 21 else -1


# === Simulation ===
num_games = 100000
win_count = push_count = lose_count = 0
current_streak = longest_streak = 0
score_count = {s: 0 for s in range(4, 22)}  # frequency of player scores

for _ in range(num_games):
    cards = list(range(52))
    random.shuffle(cards)

    p = player(cards)
    d = dealer(cards)
    score_count[p] += 1

    if d == -1:  # dealer busts
        if p <= 21:
            win_count += 1
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            lose_count += 1
            current_streak = 0
    elif p > 21:
        lose_count += 1
        current_streak = 0
    elif p > d:
        win_count += 1
        current_streak += 1
        longest_streak = max(longest_streak, current_streak)
    elif p == d:
        push_count += 1
        # streak does not change
    else:
        lose_count += 1
        current_streak = 0

win_prob = win_count / num_games
push_prob = push_count / num_games

print(f"Probability player wins: {win_prob:.4f}")
print(f"Probability of push:    {push_prob:.4f}")
print(f"Longest winning streak: {longest_streak} games")
print("Score distribution (player 2-card total):")
print(score_count)
