import json
import csv

def main():
    average = []
    peak = []
    date = []
    with open('data/session.json') as session_data:
        reports = json.load(session_data)
        for report in reports:
            try:
                logs = report['report']['sessionalarmdetails']['data']['singlesensorlog']
                for log in logs:
                    rows = log['readings']['singlesensorrow']
                    for row in rows:
                        average.append(row['average'])
                        peak.append(row['peak'])
                        date.append(row['dateoccurred'])
            except:
                pass

    with open('average.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(average)
    with open('peak.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(peak)
    with open('date.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(date)

if __name__ == "__main__":
    main()
