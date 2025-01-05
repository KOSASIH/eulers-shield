class FeeAdjuster:
    def __init__(self, base_fee=0.01, dynamic_adjustment_factor=0.001):
        self.base_fee = base_fee  # Base fee in USD
        self.dynamic_adjustment_factor = dynamic_adjustment_factor  # Factor for dynamic adjustment

    def calculate_fee(self, transaction_amount, network_conditions=None):
        """
        Calculate the transaction fee based on the transaction amount and network conditions.
        
        :param transaction_amount: The amount of the transaction in USD.
        :param network_conditions: Optional; a dictionary containing network conditions.
        :return: Calculated fee in USD.
        """
        # Start with the base fee
        fee = self.base_fee

        # Adjust fee based on transaction amount
        if transaction_amount > 1000:  # Example threshold for high-value transactions
            fee += transaction_amount * 0.005  # 0.5% fee for high-value transactions
        else:
            fee += transaction_amount * 0.01  # 1% fee for lower-value transactions

        # Dynamic adjustment based on network conditions
        if network_conditions:
            if network_conditions.get('congestion') == 'high':
                fee += self.dynamic_adjustment_factor * 2  # Increase fee during high congestion
            elif network_conditions.get('congestion') == 'low':
                fee -= self.dynamic_adjustment_factor  # Decrease fee during low congestion

        # Ensure the fee is not negative
        return max(fee, 0)

    def set_base_fee(self, new_base_fee):
        """Set a new base fee."""
        self.base_fee = new_base_fee

    def set_dynamic_adjustment_factor(self, new_factor):
        """Set a new dynamic adjustment factor."""
        self.dynamic_adjustment_factor = new_factor

# Example usage
if __name__ == "__main__":
    fee_adjuster = FeeAdjuster()

    # Example transaction amounts and network conditions
    transaction_amounts = [500, 1500, 2000]
    network_conditions = [
        {'congestion': 'low'},
        {'congestion': 'high'},
        {'congestion': 'normal'}
    ]

    for amount in transaction_amounts:
        for conditions in network_conditions:
            fee = fee_adjuster.calculate_fee(amount, conditions)
            print(f"Transaction Amount: ${amount}, Network Conditions: {conditions}, Calculated Fee: ${fee:.2f}")
