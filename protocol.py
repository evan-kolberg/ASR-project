from random import randint
import csv
import timeit


def rsa_encrypt(plaintext, e, n):
    return pow(plaintext, e, n)

def rsa_decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

def find_random_prime(limit):
    while True:
        candidate = randint(1, limit)
        if is_prime(candidate):
            return candidate

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def bob_step1(j, e, n):
    x = randint(1, n)
    c = rsa_encrypt(x, e, n)
    m = (c - j + 1) % n
    return m

def alice(m, d, n):
    Y = [rsa_decrypt((m + i - 1) % n, d, n) for i in range(1, 11)]
    p = find_random_prime(n // 2)
    Z = [y % p for y in Y]
    I = 5
    W = [(z + 1) % p if i > I else z for i, z in enumerate(Z, start=1)]
    return p, W

def bob_step2(p, W):
    I = 5
    x = W[I - 1]
    return x % p


def run_protocol(e, n, d):
    I = randint(0, 9)
    J = randint(0, 9)

    m = bob_step1(J, e, n)

    start_time = timeit.default_timer()
    p, W = alice(m, d, n)
    alice_time = timeit.default_timer() - start_time

    start_time = timeit.default_timer()
    x = bob_step2(p, W)
    bob_time = timeit.default_timer() - start_time

    output = x == W[I - 1]
    correct = output == (I > J)

    return I, J, output, correct, alice_time + bob_time


def analyze_results(csv_file):
    total_compute_time = 0
    num_correct = 0
    num_total = 0

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_compute_time += float(row["Total Compute Time"])
            num_total += 1
            if row["Correct"] == "True":
                num_correct += 1

    if num_total > 0:
        average_compute_time = (total_compute_time / num_total) * 1000000
        accuracy_percentage = (num_correct / num_total) * 100
    else:
        average_compute_time = 0
        accuracy_percentage = 0

    return average_compute_time, accuracy_percentage


# Faux inputs
e = 3
n = 77
d = 27

rand = randint(1, 9999999999)

# Number of iterations for testing
num_iterations = 1000000

# CSV file to record results
csv_file = f"protocol_results{str(rand)}.csv"
output_file = f"analysis_results{str(rand)}.txt"


if __name__ == '__main__':
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["I", "J", "Output", "Correct", "Total Compute Time"])

        for _ in range(num_iterations):
            result = run_protocol(e, n, d)
            writer.writerow(result)

    print(f"\n\n\tProtocol results recorded in '{csv_file}'")
    average_compute_time, accuracy_percentage = analyze_results(csv_file)

    # Save the printed output to a file
    with open(output_file, mode="w") as output_file:
        output_file.write(f"Protocol results recorded in '{csv_file}'\n")
        output_file.write(f"Average Compute Time (per iteration): {average_compute_time} microseconds\n")
        output_file.write(f"Accuracy Percentage: {accuracy_percentage}%\n\n")

    print(f"\tAverage Compute Time (per iteration): {average_compute_time} microseconds")
    print(f"\tAccuracy Percentage: {accuracy_percentage}%\n\n")








