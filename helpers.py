# for ps0
def isInt(test):
    try:
        int(test)
        return True
    except ValueError:
        return False


def isFloat(test):
    try:
        float(test)
        return True
    except ValueError:
        return False


# for ps1


def get_user_input_as_float(message: str) -> float:
    try:
        value = input(message)
        return float(value)
    except ValueError:
        print('Please, use number!')
        return get_user_input_as_float(message)


# for ps3


def get_user_input_as_int(message: str) -> int:
    try:
        value = input(message)
        return int(value)
    except ValueError:
        print('Please, use number! Could be decimal')
        return get_user_input_as_int(message)
