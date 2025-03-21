# user_from_playlists.py
import sys, os
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from utils import parse_playlist, parse_tracks
from user import User

# Spotify App Credentials
client_id = '104ec8795164430c814e8b4e98a6d781'
client_secret = 'e1dbca47ea984b6a8256631b4bbcfab8'

# Initialize Spotify client (public playlist access only)
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# List of public playlist IDs
artist_playlist_ids =  ['5l7T9Q5z13VeUNVyWvxhqO', '2ntYm3kyUfO2AfVBsSAzPo', '64Oj3WwNX5pIRDqNqZ2Qjc', '4OWUKCryi1l2GuFYStGokT', '3yoS7AFclOLR1KqrdOaMcV',
'7c2bs2HJ60YGy242ZpJlzG', '1aNFkYUK4qTUe8H96jEOzA', '5Seki47tWtdSKWCIiBqsPd', '5HGPJlM2Gt9JeUTEbgf8RJ', '1CKoQPN1H7GFs04GOJqgWZ', '6IMlcf2HRrodVeL0Xfk3VD',
'5hz7XzZIM1ym4bfrM1qC5Y', '3oesM2g2EEiq2vKH8GHLA0', '16JHeU8pP3VJgjaN6cna80', '74lnx4RdPFNTh6lXu7kmjI', '4ZzhCjAa908ksareKBFyFK', '5m3qTsZchMmr6RxktXJkvb',
'7JB2J9HK5B81nrlhp5fEjH', '2mZiZyvSZCxoHtdGOydRwt', '34fty458ZfppCwtVcILtLv', '132CWpGyzC0xwlCSytPkyF', '1qIaMEuzE3apJoHg1Cn5D0', '1bcUbLMRmaIVQMeGj6zna8', 
'1swN6t0Ey7kWXDWZLXKpgj', '34zWzANNsC9bLiLYBfh4xu', '0zR0G69ovhQMFPr8jemUt4', '1QI6oJP2XX9qH9VUtzs4XO', '0a2Pozd9B8wdIweLKFqoqM', '46r9hdhyc5tz0SxTQoNGRS', 
'35suDaWu9PbLO73zuiSoaH', '3V0XrZunNamHSuv60JOLJz', '1Jg22QbjypynvCtXk6Glj0', '6L7NONohzTwgElpMyLzq0N', '1qvSgXL6BJimuqsyALKYpy', '57wlnbW8PztQxIK1cau3Ja', 
'1ZpAt7rQ7xdmJUQWT2QYfS', '41wGhbkZXokXDqqDAghvrh', '28XvQlZz8avJz6SLLEdAVo', '0NtGpbI99cjyyw8P19Q9dV', '2khXVhAHAM2o4s5FBUu31c', '1r2nh60TmpJssGag6Fb4VC',
'4QX125F8Su90D9KDp44sri', '5mIzlhkwv5ReWTeQMpjXZD', '6WVrFx3cmTJ27AaA1AizXY', '0gLJaI8oizE4uW5hnjNfWZ', '7s3nfTcn9fQDgt6X6hipQX', '4TSpzW6OlU0jt3qbWF5YS3',
'4tCndowzSB3DJNQ08S8yMO', '1FmaAHmqqfF1lb75EJAsXp', '6irxX4BFzhFTbwdN5fAO5F', '7kKn8RJ4peGisJ95zhSFk6', '7JHDFzKbOnp3SNGWBWh8bS', '142s6UsLP8kZa7LpsnN8RP', 
'13Cl7qnKBLgBDW0t1If2N2', '6ViWcperOekPr0AqXbG1GX', '3ELdIyKE6YOu3Hv4t1jfhf', '4Qe0D1C0eMebHSXclEkFqV', '4c5RI9pzBbyaZ3sPRAHjbO', '1HMGJ1bhOLlt9W0w1IDQiQ',
'5qYngBh76m6Rs2z99rAkr1', '6O3A5CbN9OEvEBda15aRKD', '2bOkXc6XQtu0rOPkTMONdE', '7ae35EX3zZi3omU8gEhjoc', '2Drk02sTIc7DzkjNPiPclZ', '33Y5wtiaQVW7C4TL3EzYPP', 
'4lUORhVikyX0refmSdBvM0', '2uRR1Bp3F1NCDLiCTfveoZ', '4pP02GCSKkGNJX6OCgLC7f', '7mJ6Sa21outbHAlSHiMtAg', '2eRxJsH4O1nWIkYZIYKhYT', '6wl7qmxZwHs2ksOjXW0Ic7',
'3SI8MGbO7Mh7IFej3quFez', '5S98I8WQZioGGtPDEgBqJL', '3lvr9d1jwvAr8qam1Pi0oW', '6EPnejp6MHtLjO2fH2IDr5', '6LcZc3RtIdrhvkPursidLa', '4OwysqVLAY5N6vuolj7EZU',
'67HpXk5Jc64XoI7v3EcALu', '3XpIl9AfsJvhewp5eVoiWG', '4n8yaiXWIqISDKbgn86oCi', '4nPaTplmjsLEBqBmhFTEd6', '48q0Ancx4BXi79PdAh4odK', '67NpGAJ9vLwg4vKt1r8f23',
'10IlBUkN2gn4114CEOackt', '28WcaBl4iErSpPhkc2kIa5', '2rZ8xIaU78OhTL5IY0wBJC', '5sqFQ0LflDNdIauWWfhsHX', '0N5SCRnRmWjS6Y2oEsxvHy', '7wrpUEtMfkIMQ2cQDKtVEb',
 '3aLutwPwoq3LPASQTYU6zX', '3cOvG4XLHBOgGGeql8vbrS' ]



""" top 50 USA artitts radio plsylist ID:"""

# RELA USERS THAT ARE PROCESSED(if changes made to this file rerun ): 
user_playlist_ids =["6ChSRuGzWIczjZrp90BQzz" ,"298ake83n1yhQ7gkwjMWvW" , "40mZ7Gaf29yKaxrmhrprpN", "04vajMJKqrwB1O7ib4V8rt",
                "6YlQzadiLbJGadpoU5RLK3" ,"7zSThiDt2I7KKfZV6IwGPK" ,"6sJRtdkkDf5wbxU3VdSzbP", "76kxhBeCZ96VobdTzzdeKn", 
                "2wb0rMjJ5hutwTYJI8X4X1" , "0m5IYySEaM09FmHJIdykEp", "2tWFZzDS89QEeKFGLoks5U" , "6pHLiYgCEk5tO2NK29A9X3",
                "6NSWokS0pez4VnnkJCeIXb" ,"74TmSEjAwIqDr1wgRijfFx", "4sHoEQ24vcPxLxHzWQDyVg", "4vhKJUznLeYjQP0jbt13Qm",
                "1gD5khdDLnM3MsRP0delei", "2O0aXCqEqfr68dLXScLRbz" ,
                "4UPRr6AuZxCPIFLTJlCfs5", "43YS3rrnq6RuPqNlm4Ex0q" , "4iKlDePfpw3uWf1jpF1Csa" ]  


def real_people():
    output_dir = "generated_users"
    os.makedirs(output_dir, exist_ok=True)

    # Process each playlist
    for i, playlist_id in enumerate(user_playlist_ids):
        try:
            playlist_data = parse_playlist(sp, playlist_id)

            if not playlist_data or not playlist_data.get('name'):
                print(f"Skipping playlist {playlist_id} - no name found")
                continue

            base_username = playlist_data['name'][:10].lower().replace(" ", "")
            username = f"{playlist_id}-{base_username}"

            parsed_tracks, subgenres, supergenres = parse_tracks(  sp, playlist_data['tracks'], genre_cache={})
            track_uris = [track['uri'] for track in parsed_tracks]

            user = User(user_id=username,
                        top_tracks=track_uris ,
                        subgenres=subgenres,
                        supergenres=supergenres)

            output_path = os.path.join(output_dir, f"{username}.json")
            with open(output_path, "w") as f:
                json.dump(user.__dict__, f, indent=2)

            print(f"Saved: {output_path}")

        except Exception as e:
            print(f"Error processing {playlist_id}: {e}")



def artist_users():
    # Output directory
    output_dir = "top_artist_users"
    os.makedirs(output_dir, exist_ok=True)

    # Process each playlist
    for playlist_id in artist_playlist_ids:
        try:
            playlist_data = parse_playlist(sp, playlist_id)

            if not playlist_data or not playlist_data.get('name'):
                print(f"Skipping playlist {playlist_id} - no name found")
                continue

            base_username = playlist_data['name'].strip().lower().replace(" ", "_")
            parsed_tracks, subgenres, supergenres = parse_tracks(
                sp, playlist_data['tracks'], genre_cache={}
            )
            track_uris = [track['uri'] for track in parsed_tracks]

            if len(track_uris) < 50:
                print(f" Playlist {playlist_id} has fewer than 50 tracks — skipping")
                continue

            # Create 5 chunks of 10 tracks each
            for idx in range(5):
                chunk = track_uris[idx * 10 : (idx + 1) * 10]
                username = f"{base_username}_{idx+1}"

                user = User(
                    user_id=username,
                    top_tracks=chunk,
                    subgenres=subgenres,
                    supergenres=supergenres
                )

                output_path = os.path.join(output_dir, f"{username}.json")
                with open(output_path, "w") as f:
                    json.dump(user.__dict__, f, indent=2)

                print(f"aved: {output_path}")

        except Exception as e:
            print(f"Error processing {playlist_id}: {e}")

if __name__ == '__main__':
    real_people()
    artist_users()

     