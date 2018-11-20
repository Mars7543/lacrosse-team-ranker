from openpyxl import load_workbook


class Team():
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.games = []

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def get_games(self):
        return self.games

    def add_game(self, game):
        self.games.append(game)

    def __str__(self):
        return self.name + " | " + str(self.points) + " Points"


class Game():
    def __init__(self, teamA, teamB, scoreA, scoreB):
        self.teamA = teamA
        self.teamB = teamB

        self.scoreA = scoreA
        self.scoreB = scoreB

    def get_teamA(self):
        return self.teamA

    def get_teamB(self):
        return self.teamB

    def get_scoreA(self):
        return self.teamA

    def get_scoreB(self):
        return self.teamB

    # return team w/ greater points or None if the match was a tie
    def get_winner(self):
        if self.scoreA > self.scoreB:
            return self.teamA

        elif self.scoreB > self.scoreA:
            return self.teamB

        else:
            return None


    def __str__(self):
        result = "Tie Game"

        if self.get_winner():
            result = self.get_winner().get_name() + " Won!"

        return self.teamA.get_name() + " vs. " + self.teamB.get_name() + "\n" \
               + str(self.scoreA) + " to " + str(self.scoreB) + "\n" \
               + result + "\n"


class Manager():
    def __init__(self):
        self.teams = [] # list of team objects
        self.games = [] # list of game objects

        self.__team_names = []  # list of team names added --used to prevent adding duplicate teams

    def get_teams(self):
        return self.teams

    def get_team(self, team_name):
        try: # if team exists return it
            return self.teams[self.__team_names.index(team_name)]
        except:
            return None

    def add_team(self, team):
        if team.get_name() not in self.__team_names: # if the team has not already been added to the list of teams then add it
            self.teams.append(team)
            self.__team_names.append(team.get_name())
        else:  # if it already existed then update it
            self.teams[self.__team_names.index(team.get_name())] = team

    def get_games(self):
        return self.games

    def add_game(self, game):
        self.games.append(game)

    def print_teams(self):
        teams = sorted(self.teams, key=lambda team: team.points, reverse=True)

        place = 1
        previous = None

        for team in teams:
            if place != 1:
                if previous.points == team.points:
                    print("|", team)
            else:
                print(place, team)

            place += 1
            previous = team

