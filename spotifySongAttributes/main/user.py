# user.py
from utils import load_genre_cache, get_top_100, parse_tracks
from datetime import datetime

class User:
    def __init__(self, user_id, top_tracks, subgenres, supergenres):
        self.user_id = user_id
        self.top_tracks = top_tracks
        self.subgenres = subgenres
        self.supergenres = supergenres
        self.created_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()

    def __repr__(self):
        return (f"User(user_id={self.user_id}, "
                f"top_tracks_count={len(self.top_tracks)}, "
                f"subgenres_count={len(self.subgenres)}, "
                f"supergenres_count={len(self.supergenres)})")

    @classmethod
    def from_spotify(cls, sp, genre_cache):
        """
        Create a User object from Spotify API data
        
        Args:
            sp: Authenticated Spotify client
            genre_cache: Dictionary of cached artist genres
            
        Returns:
            User: A new User object populated with Spotify data
        """
        # Get basic user profile
        profile = sp.current_user()
        user_id = profile['id']
        
        # Get top tracks
        top_100_raw = get_top_100(sp)
        parsed_tracks, subgenre_distro, supergenre_distro = parse_tracks(sp, top_100_raw, genre_cache)

        return cls(
            user_id=user_id,
            top_tracks=parsed_tracks,
            subgenres=subgenre_distro,
            supergenres=supergenre_distro
        )
        
    @classmethod
    def from_dynamodb(cls, user_data):
        """
        Create a User object from DynamoDB data
        
        Args:
            user_data: Dictionary of user data from DynamoDB
            
        Returns:
            User: A User object populated with data from DynamoDB
        """
        user = cls(
            user_id=user_data.get('user_id'),
            top_tracks=user_data.get('top_tracks', []),
            subgenres=user_data.get('subgenres', {}),
            supergenres=user_data.get('supergenres', {})
        )
        
        # Add any additional attributes from DynamoDB
        for key, value in user_data.items():
            if not hasattr(user, key):
                setattr(user, key, value)
                
        return user