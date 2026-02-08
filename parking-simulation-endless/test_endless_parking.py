"""
Unit tests for the endless road parking simulation module.
"""

import unittest
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
            self.assertGreaterEqual(result.walking_distance_total, 0)
            self.assertIn(result.found_before_destination, [True, False])
    
    def test_walking_distance_calculation(self):
        """Test that walking distance is calculated correctly."""
        results = self.simulator.run()
        for result in results:
            expected_walk = abs(result.parked_position - result.destination_position)
            self.assertAlmostEqual(result.walking_distance_total, expected_walk, places=5)
    
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
        """Test that high p_empty results in parking close to destination."""
        params = SimulationParams(
            destination_distance=100.0,
            p_empty=0.9,  # Very high probability
            space_interval=1.0,
            num_simulations=1000
        )
        simulator = EndlessRoadParkingSimulator(params)
        results = simulator.run()
        stats = simulator.get_statistics()
        
        # With p=0.9, average position should be close to 1/0.9 ≈ 1.11
        self.assertLess(stats['mean_parking_position'], 10)
    
    def test_low_probability_drives_past_destination(self):
        """Test that low p_empty results in driving past destination."""
        params = SimulationParams(
            destination_distance=20.0,
            p_empty=0.1,  # Very low probability
            space_interval=1.0,
            num_simulations=1000
        )
        simulator = EndlessRoadParkingSimulator(params)
        results = simulator.run()
        stats = simulator.get_statistics()
        
        # With p=0.1, expected position is 1/0.1 = 10
        # Most should be past destination (20)
        fraction_after = stats['fraction_after_destination']
        self.assertGreater(fraction_after, 0.5)


if __name__ == '__main__':
    unittest.main()
