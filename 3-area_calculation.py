"""Area Calculation"""

__author__ = "Ryan Milia"

""" Date: March 06, 2025
    Description:
    This module calculates the area (Ha) of burn severity levels.
    - Opens the preprocessed masked burn severity map.
    - Defines severity ranges based on burn severity levels.
    - Calculates and prints the area (Ha) covered by each severity level.
    - The areas are computed based on pixel values.
    - Produces multiple graphs to visualize the results:
      1. Bar chart of areas for each burn severity level.
      2. Histogram showing the distribution of burn severity pixel values.
      3. Boxplot to show distribution for each severity range.
"""
import numpy
import rasterio
import matplotlib.pyplot as plt

# Calculate the area of burn severity levels within a specified range
def area(low: float, high: float, array, label):
    area = numpy.logical_and(
            (low <= array), (array <= high)).sum() * (10 * 10) / 10000  # Convert to hectares
    print(f'{label}: {area} hectares')
    return area

# Function to plot the area bar chart
def plot_bar_chart(severity_levels, areas):
    plt.figure(figsize=(10, 6))
    plt.bar(severity_levels, areas, color=['blue', 'green', 'yellow', 'red'])
    plt.xlabel('Burn Severity Levels')
    plt.ylabel('Area (hectares)')
    plt.title('Area of Each Burn Severity Level')
    plt.tight_layout()
    plt.show()

# Function to plot the histogram of burn severity pixel values
def plot_histogram(data):
    plt.figure(figsize=(10, 6))
    plt.hist(data.flatten(), bins=50, color='gray', edgecolor='black')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Burn Severity Pixel Values')
    plt.tight_layout()
    plt.show()

# Function to plot the boxplot for burn severity ranges
def plot_boxplot(data, severity_ranges):
    plt.figure(figsize=(10, 6))
    plt.boxplot([data[(data >= low) & (data <= high)].flatten() for low, high in severity_ranges],
                labels=['Low', 'Moderate-low', 'Moderate-high', 'High'])
    plt.xlabel('Burn Severity Levels')
    plt.ylabel('Pixel Value')
    plt.title('Boxplot of Burn Severity Pixel Values by Severity Level')
    plt.tight_layout()
    plt.show()

input_filename = r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\masked_burn_severity.tif' 

# Open the masked burn severity raster file
with rasterio.open(input_filename) as burn_severity:
    # Read data from the burn severity raster
    data = burn_severity.read(1)
    
    # Calculate areas for each severity range
    low_area = area(0.1, 0.269, data, 'Low severity')
    moderate_low_area = area(0.27, 0.439, data, 'Moderate-low severity')
    moderate_high_area = area(0.44, 0.659, data, 'Moderate-high severity')
    high_area = area(0.66, 1.3, data, 'High severity')

# Prepare data for the graph
severity_levels = ['Low severity', 'Moderate-low severity', 'Moderate-high severity', 'High severity']
areas = [low_area, moderate_low_area, moderate_high_area, high_area]

# Plotting the graphs

# 1. Bar chart of areas for each burn severity level
plot_bar_chart(severity_levels, areas)

# 2. Histogram of pixel values in the burn severity map
plot_histogram(data)

# 3. Boxplot of pixel values for each severity range
severity_ranges = [(0.1, 0.269), (0.27, 0.439), (0.44, 0.659), (0.66, 1.3)]
plot_boxplot(data, severity_ranges)

# Save the graphs to files
plt.figure(figsize=(10, 6))
plt.bar(severity_levels, areas, color=['blue', 'green', 'yellow', 'red'])
plt.xlabel('Burn Severity Levels')
plt.ylabel('Area (hectares)')
plt.title('Area of Each Burn Severity Level')
plt.tight_layout()
plt.savefig(r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\burn_severity_area_graph.png')

plt.figure(figsize=(10, 6))
plt.hist(data.flatten(), bins=50, color='gray', edgecolor='black')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Histogram of Burn Severity Pixel Values')
plt.tight_layout()
plt.savefig(r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\burn_severity_histogram.png')

plt.figure(figsize=(10, 6))
plt.boxplot([data[(data >= low) & (data <= high)].flatten() for low, high in severity_ranges],
            labels=['Low', 'Moderate-low', 'Moderate-high', 'High'])
plt.xlabel('Burn Severity Levels')
plt.ylabel('Pixel Value')
plt.title('Boxplot of Burn Severity Pixel Values by Severity Level')
plt.tight_layout()
plt.savefig(r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\burn_severity_boxplot.png')

print("Graphs have been saved as burn_severity_area_graph.png, burn_severity_histogram.png, and burn_severity_boxplot.png")