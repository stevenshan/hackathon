import json

with open("data/session.json", "r") as file:
	sessions = json.load(file)

for session in sessions:
	details = session["report"]["sessionalarmdetails"]
	print(details["site"], details["alarmtype"], details["alarmvalue"], session["path"])