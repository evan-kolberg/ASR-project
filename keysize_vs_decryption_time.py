from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
import matplotlib.pyplot as plt
import time
import numpy as np

# Generate RSA key pair
def generate_key_pair(key_size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Measure decryption time for a given key pair
def measure_decryption_time(private_key, ciphertext):
    start_time = time.perf_counter()
    plaintext = private_key.decrypt(
        ciphertext,
        padding=PKCS1v15()
    )
    end_time = time.perf_counter()
    decryption_time = end_time - start_time
    return decryption_time

def main():
    key_sizes = [768, 1280, 1792, 2304, 2816, 3328, 3840,
                 4352, 4864, 5376, 5888, 6400, 6912, 7424, 7936,
                 8448, 8960, 9472, 9984, 10496]
    decryption_times = []

    for key_size in key_sizes:
        print(key_size)
        private_key, public_key = generate_key_pair(key_size)

        # Encrypt a sample message
        message = b"Hello, RSA Decryption Time!"
        ciphertext = public_key.encrypt(
            message,
            padding=PKCS1v15()
        )

        # Measure decryption time
        decryption_time = measure_decryption_time(private_key, ciphertext)
        decryption_times.append(decryption_time)

    # Exponential fit through origin (0,0)
    poly_degree = 4  # You can adjust the degree of the polynomial fit
    poly_coefficients = np.polyfit(key_sizes, decryption_times, poly_degree)
    polynomial_fit = np.polyval(poly_coefficients, key_sizes)

    # Plotting
    plt.scatter(key_sizes, decryption_times, c='blue', marker='o')
    plt.plot(key_sizes, polynomial_fit, linestyle='--', color='red', label=f'Polynomial Fit (Degree {poly_degree})')
    plt.xlabel('Key Size (bits)')
    plt.ylabel('Decryption Time (seconds)')
    plt.title('RSA Key Size vs Decryption Time')
    plt.xlim(0, max(key_sizes) + 0.1 * max(key_sizes))  # Set x-axis range starting from 0
    plt.ylim(0, max(decryption_times) + 0.1 * max(decryption_times))  # Set y-axis range
    plt.legend()
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()




