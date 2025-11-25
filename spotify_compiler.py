import json
import os
from collections import defaultdict

# Folder containing your JSON files
folder_path = 'spotify'  # ⬅️ Change this to your folder

# Initialize accumulators
song_play_time = defaultdict(int)
artist_tally = defaultdict(int)
total_seconds = 0

# Loop through each JSON file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Skipping {filename}: JSON error - {e}")
                continue

        # Process each entry
        for entry in data:
            ms_played = entry.get('ms_played', 0)
            seconds_played = ms_played / 1000
            total_seconds += seconds_played

            track_name = entry.get('master_metadata_track_name')
            if track_name:
                song_play_time[track_name] += seconds_played

            artist_name = entry.get('master_metadata_album_artist_name')
            if artist_name:
                artist_tally[artist_name] += 1

# Sort by time and play count
sorted_songs = sorted(song_play_time.items(), key=lambda x: x[1], reverse=True)
sorted_artists = sorted(artist_tally.items(), key=lambda x: x[1], reverse=True)

# Write the results to a summary file called spotify_summary.txt
output_path = os.path.join(folder_path, 'spotify_summary.txt')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write(f"Total time played: {total_seconds / 60:.2f} minutes\n\n")

    out.write("Play time per song (sorted):\n")
    for song, seconds in sorted_songs:
        out.write(f"  {song}: {seconds / 60:.2f} minutes\n")

    out.write("\nArtist tally (sorted):\n")
    for artist, count in sorted_artists:
        out.write(f"  {artist}: {count} plays\n")

print(f"\n✅ Summary written to: {output_path}")
