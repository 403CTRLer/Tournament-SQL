from db import *
from gen import *
from random import shuffle
from art import tprint

tour_name = n_teams = n_members = roundno = p_tb_col = 0

def show_dbs():
    csr = get_connection().cursor()
    csr.execute("SHOW DATABASES")
    dbs = csr.fetchall()
    return tuple([x[0] for x in dbs[3:]])



def teams():
    global n_teams, n_members

    for i in range(1, n_teams + 1):
        name = input(f"\nEnter team ({i}) name: ")
        insert('teams', tour_name, 'team_name', f'"{name}"')
        members_data(name)

    seperator()
    print('Completed creating tables for all teams!')



def members_data(team_name):
    global tour_name, n_teams, n_members, p_tb_col

    members = tuple()
    for i in range(1, n_members + 1):
        members += (input(f'Enter member {i}\'s name: '),)

    val = f"'{team_name}', {str(members)[1:-1] if len(members) > 1 else str(members)[1:-2]}"
    insert('players', tour_name, p_tb_col, val)



def initialize_db():
    global tour_name, n_members

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
    db = get_connection(tour_name)
    for x in range(1, n_members + 1):
        db.cursor().execute(f'ALTER TABLE players ADD member_{x} VARCHAR(30)')
    db.commit()
    seperator()



def user_inputs():
    global tour_name, n_teams, n_members, p_tb_col

    tour_name = unique_input('Enter tournament\'s name: ', show_dbs())
    n_teams = get_num_input("Enter total no of teams:")
    n_members = get_num_input('Enter no of members on each team: ')
    p_tb_col = get_member_col(n_members)

    seperator()



def flow():
    ''' calls all the function required for the proper execution of this code in order '''

    user_inputs() #Gets all data from user (Tournament name, total no of teams, total no. of members in each team)

    initialize_db() #creates all neccessary db / tables in the beginning

    teams() #Func call to get team and members data

flow()
