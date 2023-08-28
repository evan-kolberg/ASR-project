import time
import multiprocessing
import matplotlib.pyplot as plt
from random import randint, sample
import numpy as np
import csv
from cryptography.hazmat.primitives.asymmetric import rsa
from sympy import primerange, gcd
from scipy.optimize import curve_fit

# Lists to store computed values for analysis and plotting
n_bit_lengths = []
average_compute_times = []

def rsa_encrypt_decrypt(M, key):
    c = pow(M, key[0]) % key[1]
    return c

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def run_protocol(I, J, r1, r2, e, n, d):
    start = time.perf_counter()

    bob_pub_key = [e, n]
    bob_priv_key = [d, n]

    N = n.bit_length()
    X = randint(0, n)

    c = rsa_encrypt_decrypt(X, bob_pub_key)
    c = c - I

    scope = r2 + r1
    n_values = [0] * (scope + 1)

    for i in range(1, len(n_values)):
        n_values[i] = rsa_encrypt_decrypt(c + i, bob_priv_key)

    m = n_values[1:]

    N = max(m).bit_length()
    prime_list = [i for i in range(2, 2 ** (N - 1)) if is_prime(i)]

    Z = [0] * (scope)
    prime = prime_list.pop()

    for i in range(0, len(m)):
        Z[i] = m[i] % prime

    is_bool = False

    while not is_bool:
        prime_found = True
        for i in range(len(m)):
            for j in range(i + 1, len(m)):
                if abs(Z[i] - Z[j]) < 2 or not (0 < Z[i] < prime - 1):
                    prime_found = False
                    break
            if not prime_found:
                break
        
        if prime_found:
            is_bool = True
        elif prime_list:
            prime = prime_list.pop()
            Z = [val % prime for val in m]
        else:
            break

    for i in range(J, len(Z)):
        Z[i] = (Z[i] + 1) % prime

    output = X % prime != Z[I - 1]
    correct = output == (I > J)
    compute_time = time.perf_counter() - start

    return compute_time

def analyze_results(csv_file):
    total_compute_time = 0
    num_total = 0

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_compute_time += float(row["Compute Time"])
            num_total += 1

    if num_total > 0:
        average_compute_time = total_compute_time / num_total
    else:
        average_compute_time = 0

    average_compute_times.append(average_compute_time)

def plot(key_sizes, average_compute_times):
    plt.scatter(key_sizes, average_compute_times, c='blue', marker='o')
    plt.xlabel('Key Size Complexity (bits)')
    plt.ylabel('Average Compute Time (seconds)')
    plt.title('Key Size Complexity vs Compute Time')
    plt.xlim(0, max(key_sizes)+.5*max(key_sizes))
    plt.ylim(0, max(average_compute_times)+.1*max(average_compute_times))
    plt.grid(True)
    # Calculate the exponential fit
    popt, _ = curve_fit(exponential_fit_func, n_bit_lengths, average_compute_times)
    a_fit, b_fit = popt
    x_values = np.linspace(min(n_bit_lengths), max(n_bit_lengths), 100)
    exp_fit_values = exponential_fit_func(x_values, a_fit, b_fit)
    
    # Plot the exponential fit curve in dashed red
    plt.plot(x_values, exp_fit_values, 'r--', label='Exponential Fit')
    
    plt.legend()
    plt.legend(loc='upper left')
    plt.show()

def generate_n(bit_size):
    # Generate a list of prime numbers with bit sizes equal to or greater than bit_size
    prime_list = list(primerange(2 ** (bit_size - 1), 2 ** bit_size))
    
    if len(prime_list) < 2:
        raise ValueError("Not enough prime numbers for the given bit size.")
    
    # Pick the first two primes from the list
    p, q = prime_list[:2]

    # Compute n by taking the product of p and q
    n = p * q

    return n, p, q

def generate_d(n, p, q):
    # Generate a random value d that is relatively prime to (p-1) and (q-1)
    phi_n = (p - 1) * (q - 1)
    while True:
        d = randint(2, n - 1)
        if gcd(d, phi_n) == 1:
            break

    return d



def exponential_fit_func(x, a, b):
    return a * np.exp(b * x)

if __name__ == '__main__':
    num_repeats = 6
    num_iterations = 10

    for i in range(num_repeats):
        n, p, q = generate_n(i + 2)
        key_size_compute_times = []  # List to store compute times for the current key size
        for _ in range(10):
            e = 17
            d = generate_d(n, p, q)

            print(f"e:{e}, n:{n}, d:{d}")

            rand = randint(0, 999999)
            csv_file = f"protocol_results~{str(rand)}.csv"

            pool = multiprocessing.Pool()

            # List to store the results of protocol iterations
            results = []

            # Run the protocol multiple times with multiprocessing
            for _ in range(num_iterations):
                I = randint(1, 100000)
                J = randint(1, 100000)
                r1 = min(I, J)
                r2 = max(I, J)

                result = pool.apply_async(run_protocol, (I, J, r1, r2, e, n, d))
                results.append(result)

            pool.close()
            pool.join()

            # Calculate the average compute time for this iteration and add it to the list
            avg_compute_time = sum(result.get() for result in results) / num_iterations
            key_size_compute_times.append(avg_compute_time)

        # Calculate the average compute time for this key size and add it to the list
        average_compute_times.append(sum(key_size_compute_times) / len(key_size_compute_times))
        n_bit_lengths.append(n.bit_length())

    plot(n_bit_lengths, average_compute_times)










