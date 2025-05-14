import statsapi

# Define the player and team abbreviation
player_name = "Iván Herrera"
team_abbrev = "STL"

# Get the full team info
team_info = statsapi.lookup_team(team_abbrev)
if not team_info:
    print(f"❌ Could not find team info for abbreviation '{team_abbrev}'")
    exit()

team_id = team_info[0]['id']

# Get games on that date
games = statsapi.schedule(start_date="05/12/2025", end_date="05/12/2025", team=team_id)
if not games:
    print(f"❌ No games found for team ID {team_id} on 05/12/2025")
    exit()

game_id = games[0]['game_id']

# Get boxscore
boxscore = statsapi.boxscore_data(game_id)
print(f"📦 Boxscore for game ID {game_id}:")
print(boxscore)

# Get player ID
player_info = statsapi.lookup_player(player_name)
if not player_info:
    print(f"❌ Could not find player ID for {player_name}")
    exit()

player_id = player_info[0]['id']

# Get player stats
season_stats = statsapi.player_stat_data(player_id, group='hitting', type='season')
print(f"\n📊 Season stats for {player_name}:")
print(season_stats)

