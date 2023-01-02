import sys
from spotifytocsv import SpotifyToCsv
import pandas as pd


def main():
    if len(sys.argv) != 3:
        print("usage: python3 main.py <public spotify playlist url> <output filename>")
        exit(1)

    playlist_url = sys.argv[1]
    output_filename = sys.argv[2]

    if not playlist_url.startswith("https://open.spotify.com/playlist/"):
        print(f"Url '{playlist_url}' does not start with 'https://open.spotify.com/playlist/'. Please try again.")
        exit(1)

    songs = SpotifyToCsv.dict(playlist_url)
    songs = pd.DataFrame.from_dict(songs, orient="index")
    songs.to_csv(output_filename, index=False)

    print("Finished!")


if __name__ == "__main__":
    main()
