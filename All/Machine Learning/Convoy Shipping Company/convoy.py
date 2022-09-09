import pandas as pd
import json
import sqlite3
import re


def check_csv(df, f_n):
    count = 0
    for col in df:
        for row in range(len(df)):
            if isinstance(df.iloc[row][col], str):
                df.at[row, col], x = re.subn(r"\s?[a-z\._\s]+\s?", "", df.iloc[row][col])
                count += x
    f_n = f_n.partition(".")[0] + "[CHECKED].csv"
    df.to_csv(f_n, encoding='utf-8')
    print(f"{count} cell{' was' if count == 1 else 's were'} corrected in {f_n}")
    return f_n


def convert_to_sql(df, f_n):
    sql_name = f_n.replace("[CHECKED].csv", ".s3db")
    conn = sqlite3.connect(sql_name)
    cursor = conn.cursor()
    create_table = """CREATE TABLE convoy(
                    vehicle_id INTEGER PRIMARY KEY,
                    engine_capacity INTEGER NOT NULL,
                    fuel_consumption INTEGER NOT NULL,
                    maximum_load INTEGER NOT NULL,
                    score INTEGER NOT NULL);"""
    cursor.execute(create_table)
    ınsert_convoy = """INSERT INTO convoy
                    (vehicle_id, engine_capacity, fuel_consumption, maximum_load, score)
                    VALUES (?, ?, ?, ?, 0)"""
    df = df.astype(str)
    cursor.executemany(ınsert_convoy, df.values)
    select_all = "SELECT * FROM convoy"
    vehicles = cursor.execute(select_all).fetchall()
    total_rec = 0
    for vehicle in vehicles:
        new_score = get_vehicle_score(vehicle)
        cursor.execute("""UPDATE convoy SET score = ? WHERE vehicle_id = ?""", (new_score, vehicle[0]))
        total_rec += 1
    print(f"{total_rec} record{' was' if total_rec == 1 else 's were'} inserted into {sql_name}")
    conn.commit()
    conn.close()
    return sql_name


def sql_to_json_xml(f_n):
    conn = sqlite3.connect(f_n)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM convoy")
    json_list = {"convoy": []}
    xml_list = {"convoy": []}
    rows = cursor.fetchall()
    for row in rows:
        vehicle = {}
        vehicle_score = 0
        for i in range(len(row)):
            if cursor.description[i][0] == "score":
                vehicle_score = row[i]
            else:
                vehicle[cursor.description[i][0]] = row[i]
        if vehicle_score > 3:
            json_list["convoy"].append(vehicle)
        else:
            xml_list["convoy"].append(vehicle)
    j_len = len(json_list['convoy'])
    json_obj = json.dumps(json_list, indent=4)
    json_name = f_n.replace(".s3db", ".json")
    with open(json_name, "w", encoding="utf-8") as json_out:
        json_out.write(json_obj)
    print(f"{j_len} vehicle{' was' if j_len == 1 else 's were'} saved into {json_name}")
    # ------------ XML ------------
    xml_name = f_n.replace(".s3db", ".xml")
    with open(xml_name, "w", encoding="utf-8") as xml_out:
        indent = 0
        for key, value in xml_list.items():
            xml_out.write(f"{indent * ' '}<{key}>\n")
            indent += 4
            for item in value:
                xml_out.write(f"{indent * ' '}<vehicle>\n")
                indent += 4
                for col, val in item.items():
                    xml_out.write(f"{indent * ' '}<{col}>{val}</{col}>\n")
                indent -= 4
                xml_out.write(f"{indent * ' '}</vehicle>\n")
            indent -= 4
            xml_out.write(f"{indent * ' '}</{key}>\n")
    x_len = len(xml_list['convoy'])
    print(f"{x_len} vehicle{' was' if x_len == 1 else 's were'} saved into {xml_name}")


def get_vehicle_score(vehicle):
    score = 0
    distance = 450
    max_vehicle_dist = vehicle[1] / vehicle[2] * 100
    pitstop_count = distance / max_vehicle_dist
    consumed_fuel = vehicle[2] * distance / 100
    if pitstop_count <= 1:
        score += 2
    elif pitstop_count <= 2:
        score += 1
    if consumed_fuel <= 230:
        score += 2
    else:
        score += 1
    if vehicle[3] >= 20:
        score += 2
    return score


def get_file():
    file_name = input("Input file name\n")
    if file_name.endswith("xlsx"):
        dataframe = pd.read_excel(file_name, sheet_name="Vehicles", dtype=str)
        file_name = file_name.partition(".")[0] + ".csv"
        dataframe.to_csv(file_name, index=None, header=True)
        l_f = len(dataframe)
        print(f"{l_f} {'line was' if l_f == 1 else 'lines were'} added to {file_name}")

    if file_name.endswith("csv"):
        dataframe = pd.read_csv(file_name)
        if "[CHECKED]" not in file_name:
            file_name = check_csv(dataframe, file_name)
        file_name = convert_to_sql(dataframe, file_name)

    sql_to_json_xml(file_name)  # already ends with .s3db


get_file()
