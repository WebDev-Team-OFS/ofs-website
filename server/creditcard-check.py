from datetime import datetime

def luhn_check(card_number):
    # Reverse the card number and convert to a list of integers
    card_digits = [int(digit) for digit in card_number[::-1]]

    # Double every second digit from the right
    for i in range(1, len(card_digits), 2):
        card_digits[i] *= 2
        if card_digits[i] > 9:
            card_digits[i] -= 9

    # Sum all the digits
    total_sum = sum(card_digits)

    # If the total sum is divisible by 10, it's valid
    return total_sum % 10 == 0

def date_check(exp_date):
    try:
        # Parse input expiration date (MM/YY)
        exp_month, exp_year = map(int, exp_date.split("/"))

        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year % 100  # Get last two digits of the 
        
        if exp_year > current_year or (exp_year == current_year and exp_month >= current_month):
            return True
        else:
            return False
    except ValueError:
        return False

def main():
    # Input card number
    card_number = input("Enter credit card number: ").strip()

    # Validate card number (must be all digits and 16 in length)
    if len(card_number) != 16 or not card_number.isdigit():
        print("Invalid card number format! Must be 16 digits.")
        return

    # Luhn check
    if luhn_check(card_number):
        print("Valid card number!")
    else:
        print("Invalid card number!")
        return

    exp_date = input("Enter expiration date (MM/YY): ").strip()

    if date_check(exp_date):
        print("Valid expiration date!")
    else:
        print("Invalid expiration date!")

if __name__ == "__main__":
    main()
from datetime import datetime