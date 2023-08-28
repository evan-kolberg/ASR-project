from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
import matplotlib.pyplot as plt
import time

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
    key_sizes = [2**i for i in range(9, 15)]
    decryption_times = []

    for key_size in key_sizes:
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

    # Plotting
    plt.plot(key_sizes, decryption_times, marker='o', linestyle='-', color='blue')
    plt.xlabel('Key Size (bits)')
    plt.ylabel('Decryption Time (seconds)')
    plt.title('RSA Key Size vs Decryption Time')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
