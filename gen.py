from db import get_connection, insert, create_table

def get_num_input(request = ''):
    """ returns a number input from user for the given query """

    while True:
        count = input(request)
        if count.isdigit():
            return int(count)
        print("Not a valid entry | Enter a number not string!")



def unique_input(message, list):
    """ to get a unique input checks existance from the given list """

    while True:
        new = input(message)
        if new not in list:
            return new
        print(f"Input {new} already exists on {message}.\n")



def get_member_col(n_members):
    """ to generate srting for the column in player table """

    members = tuple()
    for i in range(1, n_members + 1):
        members += (f'member_{i}',)

    col = 'team_name'
    if members:
        col += ', '
        for x in members:
            col += x + ', '
        return col[:-2]

    return col




def get_winner(match_id, round, db_name):
    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT team1_id, team2_id FROM round_{round} WHERE match_id = {match_id}')
    t1, t2 = _csr.fetchall()[0]
    _csr.execute(f'SELECT * FROM teams WHERE team_id in ({t1}, {t2})')
    t1, t2 = _csr.fetchall()

    while True:
        winner = input(f'Enter winning teams from Team {t1[1]} ({t1[0]}) vs Team {t2[1]} ({t2[0]}): ')
        if winner.isdigit():
            winner = int(winner)
            if winner in [t1[0], t2[0]]:
                break
            else:
                print(f'{winner} team is not playing in this match!\n')
        else:
            print(f"Enter respective team number not '{winner}'!\n")

    win = t1 if t1[0] == winner else t2
    loss = t1 if win == t2 else t2

    _csr.execute(f'UPDATE teams SET wins = {win[2] + 1} WHERE team_id = {win[0]}')
    _csr.execute(f'UPDATE teams SET loss = {loss[2] + 1} WHERE team_id = {loss[0]}')
    _csr.execute(f'UPDATE round_{round} SET win_id = {win[0]}, win_name = "{win[1]}" WHERE match_id = {match_id}')
    _db.commit()

    return winner


def get_win_ids(round, db_name):
    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT win_id from round_{round}')

    return _csr.fetchall()



def get_teams(team_ids, db_name):
    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT team_id, team_name FROM teams WHERE team_id in {team_ids}')
    teams = _csr.fetchall()

    return teams



def create_round_tb(round, db_name):
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



def insert_round(team_ids, db_name, round):
    t1, t2 = get_teams(team_ids, db_name)

    insert(
    f"round_{round}", db_name,
    "team1_id, team1_name, team2_id, team2_name",
    f'{t1[0]}, "{t1[1]}", {t2[0]}, "{t2[1]}"')



def winner_data(_id, db_name):
    _db = get_connection(db_name)
    _csr = _db.cursor()
    _csr.execute(f'SELECT * FROM players WHERE team_id = {_id}')
    winner = _csr.fetchall()[0]
    _csr.execute(f'SELECT wins, loss FROM teams WHERE team_id = {_id}')
    winner += _csr.fetchall()[0]

    return winner
