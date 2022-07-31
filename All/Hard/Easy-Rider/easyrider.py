import json
import re


class EasyRider:

    def __init__(self):
        self.data_fields = {
            "bus_id": int,
            "stop_id": int,
            "stop_name": str,
            "next_stop": int,
            "stop_type": str,
            "a_time": str
        }
        self.data = None

    def find_errors(self):
        needed = ["stop_name", "stop_type", "a_time"]
        errors = {key: 0 for key in needed}
        total_error = 0
        for k, v in self.data_fields.items():
            for bus in self.data:
                bus_value = bus[k]
                if k == "stop_type":
                    if not isinstance(bus_value, str) or len(bus_value) > 0 and bus_value not in ["S", "O", "F"]:
                        errors[k] += 1
                        total_error += 1
                elif k == "stop_name":
                    pattern = r"^[A-Z].*(Road|Avenue|Boulevard|Street)$"
                    if not isinstance(bus_value, str) or not re.match(pattern, bus_value):
                        errors[k] += 1
                        total_error += 1
                elif k == "a_time":
                    pattern = r"^([0-1][0-9]|2[0-3]):([0-5][0-9])$"
                    if not isinstance(bus_value, str) or not re.match(pattern, bus_value):
                        errors[k] += 1
                        total_error += 1
        print(f"Type and required field validation: {total_error} errors")
        [print(f"{k}: {v}") for k, v in errors.items()]

    def find_line_stops(self):
        line_stops = {}
        for bus in self.data:
            line = bus["bus_id"]
            stop = bus["stop_id"]
            if line in line_stops:
                line_stops[line].append(stop)
            else:
                line_stops[line] = [stop]
        print("Line names and number of stops:")
        for k, v in line_stops.items():
            print(f"bus_id: {k}, stops: {len(v)}")

    def find_special_stops(self):
        buses = {}
        got_error = False
        all_stops = []
        start_stops = []
        finish_stops = []
        transfer_stops = []
        for bus in self.data:
            bus_id = bus["bus_id"]
            stop_name = bus["stop_name"]
            stop_type = bus["stop_type"]
            if bus_id not in buses:
                buses[bus_id] = [[stop_name], [stop_type]]
            else:
                buses[bus_id][0].append(stop_name)
                buses[bus_id][1].append(stop_type)
        for bus, stops in buses.items():
            has_start = False
            has_finish = False
            stop_names = stops[0]
            stop_types = stops[1]
            for x in range(len(stop_names)):
                stop_name = stop_names[x]
                stop_type = stop_types[x]
                if stop_type == "S":
                    has_start = True
                    if stop_name not in start_stops:
                        start_stops.append(stop_name)
                elif stop_type == "F":
                    has_finish = True
                    if stop_name not in finish_stops:
                        finish_stops.append(stop_name)

                if stop_name in all_stops:
                    if stop_name not in transfer_stops:
                        transfer_stops.append(stop_name)
                else:
                    all_stops.append(stop_name)
            if not has_start or not has_finish:
                got_error = True
                print(f"There is no start or end stop for the line: {bus}.")
                break
        if not got_error:
            start_stops.sort()
            transfer_stops.sort()
            finish_stops.sort()
            print(f"Start stops: {len(start_stops)} {start_stops}")
            print(f"Transfer stops: {len(transfer_stops)} {transfer_stops}")
            print(f"Finish stops: {len(finish_stops)} {finish_stops}")

    def check_on_demand_stops(self):
        all_stops = {}
        wrong_stops = []
        for bus in self.data:
            stop_name = bus["stop_name"]
            stop_type = bus["stop_type"]
            if stop_name not in all_stops:
                all_stops[stop_name] = stop_type
            else:
                saved_stop_type = all_stops[stop_name]
                if saved_stop_type == "O" or stop_type == "O" and saved_stop_type != stop_type:
                    if stop_name not in wrong_stops:
                        wrong_stops.append(stop_name)
        print("On demand stops test:")
        if wrong_stops:
            wrong_stops.sort()
            print(f"Wrong stop type: {wrong_stops}")
        else:
            print("OK")

    def check_arrival_times(self):
        current_bus_id = None
        last_stop_time = 0
        time_anomalies = {}
        for bus in self.data:
            if bus["bus_id"] != current_bus_id:
                current_bus_id = bus["bus_id"]
                last_stop_time = 0
            current_stop_time = self.convert_time(bus["a_time"])
            if current_stop_time <= last_stop_time:
                if current_bus_id in time_anomalies:
                    time_anomalies[current_bus_id].append(bus["stop_name"])
                else:
                    time_anomalies[current_bus_id] = [bus["stop_name"]]
            else:
                last_stop_time = current_stop_time
        print("Arrival time test:")
        if time_anomalies:
            for bus, anomalies in time_anomalies.items():
                print(f"bus_id line {bus}: wrong time on station {anomalies[0]}")
        else:
            print("OK")

    @staticmethod
    def convert_time(arrive_time):
        arrive_time = arrive_time.split(":")
        hours, minutes = int(arrive_time[0]), int(arrive_time[1])
        total_time = 60 * hours + minutes
        return total_time

    def main(self):
        i = input()
        self.data = json.loads(i)
        # self.find_errors()
        # self.find_line_stops()
        # self.find_special_stops()
        # self.check_arrival_times()
        self.check_on_demand_stops()


if __name__ == "__main__":
    EasyRider().main()
