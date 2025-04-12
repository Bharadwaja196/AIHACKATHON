def is_valid_feedback(score):
    return score in [-1, 0, 1]

def is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""
