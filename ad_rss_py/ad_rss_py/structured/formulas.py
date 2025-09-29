from ..core.types import RelativeConstellation
from ..physics.types import Distance, Speed, Acceleration

def calculate_safe_longitudinal_distance(constellation: RelativeConstellation) -> Distance:
    """
    Calculates the safe longitudinal distance based on the RSS formula.
    This is a simplified version for the 'same direction' scenario.
    """
    ego_state = constellation.ego_state
    other_state = constellation.other_state

    # Assuming ego is the rear vehicle and the other is the front vehicle
    # A more robust implementation would check the relative position
    v_rear = ego_state.structured_object_state.velocity
    v_front = other_state.structured_object_state.velocity

    t_response = ego_state.dynamics.response_time
    a_max = ego_state.dynamics.alpha_lon_accel_max
    b_min_correct = ego_state.dynamics.alpha_lon_brake_min # Assuming this is b_min_correct from C++ code

    # Assuming other vehicle's brake_min is the same as ego's for simplicity
    b_max_front = other_state.dynamics.alpha_lon_brake_max

    # RSS Formula for safe distance
    # d_min = v_r*t_r + 0.5*a_max*t_r^2 + (v_r + t_r*a_max)^2 / (2*b_min) - v_f^2 / (2*b_max)

    term1 = v_rear * t_response
    term2 = 0.5 * a_max * (t_response ** 2)

    numerator_term3 = (v_rear + t_response * a_max) ** 2
    denominator_term3 = 2 * b_min_correct
    term3 = numerator_term3 / denominator_term3 if denominator_term3 > 0 else 0.0

    numerator_term4 = v_front ** 2
    denominator_term4 = 2 * b_max_front
    term4 = numerator_term4 / denominator_term4 if denominator_term4 > 0 else 0.0

    safe_dist = term1 + term2 + term3 - term4

    return max(0.0, safe_dist)