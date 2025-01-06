import json
import os
from datetime import datetime

class DynamicInterestRates:
    def __init__(self, storage_file='interest_rates.json'):
        self.storage_file = storage_file
        self.interest_rates = {}
        self.load_interest_rates()

    def load_interest_rates(self):
        """Load interest rates from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.interest_rates = json.load(file)

    def save_interest_rates(self):
        """Save interest rates to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.interest_rates, file)

    def set_base_rate(self, asset, base_rate):
        """Set the base interest rate for a specific asset."""
        self.interest_rates[asset] = {
            'base_rate': base_rate,
            'last_updated': datetime.now().isoformat()
        }
        self.save_interest_rates()
        return f"Base rate for {asset} set to {base_rate}%."

    def adjust_interest_rate(self, asset, market_conditions):
        """Adjust the interest rate based on market conditions."""
        if asset not in self.interest_rates:
            raise ValueError("Asset not found. Please set a base rate first.")

        base_rate = self.interest_rates[asset]['base_rate']
        adjustment_factor = self.calculate_adjustment_factor(market_conditions)
        new_rate = base_rate + adjustment_factor

        self.interest_rates[asset]['current_rate'] = new_rate
        self.interest_rates[asset]['last_updated'] = datetime.now().isoformat()
        self.save_interest_rates()
        return f"Adjusted interest rate for {asset} to {new_rate}%."

    def calculate_adjustment_factor(self, market_conditions):
        """Calculate the adjustment factor based on market conditions."""
        # Example logic for adjustment factor
        supply_demand_ratio = market_conditions.get('supply_demand_ratio', 1)
        volatility = market_conditions.get('volatility', 0)

        # Simple formula for demonstration purposes
        adjustment_factor = (supply_demand_ratio - 1) * 2 - volatility
        return adjustment_factor

    def get_current_rate(self, asset):
        """Get the current interest rate for a specific asset."""
        if asset not in self.interest_rates:
            return "Asset not found."
        return self.interest_rates[asset].get('current_rate', "Current rate not set.")

# Example usage
if __name__ == "__main__":
    interest_rate_manager = DynamicInterestRates()

    # Set base interest rates for assets
    print(interest_rate_manager.set_base_rate("PiCoin", 5.0))
    print(interest_rate_manager.set_base_rate("Ethereum", 4.5))

    # Adjust interest rates based on market conditions
    market_conditions = {
        'supply_demand_ratio': 1.2,  # Example value
        'volatility': 0.3             # Example value
    }
    print(interest_rate_manager.adjust_interest_rate("PiCoin", market_conditions))
    print(interest_rate_manager.adjust_interest_rate("Ethereum", market_conditions))

    # Get current interest rates
    print(f"Current interest rate for PiCoin: {interest_rate_manager.get_current_rate('PiCoin')}%")
    print(f"Current interest rate for Ethereum: {interest_rate_manager.get_current_rate('Ethereum')}%")
