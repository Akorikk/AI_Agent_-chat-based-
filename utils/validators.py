def is_valid_amount(value):
    try:
        val = float(value)
        return val > 0
    except:
        return False


def is_valid_card_number(card):
    return card.isdigit() and len(card) in [13, 15, 16]


def is_valid_cvv(cvv):
    return cvv.isdigit() and len(cvv) in [3, 4]