from openpyxl import load_workbook

wb = load_workbook(filename='data.xlsx', read_only=True)
ws = wb['Sheet1']

for row in ws.iter_rows(min_row=2):
    teamA = row[0].value
    teamB = row[3].value

    scoreA = row[1].value
    scoreB = row[2].value

    print("%-25s%-20s" % (teamA, teamB))
