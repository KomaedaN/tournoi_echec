from tinydb import TinyDB, Query

User = Query()

db = TinyDB("db_player.json")
players_table = db.table("players")


class Player:
    def __init__(self, name, first_name, birthday, gender):  # players table
        self.id = (len(players_table) + 1)
        self.name = name
        self.first_name = first_name
        self.birthday = birthday
        self.gender = gender
        self.rank = (len(TinyDB("db_player.json").table("players")) + 1)
        self.score = 0.0
        self.elo = 0.0
        self.players_versus = []

    def get_serialized_player(self):  # insert serialized player
        serialized_player = {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
            "elo": self.elo,
            "players_versus": self.players_versus
        }
        players_table.insert(serialized_player)

    def update_players_rank(self):  # update rank based on elo
        pass

    @staticmethod
    def get_players_data():  # get players data for tournament creation
        players = players_table.all()
        players_data = []
        for i in range(len(players_table)):
            list_players = []
            list_players.append(players[i]["id"])
            list_players.append(players[i]["name"])
            list_players.append(players[i]["first_name"])
            list_players.append(players[i]["rank"])
            players_data.append(list_players)
        return players_data

    @staticmethod
    def get_data_from_players_id(players_id, table_information):
        list = []
        for i in range(len(players_id)):
            selected_player = players_table.search(User.id == players_id[i])
            current_choice = selected_player[0][table_information]
            list.append(current_choice)
        return list

    @staticmethod
    def get_name_data(players_id, table_information):
        list = []
        for i in range(len(players_id)):
            selected_player = players_table.search(User.id == players_id[i][2])
            current_choice = selected_player[0][table_information]
            list.append(current_choice)
        return list

    @staticmethod
    def get_players_id(data):
        list_id = []
        for i in range(len(data)):
            id = data[i][2]
            list_id.append(id)
        return list_id

    @staticmethod
    def get_score_rank_list(rank_list):
        rank_score_list = []
        for i in range(len(rank_list)):
            group_list = []
            current_player = players_table.search(User.rank == rank_list[i])
            score = current_player[0]['score']
            group_list.append(rank_list[i])
            group_list.append(score)
            rank_score_list.append(group_list)
        return rank_score_list

    @staticmethod
    def add_players_id(rank_score_list):
        group_list = []
        for i in range(len(rank_score_list)):
            list = []
            player_rank = players_table.search(User.rank == rank_score_list[i][0])
            player_id = player_rank[0]['id']
            list.append(rank_score_list[i][0])
            list.append(rank_score_list[i][1])
            list.append(player_id)
            group_list.append(list)
        return group_list

    @staticmethod
    def get_data_from_name(name_list):
        list_data = []
        for i in range(len(name_list)):
            list = []
            player_data = players_table.search(User.name == name_list[i])
            player_name = player_data[0]['name']
            player_first_name = player_data[0]['first_name']
            player_rank = player_data[0]['rank']
            player_elo = player_data[0]['elo']
            list.append(player_name)
            list.append(player_first_name)
            list.append(player_rank)
            list.append(player_elo)
            list_data.append(list)
        return list_data

    @staticmethod
    def get_data_from_rank(rank_list):
        list_data = []
        for i in range(len(rank_list)):
            list = []
            player_data = players_table.search(User.rank == rank_list[i])
            player_rank = player_data[0]['rank']
            player_name = player_data[0]['name']
            player_first_name = player_data[0]['first_name']
            player_elo = player_data[0]['elo']
            list.append(player_rank)
            list.append(player_name)
            list.append(player_first_name)
            list.append(player_elo)
            list_data.append(list)
        return list_data

    @staticmethod
    def update_player_score(player_name, player_result):
        player = players_table.search(User.name == player_name)
        player_score = player[0]['score'] + player_result
        player_points = player[0]['elo'] + player_result
        players_table.update({'score': player_score}, User.name == player_name)
        players_table.update({'elo': player_points}, User.name == player_name)

    @staticmethod
    def reset_player_score(player_id):
        for i in range(len(player_id)):
            players_table.update({'score': 0.0}, User.id == player_id[i])
