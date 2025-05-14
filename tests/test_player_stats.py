import statsapi

player_id = 608070  # José Ramírez
season = "2025"

# Get career hitting stats
career_data = statsapi.player_stat_data(player_id, group='hitting', type='career')
print("🎯 Career Stats:")
print(career_data['stats'][0]['stats'])

# Get season hitting stats
season_data = statsapi.player_stat_data(player_id, group='hitting', type='season', season=season)
print("\n📅 Season Stats:")
print(season_data['stats'][0]['stats'])

