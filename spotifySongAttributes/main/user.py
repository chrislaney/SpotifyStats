# user.py
from utils import parse_tracks, load_genre_cache, get_top_100, fetch_top_tracks

class User:
    def __init__(self, user_id, top_tracks, subgenres, supergenres):
        self.user_id = user_id
        self.top_tracks = top_tracks
        self.subgenres = subgenres
        self.supergenres = supergenres

    def __repr__(self):
        return (f"User(user_id={self.user_id}, "
                f"top_tracks={self.top_tracks[:3]}..., "
                f"subgenres={self.subgenres}, "
                f"supergenres={self.supergenres})")

    @classmethod
    def from_spotify(cls, sp, genre_cache):
        user_id = sp.current_user()['id']
       
        tracks_raw = get_top_100(sp)
        #tracks_raw = fetch_top_tracks(sp, num_tracks=100, time_range='medium_term')
        
        parsed_tracks, subgenre_distro, supergenre_distro = parse_tracks(sp, tracks_raw, genre_cache)
        # Store only the track URIs
        top_tracks = [track['uri'] for track in parsed_tracks]

        return cls(user_id, top_tracks, subgenre_distro, supergenre_distro)
