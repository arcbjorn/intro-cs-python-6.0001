from helpers import get_user_input_as_float

total_cost: float = 1000000
portion_down_payment: float = 0.25  # 25%
down_payment: float = total_cost * portion_down_payment
semi_annual_raise: float = .07
annual_return: float = 0.04

starting_annual_salary = get_user_input_as_float(
    'Enter your starting annual salary: ')

one_hundred_dollars = 100
bisection_steps: int = 0
is_three_years_possible = True
max_integer: int = 10000
min_integer: int = 0
best_integer: int = max_integer

while True:
    bisection_steps += 1
    annual_salary: float = starting_annual_salary
    best_portion_saved: float = best_integer / 10000
    monthly_savings: float = (annual_salary / 12) * best_portion_saved

    current_savings: float = 0.0
    number_of_months: int = 0
    while number_of_months <= 36:
        current_savings += monthly_savings + \
            ((current_savings * annual_return) / 12)
        number_of_months += 1

        if number_of_months % 6 == 0:
            annual_salary += annual_salary * semi_annual_raise
            monthly_savings = (annual_salary / 12) * best_portion_saved

    if abs(current_savings - down_payment) <= one_hundred_dollars:
        break

    if current_savings > down_payment:
        max_integer = best_integer
    else:
        min_integer = best_integer

    if min_integer >= max_integer:
        is_three_years_possible = False
        break

    best_integer = (
        max_integer + min_integer) // 2


if is_three_years_possible:
    print(f'Best savings rate: {best_portion_saved}')
    print(f'Steps in bisection search: {bisection_steps}')
else:
    print('It is not possible to pay the down payment in three years.')
