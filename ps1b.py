from helpers import get_user_input_as_float
import numpy as np


def get_months_to_save_for_down_payment() -> int:
    annual_salary: float = get_user_input_as_float(
        'Enter your annual salary:​ ')
    portion_saved: float = get_user_input_as_float(
        'Enter the percent of your salary to save, as a decimal: ')
    monthly_savings = (annual_salary / 12) * portion_saved

    total_cost: float = get_user_input_as_float(
        'Enter the cost of your dream home:​ ')
    portion_down_payment: float = 0.25
    down_payment = total_cost * portion_down_payment

    semi_annual_raise: float = get_user_input_as_float(
        'Enter the semi­annual raise, as a decimal:​ ')

    current_savings: float = 0
    annual_return: float = 0.04

    months_number = 0

    while current_savings < down_payment:
        current_savings += monthly_savings + \
            ((current_savings * annual_return) / 12)
        months_number += 1

        if months_number % 6 == 0:
            annual_salary += annual_salary * semi_annual_raise
            monthly_savings = (annual_salary / 12) * portion_saved

    # return int(np.rint(months_number))s
    return months_number


months = get_months_to_save_for_down_payment()
print(f'Number of months:​ {months}')
