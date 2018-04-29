import json
import csv

def main():
    average = []
    peak = []
    date = []
    site = []
    with open('data/periodic.json') as session_data:
        reports = json.load(session_data)
        for report in reports:
            try:
                logs = report['report']['instrumentlog']['logentries']['instrumentrow']
                for log in logs:
                    datetime = log['dateoccured']
                    rows = log['readings']
                    for row in rows:
                        sen = row['sensorreading']
                        site.append(sen['site'])
                        average.append(sen['average'])
                        peak.append(sen['peak'])
                        date.append(datetime)
            except:
                pass

    with open('average_p.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(average)
    with open('peak_p.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(peak)
    with open('date_p.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(date)
    with open('site_p.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(site)

if __name__ == "__main__":
    main()
