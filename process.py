from db import *
from gen import *
from random import shuffle

tour_name = n_teams = n_members = roundno = p_tb_col = winner = 0

def rounds(teams):
    global roundno

    roundno += 1
    shuffle(teams)

    create_round_tb(roundno, tour_name)

    #seperate tournament match for 3 teams
    if len(teams) == 3:
        print('3 team')
        return _3teams(teams)

    #Splitting teams in 2s
    match_making = [tuple(teams[x : x + 2]) for x in range(0, len(teams), 2)]
    #Checking for odd team
    oddteam_id = (match_making.pop())[0] if len(match_making[-1]) == 1 else None # and type(match_making[-1]) == type(tuple())

    #insert teams data on round table
    for team in match_making:
        insert_round(team, roundno, tour_name)

    for _id in range(1, len(match_making) + 1):
        get_winner(_id, roundno, tour_name)

    win_ids = [int(x) for x in get_win_ids(roundno, tour_name)]
    if oddteam_id:
        return oddteam((oddteam_id, win_ids[0]), _id + 1, win_ids[1:])

    if len(win_ids) == 1:
        return win_ids[0]

    return rounds(win_ids) #qualifying winners to next round



def _3teams(teams):
    global roundno
    t1, t2, t3 = teams
    match_id = 1

    insert_round((t1, t2), roundno, tour_name)
    m1winner = get_winner(match_id, roundno, tour_name); match_id += 1
    t4 = t2 if m1winner == t1 else t1

    insert_round((t3, t4), roundno, tour_name)
    m2winner = get_winner(match_id, roundno, tour_name); match_id += 1
    if m2winner != t4:
        insert_round((m1winner, m2winner), roundno, tour_name)
        return get_winner(match_id, roundno, tour_name)

    elif m2winner == t4:
        insert_round((m1winner, t3), roundno, tour_name)
        m3winner = get_winner(match_id, roundno, tour_name); match_id += 1

        if m3winner == t3:
            print("Round has resulted in draw! \nReplaying round!")
            roundno += 1
            create_round_tb(roundno, tour_name)
            return _3teams(teams)

        else:
            insert_round((m1winner, m2winner), roundno, tour_name)
            return get_winner(match_id, roundno, tour_name)



def oddteam(teams, match_id, win_ids):
    insert_round(teams, roundno, tour_name)

    win_ids.append(get_winner(match_id, roundno, tour_name))
    return rounds(win_ids)



def teams():
    for i in range(1, n_teams + 1):
        name = input(f"\nEnter team ({i}) name: ")
        insert('teams', tour_name, 'team_name', f'"{name}"')
        members_data(name)

    seperator()
    print('Completed creating tables for all teams!')



def members_data(team_name):
    members = tuple()
    for i in range(1, n_members + 1):
        members += (input(f'Enter member {i}\'s name: '),)

    val = f"'{team_name}', {str(members)[1:-1] if len(members) > 1 else str(members)[1:-2]}"
    insert('players', tour_name, p_tb_col, val)



def initialize_db():
    #creating db for the whole tournament
    create_db(tour_name)

    #creating table for the list of teams and their wins/loss
    create_table(
    "teams",
    "team_id INT PRIMARY KEY AUTO_INCREMENT,\
    team_name VARCHAR(30),\
    wins INT NOT NULL DEFAULT 0,\
    loss INT NOT NULL DEFAULT 0",
    tour_name)

    #creating table for list of teams with members data
    create_table(
    "players",
    "team_id INT PRIMARY KEY AUTO_INCREMENT,\
    team_name VARCHAR(30)",
    tour_name)

    #adding columns for the members
    add_member_col(n_members, "players", tour_name)
    seperator()



def user_inputs():
    global tour_name, n_teams, n_members, p_tb_col

    tour_name = unique_input("Enter tournament's name          : ", show_dbs(), "Tournament {} has already been created! \nTry a new name\n\n")
    n_teams = get_num_input("Enter total no of teams          : ")
    n_members = get_num_input("Enter no of members on each team : ")
    p_tb_col = get_member_col(('team_name',), n_members)

    seperator()



def save_winner():

    create_table("winner",
    "id INT NOT NULL,\
    name VARCHAR(30) NOT NULL,\
    wins INT NOT NULL,\
    loss INT NOT NULL",
    tour_name)

    add_member_col(n_members, "winner", tour_name)

    insert("winner", tour_name,
    get_member_col(("id", "name", "wins", "loss"), n_members),
    str(', '.join([(str(x)) if type(x) != type('') else ('"'+str(x)+'"') for x in winner_data(1, 'x')])))

    data = fetch('winner', tour_name)[0][:2] + (len(fetch('teams', tour_name, 'team_id')),)
    insert('data', 'tournament_data',
    "tournament_name, winner_id, winner, total_teams",
    f"'{tour_name}', {data[0]}, '{data[1]}', {data[2]}")


def tournament_flow():
    ''' calls all the function required for the proper execution of this code in order '''

    user_inputs() #Gets all data from user (Tournament name, total no of teams, total no. of members in each team)

    initialize_db() #creates all neccessary db / tables in the beginning

    teams() #Func call to get team and members data

    global winner
    winner = rounds([x for x in range(1, n_teams + 1)])
    winner = winner_data(winner, tour_name)

    save_winner()



tournament_flow()
