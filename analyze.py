import csv
import sys
import subprocess



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
        average_compute_time = total_compute_time / num_total
        accuracy_percentage = (num_correct / num_total) * 100
    else:
        average_compute_time = 0
        accuracy_percentage = 0

    return average_compute_time, accuracy_percentage



if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit(1)

    uid = sys.argv[1]
    csv_file = f"protocol_results~{uid}.csv"
    output_file = f"analysis_results~{uid}.txt"

    average_compute_time, accuracy_percentage = analyze_results(csv_file)

    with open(output_file, mode="w") as file:
        file.write(f"Average Compute Time (per iteration): {round(average_compute_time * 1e9, -2)/1000} microseconds (100 ns precision) | {average_compute_time} seconds\n")
        file.write(f"Accuracy Percentage: {accuracy_percentage}%")


    print(f"\n\tAnalysis results recorded in '{output_file}'")


    #subprocess.run([sys.executable, "charts.py", uid, str(average_compute_time), str(accuracy_percentage)])









