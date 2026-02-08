"""
Parking Space Simulation - Endless Road Variant

Simulates parking on an endless road where parking spaces are arranged
infinitely. If no space is found before destination, you continue driving.
Each parking space is empty with probability p, independently.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SimulationParams:
    """Parameters for the parking simulation."""
    destination_distance: float  # Distance to destination (in units)
    p_empty: float              # Probability that each space is empty (0 < p <= 1)
    space_interval: float       # Distance between parking spaces (default 1 unit)
    num_simulations: int        # Number of simulations to run
    max_search_distance: Optional[float] = None  # Max distance to search (None = unlimited)


@dataclass
class SimulationResult:
    """Results from a single parking simulation."""
    parked_position: float      # Position where you parked
    destination_position: float # Original destination position
    distance_past_destination: float  # How far past destination you parked (negative if before)
    walking_distance_forward: float   # Distance walked forward from car to destination
    walking_distance_total: float     # Total walking distance
    found_before_destination: bool    # Did you find parking before destination?
    
    def __repr__(self) -> str:
        status = "BEFORE" if self.found_before_destination else "AFTER"
        return (f"Position: {self.parked_position:.2f}, "
                f"Status: {status}, "
                f"Walk: {self.walking_distance_total:.2f}")


class EndlessRoadParkingSimulator:
    """Simulates parking on an endless road with random space availability."""
    
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
        if self.params.destination_distance <= 0:
            raise ValueError("destination_distance must be positive")
        if not (0 < self.params.p_empty <= 1):
            raise ValueError("p_empty must be in range (0, 1]")
        if self.params.space_interval <= 0:
            raise ValueError("space_interval must be positive")
        if self.params.num_simulations < 1:
            raise ValueError("num_simulations must be at least 1")
    
    def _simulate_single_parking(self) -> SimulationResult:
        """
        Simulate a single parking event on an endless road.
        
        Returns:
            SimulationResult with parking position and walking distance
        """
        current_position = 0.0
        destination = self.params.destination_position
        max_search = self.params.max_search_distance
        
        # Keep driving until you find an empty space
        while True:
            # Check if current space is empty
            if np.random.random() < self.params.p_empty:
                # Found an empty space! Park here.
                parked_position = current_position
                break
            
            # Move to next space
            current_position += self.params.space_interval
            
            # Check if we've exceeded max search distance
            if max_search is not None and current_position > max_search:
                parked_position = current_position
                break
        
        # Calculate results
        distance_past_destination = parked_position - destination
        found_before_destination = distance_past_destination < 0
        
        # Walking distance calculation:
        # If parked before destination: walk forward to destination
        # If parked after destination: walk backward to destination
        walking_distance_total = abs(distance_past_destination)
        
        return SimulationResult(
            parked_position=parked_position,
            destination_position=destination,
            distance_past_destination=distance_past_destination,
            walking_distance_forward=walking_distance_total,
            walking_distance_total=walking_distance_total,
            found_before_destination=found_before_destination
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
        
        positions = [r.parked_position for r in self.results]
        walking_distances = [r.walking_distance_total for r in self.results]
        distances_past = [r.distance_past_destination for r in self.results]
        before_dest = sum(1 for r in self.results if r.found_before_destination)
        
        return {
            'mean_parking_position': np.mean(positions),
            'std_parking_position': np.std(positions),
            'median_parking_position': np.median(positions),
            'mean_walking_distance': np.mean(walking_distances),
            'std_walking_distance': np.std(walking_distances),
            'median_walking_distance': np.median(walking_distances),
            'min_walking_distance': np.min(walking_distances),
            'max_walking_distance': np.max(walking_distances),
            'mean_distance_past_destination': np.mean(distances_past),
            'fraction_before_destination': before_dest / len(self.results),
            'fraction_after_destination': (len(self.results) - before_dest) / len(self.results),
        }
    
    def print_summary(self) -> None:
        """Print a summary of simulation results."""
        if not self.results:
            print("No results to summarize. Run simulations first.")
            return
        
        stats = self.get_statistics()
        before_count = sum(1 for r in self.results if r.found_before_destination)
        after_count = len(self.results) - before_count
        
        print("\n" + "="*70)
        print("ENDLESS ROAD PARKING SIMULATION SUMMARY")
        print("="*70)
        print(f"\nConfiguration:")
        print(f"  Destination distance: {self.params.destination_distance:.2f} units")
        print(f"  Spacing between parking spaces: {self.params.space_interval:.2f} units")
        print(f"  Probability of empty space: {self.params.p_empty}")
        print(f"  Number of simulations: {self.params.num_simulations}")
        
        print(f"\nParking Outcomes:")
        print(f"  Found BEFORE destination: {before_count} ({stats['fraction_before_destination']*100:.1f}%)")
        print(f"  Found AFTER destination: {after_count} ({stats['fraction_after_destination']*100:.1f}%)")
        
        print(f"\nParking Position Statistics:")
        print(f"  Mean position: {stats['mean_parking_position']:.4f} units")
        print(f"  Median position: {stats['median_parking_position']:.4f} units")
        print(f"  Std deviation: {stats['std_parking_position']:.4f}")
        print(f"  Mean distance past destination: {stats['mean_distance_past_destination']:.4f} units")
        
        print(f"\nWalking Distance Statistics:")
        print(f"  Mean walking distance: {stats['mean_walking_distance']:.4f} units")
        print(f"  Median walking distance: {stats['median_walking_distance']:.4f} units")
        print(f"  Std deviation: {stats['std_walking_distance']:.4f}")
        print(f"  Min walking distance: {stats['min_walking_distance']:.4f}")
        print(f"  Max walking distance: {stats['max_walking_distance']:.4f}")
        
        print("="*70 + "\n")
