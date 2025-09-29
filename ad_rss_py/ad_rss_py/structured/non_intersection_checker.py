from ..core.types import RelativeConstellation, LongitudinalRelativePosition
from ..state.types import RssState, LongitudinalRssState, LateralRssState, UnstructuredRssState, LongitudinalResponse, LateralResponse, UnstructuredConstellationResponse, RssStateInformation
from .formulas import calculate_safe_longitudinal_distance

class RssNonIntersectionConstellationChecker:
    def check_constellation(self, constellation: RelativeConstellation) -> RssState:
        """
        Checks a non-intersection constellation and returns the RssState.
        """
        # --- Longitudinal Check ---
        is_safe_lon = True
        lon_response = LongitudinalResponse.None_

        # We only check for safety if the ego vehicle is behind the other vehicle
        if constellation.relative_position.longitudinal_position == LongitudinalRelativePosition.AtBack:
            safe_dist = calculate_safe_longitudinal_distance(constellation)
            current_dist = constellation.relative_position.longitudinal_distance

            if current_dist < safe_dist:
                is_safe_lon = False
                lon_response = LongitudinalResponse.BrakeMin

            lon_rss_info = RssStateInformation(current_distance=current_dist, safe_distance=safe_dist)
        else:
            # If not AtBack, it's considered safe from a longitudinal perspective for this simplified model
            lon_rss_info = RssStateInformation(current_distance=constellation.relative_position.longitudinal_distance, safe_distance=0.0)

        longitudinal_state = LongitudinalRssState(
            is_safe=is_safe_lon,
            response=lon_response,
            rss_state_information=lon_rss_info
        )

        # --- Lateral Check (Simplified) ---
        # In this simplified version, we assume lateral situations are always safe.
        # A real implementation would have detailed lateral distance calculations.
        lat_rss_info = RssStateInformation(current_distance=constellation.relative_position.lateral_distance, safe_distance=0.0)
        lateral_state_left = LateralRssState(is_safe=True, response=LateralResponse.None_, rss_state_information=lat_rss_info)
        lateral_state_right = LateralRssState(is_safe=True, response=LateralResponse.None_, rss_state_information=lat_rss_info)

        # --- Unstructured State (Not applicable for this checker) ---
        unstructured_state = UnstructuredRssState(is_safe=True, response=UnstructuredConstellationResponse.None_)

        return RssState(
            constellation_id=constellation.constellation_id,
            object_id=constellation.object_id,
            constellation_type=constellation.constellation_type,
            longitudinal_state=longitudinal_state,
            lateral_state_left=lateral_state_left,
            lateral_state_right=lateral_state_right,
            unstructured_constellation_state=unstructured_state
        )