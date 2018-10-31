from openpyxl import load_workbook

def load_teams(file):
    wb = load_workbook(filename=file, read_only=True)
    ws = wb['Sheet1']
    unique_id = 1
    team_ids = {}
    for row in ws.iter_rows(min_row=2):
        teamA = row[0].value # Name of Team A
        if teamA not in team_ids.keys():
            team_ids[teamA] = unique_id
            unique_id += 1

    return team_ids
