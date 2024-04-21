"""
SENG 533 Project - Group 30
Script written by Tony Vo

The log file contains information about the methods executed by the TeaStore application, with each line
written in a standardized format. The script reads the log file line by line, extracts the method information, 
and counts the different persistence types used in the application.
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set the style of the plots
sns.set_theme(style = "whitegrid")

# Function to count the different persistence types in the log file
def count_types(filepath):
    # Dictionary to store the count of each persistence type
    count = defaultdict(int)

    # Open the log file and read each line
    with open(filepath, "r") as file:
        # Iterate over each line in the file
        for line in file:
            # Split the line by the delimiter ";"
            parts = line.split(";")

            # Check if the line contains the method information
            if len(parts) > 2:
                # Extract the method part from the line
                method_part = parts[2]

                # Check if the method part contains the word "Persistence"
                if "Persistence" in method_part:
                    # Find the start and end index of the persistence type
                    start = method_part.find("Persistence")
                    end = method_part.find(".", start)
                    # Extract the persistence type from the method part
                    type = method_part[start:end]

                    # Increment the count of the persistence type
                    count[type] += 1
    
    # Return the count of each persistence type
    return count

# Path to the log file
filepath = "kieker-20240414-231103210-UTC-001.dat"
# Count the different persistence types in the log file
results = count_types(filepath)

# Create a DataFrame from the results
data = pd.DataFrame(list(results.items()), columns = ["Persistence Type", "Count"])
# Sort the DataFrame by the count of each persistence type
data = data.sort_values("Count", ascending = False)
# Reset the index of the DataFrame
data = data.reset_index().head(5)

# Plot the count of different persistence types
plt.figure(figsize = (12, 12))
bar_plot = sns.barplot(x = "Persistence Type", y = "Count", data = data, palette = "viridis", errorbar = "sd")

# Add the count of each persistence type on top of the bars, the x-axis labels, and the y-axis label
plt.title("Count of Different Persistence Types in TeaStore Log")
plt.xlabel("Persistence Type")
plt.ylabel("Count")

# Add the count of each persistence type on top of the bars
for index, row in data.iterrows():
    bar_plot.text(index, row.Count + 10, round(row.Count, 2), color = "black", va = "bottom", ha = "center")

# Rotate the x-axis labels for better readability
plt.xticks(rotation = 45)
# Adjust the plot layout to ensure all elements are visible
plt.tight_layout()
# Save the plot as a PNG file
plt.savefig("TeaStore_Persistence_Type_Counts.png")
# Display the plot
plt.show()
