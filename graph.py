from load_file import load_teams
from openpyxl import load_workbook

class Graph(object):
    def __init__(self, file):
        self.adj = {}

        wb = load_workbook(filename=file, read_only=True)
        ws = wb['Sheet1']
        team_ids = load_teams(file)

        for row in ws.iter_rows(min_row=2):
            teamA = row[0].value  # Name of Team A
            teamB = row[3].value # Name of Team B

            scoreA = row[1].value # Score of Team A
            scoreB = row[2].value # Score of Team B


    def connect_nodes(self, nodeA, nodeB, scoreA, scoreB):
        key_list = self.adj.keys()

        if nodeA in key_list:
            self.adj.get(nodeA)[nodeB] = scoreA

        else:
            self.adj[nodeA] = {nodeB : scoreA}

        if nodeB in key_list:
            self.adj.get(nodeB)[nodeA] = scoreB

        else:
            self.adj[nodeB] = {nodeA : scoreB}
