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
  value = input(message)
  if (isFloat(value)):
    return float(value)
  else:
    print('Please, use number!')
    return get_user_input_as_float(message)