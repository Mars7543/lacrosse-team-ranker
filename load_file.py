from openpyxl import load_workbook

def load_teams(file):
    # load excel sheet into an iterable object
    wb = load_workbook(filename=file, read_only=True)
    ws = wb['Sheet1']

    # each team will have a unique id which will be stored in a dictionary
    unique_id = 1
    team_ids = {}

    # loop through every row
    for row in ws.iter_rows(min_row=2):
        teamA = row[0].value # Name of Team A

        # if the team isn't in the dictionary add it with an id
        if teamA not in team_ids.keys():
            team_ids[teamA] = unique_id
            unique_id += 1

    return team_ids
