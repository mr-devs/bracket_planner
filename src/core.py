"""
The core code for generating matchups of teams of two people from a list of names.
"""
import random
from collections import defaultdict

class Team:
    """Object to represent created teams."""
    def __init__(self, player1, player2):
        capitalized_names1 = [p.capitalize() for p in player1.split()]
        capitalized_names2 = [p.capitalize() for p in player2.split()]
        
        self.player1 = " ".join(capitalized_names1)
        self.player2 = " ".join(capitalized_names2)
        
    def __str__(self):
        return f"{self.player1} & {self.player2}"
    
    def __repr__(self):
        return f"Team({self.player1}, {self.player2})"
    

class Bracket_Generator:
    def __init__(self, file_path=None):
        self._file_path = file_path
        self._load_type = 'file'
        self._problem_pairs = defaultdict(list)
        self._individual_players = list()
        self._players_raw = None
        self._teams = list()
        self._matchups = list()
    
    
    @staticmethod
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
        if not isinstance(seq, list):
            raise ValueError("`seq` must be a list")
        return list(seq[pos:pos + size] for pos in range(0, len(seq), size))
    
    @staticmethod
    def get_input_on_odd_names():
        """
        Asks for input on odd number of players. Repeatedly asks for answer
        if proper response is not given,
        """
        message = ("Can't make teams of two with an odd number of players!!\n\n"
            "Input one of the two options below:\n"
            "\t 1. 'add' - to add a new player\n"
            "\t 2. 'remove' - to remove a random player from the current list\n")
        
        answer = None
        while answer not in ['add','remove']:
            answer = input(message)
            if answer == 'add':
                return answer
            elif answer == 'remove':
                return answer
            else:
                print("*** INCORRECT INPUT ***")
    
    
    def process_names(self):
        """
        Process player names.
        """
        if self._load_type == 'file':
            with open(self._file_path, "r") as f:
                # Anyone beyond "!!" on a line indicates players who can't be matched
                self._players_raw = [line.rstrip("\n").split("!!") for line in f]
        
        elif self._load_type == 'list':
            self._players_raw = [line.rstrip("\n").split("!!") for line in self._players_raw]

        # If there are less than four players, there is no bracket to make
        if len(self._players_raw) < 4:
            raise ValueError("There must be at least four players input!")

        # Handle an odd number of players...
        odd_number_of_players = len(self._players_raw) % 2 != 0
        if odd_number_of_players:
            answer = self.get_input_on_odd_names()
            
            if answer == 'add':
                new_name = input("Enter the name of the new player.\n\t--> ")
                self._players_raw.append([new_name])
            if answer == 'remove':
                random_player = random.choice(self._players_raw)
                print(f"REMOVING PLAYER: {random_player[0]}")
                self._players_raw.remove(random_player)
            
    
    def generate_problem_pairs_and_player_list(self):
        """
        Build `self._problem_pairs` dictionary indicating who can't be paired
        with whom and `self._individual_players` list, containing all players
        
        `_problem_pairs` (dict) Form:
            {focal_player1 : [problemplayer1, problemplayer2],
            focal_player2 : [problemplayer3, problemplayer4]}
        
        `_individual_players` (list) Form:
            [player1, player2, ..., playerN]
        """

        for player in self._players_raw:
            
            # Take first user, stripping extra whitespace
            current_player = player[0].rstrip()
            
            # Add user to players list
            self._individual_players.append(current_player)
            
            # Extra users are those we don't want to pair with `current_player`
            dont_pair_players = player[1:]

            if dont_pair_players != []:
                self._problem_pairs[current_player] = dont_pair_players
                for temp_player in dont_pair_players:
                    self._problem_pairs[temp_player].append(current_player)

    
    def randomize_player_order(self):
        """
        Shuffle player list. Also, puts users who have pair restrictions
        at the front of the list to pair them first.
        """
        restricted_players = [p.rstrip() for p in self._problem_pairs.keys()]
        
        for player in restricted_players:
            self._individual_players.remove(player)

        random.shuffle(self._individual_players)
        random.shuffle(restricted_players)

        self._individual_players = restricted_players + self._individual_players
    
    
    def generate_teams(self):
        """
        Create all teams taking into account players
        who cannot be paired together.
        """
        problem_count = 0

        while len(self._individual_players) > 0:
            indv_player = self._individual_players.pop()

            random_partner = random.choice(self._individual_players)

            if random_partner not in self._problem_pairs[indv_player]:
                self._individual_players.remove(random_partner)
                self._teams.append(Team(indv_player, random_partner))
            
            # If we randomly choose a problem pair, we just keep
            # choosing new ones until we find a match — or throw an
            # error b/c this is very rare.
            else:
                switch = True
                while switch:
                    random_partner = random.choice(self._individual_players)

                    if random_partner not in self._problem_pairs[indv_player]:
                        self._individual_players.remove(random_partner)
                        self._teams.append(Team(indv_player, random_partner))
                        switch = False

                    else:
                        # Catch rare infinite loops.
                        problem_count += 1
                        if problem_count > 10:
                            raise Exception(
                                "RAN INTO A VERY RARE PROBLEM...\n\n"
                                "Please restart the script again!!"
                            )

                            
    def generate_matches(self):
        """Randomly match teams to play one another"""
        
        random.shuffle(self._teams)
        self._matchups = self.chunker(self._teams, size=2)
    
    
    def print_matches(self):
        """Print the matchups!!"""
        print("-"*100)
        print('*'*45, 'MATCHES', '*'*45)
        print("-"*100)
        for game_num, match in enumerate(self._matchups, start=1):
            
            num_teams = len(match)
            
            # If we have two teams in a match up, we print that game
            if num_teams == 2:
                print(f"Game {game_num}:   {match[0]}\t vs.\t {match[1]}", end="\n\n")
            
            # If there is only one team in a match, we had an odd number of teams
            # so that team automatically advances to the next round
            elif num_teams == 1:
                print(f"Automatically advances to second round: {match[0]}")

            else:
                raise Exception("Unknown error")
    

    def make_bracket(self, filepath:str=None, names:list=None):
        """
        Create an entire bracket of two-player teams indicating who is
        on each team and who will be playing one another. All teams and matchups
        are randomized. Also handles players who should not be put on the
        same team (see NOTE).

        Parameters:
        -----------
        - filepath (str) : path to a file containing the names of players to
            be included in the bracket. Files must contain one player's name on
            each line. If this parameter is passed, `names` cannot also be included.
        - names (list) : a list of names (strings) of the players to be included
            in the bracket. If this parameter is passed, `filepath`
            cannot also be included.
        
        NOTE: Players that should not be put on the same team can be handled by
            including *after* a player's name the `!!` immediately followed by
            the players that they can't be paired with. For example:
            
            ---- Example file ----
            Tom Brady
            Billy Bob Thorton
            Kanye West !!Pete Davidson
            Stevie Nicks
            Angelina Jolie !!Billy Bob Thorton
            Pete Davidson
            ----------------------

            ---- Example list ----
            lst = ['Tom Brady', 'Billy Bob Thorton', 'Kanye West !!Pete Davidson',
            'Stevie Nicks', 'Angelina Jolie !!Billy Bob Thorton', 'Pete Davidson']
            ----------------------

            In the above example Kanye West would never be put on the same
            team as Pete Davidson because we included `!!Pete Davidson` after
            his name.
            
        REMEMBER:
        1. There should be no space between the `!!` and the name.
        2. It doesn't matter if you include both the pairs that can't match on
            both lines. For instance, we don't need to include `!!Kanye West`
            on the line that starts with `Pete Davidson`.
        3. As you can see, the strings within a list should be input exactly
            the same way as the lines on the file.
        """

        if (filepath is None) and (names is None):
            raise ValueError("`filepath` or `names` must be included.")
        if all(obj for obj in [bool(filepath), bool(names)]):
            raise ValueError("Both `filepath` and `names` cannot be included simultaneously.")
        if (names is not None) and (not isinstance(names, list)):
            raise TypeError("`names` must be of type list.")
        if (filepath is not None) and (not isinstance(filepath, str)):
            raise TypeError("`filepath` must be of type str.")
        
        if filepath is not None:
            self._file_path = filepath
            self._load_type = 'file'
        else:
            self._players_raw = names
            self._load_type = 'list'
        
        self.process_names()
        self.generate_problem_pairs_and_player_list()
        self.randomize_player_order()
        self.generate_teams()
        self.generate_matches()
        self.print_matches()
