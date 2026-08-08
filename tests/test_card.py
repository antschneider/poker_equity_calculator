import pytest
from core.card import (
    RANKS,
    SUITS,  
    from_str,
    get_rank,
    get_rank_char,
    get_suit,
    get_suit_char,
    get_prime,
    to_str, 
    new_deck,
    remaining_deck
)

def test_card_encoding_decoding():
    """Test that card encod to integers and decode back to string correctly."""
    test_cases = [
        ("Ah", "A", "h", 41, 12, 4),
        ("2c", "2", "c", 2, 0, 1),
        ("Td", "T", "d", 23, 8, 2),
        ("Ks", "K", "s", 37, 11, 8),
        ("5h", "5", "h", 7, 3, 4),
     ] 

    for card_str, expected_rank, expected_suit, expected_prime, expected_rank_idx, expected_suit_mask in test_cases:
        card_int = from_str(card_str)

        assert isinstance(card_int, int)
        assert get_rank(card_int) == expected_rank_idx
        assert get_rank_char(card_int) == expected_rank
        assert get_suit(card_int) == expected_suit_mask
        assert get_suit_char(card_int) == expected_suit
        assert get_prime(card_int) == expected_prime
        assert to_str(card_int) == card_str

def test_bitwise_isolation():
    """Verify that bits for rank, suit, and prime do not bleed into one another."""
    ace_hearts = from_str("Ah")

    expected_prime = (ace_hearts >> 16) & 0xFFFF
    expected_rank = (ace_hearts >> 12) & 0xF
    expected_suit = ace_hearts & 0xF

    assert expected_prime == 41
    assert expected_rank == 12
    assert expected_suit == 4

def test_new_deck():
    """Verify that new_deck returns 52 unique 32-bit integers"""
    test_deck = new_deck()

    assert len(test_deck) == 52
    assert len(set(test_deck)) == 52

    reconstructed_deck = [to_str(c) for c in test_deck]
    for r in RANKS:
        for s in SUITS:
            assert f"{r}{s}" in reconstructed_deck

def test_remaining_deck():
    """Verify that dead cards are properly filtered out of the deck"""
    hero_cards = [from_str("Ah"), from_str("Kh")]
    villian_cards = [from_str("Ks"), from_str("Kc")]
    board_cards = [from_str("Ac"), from_str("Qc"), from_str("Ts")]

    dead_cards = hero_cards + villian_cards + board_cards
    test_remaining = remaining_deck(dead_cards)

    assert len(test_remaining) == 45
    assert len(set(test_remaining)) == 45

    for dead in dead_cards:
        assert dead not in test_remaining