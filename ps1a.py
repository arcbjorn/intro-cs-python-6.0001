from helpers import get_user_input_as_float
import numpy as np


def get_months_to_save_for_down_payment() -> int:
    total_cost: float = get_user_input_as_float(
        'Enter the cost of your dream home:​ ')
    portion_down_payment: float = 0.25
    portion_down_payment_in_cash = total_cost * portion_down_payment

    current_savings: float = 0
    annual_return: float = 0.04
    portion_saved: float = get_user_input_as_float(
        'Enter the percent of your salary to save, as a decimal: ')

    annual_salary: float = get_user_input_as_float(
        'Enter your annual salary:​ ')
    monthly_salary: float = annual_salary / 12

    months_number = 0

    while current_savings < portion_down_payment_in_cash:
        current_savings += monthly_salary * portion_saved
        if months_number > 0:
            current_savings += current_savings * (annual_return / 12)
        months_number += 1

    # return int(np.rint(months_number))
    return months_number


months = get_months_to_save_for_down_payment()
print(f'Number of months:​ {months}')
