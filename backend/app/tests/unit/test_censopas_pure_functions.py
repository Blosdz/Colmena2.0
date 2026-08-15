import pytest

from app.analytics.censopas.classification import classify_collective_result, classify_construct_score
from app.analytics.censopas.scoring import (
    aggregate_construct_score,
    apply_direction,
    derive_item_values,
    score_item,
)


def test_score_item_maps_raw_code() -> None:
    assert score_item("1", {"1": 0, "2": 50, "3": 100}) == 0
    assert score_item("3", {"1": 0, "2": 50, "3": 100}) == 100


def test_score_item_missing_code_returns_none() -> None:
    assert score_item(None, {"1": 0}) is None
    assert score_item("9", {"1": 0}) is None


def test_apply_direction_reverses_score() -> None:
    assert apply_direction(80, "REVERSE") == 20
    assert apply_direction(80, "DIRECT") == 80
    assert apply_direction(80, None) == 80


def test_aggregate_construct_score_weighted_average() -> None:
    # dos ítems, mismo peso, uno REVERSE
    score = aggregate_construct_score([(80, 1, "DIRECT"), (80, 1, "REVERSE")])
    assert score == 50.0  # (80 + 20) / 2


def test_aggregate_construct_score_empty_returns_none() -> None:
    assert aggregate_construct_score([]) is None


def test_classify_construct_score_higher_better() -> None:
    assert classify_construct_score(10, 33, 66, "HIGHER_BETTER") == "DESFAVORABLE"
    assert classify_construct_score(50, 33, 66, "HIGHER_BETTER") == "INTERMEDIO"
    assert classify_construct_score(90, 33, 66, "HIGHER_BETTER") == "FAVORABLE"


def test_classify_construct_score_lower_better() -> None:
    assert classify_construct_score(10, 33, 66, "LOWER_BETTER") == "FAVORABLE"
    assert classify_construct_score(90, 33, 66, "LOWER_BETTER") == "DESFAVORABLE"



def test_derive_item_values_keeps_risk_and_transformed_score_separate() -> None:
    risk, score = derive_item_values("1", {"1": 1, "5": 5}, "REVERSE")
    assert risk == 5
    assert score == 100
    risk, score = derive_item_values("5", {"1": 1, "5": 5}, "DIRECT")
    assert risk == 5
    assert score == 100


def test_classification_includes_exact_cutoff_boundaries() -> None:
    assert classify_construct_score(33, 33, 66, "LOWER_BETTER") == "FAVORABLE"
    assert classify_construct_score(66, 33, 66, "LOWER_BETTER") == "INTERMEDIO"


@pytest.mark.parametrize(
    ("fav", "inter", "unfav", "expected"),
    [
        (10, 20, 70, "RIESGO_ALTO"),
        (60, 20, 20, "FACTOR_PROTECTOR"),
        (20, 60, 20, "RIESGO_MEDIO"),
        (34, 33, 33, "REVISION"),
    ],
)
def test_classify_collective_result(fav, inter, unfav, expected) -> None:
    assert classify_collective_result(fav, inter, unfav) == expected
