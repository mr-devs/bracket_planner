# bracket_planner
A simple bracket planner. Takes a list of names and randomly creates teams and then decides which teams will play one another. Handles teams of two as well as teams of one.

## Example Usage
From the root directory of this folder you can run...

```
python3 src/make_teams.py --file data/nan_players.txt --players-per-team 2
```

or

```
python3 src/make_teams.py -f data/nan_players.txt -p 2
```

Can also run the below for more information about script options.

```
python3 src/make_teams.py -h
```