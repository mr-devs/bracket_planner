"""
Given a list of names in a .txt file, randomly generate teams of two and then
decide who will be playing who.
"""
import argparse
import os

try:
    from core import Bracket_Generator
except:
    raise ImportError(
        "You must be in the `src` folder of the `bracket_planner` project"
        )

SOURCE_DIR = "src"


# Create Functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_cl_args():
    """Set CLI Arguments."""

    # Initiate the parser
    parser = argparse.ArgumentParser(
        description="Generate two player team matchups given an input file of player names."
    )
    # Add optional arguments
    parser.add_argument(
        "-f", "--file",
        metavar='File',
        help="Full path to the file (.txt) containing the "
        "players you would like to assign to teams. "
        "Each line should be one players names. Players that cannot be matched "
        "together should immediately follow `!!` on the same line like"
        ": player one !!cant match this player !!or this player",
        required=True
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    # Assign the file name to a variable and return it
    ids_file = args.file
    return ids_file

if __name__ == "__main__":
    
    file_path = parse_cl_args()
    BG = Bracket_Generator(file_path=file_path)
    BG.load_names()
    BG.generate_problem_pairs_and_player_list()
    BG.randomize_player_order()
    BG.generate_teams()
    BG._teams
    BG.generate_matches()
    BG.print_matches()