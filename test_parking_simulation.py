"""
Unit tests for the parking simulation module.
"""

import unittest
import numpy as np
from parking_simulation import (
    ParkingSimulator, 
    SimulationParams, 
    SimulationResult
)


class TestSimulationParams(unittest.TestCase):
    """Test SimulationParams validation."""
    
    def test_valid_params(self):
        """Test that valid parameters are accepted."""
        params = SimulationParams(
            num_spaces=50,
            p_empty=0.5,
            num_simulations=1000
        )
        self.assertEqual(params.num_spaces, 50)
        self.assertEqual(params.p_empty, 0.5)
        self.assertEqual(params.num_simulations, 1000)
    
    def test_invalid_num_spaces(self):
        """Test that invalid num_spaces raises error."""
        params = SimulationParams(
            num_spaces=0,
            p_empty=0.5,
            num_simulations=1000
        )
        simulator = ParkingSimulator(params)
        with self.assertRaises(ValueError):
            simulator._validate_params()
    
    def test_invalid_p_empty(self):
        """Test that invalid p_empty raises error."""
        params = SimulationParams(
            num_spaces=50,
            p_empty=1.5,
            num_simulations=1000
        )
        simulator = ParkingSimulator(params)
        with self.assertRaises(ValueError):
            simulator._validate_params()


class TestParkingSimulator(unittest.TestCase):
    """Test ParkingSimulator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = SimulationParams(
            num_spaces=50,
            p_empty=0.5,
            num_simulations=100
        )
        self.simulator = ParkingSimulator(self.params)
    
    def test_simulation_runs(self):
        """Test that simulation runs without errors."""
        results = self.simulator.run()
        self.assertEqual(len(results), 100)
    
    def test_result_validity(self):
        """Test that results are valid."""
        results = self.simulator.run()
        for result in results:
            self.assertGreaterEqual(result.first_available_position, 1)
            self.assertLessEqual(result.first_available_position, 50)
            self.assertEqual(result.walking_distance, result.first_available_position)
    
    def test_statistics(self):
        """Test that statistics are calculated correctly."""
        self.simulator.run()
        stats = self.simulator.get_statistics()
        
        self.assertIn('mean_distance', stats)
        self.assertIn('std_distance', stats)
        self.assertGreater(stats['mean_distance'], 0)


class TestSimulationResult(unittest.TestCase):
    """Test SimulationResult data class."""
    
    def test_result_creation(self):
        """Test creating a SimulationResult."""
        result = SimulationResult(
            first_available_position=25,
            walking_distance=25.0
        )
        self.assertEqual(result.first_available_position, 25)
        self.assertEqual(result.walking_distance, 25.0)


if __name__ == '__main__':
    unittest.main()
