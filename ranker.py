from functions import *
from sys import argv


def main(file):
    start = datetime.now()

    team_manager = process_data(file)

    run_win_alg(team_manager)
    run_score_alg(team_manager)
    run_score_win_alg(team_manager)

    end = datetime.now()
    print("\nElapsed Time: %.1fs" % (end - start).total_seconds())


try:
    main(argv[1])
except IndexError:
    print ("Error: No Datafile Specified\nFormat: python ranker.py filename.ext")