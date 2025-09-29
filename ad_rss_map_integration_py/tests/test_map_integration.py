import unittest
from datetime import datetime

# Main classes to test
from ad_rss_map_integration_py.world_model_creation import RssWorldModelCreation, RssConstellationCreationMode, RssRestrictSpeedLimitMode
from ad_rss_map_integration_py.rss_object_data import RssObjectData

# Dependent data types
from ad_rss_py.world.types import ObjectId, ObjectType, RssDynamics
from ad_rss_py.physics.types import SpeedRange, AngularVelocity, Angle, Dimension3D, Speed, Distance, ParametricValue
from ad_rss_map_integration_py.map.match.types import Object as MapMatchedObject, ENUObjectPosition, MapMatchedObjectBoundingBox
from ad_rss_map_integration_py.map.point.types import ENUPoint, GeoPoint, ENUHeading, BoundingSphere, ECEFPoint, ParaPoint
from ad_rss_map_integration_py.map.route.types import FullRoute, RoadSegment, LaneSegment, LaneInterval, RouteCreationMode
from ad_rss_map_integration_py.map.lane.types import LaneId


class TestMapIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a complex set of mock data for the integration test."""

        # Common physics and dynamics
        self.dynamics = RssDynamics(alpha_lon_accel_max=2.0, alpha_lon_brake_min=4.0, alpha_lon_brake_max=8.0,
                                    alpha_lat_accel_max=0.2, alpha_lat_brake_min=0.8, lateral_fluctuation_margin=0.1,
                                    response_time=1.0)

        # --- Create Map-Matched Object for Ego ---
        ego_enu_pos = ENUObjectPosition(
            center_point=ENUPoint(x=0, y=0, z=0),
            heading=ENUHeading(0.0),
            enu_reference_point=GeoPoint(longitude=0.0, latitude=0.0, altitude=0.0),
            dimension=Dimension3D(length=4.5, width=1.8, height=1.6)
        )
        self.ego_map_object = MapMatchedObject(enu_position=ego_enu_pos)

        # --- Create RssObjectData for Ego ---
        self.ego_object_data = RssObjectData(
            last_update=datetime.now(),
            id=ObjectId(1),
            type=ObjectType.EgoVehicle,
            match_object=self.ego_map_object,
            speed_range=SpeedRange(minimum=Speed(20.0), maximum=Speed(22.0)),
            yaw_rate=AngularVelocity(0.0),
            steering_angle=Angle(0.0),
            rss_dynamics=self.dynamics
        )

        # --- Create Map-Matched Object for Other Vehicle ---
        other_enu_pos = ENUObjectPosition(
            center_point=ENUPoint(x=50, y=2, z=0),
            heading=ENUHeading(0.0),
            enu_reference_point=GeoPoint(longitude=0.0, latitude=0.0, altitude=0.0),
            dimension=Dimension3D(length=5.0, width=2.0, height=1.8)
        )
        self.other_map_object = MapMatchedObject(enu_position=other_enu_pos)

        # --- Create RssObjectData for Other Vehicle ---
        self.other_object_data = RssObjectData(
            last_update=datetime.now(),
            id=ObjectId(2),
            type=ObjectType.OtherVehicle,
            match_object=self.other_map_object,
            speed_range=SpeedRange(minimum=Speed(18.0), maximum=Speed(20.0)),
            yaw_rate=AngularVelocity(0.0),
            steering_angle=Angle(0.0),
            rss_dynamics=self.dynamics
        )

        # --- Create a FullRoute for the ego vehicle ---
        lane_interval = LaneInterval(lane_id=LaneId(101), start=ParametricValue(0.0), end=ParametricValue(1.0))
        lane_segment = LaneSegment(left_neighbor=LaneId(0), right_neighbor=LaneId(0), predecessors=[], successors=[],
                                   lane_interval=lane_interval, route_lane_offset=0)
        road_segment = RoadSegment(
            drivable_lane_segments=[lane_segment],
            segment_count_from_destination=1,
            bounding_sphere=BoundingSphere(center=ECEFPoint(x=0,y=0,z=0), radius=Distance(100))
        )
        self.ego_route = FullRoute(
            road_segments=[road_segment],
            route_creation_mode=RouteCreationMode.SameDrivingDirection
        )

    def test_integration_pipeline_smoke_test(self):
        """
        A smoke test to ensure the map integration pipeline can be called end-to-end.
        """
        # 1. Instantiate RssWorldModelCreation
        world_creation = RssWorldModelCreation(
            time_index=1,
            default_ego_rss_dynamics=self.dynamics
        )

        # 2. Call appendConstellations
        result = world_creation.append_constellations(
            ego_object_data=self.ego_object_data,
            ego_route=self.ego_route,
            other_object_data=self.other_object_data,
            restrict_speed_limit_mode=RssRestrictSpeedLimitMode.Unrestricted,
            green_traffic_lights=[],
            mode=RssConstellationCreationMode.SameDirection
        )

        self.assertTrue(result)

        # 3. Get the final world model
        world_model = world_creation.get_world_model()

        # 4. Assert basic correctness
        self.assertIsNotNone(world_model)
        self.assertEqual(len(world_model.constellations), 1)

        constellation = world_model.constellations[0]
        self.assertEqual(constellation.ego_vehicle.object_id, self.ego_object_data.id)
        self.assertEqual(constellation.object.object_id, self.other_object_data.id)


if __name__ == '__main__':
    unittest.main()