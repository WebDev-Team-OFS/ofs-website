from datetime import datetime
from flask import request, jsonify, Blueprint


credit_card_bp = Blueprint("credit_check", __name__)

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


@credit_card_bp.route('/api/validate-expiration', methods=['POST'])
def validate_expiration():
    data = request.get_json()
    exp_date = data.get('exp_date')

    # Validate expiration date format (MM/YY)
    if not exp_date or len(exp_date) != 5 or exp_date[2] != "/":
        return jsonify({"error": "Invalid expiration date format! Use MM/YY."}), 400

    if date_check(exp_date):
        return jsonify({"message": "Valid expiration date!"}), 200
    else:
        return jsonify({"error": "Invalid expiration date!"}), 400
    


@credit_card_bp.route('/api/validate-card', methods=['POST'])
def validate_card():
    data = request.get_json()
    card_number = data.get('card_number')

    # Validate input
    if not card_number or len(card_number) != 16 or not card_number.isdigit():
        return jsonify({"error": "Invalid card number format! Must be 16 digits."}), 400

    # Luhn check
    if luhn_check(card_number):
        return jsonify({"message": "Valid card number!"}), 200
    else:
        return jsonify({"error": "Invalid card number!"}), 400