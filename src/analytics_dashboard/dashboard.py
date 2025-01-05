import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

class Dashboard:
    def __init__(self, data_file='dashboard_data.json'):
        self.data_file = data_file
        self.data = []
        self.load_data()

    def load_data(self):
        """Load dashboard data from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)

    def save_data(self):
        """Save dashboard data to a JSON file."""
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def update_data(self, new_data):
        """Update the dashboard with new data."""
        timestamp = datetime.now().isoformat()
        self.data.append({'timestamp': timestamp, 'data': new_data})
        self.save_data()
        self.display()

    def display(self):
        """Display the current dashboard data."""
        print("Current Dashboard Data:")
        for entry in self.data:
            print(f"Time: {entry['timestamp']}, Data: {entry['data']}")
        self.visualize_data()

    def visualize_data(self):
        """Visualize the dashboard data using matplotlib."""
        timestamps = [entry['timestamp'] for entry in self.data]
        values = [entry['data'] for entry in self.data]

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, values, marker='o')
        plt.title('Dashboard Data Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Data Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.update_data(100)  # Example data point
    dashboard.update_data(150)  # Another example data point
    dashboard.update_data(200)  # Yet another example data point
