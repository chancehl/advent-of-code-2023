import os
import functools

from typing import List, Dict
from enum import Enum

original_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
modified_cards = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


class Hand:
    cards: List[str]
    bid: int
    type: HandType

    def __init__(self, **kwargs) -> None:
        self.cards = kwargs.get("cards")
        self.bid = kwargs.get("bid")
        self.type = kwargs.get("type")

    def __str__(self) -> str:
        return f"{self.cards} (bid: ${self.bid}, type: ${self.type})"


def read_input() -> List[str]:
    file_loc = os.path.join(os.path.dirname(__file__), "./input-b.txt")

    with open(file_loc) as f:
        lines = [line.strip() for line in f]

        return lines


def count_cards(hand: str) -> Dict:
    cards = {}

    for card in hand:
        if card in cards:
            cards[card] += 1
        else:
            cards[card] = 1

    return cards


def compare_hands_modified_rules(a: Hand, b: Hand) -> int:
    # if they're not equal hand types return the greater hand
    if a.type.value != b.type.value:
        if a.type.value > b.type.value:
            return 1
        else:
            return -1

    # if they are equal hand types then start doing card comparisons
    for card_a, card_b in zip(a.cards, b.cards):
        card_a_index = modified_cards.index(card_a)
        card_b_index = modified_cards.index(card_b)

        if card_a_index != card_b_index:
            if card_a_index > card_b_index:
                return 1
            else:
                return -1


def compare_hands(a: Hand, b: Hand) -> int:
    # if they're not equal hand types return the greater hand
    if a.type.value != b.type.value:
        if a.type.value > b.type.value:
            return 1
        else:
            return -1

    # if they are equal hand types then start doing card comparisons
    for card_a, card_b in zip(a.cards, b.cards):
        card_a_index = original_cards.index(card_a)
        card_b_index = original_cards.index(card_b)

        if card_a_index != card_b_index:
            if card_a_index > card_b_index:
                return 1
            else:
                return -1


def determine_hand_type(hand: str) -> HandType:
    cards = count_cards(hand)

    counts = cards.values()

    if 5 in counts:
        return HandType.FIVE_OF_A_KIND
    elif 4 in counts:
        return HandType.FOUR_OF_A_KIND
    elif 3 in counts and 2 in counts:
        return HandType.FULL_HOUSE
    elif 3 in counts and 2 not in counts:
        return HandType.THREE_OF_A_KIND
    elif 2 in set([list(cards.values()).count(n) for n in counts]):
        return HandType.TWO_PAIR
    elif 2 in counts:
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def determine_modified_hand_type(hand: str) -> HandType:
    # if there are no jokers then just use the original rules
    if "J" not in hand:
        return determine_hand_type(hand)

    cards = count_cards(hand)
    counts = cards.values()
    wildcards = cards["J"]

    if wildcards == 5:
        return HandType.FIVE_OF_A_KIND

    return HandType.HIGH_CARD


def parse_hands(input: List[str], modified_rules=False) -> List[Hand]:
    hands = []

    for line in input:
        parts = line.split(" ")

        hand = parts[0]
        bid = int(parts[1])
        type = (
            determine_hand_type(hand)
            if not modified_rules
            else determine_modified_hand_type(hand)
        )

        hands.append(Hand(cards=list(hand), bid=bid, type=type))

    return hands


def part_one(input: List[str]) -> int:
    hands = parse_hands(input)

    total_winnings = 0

    for index, hand in enumerate(
        sorted(hands, key=functools.cmp_to_key(compare_hands))
    ):
        total_winnings += hand.bid * (index + 1)

    return total_winnings


def part_two(input: List[str]) -> int:
    hands = parse_hands(input, modified_rules=True)

    total_winnings = 0

    for index, hand in enumerate(
        sorted(hands, key=functools.cmp_to_key(compare_hands_modified_rules))
    ):
        print(hand)
        total_winnings += hand.bid * (index + 1)

    return total_winnings


if __name__ == "__main__":
    score_one = part_one(read_input())
    score_two = part_two(read_input())

    print(score_one, score_two)
