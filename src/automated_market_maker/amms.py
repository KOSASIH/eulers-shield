class LiquidityPool:
    def __init__(self, token_a, token_b):
        self.token_a = token_a
        self.token_b = token_b
        self.liquidity_a = 0
        self.liquidity_b = 0

    def add_liquidity(self, amount_a, amount_b):
        """Add liquidity to the pool."""
        self.liquidity_a += amount_a
        self.liquidity_b += amount_b
        return f"Added {amount_a} {self.token_a} and {amount_b} {self.token_b} to the pool."

    def remove_liquidity(self, amount_a, amount_b):
        """Remove liquidity from the pool."""
        if amount_a > self.liquidity_a or amount_b > self.liquidity_b:
            return "Insufficient liquidity to remove."
        
        self.liquidity_a -= amount_a
        self.liquidity_b -= amount_b
        return f"Removed {amount_a} {self.token_a} and {amount_b} {self.token_b} from the pool."

    def get_reserves(self):
        """Get current reserves of the pool."""
        return {
            'token_a': self.liquidity_a,
            'token_b': self.liquidity_b
        }

    def swap(self, amount_in, token_in):
        """Perform a swap between tokens in the pool."""
        if token_in == self.token_a:
            amount_out = self.calculate_amount_out(amount_in, self.liquidity_a, self.liquidity_b)
            self.liquidity_a += amount_in
            self.liquidity_b -= amount_out
            return f"Swapped {amount_in} {self.token_a} for {amount_out} {self.token_b}."
        elif token_in == self.token_b:
            amount_out = self.calculate_amount_out(amount_in, self.liquidity_b, self.liquidity_a)
            self.liquidity_b += amount_in
            self.liquidity_a -= amount_out
            return f"Swapped {amount_in} {self.token_b} for {amount_out} {self.token_a}."
        else:
            return "Invalid token for swap."

    def calculate_amount_out(self, amount_in, reserve_in, reserve_out):
        """Calculate the amount of output token received for a given input amount."""
        # Simple constant product formula: x * y = k
        # Assuming a 0.3% fee on swaps
        fee = 0.003
        amount_in_with_fee = amount_in * (1 - fee)
        numerator = amount_in_with_fee * reserve_out
        denominator = reserve_in + amount_in_with_fee
        return numerator / denominator

class AMM:
    def __init__(self):
        self.pools = {}

    def create_pool(self, token_a, token_b):
        """Create a new liquidity pool."""
        pool_key = (token_a, token_b)
        if pool_key in self.pools:
            return "Pool already exists."
        
        self.pools[pool_key] = LiquidityPool(token_a, token_b)
        return f"Liquidity pool created for {token_a} and {token_b}."

    def add_liquidity(self, token_a, token_b, amount_a, amount_b):
        """Add liquidity to an existing pool."""
        pool_key = (token_a, token_b)
        if pool_key not in self.pools:
            return "Pool does not exist."
        
        return self.pools[pool_key].add_liquidity(amount_a, amount_b)

    def remove_liquidity(self, token_a, token_b, amount_a, amount_b):
        """Remove liquidity from an existing pool."""
        pool_key = (token_a, token_b)
        if pool_key not in self.pools:
            return "Pool does not exist."
        
        return self.pools[pool_key].remove_liquidity(amount_a, amount_b)

    def swap(self, token_in, amount_in):
        """Perform a swap in the appropriate pool."""
        for pool_key, pool in self.pools.items():
            if token_in in pool_key:
                return pool.swap(amount_in, token_in)
        
        return "No suitable pool found for the swap."

    def get_pool_reserves(self, token_a, token_b):
        """Get reserves of a specific pool."""
        pool_key = (token_a, token_b)
        if pool_key not in self.pools:
            return "Pool does not exist."
        
        return self.pools[pool_key].get_reserves()

# Example usage
if ```python
__name__ == "__main__":
    amm = AMM()
    print(amm.create_pool('ETH', 'DAI'))  # Create a new liquidity pool
    print(amm.add_liquidity('ETH', 'DAI', 10, 2000))  # Add liquidity to the pool
    print(amm.swap('ETH', 1))  # Swap 1 ETH for DAI
    print(amm.get_pool_reserves('ETH', 'DAI'))  # Get current reserves of the pool
    print(amm.remove_liquidity('ETH', 'DAI', 5, 1000))  # Remove liquidity from the pool
