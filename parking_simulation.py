"""
Parking Space Simulation

Simulates walking distance after parking in the first available empty space.
Each parking space is empty with probability p, independently.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SimulationParams:
    """Parameters for the parking simulation."""
    num_spaces: int  # Total number of parking spaces
    p_empty: float   # Probability that each space is empty (0 < p <= 1)
    num_simulations: int  # Number of simulations to run


@dataclass
class SimulationResult:
    """Results from a single parking simulation."""
    first_available_position: int  # Position of first available space (1-indexed)
    walking_distance: float  # Distance to walk from entrance (assuming unit distance per space)
    
    def __repr__(self) -> str:
        return f"Position: {self.first_available_position}, Distance: {self.walking_distance:.2f}"


class ParkingSimulator:
    """Simulates parking scenarios with random space availability."""
    
    def __init__(self, params: SimulationParams):
        """
        Initialize the parking simulator.
        
        Args:
            params: SimulationParams object with simulation configuration
        """
        self.params = params
        self._validate_params()
        self.results: List[SimulationResult] = []
    
    def _validate_params(self) -> None:
        """Validate simulation parameters."""
        if self.params.num_spaces < 1:
            raise ValueError("num_spaces must be at least 1")
        if not (0 < self.params.p_empty <= 1):
            raise ValueError("p_empty must be in range (0, 1]")
        if self.params.num_simulations < 1:
            raise ValueError("num_simulations must be at least 1")
    
    def _simulate_single_parking(self) -> SimulationResult:
        """
        Simulate a single parking event.
        
        Returns:
            SimulationResult with the position of first available space and walking distance
        """
        # Generate random availability for each space (True = empty)
        spaces = np.random.binomial(1, self.params.p_empty, self.params.num_spaces)
        
        # Find first available space
        available_positions = np.where(spaces == 1)[0]
        
        if len(available_positions) == 0:
            # No spaces available - park at the last position
            first_available = self.params.num_spaces
        else:
            # Find first available (0-indexed, convert to 1-indexed)
            first_available = available_positions[0] + 1
        
        # Walking distance is proportional to the position
        # Assuming distance = position (in units from entrance)
        walking_distance = float(first_available)
        
        return SimulationResult(
            first_available_position=first_available,
            walking_distance=walking_distance
        )
    
    def run(self) -> List[SimulationResult]:
        """
        Run the parking simulations.
        
        Returns:
            List of SimulationResult objects
        """
        self.results = [
            self._simulate_single_parking() 
            for _ in range(self.params.num_simulations)
        ]
        return self.results
    
    def get_statistics(self) -> dict:
        """
        Calculate statistics from simulation results.
        
        Returns:
            Dictionary with statistical measures
        """
        if not self.results:
            raise ValueError("No simulation results. Run simulations first.")
        
        distances = [r.walking_distance for r in self.results]
        positions = [r.first_available_position for r in self.results]
        
        return {
            'mean_distance': np.mean(distances),
            'std_distance': np.std(distances),
            'median_distance': np.median(distances),
            'min_distance': np.min(distances),
            'max_distance': np.max(distances),
            'mean_position': np.mean(positions),
            'std_position': np.std(positions),
            'median_position': np.median(positions),
        }
    
    def print_summary(self) -> None:
        """Print a summary of simulation results."""
        if not self.results:
            print("No results to summarize. Run simulations first.")
            return
        
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("PARKING SIMULATION SUMMARY")
        print("="*60)
        print(f"\nConfiguration:")
        print(f"  Number of parking spaces: {self.params.num_spaces}")
        print(f"  Probability of empty space: {self.params.p_empty}")
        print(f"  Number of simulations: {self.params.num_simulations}")
        print(f"\nWalking Distance Statistics:")
        print(f"  Mean distance: {stats['mean_distance']:.4f}")
        print(f"  Median distance: {stats['median_distance']:.4f}")
        print(f"  Std deviation: {stats['std_distance']:.4f}")
        print(f"  Min distance: {stats['min_distance']:.4f}")
        print(f"  Max distance: {stats['max_distance']:.4f}")
        print(f"\nParking Position Statistics:")
        print(f"  Mean position: {stats['mean_position']:.4f}")
        print(f"  Median position: {stats['median_position']:.4f}")
        print(f"  Std deviation: {stats['std_position']:.4f}")
        print("="*60 + "\n")
