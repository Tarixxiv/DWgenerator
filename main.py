import random
import json

from faker import Faker
import datetime


def write_output_file(path, line_list):
    with open("output/" + path, 'w') as file:
        for line in line_list:
            file.write(line + "\n")


def add_years(start_date, years):
    try:
        return start_date.replace(year=start_date.year + years)
    except ValueError:
        # 👇️ preserve calendar day (if Feb 29th doesn't exist
        # set to March 1st)
        return start_date + (
                date(start_date.year + years, 1, 1) - date(start_date.year, 1, 1)
        )


def get_pesel():
    return str(random.randint(1000000000000000, 9999999999999999))


if __name__ == '__main__':
    fk = Faker(["de_DE"])
    generateCount = {
        "negotiators": 50,
        "strikes_per_negotiator": 10,
        "demands_per_strike": 2,
        "dock_ocupations_per_strike": 4,
        "ship_occupations": 200
    }

    # default value
    currentCount = {
        "strikes": 0,
        "negotiators": 0,
        "demands": 0,
        "dock_occupations": 0
    }

    try:
        with open('currentCount.json', 'r') as fp:
            currentCount = json.load(fp)
    except:
        pass

    dock_count = 100
    ship_names = []
    with open("shipNames") as file:
        ship_names = [line.rstrip() for line in file]

    ship_models = []
    with open("shipModels") as file:
        ship_models = [line.rstrip() for line in file]

    demand_types = []
    with open("demandTypes") as file:
        demand_types = [line.rstrip() for line in file]
    planets = []
    with open("planets") as file:
        planets = [line.rstrip() for line in file]

    start_date = datetime.date.fromisoformat("2000-01-01")
    end_date = datetime.date.fromisoformat("2023-01-01")

    negotiators = []
    negotiators_csv = []
    strikes = []
    strikes_csv = []
    demands = []
    demand_strike = []
    dock_occupations = []

    # negotiator
    for i in range(currentCount["negotiators"], currentCount["negotiators"] + generateCount["negotiators"]):
        negotiator_name = fk.first_name()
        negotiator_surname = fk.last_name()
        negotiators.append(" ".join([negotiator_name, negotiator_surname]))
        # csv
        born_date = fk.date_between(start_date=start_date, end_date=end_date)
        employment_age = random.randint(16, 200)
        employment_date = fk.date_between(start_date=add_years(start_date, 16), end_date=add_years(end_date, 16))

        negotiators_csv.append(",".join(
            [negotiator_name, negotiator_surname, str(born_date), str(employment_date), random.choice(planets),
             get_pesel()]))

        currentCount["negotiators"] += 1
        # strike
        for j in range(currentCount["strikes"], currentCount["strikes"] + generateCount["strikes_per_negotiator"]):
            date = fk.date_between(start_date=employment_date, end_date=add_years(end_date, 16))
            strike_duration = random.randint(1, 400)
            is_peaceful = random.randint(0, 1)
            time_lost_on_force = 0
            if not is_peaceful:
                time_lost_on_force = random.randint(1, 400)
            strikes.append(
                " ".join([str(random.randint(1, 10000)), str(date),
                          str(date + datetime.timedelta(days=strike_duration)), str(i)]))
            # csv
            strikes_csv.append(
                ",".join(["strajk" + str(currentCount["strikes"] + j), str(strike_duration),
                          str(is_peaceful), str(time_lost_on_force), get_pesel()]))
            currentCount["strikes"] += 1

            # demands
            for k in range(currentCount["demands"], currentCount["demands"] + generateCount["demands_per_strike"]):
                demands.append(" ".join(["demand" + str(k), random.choice(demand_types)]))
                demand_strike.append(" ".join([str(k), str(j)]))
                currentCount["demands"] += 1

            # dock occupation
            for k in range(currentCount["dock_occupations"],
                           currentCount["dock_occupations"] + generateCount["dock_ocupations_per_strike"]):
                dock_occupations.append(" ".join([str(random.randint(1, dock_count)), str(j)]))
                currentCount["dock_occupations"] += 1

    ship_occupations = []
    # ship occupation
    for _ in range(generateCount["ship_occupations"]):
        ship_occupations.append(" ".join([random.choice(ship_names),
                                          random.choice(ship_models),
                                          str(random.randint(1, currentCount["dock_occupations"]))]))

    write_output_file("negotiators.bulk", negotiators)
    write_output_file("negotiators.csv", negotiators_csv)
    write_output_file("strikes.bulk", strikes)
    write_output_file("strikes.csv", strikes_csv)
    write_output_file("demands.bulk", demands)
    write_output_file("demand_strike.bulk", demand_strike)
    write_output_file("dock_occupations.bulk", dock_occupations)
    write_output_file("ship_occupations.bulk", ship_occupations)
    with open('currentCount.json', 'w') as fp:
        json.dump(currentCount, fp)