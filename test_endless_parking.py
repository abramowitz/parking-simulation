"""
Unit tests for the endless road parking simulation module.
"""

import unittest
import sys
sys.path.insert(0, '/content/parking-simulation')

from parking_simulation_endless import (
    EndlessRoadParkingSimulator, 
    SimulationParams, 
    SimulationResult
)


class TestEndlessRoadSimulation(unittest.TestCase):
    """Test endless road parking simulator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = SimulationParams(
            destination_distance=50.0,
            p_empty=0.5,
            space_interval=1.0,
            num_simulations=100
        )
        self.simulator = EndlessRoadParkingSimulator(self.params)
    
    def test_simulation_runs(self):
        """Test that simulation runs without errors."""
        results = self.simulator.run()
        self.assertEqual(len(results), 100)
    
    def test_result_validity(self):
        """Test that results are physically valid."""
        results = self.simulator.run()
        for result in results:
            self.assertGreaterEqual(result.parked_position, 0)
            self.assertGreaterEqual(result.walking_distance, 0)
            self.assertIn(result.found_before_destination, [True, False])
    
    def test_walking_distance_calculation(self):
        """Test that walking distance is calculated correctly."""
        results = self.simulator.run()
        for result in results:
            expected_walk = abs(result.parked_position - result.destination_position)
            self.assertAlmostEqual(result.walking_distance, expected_walk, places=5)
    
    def test_distance_to_destination_is_signed(self):
        """Test that distance_to_destination has correct sign."""
        results = self.simulator.run()
        for result in results:
            if result.found_before_destination:
                # Before destination: distance_to_destination should be negative
                self.assertLess(result.distance_to_destination, 0)
            else:
                # After destination: distance_to_destination should be positive
                self.assertGreater(result.distance_to_destination, 0)
    
    def test_statistics_generation(self):
        """Test that statistics are calculated correctly."""
        self.simulator.run()
        stats = self.simulator.get_statistics()
        
        self.assertIn('mean_walking_distance', stats)
        self.assertIn('fraction_before_destination', stats)
        self.assertGreater(stats['mean_walking_distance'], 0)
        self.assertGreaterEqual(stats['fraction_before_destination'], 0)
        self.assertLessEqual(stats['fraction_before_destination'], 1)
    
    def test_high_probability_finds_parking_nearby(self):
        """Test that high p_empty results in parking close to starting point."""
        params = SimulationParams(
            destination_distance=100.0,
            p_empty=0.9,  # Very high probability (90% spaces empty)
            space_interval=1.0,
            num_simulations=1000
        )
        simulator = EndlessRoadParkingSimulator(params)
        results = simulator.run()
        stats = simulator.get_statistics()
        
        # With p=0.9, expected position is 1/p = 1/0.9 ≈ 1.11
        # Mean parking position should be very close to starting point
        self.assertLess(stats['mean_parking_position'], 5)
        
        # With p=0.9 and destination at 100, we should almost always park before destination
        self.assertGreater(stats['fraction_before_destination'], 0.95)
    
    def test_low_probability_parks_farther_out(self):
        """Test that low p_empty results in parking farther from start."""
        params = SimulationParams(
            destination_distance=100.0,
            p_empty=0.1,  # Low probability (10% spaces empty)
            space_interval=1.0,
            num_simulations=1000
        )
        simulator = EndlessRoadParkingSimulator(params)
        results = simulator.run()
        stats = simulator.get_statistics()
        
        # With p=0.1, expected position is 1/p = 1/0.1 = 10
        # Mean parking position should be around 10
        self.assertGreater(stats['mean_parking_position'], 5)
        self.assertLess(stats['mean_parking_position'], 20)
    
    def test_relationship_between_p_and_parking_distance(self):
        """Test that lower p_empty results in farther parking."""
        # High probability
        params_high = SimulationParams(
            destination_distance=100.0,
            p_empty=0.8,
            space_interval=1.0,
            num_simulations=500
        )
        sim_high = EndlessRoadParkingSimulator(params_high)
        results_high = sim_high.run()
        stats_high = sim_high.get_statistics()
        
        # Low probability
        params_low = SimulationParams(
            destination_distance=100.0,
            p_empty=0.2,
            space_interval=1.0,
            num_simulations=500
        )
        sim_low = EndlessRoadParkingSimulator(params_low)
        results_low = sim_low.run()
        stats_low = sim_low.get_statistics()
        
        # Low probability should have higher mean parking position
        self.assertGreater(
            stats_low['mean_parking_position'],
            stats_high['mean_parking_position']
        )


if __name__ == '__main__':
    unittest.main()
