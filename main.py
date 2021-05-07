import random, re, json, requests, numpy, openpyxl, os.path
from os import path
from openpyxl import Workbook, load_workbook

# some lists for later use
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

# the player class that we will use to build player objects from excel sheet data.
# it also contains some stats for tracking over the course of a game.
class Player:
    def __init__(self, arg_list):
        # player info
        self.firstname = arg_list[0]
        self.lastname = arg_list[1]
        self.age = arg_list[2]
        self.position = arg_list[3]
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

        self.inside_shot = arg_list[4]
        self.mid_shot = arg_list[5]
        self.three = arg_list[6]
        self.passing = arg_list[7]
        self.handling = arg_list[8]
        self.perimeter_d = arg_list[9]
        self.interior_d = arg_list[10]
        self.blocking = arg_list[11]
        self.stealing = arg_list[12]

# this creates a xlsx file in the same directory as main.py. I have it set to be named "Teams" by default
def create_team_spreadsheet():
    workbook = Workbook()
    workbook.save(filename="Teams.xlsx")

# creates a new sheet in the Teams spreadsheet and generates some random players for that team by entering
# data into the cells. This spreadsheet will later be read to create player objects for simming
def create_team():
    # checks to see if the "Teams" file exists. Creates one if it doesn't
    if path.exists("Teams.xlsx"):
        pass
    else:
        create_team_spreadsheet()

    # makes sure that we are working in the Teams file
    filename = "Teams.xlsx"
    workbook = load_workbook(filename=filename)

    # asks for a name for the new team, and puts some limitations on the input.
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
    # the team name ends up as the name of the sheet within the Teams file
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


    # generates 5 players (one for every position) with random ratings
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

    # saves the file, very important
    workbook.save(filename=filename)

    # feedback is good design ;)
    print("Team Successfully created\n")

# when we need to make player objects out of excel data, this is how we do it.
def load_team(team_name):
    # first we check that the Team file exists
    if path.exists("Teams.xlsx"):
        # then we make sure we are working in it
        filename = "Teams.xlsx"
        workbook = load_workbook(filename=filename)
        # we check that file to make sure that the team (given as an arg) is one of the sheets
        # within the file.
        if team_name in workbook.sheetnames:
            # If it exists, we select that sheet
            sheet = workbook[team_name]
            # this will be a list of player objects
            team = []
            # for each row in that sheet, which represents a player, we make a player object by
            # putting the data from that row into a list and feeding that list into Player() as
            # an arg. Then we put that player in the team list
            for x in range(2, sheet.max_row + 1):
                for value in sheet.iter_rows(min_row=x, max_row=x, values_only=True):
                    arg_list = list(value)
                player = Player(arg_list)
                team.append(player)
            # return the team, so that we can do something with it.
            return team

        else:
            print("That team doesn't exist in the spreadsheet, try again")
            return 1

# this is moreso a check than anything else. Just want to see that the player objects are
# successfully made from the excel sheet data
def print_team(team):
    for x in team:
        print(x.firstname, x.lastname)
        print(x.position, "\n")

        print("Inside Shot:", x.inside_shot)
        print("Mid Shot:", x.mid_shot)
        print("Three:", x.three )
        print("Passing:", x.passing)
        print("Handling:", x.handling)
        print("Perimeter D:", x.perimeter_d )
        print("Interior D:", x.interior_d)
        print("Blocking:", x.blocking )
        print("Stealing:", x.stealing, "\n")

# This will delete a sheet of data (effectively a team) from the Team file
def delete_team():
    # Check to make sure the Team file exists
    if path.exists("Teams.xlsx"):
        filename = "Teams.xlsx"
        workbook = load_workbook(filename=filename)

        # Show a list of the current sheets (Teams)
        print("Here are the current teams...")
        print(workbook.sheetnames, "\n")
        while True:
            # enter the name of a team to delete it
            team_name = input("Enter team name to delete:")
            if team_name in workbook.sheetnames:
                workbook.remove(workbook[team_name])
                break
            else:
                print("That team doesn't exist, try again")
                continue
        # save after it's done
        workbook.save(filename=filename)
        # feedback is good design
        print("%s has been deleted." % team_name)
    else:
        print("No teams currently.\n")

def show_teams():
    # for checking the sheets (Teams) in the Teams file
    if path.exists("Teams.xlsx"):
        filename = "Teams.xlsx"
        workbook = load_workbook(filename=filename)

        print(workbook.sheetnames, "\n")
    else:
        print("No teams exist currently.\n")


def main():
    # This is effectively a console based menu that keeps running until you exit it
    # the menu options are selected by entering a number that corresponds with that option.
    # Run main() and give it a try.
    while True:
        print("Menu:\n"
              "1. Generate a Team\n"
              "2. Delete a Team\n"
              "3. See Current Teams\n"
              "4. Load Teams\n"
              "5. Play a game\n"
              "6. Exit")

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
            print("Current Teams:")
            show_teams()
            s = input("Which would you like to load?:")
            team = load_team(s)
            if team == 1:
                continue
            else:
                print_team(team)
                print("\n")
                continue
        elif selection == "5":
            print("needs to be implemented\n")
            continue
        elif selection == "6":
            s = input("Are you sure (y/n):")
            if s == "y":
                break
            else:
                continue
        else:
            print("Invalid input, try again.\n")
            continue

# Work in progress. The actually act of simulating a game. Gonna break it down by quarters I guess.
def play_quarter():





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
