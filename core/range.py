from core.card import from_str, new_deck, get_rank, get_suit, RANKS, SUITS
import numpy as np
import re

# Pre-compiled range token patterns
patterns = re.compile(
    r"^(?:" 
    r"(?P<exact>([2-9TJQKA][cdhs])(?!\2)[2-9TJQKA][cdhs])"  # Exact holecards (e.g., AhKd)
    r"|(?P<pair>([2-9TJQKA])\4\+?)"                         # Poket pairs (e.g., AA, QQ+)
    r"|(?P<nonpair>([2-9TJQKA])(?!\6)([2-9TJQKA])[so]?\+?)" # Suited/Offsuited/Open (e.g., AJs+, AJo)
    r")$",                                           
    re.IGNORECASE
)

def parse_range(range_str: str) -> list[list[tuple[int, int]]]:
    """
    Parses a poker range string into token-grouped lists of 32-bit card integer pairs.
    
    Example Input:  "QQ+ AJs"
    Example Output: [[(Qh, Qs), ...], [(Ah, Jh), ...]]
    """
    # Return all 1,326 combos wrapped in a single group for 100% ranges
    if not range_str or range_str.strip() == "100%":
        return deck_range()

    combos = []
    tokens = range_str.split()
    for token in tokens:
        token_combos = []
        match = patterns.match(token)

        if not match:
            raise ValueError(f"Inproper card/range format: {token}."
                             "Proper format: AhKd, QQ(+), AJ(s/o)(+)")
        
        is_plus = token.endswith("+")
        clean = token.rstrip("+")

        # --- 1. EXACT HANDS (e.g., "AhKd") ---
        if match.lastgroup == "exact":
            r1_idx = RANKS.index(clean[0].upper())
            r2_idx = RANKS.index(clean[2].upper())
            s1, s2 = clean[1].lower(), clean[3].lower()

            if r1_idx < r2_idx:
                r1_idx, r2_idx = r2_idx, r1_idx
                s1, s2 = s2, s1

            c1 = from_str(f"{RANKS[r1_idx]}{s1}")
            c2 = from_str(f"{RANKS[r2_idx]}{s2}")

            token_combos.append((c1, c2))

        # --- 2. POCKET PAIRS (e.g., "QQ" or "TT+") ---
        elif match.lastgroup == "pair":
            r_idx = RANKS.index(clean[0].upper())
            # "TT+" iterates from Ten (idx 8) up to Ace (idx 12)
            r_target = range(r_idx, 13) if is_plus else [r_idx]
        
            for r in r_target:
                r_char = RANKS[r]
                # Generate all 6 suit combinations for the pair
                for i in range(4):
                    for j in range(i + 1, 4):
                        c1 = from_str(f"{r_char}{SUITS[i]}")
                        c2 = from_str(f"{r_char}{SUITS[j]}")
                        token_combos.append((c1, c2))

        # --- 2. POCKET PAIRS (e.g., "QQ" or "TT+") ---
        elif match.lastgroup == "nonpair":
            r1_idx = RANKS.index(clean[0].upper())
            r2_idx = RANKS.index(clean[1].upper())

            # Ensure r1_idx is always the higher-ranking card (e.g., A > J)
            if r1_idx < r2_idx:
                r1_idx, r2_idx = r2_idx, r1_idx

            # "AJs+" steps r2 from J up to K (r1 - 1)
            r2_target = range(r2_idx, r1_idx) if is_plus else [r2_idx]

            if len(clean) == 3:
                type_char = clean[2].lower()
                for r2 in r2_target:
                    r1_c, r2_c = RANKS[r1_idx], RANKS[r2]

                    if type_char == "s":    # Suited hands (4 combos per rank pair)
                        for s in SUITS:
                            c1 = from_str(f"{r1_c}{s}")
                            c2 = from_str(f"{r2_c}{s}")
                            token_combos.append((c1, c2))

                    elif type_char == "o":  # Offsuit hands (12 combos per rank pair)
                        for s1 in SUITS:
                            for s2 in SUITS:
                                if s1 == s2:
                                    continue
                                c1 = from_str(f"{r1_c}{s1}")
                                c2 = from_str(f"{r2_c}{s2}")
                                token_combos.append((c1, c2))   
            else:   # Open rank pair without 's' or 'o' specified (e.g., "AJ" = 16 combos)
                for r2 in r2_target:
                    r1_c, r2_c = RANKS[r1_idx], RANKS[r2_idx]
                    for s1 in SUITS:
                        for s2 in SUITS:
                            c1 = from_str(f"{r1_c}{s1}")
                            c2 = from_str(f"{r2_c}{s2}")
                            token_combos.append((c1, c2))
        combos.append(token_combos)
    return combos

def range_matrix(combos: list[list[tuple[int, int]]] | list[tuple[int, int]]) -> np.ndarray:
    """
    Converts 32-bit card integer pairs into a 13x13 preflop range matrix (values 0.0 to 1.0).
    
    Matrix Layout:
    - Diagonal (row == col): Pocket pairs (weight = count / 6.0)
    - Upper Triangle (row > col): Suited hands (weight = count / 4.0)
    - Lower Triangle (row < col): Offsuit hands (weight = count / 12.0)
    """
    matrix = np.zeros((13, 13), dtype=np.float32)
    if not combos:
        return matrix
    
    # Flatten nested sublists if caller passes raw result from parse_range
    flat_combos = []
    if isinstance(combos[0], list):
        for sublist in combos:
            flat_combos.extend(sublist)
    else:
        flat_combos = combos

    for c1, c2 in flat_combos:
        r1_idx, s1 = get_rank(c1), get_suit(c1)
        r2_idx, s2 = get_rank(c2), get_suit(c2)

        if r1_idx < r2_idx:
            r1_idx, r2_idx = r2_idx, r1_idx
            s1, s2 = s2, s1

        if r1_idx == r2_idx:
            # Pocket pair cell (Diagonal)
            matrix[r1_idx, r1_idx] += (1.0 / 6.0)
        elif s1 == s2:
            # Suited hand cell (Upper triangle: row > col)
            matrix[r1_idx, r2_idx] += (1.0 / 4.0)
        else:
            # Offsuit hand cell (Lower triangle: row < col)
            matrix[r2_idx, r1_idx] += (1.0 / 12.0)

    # Clip at 1.0 in case of duplicate inputs
    return np.clip(matrix, 0.0, 1.0)

def deck_range() -> list[tuple[int, int]]:
    """Generates all 1,326 possible starting hand card pairs."""
    deck = new_deck()
    combos = []
    for i in range(len(deck)):
        for j in range(i+1, len(deck)):
            c1 = deck[i]
            c2 = deck[j]
            combos.append((min(c1, c2), max(c1, c2)))
    return combos