class Team():
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.games = []

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def get_games(self):
        return self.games

    def add_game(self, game):
        self.games.append(game)

    def __str__(self):
        return self.name + " | " + ("%.2f" % self.points)

    def __eq__(self, other):
        return self.get_name() == other.get_name()


class Game():
    def __init__(self, teamA, teamB, scoreA, scoreB):
        self.teamA = teamA
        self.teamB = teamB

        self.scoreA = scoreA
        self.scoreB = scoreB

    def get_opponent(self, team):
        return self.teamA if self.teamB == team else self.teamB

    def get_score_difference(self, team):
        if team == self.teamA:
            score = self.scoreA - self.scoreB

        else:
            score = self.scoreB - self.scoreA

        if score > 10:
            return 10
        elif score < -10:
            return -10
        else:
            return score

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


class TeamManager():
    def __init__(self):
        self.teams = [] # list of team objects
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

    def get_rankings(self):
        return sorted(self.teams, key=lambda team: team.points, reverse=True)

    def reset(self):
        for team in self.teams:
            team.points = 0

        return self.teams

    def print_teams(self):
        teams = sorted(self.teams, key=lambda team: team.points, reverse=True)

        place = 1
        previous = Team("Empty")

        print("%-30s%-6s\n" % ("Team:", "Points:"))

        for team in teams:
            place_team = ""

            if previous.points == team.points:
                place_team = ": " + team.get_name()
            else:
                place_team = str(place) + " " + team.get_name()

            print("%-30s%-6.2f" % (place_team, team.get_points()))

            place += 1
            previous = team


class Level():
    def __init__(self, team, alg):
        self.team = team # starting team to calculate levels

        self.current_teams = []

        # level is a list with dictionaries containing info on a team (e.g. team, outcome of previous game, etc)
        self.current_level = [{ "team" : self.team }]

        self.checked_teams = [] # used to prevent calculating relationships to the same team multiple times

        self.alg = alg

    def get_next_level(self):
        if self.alg == "win":
            return self.win()

        elif self.alg == "score":
            return self.score()

        elif self.alg == "score_win":
            return self.score()

    # all algorithms perform bfs (breadth-first search) but only keep teams that the alg deems valid


    def win(self):
        self.current_teams = [] # empty list of currently viewed teams (used for updating a team's info if it appears mulitple times)
        next_level = [] # empty list containing information for next level which will replace current level

        # keep looping through the level until all elements have been taken out and the next level has been created
        while len(self.current_level) > 0:
            # get info about current_team
            current_team_info = self.current_level.pop(0)

            current_team = current_team_info["team"]

            # streak will be a 1 if all of the past games were wins or a -1 if the past games were all losses
            streak = current_team_info.get("streak", 0)

            games_played = current_team.get_games()

            self.checked_teams.append(current_team.get_name()) # add team to list of checked teams so it won't get checked again

            # loop through each game the current team played
            for game in games_played:
                opponent = game.get_opponent(current_team) # get opponent

                # if the opponent has not been viewed in the past levels, it can be checked
                if opponent.get_name() not in self.checked_teams:

                    """
                    won is a list containing the outcome of the games the current team played with the opponent
                    if the opponent won, the list will contain a -1 (so the current team loses a point)
                    if the opponent lost won, the list will contain a +1 (so the current team gains a point)
                    """

                    won = -1 if game.get_winner() == opponent else 1

                    # if the opposing team was already viewed in the level update its current information
                    if opponent.get_name() in self.current_teams:
                        index = self.current_teams.index(opponent.get_name())
                        next_level[index]["won"].append(won)

                    # if the outcome follows the streak (or it is the first level), add the team to the next level
                    elif won == streak or not streak:
                        next_level.append({"team": opponent, "won": [won], "streak": won, "prev_streak": streak})
                        self.current_teams.append(opponent.get_name())

        """
        teams that have been checked can still be in the level if it is added from a team's game but also in the level
        for example:
            if team b plays teams c and  d and the level is as follows [b, c, d],
                the next level would end up as [c, d, teams that c played, teams that d played] 
            
        this would cause teams c and d to be evaluated for a second time even though they were placed in the checked list 
        """
        for team_info in next_level: # only add teams that aren't in the list of checked teams to the next level
            team = team_info["team"].get_name()
            if team not in self.checked_teams:
                if 1 in team_info["won"] and -1 in team_info["won"]:
                    team_info["streak"] = 0
                self.current_level.append(team_info)

        return self.current_level

    def score(self):
        self.current_teams = []
        next_level = []

        while len(self.current_level) > 0:
            current_team_info = self.current_level.pop(0)
            current_team = current_team_info["team"]

            # extreme used to check with teams can be added to the next level as it will be between +10 and -10 points (inclusive)
            extreme = current_team_info.get("extreme")

            games_played = current_team.get_games()

            self.checked_teams.append(current_team.get_name())

            for game in games_played:
                opponent = game.get_opponent(current_team)

                if opponent.get_name() not in self.checked_teams:
                    score = game.get_score_difference(current_team) # get how many points the current team won or lost by

                    # update team if it is already in the next level
                    if opponent.get_name() in self.current_teams:
                        index = self.current_teams.index(opponent.get_name())
                        next_level[index]["score"].append(score)

                    # only add the team to the next level if it is valid (see score alg description)
                    elif not((extreme == 10 and score < 0) or (extreme == -10 and score > 0)):
                        if extreme != 10 and extreme != -10:
                            extreme = score

                        next_level.append({"team": opponent, "score": [score], "extreme": extreme})
                        self.current_teams.append(opponent.get_name())

        # add valid teams to the level
        for team_info in next_level:
            team = team_info["team"].get_name()

            # make sure team has not already been checked
            if team not in self.checked_teams:

                # check if there is a +10 and a negative score or a -10 and a positive score for a given team
                if 10 in team_info["score"]:
                    for score in team_info["score"]:
                        if score < 0:
                            continue

                elif -10 in team_info["score"]:
                    for score in team_info["score"]:
                        if score > 0:
                            continue

                # append the team_info to the level if it is valid
                self.current_level.append(team_info)

        return self.current_level

    def __str__(self):
        str = "["

        for team_info in self.current_level:
            str += team_info["team"].get_name() + ", "

        if len(str) > 1:
            str = str[:-2]

        str += "]"

        return str