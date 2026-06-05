"""
Simple rule-based fraud scoring.
Future: integrate with ML model (scikit-learn, XGBoost).
"""
def calculate_fraud_score(transaction):
    """
    transaction: dict with keys: amount, booking_time_hour, guest_nationality, 
                 payment_method, is_new_guest
    """
    score = 0
    # High amount transactions
    if transaction.get('amount', 0) > 5000:
        score += 0.3
    # Late night bookings
    hour = transaction.get('booking_time_hour', 12)
    if hour < 6 or hour > 23:
        score += 0.2
    # New guest with high amount
    if transaction.get('is_new_guest', False) and transaction.get('amount', 0) > 3000:
        score += 0.3
    # Cash payment (less traceable)
    if transaction.get('payment_method', '') == 'cash':
        score += 0.1
    return min(score, 1.0)  # 0 to 1 scale