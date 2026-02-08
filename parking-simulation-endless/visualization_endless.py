"""
Visualization utilities for endless road parking simulation results.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from parking_simulation_endless import SimulationResult


class ResultsVisualizer:
    """Visualize endless road parking simulation results."""
    
    def __init__(self, results: List[SimulationResult]):
        """
        Initialize visualizer.
        
        Args:
            results: List of SimulationResult objects
        """
        self.results = results
    
    def plot_parking_positions(self, figsize: Tuple[12, 6]) -> None:
        """
        Plot parking positions relative to destination.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        positions = [r.parked_position for r in self.results]
        destinations = [r.destination_position for r in self.results]
        
        plt.figure(figsize=figsize)
        
        # Plot destination line
        plt.axvline(x=destinations[0], color='red', linestyle='--', linewidth=2, label='Destination')
        
        # Plot parking positions
        plt.hist(positions, bins=50, edgecolor='black', alpha=0.7, color='steelblue', label='Parked positions')
        
        plt.xlabel('Distance (units)')
        plt.ylabel('Frequency')
        plt.title('Parking Positions Relative to Destination')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_walking_distance(self, figsize: Tuple[10, 6]) -> None:
        """
        Plot histogram of walking distances.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        distances = [r.walking_distance_total for r in self.results]
        
        plt.figure(figsize=figsize)
        plt.hist(distances, bins=50, edgecolor='black', alpha=0.7, color='coral')
        plt.xlabel('Walking Distance (units)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Walking Distances')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_before_after_distribution(self, figsize: Tuple[12, 5]) -> None:
        """
        Separate histogram for before/after destination parking.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        before_results = [r for r in self.results if r.found_before_destination]
        after_results = [r for r in self.results if not r.found_before_destination]
        
        before_distances = [r.walking_distance_total for r in before_results]
        after_distances = [r.walking_distance_total for r in after_results]
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Before destination
        axes[0].hist(before_distances, bins=30, edgecolor='black', alpha=0.7, color='green')
        axes[0].set_xlabel('Walking Distance (units)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title(f'Parked BEFORE Destination (n={len(before_results)})')
        axes[0].grid(axis='y', alpha=0.3)
        
        # After destination
        axes[1].hist(after_distances, bins=30, edgecolor='black', alpha=0.7, color='orange')
        axes[1].set_xlabel('Walking Distance (units)')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title(f'Parked AFTER Destination (n={len(after_results)})')
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_distance_past_destination(self, figsize: Tuple[10, 6]) -> None:
        """
        Plot histogram of distance past/before destination.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        distances_past = [r.distance_past_destination for r in self.results]
        
        plt.figure(figsize=figsize)
        plt.hist(distances_past, bins=50, edgecolor='black', alpha=0.7, color='purple')
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Destination (0)')
        plt.xlabel('Distance Past Destination (negative=before, positive=after)')
        plt.ylabel('Frequency')
        plt.title('Parking Distance Relative to Destination')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_all(self, figsize: Tuple(16, 12)) -> None:
        """
        Create a comprehensive 2x2 subplot visualization.
        
        Args:
            figsize: Figure size tuple (width, height)
        """
        fig = plt.figure(figsize=figsize)
        
        positions = [r.parked_position for r in self.results]
        distances = [r.walking_distance_total for r in self.results]
        distances_past = [r.distance_past_destination for r in self.results]
        before_count = sum(1 for r in self.results if r.found_before_destination)
        after_count = len(self.results) - before_count
        
        # Plot 1: Parking positions
        ax1 = plt.subplot(2, 2, 1)
        if self.results:
            ax1.axvline(x=self.results[0].destination_position, color='red', 
                        linestyle='--', linewidth=2, label='Destination')
        ax1.hist(positions, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax1.set_xlabel('Distance (units)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Parking Positions')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Plot 2: Walking distances
        ax2 = plt.subplot(2, 2, 2)
        ax2.hist(distances, bins=50, edgecolor='black', alpha=0.7, color='coral')
        ax2.set_xlabel('Walking Distance (units)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Walking Distances')
        ax2.grid(axis='y', alpha=0.3)
        
        # Plot 3: Distance past destination
        ax3 = plt.subplot(2, 2, 3)
        ax3.hist(distances_past, bins=50, edgecolor='black', alpha=0.7, color='purple')
        ax3.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax3.set_xlabel('Distance (negative=before, positive=after)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Distance Relative to Destination')
        ax3.grid(axis='y', alpha=0.3)
        
        # Plot 4: Before/After pie chart
        ax4 = plt.subplot(2, 2, 4)
        sizes = [before_count, after_count]
        labels = [f'Before\n({before_count})', f'After\n({after_count})']
        colors = ['green', 'orange']
        ax4.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax4.set_title('Parking Location Distribution')
        
        plt.tight_layout()
        plt.show()
