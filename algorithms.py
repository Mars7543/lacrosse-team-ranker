from classes import Level
from excel_functions import load_file, write_file
from datetime import datetime


def process_data(filename):
    start = datetime.now()

    print("Processing Data...")
    team_manager = load_file(filename)

    print("%.1fs" % (datetime.now() - start).total_seconds())

    return team_manager


def calculate_rankings(team_manager, alg):
    # reset team points before calculations
    team_manager.reset()
    teams = team_manager.get_teams()

    # print progress bar line
    print("_"*54)

    # loop through teams
    for i, team in enumerate(teams):
        # create a level_manager for the current team
        level_manager = Level(team, alg)

        # get first level
        level = level_manager.get_next_level()

        # while levels still exist calculate points
        while len(level_manager.current_level) > 0:
            for team_info in level:
                points = 0

                if alg == "win": # points = the sum of the wins (+1 for win -1 for loss) / games played
                    points += sum(team_info["won"])/len(team_info["won"])

                    if points == 0:
                        points += team_info["prev_streak"]

                elif alg == "score": # points = the sum of the points earned by the team
                    points += sum(team_info["score"])/len(team_info["score"])

                elif alg == "score_win":
                    points = sum(team_info["score"])/len(team_info["score"])

                    if points != 0:
                        points/= abs(points)

                team.points += points # add calculated points

            level = level_manager.get_next_level() # get next level

        if i % 4 == 0:
            print("█", end="")

    return team_manager.get_rankings() # return list of ranked teams


def run_win_alg(team_manager):
    start = datetime.now()
    print("\nRunning Win Algorithm...")

    teams = calculate_rankings(team_manager, "win")
    write_file(teams, "win.xlsx")

    print("\n\n%.1fs" % (datetime.now() - start).total_seconds())


def run_score_alg(team_manager):
    start = datetime.now()
    print("\nRunning Score Algorithm...")

    teams = calculate_rankings(team_manager, "score")
    write_file(teams, "score.xlsx")

    print("\n\n%.1fs" % (datetime.now() - start).total_seconds())


def run_score_win_alg(team_manager):
    start = datetime.now()
    print("\nRunning Score-Win Algorithm...")

    teams = calculate_rankings(team_manager, "score_win")
    write_file(teams, "score_win.xlsx")

    print("\n\n%.1fs" % (datetime.now() - start).total_seconds())
