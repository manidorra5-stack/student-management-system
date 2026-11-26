from app.models.grade_model import calculate_final_grade


def test_calculate_final_grade_standard():
    """40% of 15 (6.0) + 60% of 10 (6.0) = 12.0."""
    assert calculate_final_grade(15, 10) == 12.0


def test_calculate_final_grade_rounding():
    """40% of 17.5 (7.0) + 60% of 18.0 (10.8) = 17.8."""
    assert calculate_final_grade(17.5, 18.0) == 17.8


def test_calculate_final_grade_clamping():
    """Values outside [0, 20] must be clamped safely."""
    assert calculate_final_grade(25, 30) == 20.0
    assert calculate_final_grade(-5, -10) == 0.0