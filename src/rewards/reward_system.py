import json
import os
from datetime import datetime

class RewardSystem:
    def __init__(self, storage_file='user_rewards.json'):
        self.storage_file = storage_file
        self.user_rewards = {}
        self.load_rewards()

    def load_rewards(self):
        """Load user rewards from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.user_rewards = json.load(file)

    def save_rewards(self):
        """Save user rewards to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.user_rewards, file)

    def register_user(self, user_id):
        """Register a new user in the reward system."""
        if user_id not in self.user_rewards:
            self.user_rewards[user_id] = {
                'total_rewards': 0,
                'activities': []
            }
            self.save_rewards()
            return f"User {user_id} registered successfully."
        return f"User {user_id} already exists."

    def log_activity(self, user_id, activity_type, points):
        """Log user activity and calculate rewards."""
        if user_id not in self.user_rewards:
            return "User not found. Please register first."

        self.user_rewards[user_id]['total_rewards'] += points
        activity_record = {
            'activity_type': activity_type,
            'points': points,
            'timestamp': datetime.now().isoformat()
        }
        self.user_rewards[user_id]['activities'].append(activity_record)
        self.save_rewards()
        return f"Activity logged for user {user_id}: {activity_type} with {points} points."

    def get_user_rewards(self, user_id):
        """Get the total rewards and activities for a user."""
        if user_id not in self.user_rewards:
            return "User not found."
        return self.user_rewards[user_id]

    def distribute_rewards(self):
        """Distribute rewards to users based on their activities."""
        for user_id, data in self.user_rewards.items():
            # Example logic for distributing rewards
            if data['total_rewards'] > 1000:
                bonus = 100  # Bonus for high engagement
                data['total_rewards'] += bonus
                self.log_activity(user_id, 'Bonus Distribution', bonus)
        self.save_rewards()

# Example usage
if __name__ == "__main__":
    reward_system = RewardSystem()

    # Register users
    print(reward_system.register_user("user123"))
    print(reward_system.register_user("user456"))

    # Log activities
    print(reward_system.log_activity("user123", "Participated in governance vote", 50))
    print(reward_system.log_activity("user123", "Provided liquidity", 200))
    print(reward_system.log_activity("user456", "Staked tokens", 300))

    # Get user rewards
    print(reward_system.get_user_rewards("user123"))
    print(reward_system.get_user_rewards("user456"))

    # Distribute rewards
    reward_system.distribute_rewards()
    print(reward_system.get_user_rewards("user123"))
