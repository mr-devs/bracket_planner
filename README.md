# bracket_planner
A simple bracket planner. Takes a list of names and randomly creates teams and then decides which teams will play one another. Handles teams of two as well as teams of one. Odd number of teams is handled by randomly selecting which team will automatically advance to the second round.

## Example Usage
From the root directory of this folder you can run...

```
python3 src/make_teams.py --file data/players.txt --players-per-team 2
```

or

```
python3 src/make_teams.py -f data/players.txt -p 2
```

**Edit `players.txt` to include the names to use. One name per file**

---

Run the below from the root directory for more information about script options.

```
python3 src/make_teams.py -h
```