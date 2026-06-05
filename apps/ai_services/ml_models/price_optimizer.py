"""
Dynamic room pricing based on demand and competitor rates.
"""
def calculate_optimal_price(base_rate, current_occupancy, max_rooms, competitor_price=None):
    """
    base_rate: standard room price
    current_occupancy: number of occupied rooms
    max_rooms: total rooms
    competitor_price: optional avg competitor price
    """
    occupancy_rate = current_occupancy / max_rooms if max_rooms > 0 else 0
    # Higher occupancy -> increase price
    demand_factor = 1 + (occupancy_rate - 0.6) * 0.5  # starts increasing after 60% occupancy
    if demand_factor < 0.7:
        demand_factor = 0.7  # floor
    if demand_factor > 1.5:
        demand_factor = 1.5  # ceiling
    price = base_rate * demand_factor
    # If competitor price is significantly lower, cap increase
    if competitor_price and price > competitor_price * 1.2:
        price = competitor_price * 1.2
    return round(price, 2)