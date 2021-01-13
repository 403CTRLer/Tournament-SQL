from art import tprint
tprint('T O U R N A M E N T \nM A N A G E M E N T', font = 'rounded')
from db import *
from gen import *
from process import tournament_flow
from tabulate import tabulate



def start():
    """ Function called on the program beginning """

    #Checks the dbs for proper functioning of the code
    check_db_setup()

    #Continues the menu selection infintely untill the user stops
    while True:
        option = menu()
        if not option:
            break

        if option == 1:
            list_all_tournaments()

        elif option == 2:
            start_tournament()

        elif option == 3:
            display_all_winners()

        elif option == 4:
            tournament_info()

        elif option == 0:
            pass

        elif option == 0:
            pass

        elif option == 0:
            pass



def menu():
    """ prints all data for the avaiable options """

    seperator(3)

    tprint('Menu', font = 'small')
    print('Enter the respective numbers to select the option! \nEnter 0 to quit.')
    print("""
    \t1. Show all Tournaments.
    \t2. Start new tournament.
    \t3. Check winners of all tournaments.
    \t4. Get a tournament's info""")

    return get_num_input("\nSelected: ")
    seperator(n2 = 1)


def list_all_tournaments():
    """ prints tabulate form of all tournaments and it's data """

    tprint('DATA', font = 'rounded')
    print(tabulate(fetch('data', 'tournament_data'), ['S.No.', 'Name', 'Winner ID', 'Winner', 'Total Teams'], "pretty"))
    seperator()



def display_all_winners():
    """ prints tabulate form of all tournaments' winners """

    tprint('WINNERS', font = 'rounded')
    print(tabulate(fetch('data', 'tournament_data', 'SNo, tournament_name, winner'), ['S.No.', 'Name', 'Winner'], "pretty"))
    seperator()



def start_tournament():
    seperator(2)
    tprint('NEW TOURNAMENT', font = 'rounded')
    winner, tournament_name = tournament_flow()
    tprint(f'Winner of \n {tournament_name} is...\n{winner}', font = 'stop')



def tournament_info():
    seperator()
    print("Avaiable tournaments")
    list_all_tournaments()
    print("\n")
    while True:
        tournament_name = input('Enter the name of the tournament you want to get info.\nName:')
        if tournament_name in show_dbs():
            break
        print(f"Cannot find tournament '{tournament_name}', maybe you've miss spelled it!\nTry again!")

    tprint('TOURNAMENT    INFO', font = 'rounded')
    print('\n\n')
    tprint('TEAMS', font = 'small')
    print(tabulate(fetch('teams', tournament_name), ['ID', 'NAME', 'WINS', 'LOSS'], "pretty"))

    print('\n\n')
    tprint('Players', font = 'small')
    print(tabulate(fetch('players', tournament_name), [x.upper() for x in ['ID', 'Name'] + get_member_col([], 2).split(",")[1:]], "pretty"))

    rounds = [i for i in get_all_tables(tournament_name) if i.startswith('round_')]
    print(get_all_tables(tournament_name))
    print(rounds)
    for table in rounds:
        print('\n\n')
        tprint((table.upper()).replace('_', '   '), font = 'small')
        print(tabulate(fetch(table, tournament_name, 'match_id, team1_name, team2_name, win_name'), ['Match ID', 'Team 1', 'Team 2', 'Winner'], "pretty"))



def create_data_tb():
    seperator()
    print('initial setup...\n')
    create_db('tournament_data')
    create_table('data',
    """SNo INT AUTO_INCREMENT PRIMARY KEY,
    tournament_name VARCHAR(60) UNIQUE NOT NULL,
    winner_id INT,
    winner VARCHAR(30),
    total_teams INT""",
    'tournament_data')
    print('Setup Completed!')
    seperator()



def check_db_setup():
    #Checks for the data DB for storing tournament data
    if not db_existance('tournament_data'):
        return

    #Checking whether any Tournaments has been conducted
    #If not it's the first time opening the pgm, so start setup process
    dbs = show_dbs()
    create_data_tb()
    if not dbs:
        return create_db()

    repair_data_tb()



def repair_data_tb():

    all_dbs = show_dbs() #Gets all tournaments
    all_dbs.remove('tournament_data') #Removing the db from the tournament dbs

    #Geting all the tournaments record filled in the data table
    existing_dbs = [x[0] for x in fetch('data', 'tournament_data', 'tournament_name')]

    dbs = set(all_dbs) - set(existing_dbs)
    #Adds all the old tournaments record to the tournament_data DB if the table is deleted or changed.
    for db in dbs:
        data = fetch('winner', 'x')[0][:2] + (len(fetch('teams', 'x', 'team_id')),)
        insert('data', 'tournament_data',
        "tournament_name, winner_id, winner, total_teams",
        f"'{db}', {data[0]}, '{data[1]}', {data[2]}")



start()
