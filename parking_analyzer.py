"""
Analysis module for parking simulation.

Calculates expected walking distances and finds optimal starting points.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from parking_simulation_endless import EndlessRoadParkingSimulator, SimulationParams


class ParkingAnalyzer:
    """Analyze parking simulations and find optimal starting points."""
    
    def __init__(self, num_simulations: int = 5000):
        """
        Initialize analyzer.
        
        Args:
            num_simulations: Number of simulations per configuration
        """
        self.num_simulations = num_simulations
        self.results_cache = {}
    
    def expected_walking_distance(
        self, 
        starting_point: float, 
        destination: float, 
        p_empty: float
    ) -> float:
        """
        Calculate expected walking distance via simulation.
        
        Args:
            starting_point: Starting position (where you are now)
            destination: Target destination
            p_empty: Probability that each space is empty
        
        Returns:
            Expected walking distance
        """
        # Adjust destination relative to starting point
        relative_destination = destination - starting_point
        
        if relative_destination <= 0:
            raise ValueError("Destination must be ahead of starting point")
        
        params = SimulationParams(
            destination_distance=relative_destination,
            p_empty=p_empty,
            space_interval=1.0,
            num_simulations=self.num_simulations
        )
        
        simulator = EndlessRoadParkingSimulator(params)
        results = simulator.run()
        stats = simulator.get_statistics()
        
        return stats['mean_walking_distance']
    
    def theoretical_expected_position(self, p_empty: float) -> float:
        """
        Calculate theoretical expected parking position.
        
        For a geometric distribution, expected value = 1/p
        
        Args:
            p_empty: Probability that each space is empty
        
        Returns:
            Expected parking position
        """
        return 1.0 / p_empty
    
    def find_optimal_starting_point(
        self,
        destination: float,
        p_empty: float,
        search_range: Tuple[float, float] = None,
        num_points: int = 20
    ) -> Dict:
        """
        Find the optimal starting point that minimizes expected walking distance.
        
        Args:
            destination: Target destination
            p_empty: Probability that each space is empty
            search_range: (min, max) starting positions to test. 
                         Default: (0, destination-1)
            num_points: Number of points to test
        
        Returns:
            Dictionary with optimal starting point and results
        """
        if search_range is None:
            search_range = (0, destination - 1)
        
        starting_points = np.linspace(search_range[0], search_range[1], num_points)
        walking_distances = []
        
        print(f"\nFinding optimal starting point for destination={destination}, p={p_empty}")
        print(f"Testing {num_points} starting points...")
        
        for sp in starting_points:
            try:
                expected_walk = self.expected_walking_distance(sp, destination, p_empty)
                walking_distances.append(expected_walk)
                print(f"  Starting at {sp:6.2f}: Expected walk = {expected_walk:7.4f}")
            except ValueError:
                walking_distances.append(np.nan)
        
        # Find optimal
        valid_indices = ~np.isnan(walking_distances)
        valid_distances = np.array(walking_distances)[valid_indices]
        valid_points = starting_points[valid_indices]
        
        optimal_idx = np.argmin(valid_distances)
        optimal_start = valid_points[optimal_idx]
        optimal_walk = valid_distances[optimal_idx]
        
        return {
            'optimal_starting_point': optimal_start,
            'optimal_expected_walking_distance': optimal_walk,
            'starting_points': starting_points[valid_indices],
            'walking_distances': valid_distances,
            'destination': destination,
            'p_empty': p_empty,
        }
    
    def analyze_parameter_space(
        self,
        destination: float,
        p_values: List[float],
        starting_points: List[float]
    ) -> Dict:
        """
        Analyze walking distance across a parameter space.
        
        Args:
            destination: Target destination
            p_values: List of p_empty values to test
            starting_points: List of starting points to test
        
        Returns:
            Dictionary with results for heatmap visualization
        """
        results = np.zeros((len(p_values), len(starting_points)))
        
        print(f"\nAnalyzing parameter space...")
        print(f"Destination: {destination}")
        print(f"Testing {len(p_values)} p values and {len(starting_points)} starting points")
        print(f"This will take a moment...")
        
        for i, p in enumerate(p_values):
            for j, sp in enumerate(starting_points):
                try:
                    expected_walk = self.expected_walking_distance(sp, destination, p)
                    results[i, j] = expected_walk
                except ValueError:
                    results[i, j] = np.nan
            
            if (i + 1) % max(1, len(p_values) // 5) == 0:
                print(f"  Completed {i+1}/{len(p_values)} p values")
        
        return {
            'results': results,
            'p_values': p_values,
            'starting_points': starting_points,
            'destination': destination,
        }
    
    def plot_optimal_starting_point(self, analysis_result: Dict, figsize: Tuple[int, int] = (12, 6)) -> None:
        """
        Plot optimal starting point analysis.
        
        Args:
            analysis_result: Result from find_optimal_starting_point
            figsize: Figure size
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        starts = analysis_result['starting_points']
        walks = analysis_result['walking_distances']
        dest = analysis_result['destination']
        p = analysis_result['p_empty']
        optimal_start = analysis_result['optimal_starting_point']
        optimal_walk = analysis_result['optimal_expected_walking_distance']
        
        # Plot 1: Walking distance vs starting point
        axes[0].plot(starts, walks, 'o-', linewidth=2, markersize=8, color='steelblue')
        axes[0].axvline(x=optimal_start, color='red', linestyle='--', linewidth=2, label=f'Optimal: {optimal_start:.2f}')
        axes[0].axvline(x=dest, color='green', linestyle='--', linewidth=2, label=f'Destination: {dest:.2f}')
        axes[0].scatter([optimal_start], [optimal_walk], color='red', s=200, zorder=5, marker='*')
        axes[0].set_xlabel('Starting Point (position)', fontsize=12)
        axes[0].set_ylabel('Expected Walking Distance', fontsize=12)
        axes[0].set_title(f'Expected Walking Distance vs Starting Point\n(destination={dest}, p={p})', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend(fontsize=11)
        
        # Plot 2: Theoretical vs empirical
        theoretical_pos = self.theoretical_expected_position(p)
        axes[1].barh(['Theoretical\nParking Pos', 'Optimal\nStart'], 
                     [theoretical_pos, optimal_start], 
                     color=['purple', 'red'], 
                     alpha=0.7, 
                     edgecolor='black',
                     linewidth=2)
        axes[1].axvline(x=dest, color='green', linestyle='--', linewidth=2, label=f'Destination')
        axes[1].set_xlabel('Position (units)', fontsize=12)
        axes[1].set_title(f'Comparison of Positions\n(p={p})', fontsize=13, fontweight='bold')
        axes[1].legend(fontsize=11)
        axes[1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_parameter_space(self, space_result: Dict, figsize: Tuple[int, int] = (14, 8)) -> None:
        """
        Plot parameter space as heatmap.
        
        Args:
            space_result: Result from analyze_parameter_space
            figsize: Figure size
        """
        results = space_result['results']
        p_values = space_result['p_values']
        starting_points = space_result['starting_points']
        dest = space_result['destination']
        
        plt.figure(figsize=figsize)
        
        # Create heatmap
        im = plt.imshow(results, aspect='auto', origin='lower', cmap='viridis')
        
        # Set ticks and labels
        p_tick_positions = np.linspace(0, len(p_values)-1, min(6, len(p_values)), dtype=int)
        sp_tick_positions = np.linspace(0, len(starting_points)-1, min(6, len(starting_points)), dtype=int)
        
        plt.xticks(sp_tick_positions, [f'{starting_points[i]:.1f}' for i in sp_tick_positions], rotation=45)
        plt.yticks(p_tick_positions, [f'{p_values[i]:.2f}' for i in p_tick_positions])
        
        plt.xlabel('Starting Point (position)', fontsize=12)
        plt.ylabel('Probability of Empty Space (p)', fontsize=12)
        plt.title(f'Expected Walking Distance Heatmap\n(destination={dest})', fontsize=13, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im)
        cbar.set_label('Expected Walking Distance', fontsize=11)
        
        plt.tight_layout()
        plt.show()
    
    def print_analysis_summary(self, result: Dict) -> None:
        """Print summary of optimal starting point analysis."""
        print("\n" + "="*70)
        print("OPTIMAL STARTING POINT ANALYSIS")
        print("="*70)
        print(f"Destination: {result['destination']:.2f} units")
        print(f"Probability of empty space (p): {result['p_empty']}")
        print(f"\nResults:")
        print(f"  Theoretical expected parking position (1/p): {self.theoretical_expected_position(result['p_empty']):.4f}")
        print(f"  Optimal starting point: {result['optimal_starting_point']:.4f} units")
        print(f"  Expected walking distance from optimal point: {result['optimal_expected_walking_distance']:.4f} units")
        print("="*70 + "\n")
