from core.evaluator import UNSUITED_LOOKUP, FLUSH_LOOKUP, evaluate_5card, best_of_seven
from core.card import from_str
import pytest

def test_lookup_tables():
    """Test that lookup tables were generated correctly."""
    assert len(UNSUITED_LOOKUP) == 6175
    assert len(FLUSH_LOOKUP) == 1287
    # Total unique 5-card hands in poker = 7,462
    assert len(FLUSH_LOOKUP) + len(UNSUITED_LOOKUP) == 7462

@pytest.mark.parametrize(
    "hand_strs, expected_score",
    [
        (["Ah", "Kh", "Qh", "Jh", "Th"], 1),     # Royal Flush
        (["Ac", "As", "Ah", "Ad", "Kc"], 11),    # Quads (Aces with King kicker)
        (["Ac", "Ad", "As", "Kd", "Ks"], 167),   # Full House (Aces full of Kings)
        (["Ah", "Kh", "Qh", "Jh", "9h"], 323),   # Regular Flush (Ace-high)
        (["Ah", "Ad", "Ks", "Kd", "Qc"], 2468),  # Two Pair (Aces and Kings)
        (["Ah", "Kh", "Qh", "Jh", "9s"], 6186),  # High Card (Ace-high)
    ],
)
def test_evaluate_5card(hand_strs, expected_score):
    """Test that 5-card evaluator maps specific hands to exact rank scores."""
    cards = [from_str(card) for card in hand_strs]
    score = evaluate_5card(*cards)
    assert score == expected_score

@pytest.mark.parametrize(
    "hand_strs, expected_score",
    [
        (["Ah", "Kh", "Qh", "Jh", "Th", "9c", "8d"], 1),     # Royal Flush
        (["Ac", "As", "Ah", "Ad", "Kc", "9c", "8d"], 11),    # Quads
        (["Ac", "Ad", "As", "Kd", "Ks", "9c", "8d"], 167),   # Full House
        (["Ah", "Kh", "Qh", "Jh", "9h", "9c", "8d"], 323),   # Regular Flush
        (["Ah", "Ad", "Ks", "Kd", "Qc", "9c", "8d"], 2468),  # Two Pair
        (["Ah", "Kh", "Qh", "Jh", "9s", "8d", "7s"], 6186),  # High Card
    ],
)
def test_best_of_seven(hand_strs, expected_score):
    """Test that 7-card evaluator correctly picks the top 5-card hand rank."""
    cards = [from_str(card) for card in hand_strs]
    assert best_of_seven(cards) == expected_score