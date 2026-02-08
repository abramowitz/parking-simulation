"""
Example analysis of optimal starting points for parking.
"""

import sys
sys.path.insert(0, '/content/parking-simulation')

from parking_analyzer import ParkingAnalyzer
import numpy as np


def main():
    """Run analysis examples."""
    
    analyzer = ParkingAnalyzer(num_simulations=3000)
    
    # Example 1: Find optimal starting point for given p
    print("\n" + "="*70)
    print("EXAMPLE 1: OPTIMAL STARTING POINT FOR GIVEN PROBABILITY")
    print("="*70)
    
    destination = 100.0
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    results_list = []
    for p in p_values:
        result = analyzer.find_optimal_starting_point(
            destination=destination,
            p_empty=p,
            search_range=(0, destination - 1),
            num_points=15
        )
        results_list.append(result)
        analyzer.print_analysis_summary(result)
        analyzer.plot_optimal_starting_point(result)
    
    # Summary table
    print("\n" + "="*70)
    print("SUMMARY TABLE: OPTIMAL STARTING POINTS FOR DIFFERENT p VALUES")
    print("="*70)
    print(f"\nDestination: {destination}")
    print(f"{'p_empty':<10} {'Theory (1/p)':<15} {'Optimal Start':<15} {'Expected Walk':<15}")
    print("-" * 55)
    
    for result in results_list:
        p = result['p_empty']
        theory = analyzer.theoretical_expected_position(p)
        optimal_start = result['optimal_starting_point']
        expected_walk = result['optimal_expected_walking_distance']
        print(f"{p:<10.2f} {theory:<15.4f} {optimal_start:<15.4f} {expected_walk:<15.4f}")
    
    # Example 2: Parameter space analysis
    print("\n\n" + "="*70)
    print("EXAMPLE 2: PARAMETER SPACE ANALYSIS")
    print("="*70)
    
    p_space = np.linspace(0.1, 0.9, 6)
    starting_points = np.linspace(0, destination - 1, 15)
    
    space_result = analyzer.analyze_parameter_space(
        destination=destination,
        p_values=p_space,
        starting_points=starting_points
    )
    
    analyzer.plot_parameter_space(space_result)
    
    # Example 3: Specific scenario
    print("\n\n" + "="*70)
    print("EXAMPLE 3: DETAILED ANALYSIS FOR SPECIFIC SCENARIO")
    print("="*70)
    print("Scenario: Shopping mall with destination 80 units away")
    print("Parking availability: 70% (p=0.7)")
    
    specific_result = analyzer.find_optimal_starting_point(
        destination=80.0,
        p_empty=0.7,
        search_range=(0, 79),
        num_points=20
    )
    
    analyzer.print_analysis_summary(specific_result)
    analyzer.plot_optimal_starting_point(specific_result, figsize=(14, 6))
    
    print("\n✓ Analysis complete!")


if __name__ == "__main__":
    main()
