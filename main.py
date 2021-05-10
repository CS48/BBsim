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

# for making a coin flip based on probability p. Such as an attack that has a 30% probability to work
def flip(p):
    return 'H' if random.random() < p else 'T'


def serialize_playerids_json(list):
    # opening the file in w mode should delete the data, so i don't have to worry about manually overwriting.
    file = 'player_ids.txt'
    filepath = os.path.abspath(os.getcwd())
    with open(os.path.join(filepath, file), 'w') as outfile:
        json.dump(list, outfile)

def serialize_gameids_json(list):
    # opening the file in w mode should delete the data, so i don't have to worry about manually overwriting.
    file = 'game_ids.txt'
    filepath = os.path.abspath(os.getcwd())
    with open(os.path.join(filepath, file), 'w') as outfile:
        json.dump(list, outfile)

def deserialize_playerids_json():
    file = 'player_ids.txt'
    filepath = os.path.abspath(os.getcwd())
    if path.exists(os.path.join(filepath, file)):
        with open(os.path.join(filepath, file)) as json_file:
            data = json.load(json_file)
        return list(data)
    else:
        print("No player id txt file.")

def deserialize_gameids_json():
    file = 'game_ids.txt'
    filepath = os.path.abspath(os.getcwd())
    if path.exists(os.path.join(filepath, file)):
        with open(os.path.join(filepath, file)) as json_file:
            data = json.load(json_file)
        return list(data)
    else:
        print("No game id txt file.")

def generate_id(list):
    if list is None:
        id = random.randint(1, 1000)
        return id
    else:
        pass

    while True:
        id = random.randint(1, 1000)
        if id in list:
            continue
        else:
            return id

def append_id(id, list):
    if list is None:
        list = [id]
        return list
    else:
        list.append(id)
        return list

def delete_id(id, list):
    if id in list:
        delete_this = list.index(id)
        del list[delete_this]
        return list
    else:
        print("Couldn't find id")

# the player class that we will use to build player objects from excel sheet data.
# it also contains some stats for tracking over the course of a game.
class Player:
    def __init__(self, arg_list):
        # player info

        self.player_id = arg_list[0]
        self.firstname = arg_list[1]
        self.lastname = arg_list[2]
        self.age = arg_list[3]
        self.position = arg_list[4]
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

        self.inside_shot = arg_list[5]
        self.mid_shot = arg_list[6]
        self.three = arg_list[7]
        self.passing = arg_list[8]
        self.handling = arg_list[9]
        self.perimeter_d = arg_list[10]
        self.interior_d = arg_list[11]
        self.blocking = arg_list[12]
        self.stealing = arg_list[13]



# creates a new sheet in the Teams spreadsheet and generates some random players for that team by entering
# data into the cells. This spreadsheet will later be read to create player objects for simming
def create_team():
    # checks to see if the "Teams" file exists. Creates one if it doesn't
    if path.exists("Teams.xlsx"):
        pass
    else:
        workbook = Workbook()
        workbook.save(filename="Teams.xlsx")

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
    team_sheet["A1"] = "player_id"
    team_sheet["B1"] = "first_name"
    team_sheet["C1"] = "last_name"
    team_sheet["D1"] = "age"
    team_sheet["E1"] = "position"
    team_sheet["F1"] = "inside_shot"
    team_sheet["G1"] = "mid_shot"
    team_sheet["H1"] = "three"
    team_sheet["I1"] = "passing"
    team_sheet["J1"] = "handling"
    team_sheet["K1"] = "perimeter_d"
    team_sheet["L1"] = "interior_d"
    team_sheet["M1"] = "blocking"
    team_sheet["N1"] = "stealing"

    # generates 5 players (one for every position) with random ratings
    for x in range(0, len(positions)):
        row = x+2

        # create_playerids_txt()
        print("hi")
        playerids = deserialize_playerids_json()
        new_id = generate_id(playerids)
        updated_list = append_id(new_id, playerids)
        serialize_playerids_json(updated_list)

        team_sheet["A%d" % row] = new_id
        team_sheet["B%d" % row] = random.choice(first_name_data)
        team_sheet["C%d" % row] = random.choice(last_name_data)
        team_sheet["D%d" % row] = random.choice(ages)
        team_sheet["E%d" % row] = positions[x]
        team_sheet["F%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["G%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["H%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["I%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["J%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["K%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["L%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["M%d" % row] = int(numpy.random.normal(50,15, 1))
        team_sheet["N%d" % row] = int(numpy.random.normal(50,15, 1))

    # saves the file, very important
    workbook.save(filename=filename)

    # Now we will to create a team records sheet to store the team's wins and losses
    if path.exists("Team_results.xlsx"):
        pass
    else:
        workbook = Workbook()
        workbook.save(filename="Team_results.xlsx")

    # I want to name the file "Team_results" and the sheet will be the name of the team.
    filename = "Team_results.xlsx"
    workbook = load_workbook(filename=filename)
    result_sheet = workbook.create_sheet(team_name)

    result_sheet["A1"] = "game_id"
    result_sheet["B1"] = "opponent"
    result_sheet["C1"] = "result"

    workbook.save(filename=filename)

    # feedback is good design ;)
    print("Team Successfully created\n")

# when we need to make player objects out of excel data, this is how we do it.
def load_team():
    # first we check that the Team file exists
    if path.exists("Teams.xlsx"):
        # then we make sure we are working in it
        filename = "Teams.xlsx"
        workbook = load_workbook(filename=filename)
        # we check that file to make sure that the team (given as an arg) is one of the sheets
        # within the file.
        while True:
            team_name = input("Which team would you like to load?:")
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
                return team, team_name
            else:
                print("That team doesn't exist in the spreadsheet, try again")
                continue

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

                # this should update the id list to make sure that it is cleared of the deleted players
                sheet = workbook[team_name]
                ids_to_delete = []
                for x in range(2, sheet.max_row + 1):
                    ids_to_delete.append(sheet["A%d" % x].value)
                id_list = deserialize_playerids_json()
                print(ids_to_delete)
                print(id_list)
                for x in ids_to_delete:
                    id_list = delete_id(x, id_list)
                serialize_playerids_json(id_list)

                workbook.remove(workbook[team_name])
                break
            else:
                print("That team doesn't exist, try again")
                continue
        # save after it's done
        workbook.save(filename=filename)

        if path.exists("Team_results.xlsx"):
            filename = "Team_results.xlsx"
            workbook = load_workbook(filename=filename)
            workbook.remove(workbook[team_name])

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


# So I'm considering a pass function. It's really not necessary in a text based sim, but i think it could be cool to
# be able to sim how the ball moves around the court. I'll have to determine how likely a pass it to happen. Maybe I'll
# create a variable called "defensive pressure" that determines how likely a pass is to happen. def_pressure could be
# determined by the defenders defense stats along with the ball handler's handling. It would also eventually need to
# consider the shot clock running down. This will be cool to code up.

# alright, so i'm just gonna try something here and see how it works
def Pass(ball_handler, active_away, active_home, away_def_assign, home_def_assign, homepossession, shot_clock):
    pass_chance = 0
    if homepossession:
        defender = away_def_assign[ball_handler]
    else:
        defender = home_def_assign[ball_handler]

    handler_shooting_avg = (ball_handler.three + ball_handler.mid_shot + ball_handler.inside_shot) / 3
    def_defense_avg = (defender.perimeter_d + defender.interior_d) / 2

    n = abs(handler_shooting_avg - def_defense_avg)

    if 0 < shot_clock <= 4:
        print("The shot is clock is running down! Shot Clock: %d" % shot_clock)
        return ball_handler
    elif shot_clock < 0:
        print("Shot clock violation! Turnover")
        return 1
    else:
        pass




    if handler_shooting_avg > def_defense_avg:
        if n >= 50:
            pass_chance = 0.20
        elif 25 <= n < 50:
            pass_chance = 0.40
        else:
            pass_chance = 0.60
    else:
        pass_chance = 0.75

    if flip(pass_chance) == 'H':
        if homepossession:
            while True:
                target = random.choice(list(active_home.values()))
                if target == ball_handler:
                    continue
                else:
                    break
            shot_clock = shot_clock - abs(int(numpy.random.normal(5, 2, 1)))
            print("%s %s passes to %s %s. Shot Clock: %d" % (ball_handler.firstname, ball_handler.lastname, target.firstname
                                                          ,target.lastname, shot_clock))
            return Pass(target, active_away, active_home, away_def_assign, home_def_assign, True, shot_clock)
        else:
            while True:
                target = random.choice(list(active_away.values()))
                if target == ball_handler:
                    continue
                else:
                    break
            shot_clock = shot_clock - abs(int(numpy.random.normal(5, 2, 1)))
            print("%s %s passes to %s %s. Shot Clock: %d" % (ball_handler.firstname, ball_handler.lastname, target.firstname
            ,target.lastname, shot_clock))
            return Pass(target, active_away, active_home, away_def_assign, home_def_assign, False, shot_clock)
    else:
        return ball_handler



        # select a team_mate besides oneself to pass to


#outcomes of a shot attempt: made shot, missed shot, air ball out of bounds, blocked shot
def shoot(shooter, defender):
    shot_score = 0
    def_score = 0

    # first i would like to determine the type of shot that they would most likely shoot based on rating.
    # For that, I would need to be able to determine how each of a player's three shooting ratings compare to each
    # other

    # 1 = close, 2 = mid, 3 = three
    shot_type = [1, 2, 3]

    # a very basic way of deciding whether a player would take more threes vs mid vs close shots
    if shooter.three >= 80 and shooter.mid_shot <= 80 and shooter.inside_shot <= 80:
        shot = random.choices(shot_type, weights=(25, 25, 50), k=1)
    elif shooter.three <= 80 and shooter.mid_shot >= 80 and shooter.inside_shot <= 80:
        shot = random.choices(shot_type, weights=(25, 50, 25), k=1)
    elif shooter.three <= 80 and shooter.mid_shot <= 80 and shooter.inside_shot >= 80:
        shot = random.choices(shot_type, weights=(50, 25, 25), k=1)
    else:
        shot = random.choices(shot_type, weights=(33, 33, 33), k=1)

    # I'm gonna do the same thing that i did with attacking in the vb sim
    # The shooter gets put into a qualitative category based on their relevant
    # shooting stat (0 = awful, 1 = bad, 2 = average, 3 = good, 4 = great). The same
    # is done for the defender. Then we determine the chance of the shooter
    # making the shot based off of that comparison.

    # determining shooter category
    # inside shot
    if shot[0] == 1:
        # output for console
        print("%s %s shoots from close range" % (shooter.firstname, shooter.lastname))

        if 0 <= shooter.inside_shot < 20:
            shot_score = shot_score + 0
        elif 20 <= shooter.inside_shot < 40:
            shot_score = shot_score + 1
        elif 40 <= shooter.inside_shot < 60:
            shot_score = shot_score + 2
        elif 60 <= shooter.inside_shot < 80:
            shot_score = shot_score + 3
        elif 80 <= shooter.inside_shot <= 100:
            shot_score = shot_score + 4
        else:
            print("shot_score error: stat not between 0 and 100")

        if 0 <= defender.interior_d < 20:
            def_score = def_score + 0
        elif 20 <= defender.interior_d < 40:
            def_score = def_score + 1
        elif 40 <= defender.interior_d < 60:
            def_score = def_score + 2
        elif 60 <= defender.interior_d < 80:
            def_score = def_score + 3
        elif 80 <= defender.interior_d <= 100:
            def_score = def_score + 4
        else:
            print("shot_score error: stat not between 0 and 100")

    # mid range shot
    elif shot[0] == 2:
        # output for console
        print("%s %s shoots from mid range" % (shooter.firstname, shooter.lastname))

        if 0 <= shooter.mid_shot < 20:
            shot_score = shot_score + 0
        elif 20 <= shooter.mid_shot < 40:
            shot_score = shot_score + 1
        elif 40 <= shooter.mid_shot < 60:
            shot_score = shot_score + 2
        elif 60 <= shooter.mid_shot < 80:
            shot_score = shot_score + 3
        elif 80 <= shooter.mid_shot <= 100:
            shot_score = shot_score + 4
        else:
            print("shot_score error: stat not between 0 and 100")

        if 0 <= ((defender.perimeter_d + defender.interior_d)/2) < 20:
            def_score = def_score + 0
        elif 20 <= ((defender.perimeter_d + defender.interior_d)/2) < 40:
            def_score = def_score + 1
        elif 40 <= ((defender.perimeter_d + defender.interior_d)/2) < 60:
            def_score = def_score + 2
        elif 60 <= ((defender.perimeter_d + defender.interior_d)/2) < 80:
            def_score = def_score + 3
        elif 80 <= ((defender.perimeter_d + defender.interior_d)/2) <= 100:
            def_score = def_score + 4
        else:
            print("shot_score error: stat not between 0 and 100")
    # three
    elif shot[0] == 3:
        # output for console
        print("%s %s shoots from three" % (shooter.firstname, shooter.lastname))

        if 0 <= shooter.three < 20:
            shot_score = shot_score + 0
        elif 20 <= shooter.three < 40:
            shot_score = shot_score + 1
        elif 40 <= shooter.three < 60:
            shot_score = shot_score + 2
        elif 60 <= shooter.three < 80:
            shot_score = shot_score + 3
        elif 80 <= shooter.three <= 100:
            shot_score = shot_score + 4
        else:
            print("shot_score error: stat not between 0 and 100")

        if 0 <= defender.perimeter_d < 20:
            def_score = def_score + 0
        elif 20 <= defender.perimeter_d < 40:
            def_score = def_score + 0
        elif 40 <= defender.perimeter_d < 60:
            def_score = def_score + 0
        elif 60 <= defender.perimeter_d < 80:
            def_score = def_score + 0
        elif 80 <= defender.perimeter_d <= 100:
            def_score = def_score + 0
        else:
            print("shot_score error: stat not between 0 and 100")

    else:
        print("Error in deciding type of shot")

    # get the success probability by calling the function and passing in the shot score and def score
    success_prob = shot_succ_prob(shot_score, def_score)

    # make a coin flip using the success probability to determine if the shot is made.
    if flip(success_prob) == 'H':
        # output for console
        print("It's good!")
        # the return will be used to determine how many points to give
        if shot[0] == 1 or shot[0] == 2:
            return 2
        elif shot[0] == 3:
            return 3
        else:
            print("error exiting shot flip")
    else:
        print("It's a missed shot")
        return 0


# convoluted bullshit. There is 100% a better method than this. Please find it.
# all it does is determine a success probability for a shot based on the qualitative category of the players' ratings.
def shot_succ_prob(shot_score, def_score):

    if shot_score == 0 and def_score == 0:
        success_prob = 0.30
    elif shot_score == 0 and def_score == 1:
        success_prob = 0.25
    elif shot_score == 0 and def_score == 2:
        success_prob = 0.20
    elif shot_score == 0 and def_score == 3:
        success_prob = 0.15
    elif shot_score == 0 and def_score == 4:
        success_prob = 0.10
    elif shot_score == 1 and def_score == 0:
        success_prob = 0.35
    elif shot_score == 1 and def_score == 1:
        success_prob = 0.30
    elif shot_score == 1 and def_score == 2:
        success_prob = 0.25
    elif shot_score == 1 and def_score == 3:
        success_prob = 0.20
    elif shot_score == 1 and def_score == 4:
        success_prob = 0.15
    elif shot_score == 2 and def_score == 0:
        success_prob = 0.40
    elif shot_score == 2 and def_score == 1:
        success_prob = 0.35
    elif shot_score == 2 and def_score == 2:
        success_prob = 0.30
    elif shot_score == 2 and def_score == 3:
        success_prob = 0.25
    elif shot_score == 2 and def_score == 4:
        success_prob = 0.20
    elif shot_score == 3 and def_score == 0:
        success_prob = 0.45
    elif shot_score == 3 and def_score == 1:
        success_prob = 0.40
    elif shot_score == 3 and def_score == 2:
        success_prob = 0.35
    elif shot_score == 3 and def_score == 3:
        success_prob = 0.30
    elif shot_score == 3 and def_score == 4:
        success_prob = 0.25
    elif shot_score == 4 and def_score == 0:
        success_prob = 0.60
    elif shot_score == 4 and def_score == 1:
        success_prob = 0.55
    elif shot_score == 4 and def_score == 2:
        success_prob = 0.50
    elif shot_score == 4 and def_score == 3:
        success_prob = 0.45
    elif shot_score == 4 and def_score == 4:
        success_prob = 0.40
    else:
        print("problem with success prob")

    return success_prob


def game_to_21(active_away, active_home, away_def_assign, home_def_assign, awaypoints, homepoints, home_possession):

    if awaypoints < 21 and homepoints < 21 or abs(awaypoints - homepoints) < 2:
        if home_possession:
            print("Home possession")
            # randomly select a ball_handler from the list of active home players
            ball_handler = random.choice(list(active_home.values()))
            shooter = Pass(ball_handler, active_away, active_home, away_def_assign, home_def_assign, home_possession, 24)
            # look at the away defensive assignments to select the right defender
            if shooter == 1:
                return game_to_21(active_away, active_home, away_def_assign, home_def_assign, awaypoints, homepoints, False)
            else:
                pass

            defender = away_def_assign[shooter]
            # call the shot function
            shot_result = shoot(shooter, defender)

            # assign points based on results
            if shot_result == 2:
                homepoints = homepoints + 2
            elif shot_result == 3:
                homepoints = homepoints + 3
            elif shot_result == 0:
                pass
            else:
                print("problem with points")

            print("\nScore:", awaypoints, homepoints, "\n")

            # recursively call the function again for the next possession
            return game_to_21(active_away, active_home, away_def_assign, home_def_assign, awaypoints, homepoints, False)

        # Away possession
        else:
            print("Away possession")
            # randomly select a ball_handler from the list of active home players
            ball_handler = random.choice(list(active_away.values()))
            shooter = Pass(ball_handler, active_away, active_home, away_def_assign, home_def_assign, home_possession,
                           24)

            if shooter == 1:
                return game_to_21(active_away, active_home, away_def_assign, home_def_assign, awaypoints, homepoints, True)
            else:
                pass

            defender = home_def_assign[shooter]
            shot_result = shoot(shooter, defender)

            if shot_result == 2:
                awaypoints = awaypoints + 2
            elif shot_result == 3:
                awaypoints = awaypoints + 3
            elif shot_result == 0:
                pass
            else:
                print("problem with points")

            print("\nScore:", awaypoints, homepoints, "\n")

            return game_to_21(active_away, active_home, away_def_assign, home_def_assign, awaypoints, homepoints, True)

    else:
        if homepoints > awaypoints:
            print("\nGame Over! Home Wins \nAway:%d Home:%d \n" % (awaypoints, homepoints))
            return 2
        else:
            print("\nGame Over! Away Wins \nAway:%d Home:%d \n" % (awaypoints, homepoints))
            return 1


# Work in progress. The actually act of simulating a game. Gonna break it down by quarters I guess.
def play():
    # make sure there is a teams file before we do anything
    if path.exists("Teams.xlsx"):
        pass
    else:
        print("There are no teams currently.")
        return 0


    # work in the teams file
    filename = "Teams.xlsx"
    workbook = load_workbook(filename=filename)
    # let the user select the two teams that are gonna play
    print("Here are the teams that are available:\n")
    show_teams()

    print("Who is the away team?")
    result = load_team()
    away_team = result[0]
    away_name = result[1]

    print("Who is the home team?")
    result = load_team()
    home_team = result[0]
    home_name = result[1]


    # I'm gonna use a dict to assign players from the team to the 5 active spots on the floor. This will be useful
    # later if you have teams of more than 5 players
    active_away = {1: None, 2: None, 3: None, 4: None, 5: None}
    active_home = {1: None, 2: None, 3: None, 4: None, 5: None}

    # assigning to active dicts
    for x in range(1, 6):
        active_away[x] = away_team[x - 1]
        active_home[x] = home_team[x - 1]

    # printing out a list to check
    print("Away team active players\n")
    for x in range(1,6):
        print("%s %s" % (active_away[x].firstname, active_away[x].lastname))
    print("\nHome team active players\n")
    for x in range(1,6):
        print("%s %s" % (active_home[x].firstname, active_home[x].lastname))


    # So this is just an idea, but i thought it would be cool to be able to assign defenders. So in order to do that,
    # you need to know what defender to reference whenever a certain player has the ball. I can do this by creating a
    # dict where the active players on one team are the keys and the active players on the other team are the values.
    # I'll need one of these for both teams because their assignments may not mirror each other.

    away_def_assign = {active_home[1]: active_away[1], active_home[2]: active_away[2], active_home[3]: active_away[3]
        , active_home[4]: active_away[4], active_home[5]: active_away[5]}
    home_def_assign = {active_away[1]: active_home[1], active_away[2]: active_home[2], active_away[3]: active_home[3]
        , active_away[4]: active_home[4], active_away[5]: active_home[5]}

    print("Away Defensive Assignments\n")
    for x in away_def_assign:
        print("%s %s : %s %s\n" % (x.firstname, x.lastname, away_def_assign[x].firstname, away_def_assign[x].lastname))
    print("Home Defensive Assignment\n")
    for x in home_def_assign:
        print("%s %s : %s %s\n" % (x.firstname, x.lastname, home_def_assign[x].firstname, home_def_assign[x].lastname))

    game_result = game_to_21(active_away, active_home, away_def_assign, home_def_assign, 0, 0, False)

    # log game result in the team_results file
    # first we need to give the game an id
    game_ids = deserialize_gameids_json()
    new_id = generate_id(game_ids)
    updated_list = append_id(new_id, game_ids)
    serialize_gameids_json(updated_list)

    # updating team results sheet for away team
    filename = "Team_results.xlsx"
    workbook = load_workbook(filename=filename)
    awayteam_sheet = workbook[away_name]
    x = awayteam_sheet.max_row + 1
    awayteam_sheet["A%d" % x] = new_id
    awayteam_sheet["B%d" % x] = home_name
    if game_result == 1:
        awayteam_sheet["C%d" % x] = "W"
    elif game_result == 2:
        awayteam_sheet["C%d" % x] = "L"
    else:
        print("problem with determining away W or L")
    workbook.save(filename=filename)

    # updating team results sheet for home team
    hometeam_sheet = workbook[home_name]
    x = hometeam_sheet.max_row + 1
    hometeam_sheet["A%d" % x] = new_id
    hometeam_sheet["B%d" % x] = away_name
    if game_result == 1:
        hometeam_sheet["C%d" % x] = "L"
    elif game_result == 2:
        hometeam_sheet["C%d" % x] = "W"
    else:
        print("problem with determining home W or L")
    workbook.save(filename=filename)



    # This section for saving stats in a game xlsx
    #if not path.exists('Game_stats.xlsx'):
       # workbook = Workbook()
        #workbook.save(filename="Game_stats.xlsx")
    #else:
     #   pass
    # makes sure that we are working in the Game_stats file
    #filename = "Game_stats.xlsx"
    #workbook = load_workbook(filename=filename)


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
            team = load_team()
            print_team(team)
            print("\n")
            continue
        elif selection == "5":
            play()
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








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
