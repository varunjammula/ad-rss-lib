from ..state.types import RssStateSnapshot, ProperResponse, LongitudinalResponse, LateralResponse, AccelerationRestriction
from ..physics.types import MetricRange

class RssResponseResolving:
    def provide_proper_response(self, state_snapshot: RssStateSnapshot) -> ProperResponse:
        """
        Resolves the individual RSS states into a single proper response.
        """
        is_safe = True
        dangerous_objects = []

        # Start with the least restrictive responses
        lon_response = LongitudinalResponse.None_
        lat_response_left = LateralResponse.None_
        lat_response_right = LateralResponse.None_

        # Initialize acceleration restrictions with vehicle defaults
        default_dynamics = state_snapshot.default_ego_vehicle_rss_dynamics
        accel_lon_max = default_dynamics.alpha_lon_accel_max
        accel_lon_min = default_dynamics.alpha_lon_brake_max # This is brake_max, the hardest brake

        accel_lat_max_left = default_dynamics.alpha_lat_accel_max
        accel_lat_min_left = -default_dynamics.alpha_lat_brake_min # Symmetric for this simplified model

        accel_lat_max_right = default_dynamics.alpha_lat_accel_max
        accel_lat_min_right = -default_dynamics.alpha_lat_brake_min

        for state in state_snapshot.individual_responses:
            # --- Longitudinal ---
            if not state.longitudinal_state.is_safe:
                is_safe = False
                if state.object_id not in dangerous_objects:
                    dangerous_objects.append(state.object_id)

                # The response is an enum, so higher value means more severe action
                if state.longitudinal_state.response.value > lon_response.value:
                    lon_response = state.longitudinal_state.response

                # Restrict longitudinal acceleration. For simplicity, we'll just forbid acceleration.
                # A real implementation would calculate a precise maximum allowed acceleration.
                accel_lon_max = 0.0

            # --- Lateral (Simplified) ---
            # In this simplified version, lateral is always safe, so we don't update lat_response
            # or lateral acceleration restrictions based on state.

        accel_restriction = AccelerationRestriction(
            longitudinal_range=MetricRange(minimum=accel_lon_min, maximum=accel_lon_max),
            lateral_left_range=MetricRange(minimum=accel_lat_min_left, maximum=accel_lat_max_left),
            lateral_right_range=MetricRange(minimum=accel_lat_min_right, maximum=accel_lat_max_right)
        )

        return ProperResponse(
            time_index=state_snapshot.time_index,
            is_safe=is_safe,
            dangerous_objects=dangerous_objects,
            longitudinal_response=lon_response,
            lateral_response_left=lat_response_left,
            lateral_response_right=lat_response_right,
            # unstructured response is not handled yet
            acceleration_restrictions=accel_restriction
        )