# Parking Simulation

A Monte Carlo simulation for analyzing walking distance after parking a car in the first available empty space.

## Problem Statement

You arrive at a parking lot with `n` parking spaces arranged in a line. Each space is independently empty with probability `p`. You park in the first available (empty) space. What is the expected walking distance from the lot entrance to your parked car?

## Mathematical Background

Given:
- `n` total parking spaces
- Each space is empty with probability `p` (independently)
- You park in the first available empty space

The position of the first available space follows a geometric distribution (approximately) when `p` is not too small.

Expected position ≈ `1/p` (for large lots)

## Installation

```bash
pip install numpy matplotlib
```

## Usage

### Basic Example

```python
from parking_simulation import ParkingSimulator, SimulationParams

# Create simulation parameters
params = SimulationParams(
    num_spaces=100,      # 100 parking spaces
    p_empty=0.8,         # 80% chance each space is empty
    num_simulations=10000 # Run 10,000 simulations
)

# Run simulation
simulator = ParkingSimulator(params)
results = simulator.run()

# Print summary statistics
simulator.print_summary()
```

### With Visualization

```python
from parking_simulation import ParkingSimulator, SimulationParams
from visualization import ResultsVisualizer

params = SimulationParams(num_spaces=100, p_empty=0.5, num_simulations=10000)
simulator = ParkingSimulator(params)
results = simulator.run()

visualizer = ResultsVisualizer(results)
visualizer.plot_combined()
```

## Running Tests

```bash
python -m unittest test_parking_simulation.py
```

## Results

The simulation demonstrates that:

1. **Higher probability of empty spaces** → Closer average parking position
2. **Lower probability of empty spaces** → Farther average parking position
3. Expected position ≈ `1/p` for reasonable parameters

Example results:
- p = 0.2: Average distance ≈ 5
- p = 0.5: Average distance ≈ 2-3
- p = 0.8: Average distance ≈ 1-2

## Files

- `parking_simulation.py` - Core simulation module
- `visualization.py` - Plotting utilities
- `example.py` - Example usage scenarios
- `test_parking_simulation.py` - Unit tests
- `README.md` - This file

## License

MIT
