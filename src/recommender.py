from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numeric fields to numbers."""
    # Columns that should become floats (0-1 scores and BPM) vs. an int (id).
    float_columns = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = dict(row)
            # Convert numeric fields so later scoring math works on numbers, not strings.
            song["id"] = int(song["id"])
            for column in float_columns:
                song[column] = float(song[column])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences, returning (score, reasons)."""
    # Algorithm Recipe: start at 0 and add points for each feature that fits.
    score = 0.0
    reasons: List[str] = []

    # Genre: exact match -> +2.0 (the strongest taste signal).
    if user_prefs.get("genre") == song.get("genre"):
        score += 2.0
        reasons.append(f"genre match ({song.get('genre')}) (+2.0)")

    # Mood: exact match -> +1.0.
    if user_prefs.get("mood") == song.get("mood"):
        score += 1.0
        reasons.append(f"mood match ({song.get('mood')}) (+1.0)")

    # Energy: closeness to the target -> +1.0 * (1 - |target - song energy|).
    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_points = 1.0 * (1.0 - abs(float(target_energy) - float(song["energy"])))
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {float(target_energy):.2f} (+{energy_points:.2f})"
        )

    # Acousticness: gradient on the song's 0-1 value, weighted 0.5 (optional pref).
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        acousticness = float(song["acousticness"])
        acoustic_fit = acousticness if likes_acoustic else (1.0 - acousticness)
        acoustic_points = 0.5 * acoustic_fit
        score += acoustic_points
        preference = "acoustic" if likes_acoustic else "electronic"
        reasons.append(
            f"{preference} feel ({acousticness:.2f}), as you like (+{acoustic_points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation), highest first."""
    # Process: use score_song as the "judge" for every song in the catalog.
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # Ranking: sort highest score first, breaking ties by energy closeness to the
    # target, then alphabetically by title (so results are stable/deterministic).
    # Two passes: first the A->Z title tie-breaker, then the descending score sort.
    # Python's sort is stable, so the title order is preserved within equal scores.
    target_energy = float(user_prefs.get("energy", 0.0))
    scored.sort(key=lambda item: item[0]["title"])          # ascending title (last tie-breaker)
    scored.sort(
        key=lambda item: (
            item[1],                                              # score
            1.0 - abs(target_energy - float(item[0]["energy"])),  # energy closeness
        ),
        reverse=True,
    )

    # Output: keep the top k, turning each song's reasons into one explanation string.
    return [
        (song, score, "; ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in scored[:k]
    ]
