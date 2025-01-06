import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class UserBehaviorAnalytics:
    def __init__(self, activity_log_file='user_activity_log.json'):
        self.activity_log_file = activity_log_file
        self.activity_log = []
        self.load_activity_log()

    def load_activity_log(self):
        """Load user activity log from a JSON file."""
        if os.path.exists(self.activity_log_file):
            with open(self.activity_log_file, 'r') as file:
                self.activity_log = json.load(file)

    def save_activity_log(self):
        """Save user activity log to a JSON file."""
        with open(self.activity_log_file, 'w') as file:
            json.dump(self.activity_log, file)

    def log_activity(self, user_id, activity_type, details):
        """Log user activity."""
        activity_record = {
            'user_id': user_id,
            'activity_type': activity_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.activity_log.append(activity_record)
        self.save_activity_log()

    def get_user_activity(self, user_id):
        """Get all activities for a specific user."""
        user_activities = [activity for activity in self.activity_log if activity['user_id'] == user_id]
        return user_activities

    def generate_activity_report(self):
        """Generate a report of user activities."""
        df = pd.DataFrame(self.activity_log)
        report = df.groupby(['user_id', 'activity_type']).size().reset_index(name='counts')
        return report

    def visualize_activity(self):
        """Visualize user activity data."""
        df = pd.DataFrame(self.activity_log)
        if df.empty:
            print("No activity data available for visualization.")
            return

        activity_counts = df['activity_type'].value_counts()
        plt.figure(figsize=(10, 5))
        activity_counts.plot(kind='bar', color='skyblue')
        plt.title('User Activity Distribution')
        plt.xlabel('Activity Type')
        plt.ylabel('Number of Activities')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    analytics = UserBehaviorAnalytics()

    # Log some user activities
    analytics.log_activity("user123", "Deposit", {"amount": 1000})
    analytics.log_activity("user123", "Vote", {"proposal_id": 1, "vote": "for"})
    analytics.log_activity("user456", "Withdraw", {"amount": 500})

    # Get user activity
    user_activities = analytics.get_user_activity("user123")
    print(f"User Activities for user123: {user_activities}")

    # Generate activity report
    report = analytics.generate_activity_report()
    print("Activity Report:")
    print(report)

    # Visualize activity
    analytics.visualize_activity()
