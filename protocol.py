from random import randint
import csv
import time
import subprocess
import sys
import multiprocessing


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

    bobPubKey = [e, n]
    bobPrivKey = [d, n]

    N = n.bit_length()
    X = randint(0, n)

    c = rsa_encrypt_decrypt(X, bobPubKey)
    c = c - I

    scope = r2 + r1
    n = [0] * (scope + 1)

    for i in range(1, len(n)):
        n[i] = rsa_encrypt_decrypt(c + i, bobPrivKey)

    m = n[1:]

    N = max(m).bit_length()
    prime_list = [i for i in range(2, 2 ** (N - 1)) if is_prime(i)]

    Z = [0] * (scope)
    prime = prime_list.pop()

    for i in range(0, len(m)):
        Z[i] = m[i] % prime

    bool = False

    while not bool:
        prime_found = True
        for i in range(len(m)):
            for j in range(i + 1, len(m)):
                if abs(Z[i] - Z[j]) < 2 or not (0 < Z[i] < prime - 1):
                    prime_found = False
                    break
            if not prime_found:
                break
        
        if prime_found:
            bool = True
        elif prime_list:
            prime = prime_list.pop()
            Z = [val % prime for val in m]
        else:
            break


    for i in range(J, len(Z)):
        Z[i] = (Z[i] + 1) % prime

    
    if X % prime == Z[I - 1]:
        output = False 
    else:
        output = True

    correct = output == (I > J)
    compute_time = time.perf_counter() - start

    return I, J, output, correct, compute_time


def process_iteration(args):
    I, J, r1, r2, e, n, d = args
    result = run_protocol(I, J, r1, r2, e, n, d)
    return result

if __name__ == '__main__':
    start = time.perf_counter()

    e = 17
    n = 3233
    d = 413

    num_iterations = 20

    rand = randint(0, 999999)
    csv_file = f"protocol_results~{str(rand)}.csv"

    pool = multiprocessing.Pool()

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["I", "J", "Output", "Correct", "Compute Time"])
        
        iteration_args = []

        for i in range(num_iterations):
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

    time_elapsed = time.perf_counter()-start

    print(f"\tProtocol results recorded in 'protocol_results~{rand}.csv'")
    subprocess.run([sys.executable, "analyze.py", str(rand), str(time_elapsed)])







