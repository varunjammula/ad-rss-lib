from ..world.types import WorldModel
from ..state.types import ProperResponse
from .situation_extraction import RssSituationExtraction
from .situation_checking import RssSituationChecking
from .response_resolving import RssResponseResolving

class RssCheck:
    """
    Main class for performing the RSS check.
    """
    def __init__(self):
        self._situation_extraction = RssSituationExtraction()
        self._situation_checking = RssSituationChecking()
        self._response_resolving = RssResponseResolving()

    def calculate_proper_response(self, world_model: WorldModel) -> ProperResponse:
        """
        Calculates the proper RSS response for a given world model.

        This method orchestrates the three main steps of the RSS calculation:
        1. Situation Extraction: Transforms the world model into relative constellations.
        2. Situation Checking: Evaluates the safety of each constellation.
        3. Response Resolving: Consolidates the individual safety states into a single,
           actionable response for the ego vehicle.
        """
        # 1. Extract situations from the world model
        situation_snapshot = self._situation_extraction.extract_situation(world_model)

        # 2. Check the safety of the extracted situations
        state_snapshot = self._situation_checking.check_situation(situation_snapshot)

        # 3. Resolve the states into a single proper response
        proper_response = self._response_resolving.provide_proper_response(state_snapshot)

        return proper_response