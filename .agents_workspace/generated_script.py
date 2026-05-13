import random

def generate_and_analyze_numbers():
    """
    Generates 10 random numbers between 1 and 100,
    then calculates and returns their sum and average.
    """
    try:
        # Generate 10 random numbers between 1 and 100
        random_numbers = [random.randint(1, 100) for _ in range(10)]
        
        # Calculate sum and average
        total_sum = sum(random_numbers)
        average = total_sum / len(random_numbers)
        
        # Return results as a dictionary
        return {
            'numbers': random_numbers,
            'sum': total_sum,
            'average': average,
            'count': len(random_numbers)
        }
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def display_results(results):
    """
    Displays the analysis results in a formatted way.
    """
    if results:
        print("=" * 50)
        print("RANDOM NUMBER ANALYSIS")
        print("=" * 50)
        
        # Display the generated numbers
        print(f"\nGenerated Numbers: {results['numbers']}")
        print(f"\nNumber Count: {results['count']}")
        print(f"Sum of Numbers: {results['sum']}")
        print(f"Average: {results['average']:.2f}")
        
        # Additional statistics
        min_num = min(results['numbers'])
        max_num = max(results['numbers'])
        
        print(f"Minimum Value: {min_num}")
        print(f"Maximum Value: {max_num}")
        print(f"Range: {max_num - min_num}")
        
        print("\n" + "=" * 50)
    else:
        print("No results to display.")

if __name__ == "__main__":
    # Set seed for reproducibility (optional - comment out for true randomness)
    # random.seed(42)
    
    # Generate and analyze the numbers
    results = generate_and_analyze_numbers()
    
    # Display the results
    display_results(results)
    
    # Additional formatted output
    if results:
        print("\nDetailed Breakdown:")
        print("-" * 30)
        for i, num in enumerate(results['numbers'], 1):
            print(f"Number {i:2d}: {num:3d}")
        print("-" * 30)
        print(f"Total Sum: {results['sum']}")