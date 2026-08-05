from core.card import from_str, RANKS, SUITS, new_deck

def parse_range(range_str: str) -> list[tuple[int, int]]: 

    # TODO: track known cards; if AhQd, Ah and Qd should not be used in ranges; 
    # if 4 known of card already then don't add 5th to ranges (AA, AsAh, QQ+ != AA)
    # TODO: allow for pocker pair neither of unknown suit (AJ+ or AJ)
    
    if not range_str:
        return full_range()

    pockets = range_str.split()
    combos = []
    for pocket in pockets:
        combos.append(pocket_range(pocket))

    return combos  

def pocket_range(pocket_str: str) -> list[tuple[int, int]]:
    is_plus = pocket_str.endswith("+")
    clean = pocket_str.rstrip("+")

    # Specific 2-card pairs: e.g., AhKd
    if len(clean) == 4:
        c1 = from_str(clean[:2])
        c2 = from_str(clean[2:])

        return [(min(c1, c2), max(c1, c2))] # Higher card first

    # Pocket pairs: e.g., JJ or JJ+
    if len(clean) == 2 and clean[0] == clean[1]:
        r_char = clean[0].upper()
        r_idx = RANKS.index(r_char)

        # All higher pairs (e.g., QQ+ -> QQ, KK, AA) if "+"
        target_ranks = range(r_idx, 13) if is_plus else [r_idx]

        combos = []
        for r in target_ranks:
            rank_char = RANKS[r]

            suits = list(SUITS)
            for i in range(len(suits)):
                for j in range(i+1, len(suits)):
                    c1 = from_str(f"{rank_char}{suits[i]}")
                    c2 = from_str(f"{rank_char}{suits[j]}")
                    combos.append((c1, c2))

        return combos

    # Suited or offsuited hand: e.g., "AQs", "AQs+", "AJo", "AJo+"
    if len(clean) == 3:
        r1_char, r2_char, type_char = clean[0].upper(), clean[1].upper(), clean[2].lower()
        r1_idx = RANKS.index(r1_char)
        r2_idx = RANKS.index(r2_char)

        # High card must be first: "KA" -> "AK"
        if r1_idx < r2_idx:
            r1_idx, r2_idx = r2_idx, r1_idx

        # All higher second cards (e.g., AJs+ -> AJs, AQs, AKs) if "+""
        r2_target_range = range(r2_idx, r1_idx) if is_plus else [r2_idx]

        combos = []
        for r2 in r2_target_range:
            r1_c = RANKS[r1_idx]
            r2_c = RANKS[r2]

            if type_char == 's':
                for s in SUITS:
                    c1 = from_str(f"{r1_c}{s}")
                    c2 = from_str(f"{r2_c}{s}")
                    combos.append((c1, c2))

            elif type_char == 'o':
                suits = list(SUITS)
                for i in range(len(suits)):
                    for j in range(i+1, len(suits)):
                        c1 = from_str(f"{r1_c}{suits[i]}")
                        c2 = from_str(f"{r2_c}{suits[j]}")
                        combos.append((c1, c2))
        return combos

def full_range() -> list[tuple[int, int]]:
    deck = new_deck()
    combos = []
    for i in range(len(deck)):
        for j in range(i+1, len(deck)):
            # New deck already returns a list of integers so dont need to call from_str
            c1 = deck[i]
            c2 = deck[j]
            combos.append((min(c1, c2), max(c1, c2)))

    return combos