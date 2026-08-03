RANKS = "23456789TJQKA"
SUITS = "cdhs"
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41] 
SUIT_MASKS = {'c': 1, 'd': 2, 'h': 4, 's': 8}

def from_str(card_str: str) -> int:
    """Converts card string (e.g., 'Ah') -> 32-bit card integer"""
    if len(card_str) != 2:
        raise ValueError(f'Invalid card format: "{card_str}". Expected exactly two characters (e.g., "Ah").')
    
    rank_char, suit_char = card_str[0].upper(), card_str[1].lower()

    if rank_char not in RANKS:
        raise ValueError(f"Invalid card rank: '{rank_char}'. Must be one of {RANKS}.")
    if suit_char not in SUITS:
        raise ValueError(f"Invalid card suit: '{suit_char}'. Must be one of {SUITS}.")

    r = RANKS.index(rank_char)
    s = SUIT_MASKS[suit_char]
    prime = PRIMES[r]
    return (prime << 16) | (r << 12) | (s << 8)

def get_rank_idx(card: int) -> int:
    """Extracts rank (0-12) from integer."""
    return (card >> 12) & 0xF

def get_rank_char(card: int) -> str:
    """Extracts rank character from integer."""
    return RANKS[(card >> 12) & 0xF]

def get_suit_mask(card: int) -> int:
    """Extracts suit mask (1, 2, 4, 8) from integer."""
    return (card >> 8) & 0xF

def get_suit_char(card: int) -> str:
    """Extracts suit character from integer."""
    return SUITS[((card >> 8) & 0xF).bit_length() - 1]

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