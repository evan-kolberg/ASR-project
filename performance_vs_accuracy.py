from random import randint
import csv
import time
import subprocess
import sys
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np

# Lists to store computed values for analysis and plotting
average_compute_times = []
accuracy_percentages = []

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

    return I, J, output, correct, compute_time

def process_iteration(args):
    I, J, r1, r2, e, n, d = args
    result = run_protocol(I, J, r1, r2, e, n, d)
    return result

def analyze_results(csv_file):
    total_compute_time = 0
    num_correct = 0
    num_total = 0

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_compute_time += float(row["Compute Time"])
            num_total += 1
            if row["Correct"] == "True":
                num_correct += 1

    if num_total > 0:
        average_compute_time = total_compute_time / num_total
        accuracy_percentage = (num_correct / num_total) * 100
    else:
        average_compute_time = 0
        accuracy_percentage = 0

    average_compute_times.append(average_compute_time)
    accuracy_percentages.append(accuracy_percentage)

def plot(average_compute_times, accuracy_percentages):
    plt.scatter(average_compute_times, accuracy_percentages, c='blue', marker='o')
    plt.xlabel('Average Compute Time (seconds)')
    plt.ylabel('Average Accuracy (%)')
    plt.title('Average Compute Time vs Average Accuracy')
    plt.ylim(0, 110)
    plt.xlim(0, max(average_compute_times) + 1)
    plt.grid(True)

    # Calculate the line of best fit
    fit = np.polyfit(average_compute_times, accuracy_percentages, 1)
    fit_fn = np.poly1d(fit)

    # Generate x values for the line of best fit
    x_values = np.linspace(min(average_compute_times), max(accuracy_percentages), 100)

    # Plot the line of best fit
    plt.plot(x_values, fit_fn(x_values), 'r--', label='Line of Best Fit')

    # Place the legend in the bottom left corner
    plt.legend(loc='lower left')
    
    plt.show()


if __name__ == '__main__':
    num_repeats = 100

    for _ in range(num_repeats):
        e = 17
        n = 3233
        d = 413

        num_iterations = 10

        rand = randint(0, 999999)
        csv_file = f"protocol_results~{str(rand)}.csv"

        pool = multiprocessing.Pool()

        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["I", "J", "Output", "Correct", "Compute Time"])
            
            iteration_args = []

            for _ in range(num_iterations):
                I = randint(1, 100000)
                J = randint(1, 100000)

                r1 = min(I, J)
                r2 = max(I, J)

                iteration_args.append((I, J, r1, r2, e, n, d))

            results = pool.map(process_iteration, iteration_args)

            for result in results:
                writer.writerow(result)

        pool.close()
        pool.join()

        analyze_results(csv_file)

    plot(average_compute_times, accuracy_percentages)
