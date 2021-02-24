from db import get_connection, insert, create_table

def unique_input(message, list, err_msg = "Input {} already exists.\n"):
    """ to get a unique input checks existance from the given list """

    while True:
        new = input(message)
        if new not in list:
            return new
        print(err_msg.format(new))



def get_num_input(request = ''):
    """ returns a number input from user for the given query """

    while True:
        num = input(request)
        if num.isdigit():
            return int(num)
        print("Not a valid entry | Enter a number not string!\n")



def get_member_col(prev_col : str, n_members : int):
    """ to generate srting for the column in player table """

    col = ', '.join(prev_col)
    members = str(', '.join([f"member_{x}" for x in range(1, n_members + 1)]))
    if members:
        col += ', ' + members

    return col



def add_member_col(n_members : int, tb_name : str, db_name : str):
    """ adds columns for the number of members in each team on given table """

    _db = get_connection(db_name)
    for i in range(1, n_members + 1):
        _db.cursor().execute(f'ALTER TABLE {tb_name} ADD member_{i} VARCHAR(30)')
    _db.commit()



def create_round_tb(round, db_name):
    """ creates table for every round """

    create_table(
    f"round_{round}",
    "match_id INT AUTO_INCREMENT PRIMARY KEY,\
    team1_id INT,\
    team1_name VARCHAR(50),\
    team2_id INT,\
    team2_name VARCHAR(50),\
    win_id VARCHAR(7) DEFAULT 'Pending',\
    win_name VARCHAR(50) DEFAULT 'Pending'",
    db_name)



def get_teams(team_ids, db_name):
    """ returns all data from the teams table for given teams """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT * FROM teams WHERE team_id in {team_ids}')

    return _csr.fetchall()



def insert_round(team_ids, round, db_name):
    """ inserts data on round table """

    team_1, team_2 = get_teams(team_ids, db_name)

    insert(
    f"round_{round}", db_name,
    "team1_id, team1_name, team2_id, team2_name",
    f'{team_1[0]}, "{team_1[1]}", {team_2[0]}, "{team_2[1]}"')



def get_winner(match_id, round, db_name):
    """ stores the win/loss count on DB and returns the winning team ID """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT team1_id, team2_id FROM round_{round} WHERE match_id = {match_id}')
    _csr.execute(f'SELECT * FROM teams WHERE team_id in {_csr.fetchall()[0]}')
    team_1, team_2 = _csr.fetchall()

    while True:
        winner = input(f'Enter winning teams from Team {team_1[1]} ({team_1[0]}) vs Team {team_2[1]} ({team_2[0]}): ')
        if winner.isdigit():
            winner = int(winner)
            if winner in [team_1[0], team_2[0]]:
                break
            else:
                print(f'{winner} team is not playing in this match!\n')
        else:
            print(f"Enter respective team number not '{winner}'!\n")

    win = team_1 if team_1[0] == winner else team_2
    loss = team_1 if win == team_2 else team_2

    _csr.execute(f'UPDATE teams SET wins = {win[2] + 1} WHERE team_id = {win[0]}')
    _csr.execute(f'UPDATE teams SET loss = {loss[2] + 1} WHERE team_id = {loss[0]}')
    _csr.execute(f'UPDATE round_{round} SET win_id = {win[0]}, win_name = "{win[1]}" WHERE match_id = {match_id}')
    _db.commit()

    return winner



def get_win_ids(round, db_name):
    """ returns all the inning team ID from a round """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT win_id from round_{round}')

    return [x[0] for x in _csr.fetchall()]



def winner_data(_id, db_name):
    """ returns required info winners """

    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT * FROM teams WHERE team_id = {_id}')
    winner = _csr.fetchall()[0]
    _csr.execute(f'SELECT * FROM players WHERE team_id = {_id}')
    winner += _csr.fetchall()[0][2:]

    return winner
