"""
Example usage of the endless road parking simulation module.
"""

from parking_simulation_endless import EndlessRoadParkingSimulator, SimulationParams
from visualization_endless import ResultsVisualizer


def main():
    """Run example parking simulations on an endless road."""
    
    print("\n" + "="*70)
    print("SCENARIO: Endless Road Parking with Destination at 50 units")
    print("="*70)
    
    # Scenario 1: High availability (p=0.8) - Easy to find parking
    print("\n--- Scenario 1: HIGH AVAILABILITY (p=0.8) ---")
    print("Most parking spaces are empty - likely to find one nearby")
    params1 = SimulationParams(
        destination_distance=50.0,
        p_empty=0.8,
        space_interval=1.0,
        num_simulations=10000
    )
    simulator1 = EndlessRoadParkingSimulator(params1)
    results1 = simulator1.run()
    simulator1.print_summary()
    
    # Scenario 2: Medium availability (p=0.5) - Moderate difficulty
    print("\n--- Scenario 2: MEDIUM AVAILABILITY (p=0.5) ---")
    print("About half the spaces are empty - mixed results")
    params2 = SimulationParams(
        destination_distance=50.0,
        p_empty=0.5,
        space_interval=1.0,
        num_simulations=10000
    )
    simulator2 = EndlessRoadParkingSimulator(params2)
    results2 = simulator2.run()
    simulator2.print_summary()
    
    # Scenario 3: Low availability (p=0.2) - Hard to find parking
    print("\n--- Scenario 3: LOW AVAILABILITY (p=0.2) ---")
    print("Few spaces are empty - likely to drive past destination")
    params3 = SimulationParams(
        destination_distance=50.0,
        p_empty=0.2,
        space_interval=1.0,
        num_simulations=10000
    )
    simulator3 = EndlessRoadParkingSimulator(params3)
    results3 = simulator3.run()
    simulator3.print_summary()
    
    # Scenario 4: Very low availability (p=0.1) - Very hard to find parking
    print("\n--- Scenario 4: VERY LOW AVAILABILITY (p=0.1) ---")
    print("Most spaces are occupied - definitely driving past destination")
    params4 = SimulationParams(
        destination_distance=50.0,
        p_empty=0.1,
        space_interval=1.0,
        num_simulations=10000
    )
    simulator4 = EndlessRoadParkingSimulator(params4)
    results4 = simulator4.run()
    simulator4.print_summary()
    
    # Visualize the key scenario
    print("\nGenerating visualizations for Scenario 2 (p=0.5)...")
    visualizer = ResultsVisualizer(results2)
    visualizer.plot_all()


if __name__ == "__main__":
    main()
