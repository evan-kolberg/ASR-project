from random import randint
import csv
import time
import subprocess
import sys

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

    start_time = time.perf_counter()

    m = bob_step1(J, e, n)
    p, W = alice(m, d, n)
    x = bob_step2(p, W)
    output = x == W[I - 1]

    end_time = time.perf_counter() - start_time

    correct = output == (I > J)

    return I, J, output, correct, end_time



# Faux inputs
e = 3
n = 77
d = 27

# Number of iterations for testing
num_iterations = 1000000



# File to record results
rand = randint(0, 9999999999)
csv_file = f"protocol_results~{str(rand)}.csv"

if __name__ == '__main__':
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["I", "J", "Output", "Correct", "Total Compute Time"])

        for _ in range(num_iterations):
            result = run_protocol(e, n, d)
            writer.writerow(result)

    print(f"\n\tProtocol results recorded in 'protocol_results~{rand}.csv'")



    subprocess.run([sys.executable, "analyze.py", str(rand)])











