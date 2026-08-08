RANKS = "23456789TJQKA"
SUITS = "cdhs"
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

def from_str(card_str: str) -> int:
    """Converts card string (e.g., 'Ah') -> 32-bit card integer"""
    rank_char, suit_char = card_str[0], card_str[1]

    r = RANKS.index(rank_char)
    s = 1 << SUITS.index(suit_char)
    prime = PRIMES[r]
    return (prime << 16) | (r << 12) | s

def get_rank(card: int) -> int:
    """Extracts rank (0-12) from integer."""
    return (card >> 12) & 0xF

def get_rank_char(card: int) -> str:
    """Extracts rank character from integer."""
    return RANKS[(card >> 12) & 0xF]

def get_suit(card: int) -> int:
    """Extracts suit mask (1, 2, 4, 8) from integer."""
    return card & 0xF

def get_suit_char(card: int) -> str:
    """Extracts suit character from integer."""
    return SUITS[(card & 0xF).bit_length() - 1]

def get_prime(card: int) -> int:
    """Extracts prime factor from integer."""
    return (card >> 16) & 0xFFFF

def to_str(card: int) -> str:
    """Converts 32-bit card integer -> card string (e.g., 'Ah')"""
    return get_rank_char(card) + get_suit_char(card)

def new_deck() -> list[int]:
    """Returns new 52-card deck as integers."""
    return [from_str(f"{r}{s}") for r in RANKS for s in SUITS]

def remaining_deck(dead_cards: list[int]) -> list[int]:
    """Returns 52-card deck with all dead cards removed."""
    return [card for card in new_deck() if card not in dead_cards]