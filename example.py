"""
Example usage of the parking simulation module.
"""

from parking_simulation import ParkingSimulator, SimulationParams
from visualization import ResultsVisualizer


def main():
    """Run example parking simulations."""
    
    # Scenario 1: High availability (p=0.8)
    print("\n--- Scenario 1: High Availability (p=0.8) ---")
    params1 = SimulationParams(
        num_spaces=100,
        p_empty=0.8,
        num_simulations=10000
    )
    simulator1 = ParkingSimulator(params1)
    results1 = simulator1.run()
    simulator1.print_summary()
    
    # Scenario 2: Medium availability (p=0.5)
    print("\n--- Scenario 2: Medium Availability (p=0.5) ---")
    params2 = SimulationParams(
        num_spaces=100,
        p_empty=0.5,
        num_simulations=10000
    )
    simulator2 = ParkingSimulator(params2)
    results2 = simulator2.run()
    simulator2.print_summary()
    
    # Scenario 3: Low availability (p=0.2)
    print("\n--- Scenario 3: Low Availability (p=0.2) ---")
    params3 = SimulationParams(
        num_spaces=100,
        p_empty=0.2,
        num_simulations=10000
    )
    simulator3 = ParkingSimulator(params3)
    results3 = simulator3.run()
    simulator3.print_summary()
    
    # Visualize results
    print("Generating visualizations...")
    visualizer = ResultsVisualizer(results2)
    visualizer.plot_combined()


if __name__ == "__main__":
    main()
