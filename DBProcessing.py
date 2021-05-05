import json
from datetime import date, timedelta
import random
import csv


with open('aemet_db.json') as f:
    aemet_db_raw = json.load(f)

historic_avg_dict = {}
measures_by_date = {}
for measure in aemet_db_raw:
    date_obj = date.fromisoformat(measure["fecha"])
    tMax = float(measure["tmax"].replace(",","."))
    measure_clean = {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day, "week": date_obj.strftime("%a"), "actual": tMax}
    measures_by_date[date_obj] = measure_clean

    key = f"{date_obj.month}-{date_obj.day}"
    if key in historic_avg_dict:
        historic_avg_dict[key].append(tMax)
    else:
        historic_avg_dict[key] = [tMax]

for keyDay, values in historic_avg_dict.items():
    historic_avg_dict[keyDay] = round((sum(values) / len(values)), 2)

for date, measure in measures_by_date.items():
    key = f"{date.month}-{date.day}"
    measures_by_date[date]["average"] = historic_avg_dict[key]
    measures_by_date[date]["friend"] = round(historic_avg_dict[key] + random.randint(-5, 5), 2)
    try:
        measures_by_date[date]["temp_1"] = measures_by_date[date - timedelta(days=1)]["actual"]
    except KeyError:
        measures_by_date[date]["temp_1"] = measures_by_date[date - timedelta(days=0)]["actual"]
    try:
        measures_by_date[date]["temp_2"] = measures_by_date[date - timedelta(days=2)]["actual"]
    except KeyError:
        measures_by_date[date]["temp_2"] = measures_by_date[date]["temp_1"]


with open('aemet_db_tidy.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["year", "month", "day", "week", "temp_2", "temp_1", "average", "actual", "friend"])
    for date, measure in measures_by_date.items():
        writer.writerow([measures_by_date[date]["year"], measures_by_date[date]["month"], measures_by_date[date]["day"],
                         measures_by_date[date]["week"], measures_by_date[date]["temp_2"], measures_by_date[date]["temp_1"],
                         measures_by_date[date]["average"], measures_by_date[date]["actual"], measures_by_date[date]["friend"]])
