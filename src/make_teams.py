"""
Given a list of names in a .txt file, randomly generate teams of one or two
and then decide who will be playing who.
"""
import argparse
import random


def parse_cl_args():
    """Set CLI Arguments."""

    # Initiate the parser
    parser = argparse.ArgumentParser(
        description="Generate one or two player team matchups for foosball, given a new-line delimited input file "
                    " (.txt) of player names. Automatically handles odd number of teams by selecting who skips "
                    "the first round."
    )
    # Add optional arguments
    parser.add_argument(
        "-f", "--file",
        metavar='File',
        help="Full path to the file (.txt) containing the "
        "players you would like to assign to teams. "
        "Each line should be one name.",
        required=True
    )
    parser.add_argument(
        "-p", "--players-per-team",
        metavar='Number of players per team',
        help="Number of players to assign to each team. Allowable options are: `1` and `2`.",
        choices=['1', '2'],
        required=True
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    # Assign the file name to a variable and return it
    return args


def load_players(file_path):
    """
    Parse a new-line delimited .txt file of names into a list of those names
    """
    with open(file_path, "r") as f:
        players = [line.rstrip("\n") for line in f]
    return players


def chunker(seq: list, size: int) -> list:
        """
        Convert a list (seq) into a list of
        smaller lists (with len <= size), where only the
        last list will have len < size.

        Parameters:
        ----------
        - seq (list) : the iterable you'd like to chunk into
            smaller lists
        - size (int) : the size of the returned chunk(s)

        Return:
        ----------
        - list

        Exceptions:
        ----------
        - ValueError
        
        ~~~

        Example Usage:
        my_list = [1,2,3,4,5,6,7,8,9]
        chunker(seq = my_list, size = 2)

        # Returns
        [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
        """
        if (not isinstance(seq, list)) or (not isinstance(size, int)):
            raise ValueError("`seq` must be a list and `size` must be an integer.")
        return list(seq[pos:pos + size] for pos in range(0, len(seq), size))

def print_matches(matchups, players_per_team):
    """Print the matchups!!"""
    print("-"*100)
    print('*'*45, 'MATCHES', '*'*45)
    print("-"*100)
    
    for game_num, match in enumerate(matchups, start=1):
        # If we have two teams in a match up, we print that game
        num_teams = len(match)
        if num_teams == 2:
            team1 = match[0]
            team2 = match[1]

            # Make the player names look nice
            if players_per_team == 1:
                team1clean = " ".join([p.capitalize() for p in team1[0].split()])
                team2clean = " ".join([p.capitalize() for p in team2[0].split()])
            else:
                team1clean = []
                team2clean = []
                for player in team1:
                    pretty_name = " ".join([p.capitalize() for p in player.split()])
                    team1clean.append(pretty_name)
                for player in team2:
                    pretty_name = " ".join([p.capitalize() for p in player.split()])
                    team2clean.append(pretty_name)
                team1clean = " & ".join(team1clean)
                team2clean = " & ".join(team2clean)

            print(f"Game {game_num}:   {team1clean}\t vs.\t {team2clean}", end="\n\n")        
        
        # If there is only one team in a match, we had an odd number of teams
        # so that team automatically advances to the next round
        elif num_teams == 1:
            team1 = match[0]
            if players_per_team == 1:
                team1clean = " ".join([p.capitalize() for p in team1[0].split()])
            else:
                team1clean = []
                for player in team1:
                    pretty_name = " ".join([p.capitalize() for p in player.split()])
                    team1clean.append(pretty_name)
                team1clean = " & ".join(team1clean)

            print(f"Automatically advances to second round: {team1clean}")

        else:
            raise Exception("Unknown error")
        
    print("-"*100)
    print('*'*100)
    print("-"*100)

if __name__ == "__main__":

    # Load CL args
    args = parse_cl_args()
    file_path = args.file
    players_per_team = int(args.players_per_team)

    players = load_players(file_path)

    # Ensure the number of players is sufficient to make a bracket
    if len(players) < 4:
        raise ValueError("There must be at least four players input!")
    if (players_per_team==2) & (len(players) % 2 != 0):
        players_w_nums = [f'{idx}. {p}' for idx, p in enumerate(players, start=1)]
        players_list = "\n".join(players_w_nums)
        raise ValueError(
            "There must be an even number of players!\n\n"
            f"I count {len(players)} players, currently. "
            f"They are:\n{players_list}"
            )
    
    random.shuffle(players)
    
    # Create teams of size `players_per_team`
    teams = chunker(seq=players, size=players_per_team)
    
    # Create matchups
    random.shuffle(teams)
    matchups = chunker(seq=teams, size=2)
    print(matchups)
    print_matches(matchups, players_per_team)

    

    



