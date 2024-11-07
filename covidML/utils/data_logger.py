import csv

def log_result(gender, asthma, fever, prediction, actual_result):
    """Log the prediction and the actual result to a CSV."""
    with open('covid_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([gender, asthma, fever, prediction, actual_result])

