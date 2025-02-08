import json
import matplotlib.pyplot as plt
import pandas as pd

# ========================= TEAM PERFORMANCE ANALYSIS ========================= #

# Load match data for team analysis
match_file_path = "stats_match.json"
with open(match_file_path, "r") as file:
    match_data = json.load(file)

# Dictionary to store total points and match counts per team
team_stats = {}

# Iterate over each match entry
for match in match_data:
    teams_data = match.get("teams", {}).get("team", [])

    # Ensure there are teams in the match
    for team in teams_data:
        team_name = team.get("name", "Unknown Team")
        team_score = int(team.get("score", 0))

        if team_name not in team_stats:
            team_stats[team_name] = {"total_points": 0, "matches_played": 0}
        team_stats[team_name]["total_points"] += team_score
        team_stats[team_name]["matches_played"] += 1

# Compute average points per match for each team
average_points_per_team = {
    team: stats["total_points"] / stats["matches_played"]
    for team, stats in team_stats.items() if stats["matches_played"] > 0
}

# Convert to DataFrame
df_teams = pd.DataFrame(list(average_points_per_team.items()), columns=["Team", "Avg Points per Match"])
df_teams = df_teams.sort_values(by="Avg Points per Match", ascending=False)

# Plotting Graph 1: Average Points per Match per Team
plt.figure(figsize=(12, 6))
plt.bar(df_teams["Team"], df_teams["Avg Points per Match"], color="skyblue")
plt.xlabel("Teams")
plt.ylabel("Average Points per Match")
plt.title("Average Points per Match for Each Team (2014-2019)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ========================= PLAYER PERFORMANCE ANALYSIS ========================= #

# Load player data
player_file_path = "stats_player.json"
with open(player_file_path, "r") as file:
    player_data = json.load(file)

# Extract player stats
player_stats = []
for player in player_data:
    player_bio = player.get("bio")  # Using .get() prevents KeyError
    if not player_bio:  # If bio is missing, skip the player
        continue
    player_name = player_bio.get("full_name", "Unknown Player")  # Use "full_name" instead of "name"

    for stat in player.get("over_all_stats", []):
        match_played = stat.get("match_played", 0)
        raid_points = stat.get("raid_points_per_match", 0)
        tackle_points = stat.get("total_tackle_points", 0)
        success_raid_percent = stat.get("success_raid_percent", 0)
        total_points = stat.get("point", 0)
        career_best_points = stat.get("career_best_points", 0)

        if match_played > 0:
            player_stats.append({
                "Player": player_name,
                "Matches Played": match_played,
                "Raid Points/Match": raid_points,
                "Tackle Points": tackle_points,
                "Success Raid %": success_raid_percent,
                "Total Points": total_points,
                "Career Best Points": career_best_points
            })

df_players = pd.DataFrame(player_stats)

# Identifying Top Players
most_consistent_player = df_players.groupby("Player")["Raid Points/Match"].mean().idxmax()
most_explosive_player = df_players.groupby("Player")["Success Raid %"].mean().idxmax()
best_overall_player = df_players.groupby("Player")["Total Points"].sum().idxmax()
highest_individual_performance = df_players.loc[df_players["Career Best Points"].idxmax()]["Player"]

player_insights = pd.DataFrame({
    "Category": ["Most Consistent Player", "Most Explosive Player", "Best Overall Player", "Highest Individual Performance"],
    "Player": [most_consistent_player, most_explosive_player, best_overall_player, highest_individual_performance],
    "Value": [
        df_players.groupby("Player")["Raid Points/Match"].mean().max(),
        df_players.groupby("Player")["Success Raid %"].mean().max(),
        df_players.groupby("Player")["Total Points"].sum().max(),
        df_players["Career Best Points"].max()
    ]
})

# Plotting Graph 2: Top Player Performances
plt.figure(figsize=(10, 6))
bars = plt.barh(player_insights["Category"], player_insights["Value"], color=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"])
for bar, player in zip(bars, player_insights["Player"]):
    plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, f"{player}", va='center', fontsize=12, fontweight="bold")
plt.xlabel("Performance Metric Value")
plt.title("Top Player Performances in Pro Kabaddi League (2014-2019)")
plt.tight_layout()
plt.show()

# Plotting Graph 3: Raid Points vs. Tackle Points (Top Players)
plt.figure(figsize=(10, 6))
plt.scatter(df_players["Raid Points/Match"], df_players["Tackle Points"], color="red", alpha=0.7)
plt.xlabel("Raid Points per Match")
plt.ylabel("Tackle Points")
plt.title("Raid Points vs. Tackle Points (Player Performance)")
plt.grid(True)
plt.show()

# Plotting Graph 4: Success Raid % vs. Total Points (Best Raiders)
plt.figure(figsize=(10, 6))
plt.scatter(df_players["Success Raid %"], df_players["Total Points"], color="green", alpha=0.7)
plt.xlabel("Success Raid %")
plt.ylabel("Total Points")
plt.title("Success Raid % vs. Total Points (Best Raiders)")
plt.grid(True)
plt.show()

# Plotting Graph 5: Team Performance Trends Over Seasons (Average Points)
df_season_performance = df_players.groupby("Matches Played")["Total Points"].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(df_season_performance["Matches Played"], df_season_performance["Total Points"], marker="o", linestyle="-", color="blue")
plt.xlabel("Matches Played")
plt.ylabel("Average Total Points")
plt.title("Team Performance Trends Over Seasons")
plt.grid(True)
plt.show()
