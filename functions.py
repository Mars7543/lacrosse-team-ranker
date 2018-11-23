from classes import Team, Game, TeamManager, Level
from excel_functions import load_file, write_file
from copy import deepcopy
from datetime import datetime
import test


def process_data(filename):
    start = datetime.now()

    print("Processing Data...")
    team_manager = load_file(filename)

    end = datetime.now()
    print("%.1fs" % (end - start).total_seconds())

    return team_manager


def calculate_rankings(team_manager, alg):
    # reset team points before calculations
    team_manager.reset()
    teams = team_manager.get_teams()

    # print progress bar line
    for i in range(54):
        print("_", end="")

    print()

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

    end = datetime.now()
    print("\n\n%.1fs" % (end - start).total_seconds())


def run_score_alg(team_manager):
    start = datetime.now()
    print("\nRunning Score Algorithm...")

    teams = calculate_rankings(team_manager, "score")
    write_file(teams, "score.xlsx")

    end = datetime.now()
    print("\n\n%.1fs" % (end - start).total_seconds())


def run_score_win_alg(team_manager):
    start = datetime.now()
    print("\nRunning Score-Win Algorithm...")

    teams = calculate_rankings(team_manager, "score_win")
    write_file(teams, "score_win.xlsx")

    end = datetime.now()
    print("\n\n%.1fs" % (end - start).total_seconds())


def main(time_check=False):
    start = datetime.now()

    team_manager = process_data("data.xlsx")

    run_win_alg(team_manager)
    run_score_alg(team_manager)
    run_score_win_alg(team_manager)

    end = datetime.now()
    print("\nElapsed Time: %.1fs" % (end - start).total_seconds())


main(time_check=True)