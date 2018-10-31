from load_file import load_teams
from openpyxl import load_workbook

class Graph(object):
    def __init__(self, file):
        self.adj = {}

        wb = load_workbook(filename=file, read_only=True)
        ws = wb['Sheet1']
        team_ids = load_teams(file)
        self.id_to_team_name = self.__get_id_to_team__(team_ids)

        for row in ws.iter_rows(min_row=2):
            teamA = row[0].value  # Name of Team A
            teamB = row[3].value  # Name of Team B

            scoreA = row[1].value  # Score of Team A
            scoreB = row[2].value  # Score of Team B

            self.__connect_nodes__(team_ids.get(teamA), team_ids.get(teamB), scoreA, scoreB)

    def __get_id_to_team__(self, team_ids):
        id_to_team = {}
        for key, value in team_ids.items():
            id_to_team[value] = key

        return id_to_team

    def __connect_nodes__(self, nodeA, nodeB, scoreA, scoreB):
        key_list = self.adj.keys()

        if nodeA in key_list:
            self.adj.get(nodeA)[nodeB] = scoreA

        else:
            self.adj[nodeA] = {nodeB : scoreA}

        if nodeB in key_list:
            self.adj.get(nodeB)[nodeA] = scoreB

        else:
            self.adj[nodeB] = {nodeA : scoreB}

    #  Prints the graph for testing purposes.
    def print_graph(self):
        for key, value in self.adj.items():
            print("%-20s" % self.id_to_team_name.get(key))

            for key2, value2 in value.items():
                print("%-20sTeam %10s:%10s" % ("", self.id_to_team_name.get(key2), value2))

    def get_ranking_of(self, teamA):
        pass

graph = Graph("data.xlsx")
graph.print_graph()