"""
Visualization utilities for parking simulation results.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List
from parking_simulation import SimulationResult


class ResultsVisualizer:
    """Visualize parking simulation results."""
    
    def __init__(self, results: List[SimulationResult]):
        """
        Initialize visualizer.
        
        Args:
            results: List of SimulationResult objects
        """
        self.results = results
    
    def plot_distance_histogram(self, bins: int = 30, figsize: Tuple[10, 6]) -> None:
        """
        Plot histogram of walking distances.
        
        Args:
            bins: Number of histogram bins
            figsize: Figure size tuple (width, height)
        """
        distances = [r.walking_distance for r in self.results]
        
        plt.figure(figsize=figsize)
        plt.hist(distances, bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
        plt.xlabel('Walking Distance (units)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Walking Distances')
        plt.grid(axis='y', alpha=0.3)
        plt.show()
    
    def plot_position_histogram(self, bins: int = 30, figsize: Tuple[10, 6]) -> None:
        """
        Plot histogram of parking positions.
        
        Args:
            bins: Number of histogram bins
            figsize: Figure size tuple (width, height)
        """
        positions = [r.first_available_position for r in self.results]
        
        plt.figure(figsize=figsize)
        plt.hist(positions, bins=bins, edgecolor='black', alpha=0.7, color='coral')
        plt.xlabel('Parking Position')
        plt.ylabel('Frequency')
        plt.title('Distribution of Parking Positions')
        plt.grid(axis='y', alpha=0.3)
        plt.show()
    
    def plot_combined(self, figsize: Tuple(14, 6)) -> None:
        """
        Plot both distance and position histograms side by side.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        distances = [r.walking_distance for r in self.results]
        positions = [r.first_available_position for r in self.results]
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        axes[0].hist(distances, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
        axes[0].set_xlabel('Walking Distance (units)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Distribution of Walking Distances')
        axes[0].grid(axis='y', alpha=0.3)
        
        axes[1].hist(positions, bins=30, edgecolor='black', alpha=0.7, color='coral')
        axes[1].set_xlabel('Parking Position')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Distribution of Parking Positions')
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
