import random, re, json, requests, numpy, openpyxl, os.path
from os import path
from openpyxl import Workbook, load_workbook

ages = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
positions = ["PG", "SG", "SF", "PF", "C"]
first_name_data = ["Jacob", "Michael", "Matthew", "Joshua", "Christopher", "Nicholas", "Andrew", "Joseph", "Daniel",
                   "Tyler", "William", "Brandon", "Ryan", "John", "Zachary", "David", "Anthony", "James", "Justin",
                   "Alexander", "Jonathan", "Christian", "Austin", "Dylan", "Ethan", "Benjamin", "Noah", "Samuel",
                   "Robert", "Nathan", "Cameron", "Kevin", "Thomas", "Jose", "Hunter", "Jordan", "Kyle", "Caleb",
                   "Jason", "Logan", "Aaron", "Eric", "Brian", "Gabriel", "Adam", "Jack", "Isaiah", "Juan", "Luis",
                   "Connor", "Charles", "Elijah", "Isaac", "Steven", "Evan", "Jared", "Sean", "Timothy", "Luke",
                   "Cody", "Nathaniel", "Alex", "Seth", "Mason", "Richard", "Carlos", "Angel", "Patrick", "Devin",
                   "Bryan", "Cole"]
last_name_data = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                  "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson",
                  "White", "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez",
                  "Hall", "Young", "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson",
                  "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts"]
class Player:
    def __init__(self, playertype="None"):
        # player info
        self.firstname = random.choice(first_name_data)
        self.lastname = random.choice(last_name_data)
        self.age = random.choice(ages)
        self.position = playertype
        # stat tracking
        self.points = 0
        self.made_shots = 0
        self.shot_attempts = 0
        self.made_threes = 0
        self.three_attempts = 0
        self.assists = 0
        self.rebounds = 0
        self.blocks = 0
        self.steals = 0
        self.turnovers = 0

        # attributes generate randomly based on player type and ovr is determined by a formula that is weighted
        # differently for each position

        self.inside_shot = int(numpy.random.normal(50,15, 1))
        self.mid_shot = int(numpy.random.normal(50,15, 1))
        self.three = int(numpy.random.normal(50,15, 1))
        self.passing = int(numpy.random.normal(50,15, 1))
        self.handling = int(numpy.random.normal(50,15, 1))
        self.perimeter_d = int(numpy.random.normal(50,15, 1))
        self.interior_d = int(numpy.random.normal(50,15, 1))
        self.blocking = int(numpy.random.normal(50,15, 1))
        self.stealing = int(numpy.random.normal(50,15, 1))


def create_team_spreadsheet():
    workbook = Workbook()
    workbook.save(filename="Teams.xlsx")


def create_team():
    if path.exists("Teams.xlsx"):
        pass
    else:
        create_team_spreadsheet()

    filename = "Teams.xlsx"
    workbook = load_workbook(filename=filename)

    while True:
        team_name = input("Please enter a team name: ")
        if len(team_name) > 10:
            print("Sorry, the limit is 10 characters. Try again.")
            continue
        elif len(team_name) < 1:
            print("You didn't enter anything. Try again")
            continue
        else:
            # we're happy with the value given.
            # we're ready to exit the loop.
            break

    team_sheet = workbook.create_sheet(team_name)

    # format sheet
    team_sheet["A1"] = "first_name"
    team_sheet["B1"] = "last_name"
    team_sheet["C1"] = "age"
    team_sheet["D1"] = "position"
    team_sheet["E1"] = "inside_shot"
    team_sheet["F1"] = "mid_shot"
    team_sheet["G1"] = "three"
    team_sheet["H1"] = "passing"
    team_sheet["I1"] = "handling"
    team_sheet["J1"] = "perimeter_d"
    team_sheet["K1"] = "interior_d"
    team_sheet["L1"] = "blocking"
    team_sheet["M1"] = "stealing"



    for x in range(0, len(positions)):
        row = x+2
        team_sheet["A%d" % row] = random.choice(first_name_data)
        team_sheet["B%d" % row] = random.choice(last_name_data)
        team_sheet["C%d" % row] = random.choice(ages)
        team_sheet["D%d" % row] = positions[x]
        team_sheet["E%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["F%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["G%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["H%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["I%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["J%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["K%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["L%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["M%d" % row] = int(numpy.random.normal(50,15, 1))

    workbook.save(filename=filename)

    print("Team Successfully created\n")

def delete_team():
    if path.exists("Teams.xlsx"):
        filename = "Teams.xlsx"
        workbook = load_workbook(filename=filename)

        print("Here are the current teams...")
        print(workbook.sheetnames, "\n")
        while True:
            team_name = input("Enter team name to delete:")
            if team_name in workbook.sheetnames:
                workbook.remove(workbook[team_name])
                break
            else:
                print("That team doesn't exist, try again")
                continue

        workbook.save(filename=filename)

        print("%s has been deleted." % team_name)
    else:
        print("No teams currently.\n")

def show_teams():
    if path.exists("Teams.xlsx"):
        filename = "Teams.xlsx"
        workbook = load_workbook(filename=filename)

        print(workbook.sheetnames, "\n")
    else:
        print("No teams exist currently.\n")

def main():

    while True:
        print("Menu:\n"
              "1. Generate a Team\n"
              "2. Delete a Team\n"
              "3. See Current Teams\n"
              "4. Play a game\n"
              "5. Exit")

        selection = input("Input a number:")
        if selection == "1":
            print("Creating a team for you...")
            create_team()
            continue
        elif selection == "2":
            delete_team()
            continue
        elif selection == "3":
            show_teams()
            continue
        elif selection == "4":
            print("needs to be implemented\n")
            continue
        elif selection == "5":
            s = input("Are you sure (y/n):")
            if s == "y":
                break
            else:
                continue
        else:
            print("Invalid input, try again.\n")
            continue







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
