from random import randint
import matplotlib.pyplot as plt
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa

# Lists to store computed values for analysis and plotting
key_sizes = [2**i for i in range(9, 14)]  # Exponential growth of key sizes
key_strengths = []

def calculate_key_strength(public_key):
    return public_key.key_size * 2

def generate_key_pair(key_size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return public_key

def analyze_key_strengths(key_sizes):
    for key_size in key_sizes:
        public_key = generate_key_pair(key_size)
        strength = calculate_key_strength(public_key)
        key_strengths.append(strength)

def plot_key_strengths(key_sizes, key_strengths):
    plt.scatter(key_sizes, key_strengths, c='darkblue', marker='o')
    plt.xlabel('Key Size (bits)')
    plt.ylabel('Key Strength (bits)')
    plt.title('Key Strength vs Key Size')
    plt.ylim(0, max(key_strengths) + 1000)
    plt.xlim(0, max(key_sizes) + 1000)
    plt.grid(True)

    # Calculate the line of best fit
    fit = np.polyfit(key_sizes, key_strengths, 1)
    fit_fn = np.poly1d(fit)

    # Generate x values for the line of best fit
    x_values = np.linspace(min(key_sizes), max(key_sizes), 100)

    # Plot the line of best fit
    plt.plot(x_values, fit_fn(x_values), 'r--', label='Line of Best Fit')

    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    analyze_key_strengths(key_sizes)
    plot_key_strengths(key_sizes, key_strengths)
