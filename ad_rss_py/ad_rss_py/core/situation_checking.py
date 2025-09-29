from ..core.types import RssSituationSnapshot
from ..state.types import RssStateSnapshot, RssState
from ..world.types import ConstellationType
from ..structured.non_intersection_checker import RssNonIntersectionConstellationChecker
# Import other checkers as they are implemented
# from ..structured.intersection_checker import RssIntersectionConstellationChecker
# from ..unstructured.unstructured_checker import RssUnstructuredConstellationChecker

class RssSituationChecking:
    def __init__(self):
        self._non_intersection_checker = RssNonIntersectionConstellationChecker()
        # self._intersection_checker = RssIntersectionConstellationChecker()
        # self._unstructured_checker = RssUnstructuredConstellationChecker()
        self._current_time_index = 0

    def check_situation(self, situation_snapshot: RssSituationSnapshot) -> RssStateSnapshot:
        if not self._check_time_increasing_consistently(situation_snapshot.time_index):
            # In a real implementation, log a warning or error
            pass

        individual_responses = []
        for constellation in situation_snapshot.constellations:
            rss_state = self._check_constellation(constellation)
            if rss_state:
                individual_responses.append(rss_state)

        return RssStateSnapshot(
            time_index=situation_snapshot.time_index,
            individual_responses=individual_responses,
            default_ego_vehicle_rss_dynamics=situation_snapshot.default_ego_vehicle_rss_dynamics
        )

    def _check_constellation(self, constellation) -> RssState:
        if constellation.constellation_type in [ConstellationType.SameDirection, ConstellationType.OppositeDirection]:
            return self._non_intersection_checker.check_constellation(constellation)
        elif constellation.constellation_type in [ConstellationType.IntersectionEgoHasPriority, ConstellationType.IntersectionObjectHasPriority, ConstellationType.IntersectionSamePriority]:
            # To be implemented
            return None
        elif constellation.constellation_type == ConstellationType.Unstructured:
            # To be implemented
            return None
        elif constellation.constellation_type == ConstellationType.NotRelevant:
            # Not relevant constellations are considered safe and don't need a detailed state
            return None
        else:
            # Should not happen with valid input
            return None

    def _check_time_increasing_consistently(self, next_time_index: int) -> bool:
        # Simplified time check
        is_consistent = next_time_index > self._current_time_index
        self._current_time_index = next_time_index
        return is_consistent