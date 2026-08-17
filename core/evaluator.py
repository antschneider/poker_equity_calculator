from core.card import get_prime, get_rank, get_suit, PRIMES
from itertools import combinations

FLUSH_LOOKUP: dict[int, int] = {}
UNSUITED_LOOKUP: dict[int, int] = {}

def _init_hand_lookup() -> None:
    """Populates lookup tables for 5-card evaluation."""
    if FLUSH_LOOKUP and UNSUITED_LOOKUP:
        return  # Prevent re-initialization

    # Straight rank bitmasks (A-high down to 5-high wheel)
    straights = [
        0b1111100000000,  # A-K-Q-J-T (Royal)
        0b0111110000000,  # K-Q-J-T-9
        0b0011111000000,  # Q-J-T-9-8
        0b0001111100000,  # J-T-9-8-7
        0b0000111110000,  # T-9-8-7-6
        0b0000011111000,  # 9-8-7-6-5
        0b0000001111100,  # 8-7-6-5-4
        0b0000000111110,  # 7-6-5-4-3
        0b0000000011111,  # 6-5-4-3-2
        0b1000000001111,  # A-5-4-3-2 (Wheel straight)
    ]

    # Get all 5 card rank combinations and sort by stregth (highest ranks first)
    rank_idx_combos = list(combinations(range(13), 5))
    rank_idx_combos.sort(key=lambda c: [c[4], c[3], c[2], c[1], c[0]], reverse=True)
    current_rank = 1

    # --- HAND STRENGTH TABLES FOR FLUSH / UNSUITED HANDS ---
    # Straight Flushes (Ranks 1 to 10)
    for mask in straights:
        FLUSH_LOOKUP[mask] = current_rank
        current_rank += 1

    # Four of a Kind (Ranks 11 to 166)
    for quad_r in reversed(range(13)):
        for kicker_r in reversed(range(13)):
            if quad_r == kicker_r:
                continue
            prod = (PRIMES[quad_r] ** 4) * PRIMES[kicker_r] 
            UNSUITED_LOOKUP[prod] = current_rank
            current_rank += 1

    # Full Houses (Ranks 167 to 322)
    for trips_r in reversed(range(13)):
        for pair_r in reversed(range(13)):
            if trips_r == pair_r:
                continue
            prod = (PRIMES[trips_r] ** 3) * (PRIMES[pair_r] ** 2)
            UNSUITED_LOOKUP[prod] = current_rank
            current_rank += 1

    # Regular Flushes (Ranks 323 to 1599)
    for combo in rank_idx_combos:
        mask = sum(1 << r for r in combo)
        if mask in FLUSH_LOOKUP:
            continue
        FLUSH_LOOKUP[mask] = current_rank
        current_rank += 1

    # Straights (Unsuited) (Ranks 1600 to 1609)
    for mask in straights:
        # Product of primes for straight rank combo
        if mask == 0b1000000001111:  # Wheel (A-5-4-3-2)
            wheel_ranks = [12, 0, 1, 2, 3]
            prod = 1
            for r in wheel_ranks:
                prod *= PRIMES[r]
        else:
            prod = 1
            for r in range(13):
                if (mask >> r) & 1:
                    prod *= PRIMES[r]
        UNSUITED_LOOKUP[prod] = current_rank
        current_rank += 1
        
    # Three of a Kind (Ranks 1610 to 2467)
    for trips in reversed(range(13)):
        for k1 in reversed(range(13)):
            if k1 == trips:
                continue
            for k2 in reversed(range(k1)):
                if k2 == trips:
                    continue
                prod = (PRIMES[trips] ** 3) * PRIMES[k1] * PRIMES[k2]
                UNSUITED_LOOKUP[prod] = current_rank
                current_rank += 1

    # Two Pair (Ranks 2468 to 3325)
    for p1 in reversed(range(13)):
        for p2 in reversed(range(p1)):
            for kicker in reversed(range(13)):
                if kicker == p1 or kicker == p2:
                    continue
                prod = (PRIMES[p1] ** 2) * (PRIMES[p2] ** 2) * PRIMES[kicker]
                UNSUITED_LOOKUP[prod] = current_rank
                current_rank += 1

    # One Pair (Ranks 3326 to 6185)
    for pair_r in reversed(range(13)):
        for k1 in reversed(range(13)):
            if k1 == pair_r:
                continue
            for k2 in reversed(range(k1)):
                if k2 == pair_r:
                    continue
                for k3 in reversed(range(k2)):
                    if k3 == pair_r:
                        continue
                    prod = (PRIMES[pair_r] ** 2) * PRIMES[k1] * PRIMES[k2] * PRIMES[k3]
                    UNSUITED_LOOKUP[prod] = current_rank
                    current_rank += 1

    # High Card / Trash (Ranks 6186 to 7462)
    for combo in rank_idx_combos:
        mask = sum(1 << r for r in combo)
        if mask in straights:
            continue
        prod = 1
        for r in combo:
            prod *= PRIMES[r]
        UNSUITED_LOOKUP[prod] = current_rank
        current_rank += 1

# Initialize tables on import
_init_hand_lookup()

def evaluate_5card(c1: int, c2: int, c3: int, c4: int, c5: int) -> int:
    """Evaluates a 5-card hand using prime multiplication & lookup tables."""
    # Flush check
    suit_mask = get_suit(c1) & get_suit(c2) & get_suit(c3) & get_suit(c4) & get_suit(c5)
    
    if suit_mask > 0:
        rank_mask = (1 << get_rank(c1)) | (1 << get_rank(c2)) | \
                    (1 << get_rank(c3)) | (1 << get_rank(c4)) | \
                    (1 << get_rank(c5))
        return FLUSH_LOOKUP[rank_mask]

    prime_product = get_prime(c1) * get_prime(c2) * get_prime(c3) * \
                    get_prime(c4) * get_prime(c5)
    return UNSUITED_LOOKUP[prime_product]


def best_of_seven(cards: list[int]) -> int:
    """Evaluates a 7-card Hold'em hand by finding the best 5-card score (min score)."""
    best_score = 9999
    for combo in combinations(cards, 5):
        score = evaluate_5card(*combo)
        if score < best_score:
            best_score = score
    return best_score