import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'R B W Y'.split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits 
                                        for rank in self.ranks]

    # 调用len(self)
    def __len__(self):
        return len(self._cards)

    # 调用self[position]
    def __getitem__(self, position):
        return self._cards[position]

suit_values = dict(R = 3, B = 2, W = 1, Y = 0)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

pass