class UAP:

    def __init__(self):
        self.score_index = {
            "Physics": [0, 2],
            "Biotech": [0, 1],
            "Chemistry": [1],
            "Mathematics": [2],
            "Engineering": [2, 3]
        }
        self.departments = {}
        self.applications = []
        self.to_accept = int(input())

    def get_applicant(self):
        with open("applicants.txt", "r") as file:
            app_list = [app.strip("\n") for app in file.readlines()]
        for app in app_list:
            app = app.split()
            app = [f"{app[0]} {app[1]}",
                   [float(app[2]), float(app[3]), float(app[4]), float(app[5]), float(app[6])],
                   [app[7], app[8], app[9]]]
            self.applications.append(app)
            for department in app[2]:
                self.departments[department] = []
        self.departments = {k: v for k, v in sorted(self.departments.items())}

    def get_accepted(self):
        for x in range(3):
            y = 0
            while y < len(self.applications):
                person = self.applications[y]
                department = person[2][x]
                special_exam = person[1][4]
                exam_list = self.score_index[department]
                score = 0
                for exam in exam_list:  # Calculate mean score
                    exam_score = person[1][exam]
                    score += round(exam_score/(len(exam_list)), 1)
                if score < special_exam:
                    score = special_exam
                self.departments[department].append([person[0], score, person])
                y += 1
            self.check_departments()

    def check_departments(self):
        for k in self.departments.keys():
            accepted_list = []
            applicants = []
            for person in self.departments[k]:
                if person[-1] == "A":
                    accepted_list.append(person)
                else:
                    applicants.append(person)
            applicants = accepted_list + self.sort_list(applicants)
            accepted_list.clear()
            for applicant in applicants:
                if len(accepted_list) < self.to_accept:
                    if applicant[2] in self.applications:
                        self.applications.remove(applicant[2])
                    if applicant[-1] != "A":
                        applicant.append("A")
                    accepted_list.append(applicant)
                else:
                    if applicant[2] not in self.applications:
                        self.applications.append(applicant[2])
            self.departments[k] = self.sort_list(accepted_list)

    def print_accepted(self):
        for dep, accepted in self.departments.items():
            with open(f"{dep}.txt", "w") as file:
                for person in accepted:
                    file.write(f"{person[0]} {person[1]}\n")
        # print("\n" + dep)
        # for person in accepted:
        #     print(f"{person[0]} {person[1]}")

    @staticmethod
    def sort_list(unsorted_list):
        return sorted(unsorted_list, key=lambda z: (-z[1], z[0]))

    def main(self):
        self.get_applicant()
        self.get_accepted()
        self.print_accepted()


if __name__ == "__main__":
    UAP().main()
