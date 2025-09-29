import unittest
from ad_rss_py.structured.constellation_id_provider import RssConstellationIdProvider
from ad_rss_py.world.types import (
    Constellation,
    ConstellationType,
    Object,
    ObjectType,
    ObjectState,
    RssDynamics,
    TimeIndex,
)
from ad_rss_py.physics.types import MetricRange, Speed


class TestRssConstellationIdProvider(unittest.TestCase):

    def setUp(self):
        """Set up the provider and some common objects."""
        self.provider = RssConstellationIdProvider()
        self.dynamics = RssDynamics(
            alpha_lon_accel_max=2.0, alpha_lon_brake_min=4.0, alpha_lon_brake_max=8.0,
            alpha_lat_accel_max=0.2, alpha_lat_brake_min=0.8, lateral_fluctuation_margin=0.1, response_time=1.0
        )
        self.time_index = TimeIndex(1)

        # Create some mock objects
        self.obj1 = Object(object_id=1, object_type=ObjectType.EgoVehicle, state=ObjectState(position=MetricRange(0, 4), velocity=Speed(10)))
        self.obj2 = Object(object_id=2, object_type=ObjectType.OtherVehicle, state=ObjectState(position=MetricRange(10, 14), velocity=Speed(10)))
        self.obj3 = Object(object_id=3, object_type=ObjectType.OtherVehicle, state=ObjectState(position=MetricRange(20, 24), velocity=Speed(10)))

    def test_provides_new_and_persistent_ids(self):
        """
        Test that new constellations get new IDs and existing ones get the same ID.
        """
        constellation12 = Constellation(constellation_type=ConstellationType.SameDirection, ego_vehicle=self.obj1, object=self.obj2, ego_vehicle_rss_dynamics=self.dynamics, object_rss_dynamics=self.dynamics, intersecting_road=None, ego_vehicle_road=None)
        constellation13 = Constellation(constellation_type=ConstellationType.SameDirection, ego_vehicle=self.obj1, object=self.obj3, ego_vehicle_rss_dynamics=self.dynamics, object_rss_dynamics=self.dynamics, intersecting_road=None, ego_vehicle_road=None)

        # First call should create new IDs
        id12_first = self.provider.get_constellation_id(self.time_index, constellation12)
        id13_first = self.provider.get_constellation_id(self.time_index, constellation13)
        self.assertEqual(id12_first, 0)
        self.assertEqual(id13_first, 1)

        # Second call should return the same IDs
        id12_second = self.provider.get_constellation_id(self.time_index, constellation12)
        id13_second = self.provider.get_constellation_id(self.time_index, constellation13)
        self.assertEqual(id12_second, id12_first)
        self.assertEqual(id13_second, id13_first)

    def test_id_is_independent_of_ego_object(self):
        """
        Test that the constellation ID is the same even if the ego and other object are swapped.
        """
        constellation12 = Constellation(constellation_type=ConstellationType.SameDirection, ego_vehicle=self.obj1, object=self.obj2, ego_vehicle_rss_dynamics=self.dynamics, object_rss_dynamics=self.dynamics, intersecting_road=None, ego_vehicle_road=None)
        constellation21 = Constellation(constellation_type=ConstellationType.SameDirection, ego_vehicle=self.obj2, object=self.obj1, ego_vehicle_rss_dynamics=self.dynamics, object_rss_dynamics=self.dynamics, intersecting_road=None, ego_vehicle_road=None)

        id12 = self.provider.get_constellation_id(self.time_index, constellation12)
        id21 = self.provider.get_constellation_id(self.time_index, constellation21)

        self.assertEqual(id12, id21)

    def test_drop_constellation_ids(self):
        """
        Test that dropping an object ID removes all associated constellations.
        """
        constellation12 = Constellation(constellation_type=ConstellationType.SameDirection, ego_vehicle=self.obj1, object=self.obj2, ego_vehicle_rss_dynamics=self.dynamics, object_rss_dynamics=self.dynamics, intersecting_road=None, ego_vehicle_road=None)
        constellation13 = Constellation(constellation_type=ConstellationType.SameDirection, ego_vehicle=self.obj1, object=self.obj3, ego_vehicle_rss_dynamics=self.dynamics, object_rss_dynamics=self.dynamics, intersecting_road=None, ego_vehicle_road=None)

        id12 = self.provider.get_constellation_id(self.time_index, constellation12)
        id13 = self.provider.get_constellation_id(self.time_index, constellation13)
        self.assertEqual(id12, 0)
        self.assertEqual(id13, 1)

        # Drop all constellations involving object 1
        self.provider.drop_constellation_ids(self.obj1.object_id)

        # Now, getting the IDs again should result in new IDs being assigned
        new_id12 = self.provider.get_constellation_id(self.time_index, constellation12)
        new_id13 = self.provider.get_constellation_id(self.time_index, constellation13)
        self.assertNotEqual(new_id12, id12)
        self.assertNotEqual(new_id13, id13)
        self.assertEqual(new_id12, 2)
        self.assertEqual(new_id13, 3)

if __name__ == '__main__':
    unittest.main()