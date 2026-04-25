from collections import Counter


def get_stable_digit(digits):
    if not digits:
        return None

    counter = Counter(digits)
    most_common, count = counter.most_common(1)[0]

    return most_common
