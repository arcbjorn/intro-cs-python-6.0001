import numpy
from helpers import isInt

x = 0
y = 0

def isInt(test):
  try:
    int(test)
    return True
  except ValueError:
    return False

def get_x_value():
  x = input('Enter number x: ')
  if (isInt(x)):
    return int(x)
  else:
    print('Please, enter number x:')
    return get_x_value()
  
def get_y_value():
  y = input('Enter number y: ')
  if (isInt(y)):
    return int(y)
  else:
    print('Please, enter number y:')
    return get_y_value()

x = get_x_value()
y = get_y_value()

print(f'X**y = {x**y}')
print(f'log(x) = {numpy.log2(x)}')
