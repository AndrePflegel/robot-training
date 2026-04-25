def format_digit_result(digit, confidence, min_confidence=0.70):
    if confidence < min_confidence:
        return "Unsicher"

    return f"Zahl: {digit} ({confidence:.2f})"
