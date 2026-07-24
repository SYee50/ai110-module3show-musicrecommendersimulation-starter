# 🎵 Music Recommender Simulation

## Project Summary

My version, SongFinder 1.0, is a small music recommender. It represents each song and a user's taste profile as data, then uses a scoring rule to suggest the songs that best fit that profile. Each song is scored on four features: genre, mood, energy, and acoustic feel. The songs are ranked so the closest matches rise to the top five. Every recommendation comes with a short "why this song" explanation showing exactly which features earned points.

---

## How The System Works

Real world music recommendation systems generally combine collaborative filtering, which learns from the listening habits of users with similar music taste, and content-based filtering, which recommends songs with similar characteristics. Spotify, for example, blends both. It draws on a user's listening history and the habits of similar listeners (collaborative filtering) while also analyzing audio features like genre, tempo, energy, and mood (content-based filtering). For my music recommender, I plan to use content-based filtering by utilizing a song's genre, energy, mood, and acousticness. These features help describe the overall characteristics of a song, allowing my system to recommend music that closely matches a user's preferences.

- What features does each `Song` use in your system
  - Each song will have a genre, mood, energy, and acousticness

- What information does your `UserProfile` store
  - The user profile will store the user's favorite genre and mood, preferred energy level and acousticness

- How does your `Recommender` compute a score for each song
  - The recommender computes a score by comparing each song to the user's preferences, one feature at a time, and adding up points. A higher total means a better fit.
  - Genre and mood are matched exactly. The song either matches the user's preference or it doesn't. A match adds a fixed number of points.
  -Energy and acousticness are scored by closeness. A song whose energy is near the user's target earns almost full points. A song that is far away earns very little. The formula is: 1 - |target - song_value|, so a perfect match scores 1.0 and the score drops as the gap grows.
  - Because genre is the strongest signal of taste, it is worth the most points, so it has the biggest influence on the final score.

- How do you choose which songs to recommend
  - Every song in the catalog is scored using the rules above.
  - The scored songs are sorted from highest to lowest score.
  - Ties are broken by whichever song's energy is closest to the target, and then alphabetically by title.
  - The top five highest-scoring songs are returned as the recommendations.


- Algorithm Recipe

For each song, start at score = 0 and add points:

| Rule | Points added |
|---|---|
| Genre matches the user's favorite genre | +2.0 |
| Mood matches the user's favorite mood | +1.0 |
| Energy closeness to the target | +1.0 × (1 − \|target_energy − song.energy\|) |
| Acousticness fit (gradient on the song's 0–1 value) | +0.5 × (song.acousticness if the user likes acoustic, else 1 − song.acousticness) |

After every song is scored, sort by score (highest first), break ties by energy closeness then title, and return the top 5.

- Potential Biases
  - Over-prioritizing genre: Because a genre match is worth +2.0 — more than any other feature — the system can bury a song that perfectly matches the user's mood, energy, *and* acousticness simply because it is in a different genre. A great "happy, high-energy" song outside the favorite genre may never surface.
  - Exact-match penalty on categories: Genre and mood are all-or-nothing, so closely related styles like pop vs. indie pop, or happy vs. uplifting score zero on those features even though a person would consider them a good match. This makes the system rigid and biased toward songs labeled with the exact same words.
  - Popularity of common labels. Genres and moods that appear more often in the catalog have more chances to match, so users with mainstream tastes get more recommendations than users with niche preferences.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```============================================================
                     🎵  MUSIC RECOMMENDER                   
============================================================
  Loaded 20 songs from the catalog.
  Your profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False
------------------------------------------------------------
  Top 5 recommendations:
============================================================

  #1  Sunrise City  —  Neon Echo
      pop · happy      Score: 4.39 / 4.5
      Why this song:
        • genre match (pop) (+2.0)
        • mood match (happy) (+1.0)
        • energy 0.82 vs target 0.80 (+0.98)
        • electronic feel (0.18), as you like (+0.41)

  #2  Gym Hero  —  Max Pulse
      pop · intense      Score: 3.35 / 4.5
      Why this song:
        • genre match (pop) (+2.0)
        • energy 0.93 vs target 0.80 (+0.87)
        • electronic feel (0.05), as you like (+0.47)

  #3  Rooftop Lights  —  Indigo Parade
      indie pop · happy      Score: 2.29 / 4.5
      Why this song:
        • mood match (happy) (+1.0)
        • energy 0.76 vs target 0.80 (+0.96)
        • electronic feel (0.35), as you like (+0.33)

  #4  Concrete Verses  —  Cypher Bloom
      hip hop · energetic      Score: 1.43 / 4.5
      Why this song:
        • energy 0.79 vs target 0.80 (+0.99)
        • electronic feel (0.12), as you like (+0.44)

  #5  Groove Machine  —  The Funk Syndicate
      funk · triumphant      Score: 1.39 / 4.5
      Why this song:
        • energy 0.84 vs target 0.80 (+0.96)
        • electronic feel (0.14), as you like (+0.43)

============================================================```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I ran three experiments to see how the recommender behaves.

- Changing the weights (energy x2, genre /2): I made a temporary copy of the code, doubled the weight of energy and cut the weight of genre in half, then ran the same starter profile through both versions. The change was smaller than I expected. It only swapped two songs that were already next to each other in the ranking, and it moved no songs in or out of the top five. This told me the system is not very sensitive to weight changes when the profile already has a strong genre and mood match, because those matches create a big point gap that the energy tweak cannot close.

- Different types of users: I built three normal profiles (High-Energy Pop, Chill Lofi, and Deep Intense Rock) and compared their results. Profiles that differ on many features produced completely different lists. Pop returned bright, high-energy, electronic songs, while Chill Lofi returned calm, low-energy, acoustic songs, with no overlap. Profiles that share a feature overlapped only where it made sense. High-Energy Pop and Deep Intense Rock both want high energy, so they shared "Gym Hero," but their genre and mood still pulled them to different number-one picks.

- Adversarial and edge cases: I ran profiles designed to try to trick the scoring. A profile with an out-of-range energy value (5.0) produced negative scores and still ranked songs silently instead of raising an error. A profile with the wrong data type for energy crashed with a ValueError. These showed the scoring has no input validation. I also tallied which songs appeared across all the runs, and a small cluster of low-energy acoustic songs (like "Library Rain") showed up far more often than anything else, which pointed to a filter-bubble bias.

---

## Limitations and Risks

My recommender has some limitations and risks:

- There are only 20 songs in the catalog, and most genres and moods appear only once. This makes the results thin and easy to skew.
- A genre match is worth the most points, so a song can win on genre alone even if its mood and energy fit worse than another song.
- Close styles like "pop" and "indie pop" don't count as a match, so the system is rigid.
- Because it only rewards the exact genres a user names, it keeps suggesting the same familiar songs and does not help users discover anything new.
- A bad energy value gives negative scores, and the wrong data type makes it crash.

---

## Reflection

Building this program taught me that a recommender is just a set of scoring rules. It turns data into a prediction by comparing each song to a user's set preferences or behaviors. The "prediction" is just which song scored best under the rules I set, and the weights I put on each feature decide the whole recommendation result. When I doubled the weight on energy and cut the weight on genre, the rankings changed, which showed me how much these decisions can influence the result.

I also learned that biases can crop up easily. It comes from the design choices and the data. Because I made genre worth the most points and matched it exactly, the system kept suggesting the same familiar songs and ignored close styles like "indie pop," which is a filter bubble. The small, uneven catalog made it worse, since some genres had only one song and the whole list leaned toward calm, low-energy tracks. This has made me think more about the recommendations that I'm often given when using an app or browsing the internet.

---

## Stress Test with Diverse Profiles

```
============================================================
                     🎵  MUSIC RECOMMENDER                   
============================================================
  Profile: Contradiction (chill mood + energy 1.0)
  Loaded 20 songs from the catalog.
  Your profile: genre=lofi, mood=chill, energy=1.0, likes_acoustic=True
------------------------------------------------------------
  Top 5 recommendations:
============================================================

  #1  Library Rain  —  Paper Lanterns
      lofi · chill      Score: 3.78 / 4.5
      Why this song:
        • genre match (lofi) (+2.0)
        • mood match (chill) (+1.0)
        • energy 0.35 vs target 1.00 (+0.35)
        • acoustic feel (0.86), as you like (+0.43)

  #2  Midnight Coding  —  LoRoom
      lofi · chill      Score: 3.77 / 4.5
      Why this song:
        • genre match (lofi) (+2.0)
        • mood match (chill) (+1.0)
        • energy 0.42 vs target 1.00 (+0.42)
        • acoustic feel (0.71), as you like (+0.35)

  #3  Focus Flow  —  LoRoom
      lofi · focused      Score: 2.79 / 4.5
      Why this song:
        • genre match (lofi) (+2.0)
        • energy 0.40 vs target 1.00 (+0.40)
        • acoustic feel (0.78), as you like (+0.39)

  #4  Spacewalk Thoughts  —  Orbit Bloom
      ambient · chill      Score: 1.74 / 4.5
      Why this song:
        • mood match (chill) (+1.0)
        • energy 0.28 vs target 1.00 (+0.28)
        • acoustic feel (0.92), as you like (+0.46)

  #5  Iron Requiem  —  Ashen Throne
      metal · aggressive      Score: 0.99 / 4.5
      Why this song:
        • energy 0.98 vs target 1.00 (+0.98)
        • acoustic feel (0.03), as you like (+0.01)

============================================================

============================================================
                     🎵  MUSIC RECOMMENDER                   
============================================================
  Profile: Energy Overflow (energy 5.0)
  Loaded 20 songs from the catalog.
  Your profile: genre=pop, mood=happy, energy=5.0, likes_acoustic=False
------------------------------------------------------------
  Top 5 recommendations:
============================================================

  #1  Sunrise City  —  Neon Echo
      pop · happy      Score: 0.23 / 4.5
      Why this song:
        • genre match (pop) (+2.0)
        • mood match (happy) (+1.0)
        • energy 0.82 vs target 5.00 (+-3.18)
        • electronic feel (0.18), as you like (+0.41)

  #2  Gym Hero  —  Max Pulse
      pop · intense      Score: -0.60 / 4.5
      Why this song:
        • genre match (pop) (+2.0)
        • energy 0.93 vs target 5.00 (+-3.07)
        • electronic feel (0.05), as you like (+0.47)

  #3  Rooftop Lights  —  Indigo Parade
      indie pop · happy      Score: -1.92 / 4.5
      Why this song:
        • mood match (happy) (+1.0)
        • energy 0.76 vs target 5.00 (+-3.24)
        • electronic feel (0.35), as you like (+0.33)

  #4  Iron Requiem  —  Ashen Throne
      metal · aggressive      Score: -2.53 / 4.5
      Why this song:
        • energy 0.98 vs target 5.00 (+-3.02)
        • electronic feel (0.03), as you like (+0.48)

  #5  Pulse Reactor  —  Volt Cascade
      edm · uplifting      Score: -2.57 / 4.5
      Why this song:
        • energy 0.95 vs target 5.00 (+-3.05)
        • electronic feel (0.04), as you like (+0.48)

============================================================

============================================================
                     🎵  MUSIC RECOMMENDER                   
============================================================
  Profile: Ghost Taste (polka / furious)
  Loaded 20 songs from the catalog.
  Your profile: genre=polka, mood=furious, energy=0.5, likes_acoustic=True
------------------------------------------------------------
  Top 5 recommendations:
============================================================

  #1  Willow Creek Road  —  The Hollow Pines
      folk · nostalgic      Score: 1.35 / 4.5
      Why this song:
        • energy 0.44 vs target 0.50 (+0.94)
        • acoustic feel (0.82), as you like (+0.41)

  #2  Coffee Shop Stories  —  Slow Stereo
      jazz · relaxed      Score: 1.31 / 4.5
      Why this song:
        • energy 0.37 vs target 0.50 (+0.87)
        • acoustic feel (0.89), as you like (+0.45)

  #3  Focus Flow  —  LoRoom
      lofi · focused      Score: 1.29 / 4.5
      Why this song:
        • energy 0.40 vs target 0.50 (+0.90)
        • acoustic feel (0.78), as you like (+0.39)

  #4  Library Rain  —  Paper Lanterns
      lofi · chill      Score: 1.28 / 4.5
      Why this song:
        • energy 0.35 vs target 0.50 (+0.85)
        • acoustic feel (0.86), as you like (+0.43)

  #5  Midnight Coding  —  LoRoom
      lofi · chill      Score: 1.27 / 4.5
      Why this song:
        • energy 0.42 vs target 0.50 (+0.92)
        • acoustic feel (0.71), as you like (+0.35)

============================================================

============================================================
                     🎵  MUSIC RECOMMENDER                   
============================================================
  Profile: Empty Profile ({})
  Loaded 20 songs from the catalog.
  Your profile: genre=None, mood=None, energy=None, likes_acoustic=None
------------------------------------------------------------
  Top 5 recommendations:
============================================================

  #1  Moonlit Sonata Drift  —  Amber Quartet
      classical · melancholy      Score: 0.00 / 4.5
      Why this song:
        • no strong matches

  #2  Spacewalk Thoughts  —  Orbit Bloom
      ambient · chill      Score: 0.00 / 4.5
      Why this song:
        • no strong matches

  #3  Library Rain  —  Paper Lanterns
      lofi · chill      Score: 0.00 / 4.5
      Why this song:
        • no strong matches

  #4  Coffee Shop Stories  —  Slow Stereo
      jazz · relaxed      Score: 0.00 / 4.5
      Why this song:
        • no strong matches

  #5  Delta Sorrow  —  Rufus Lowe
      blues · dark      Score: 0.00 / 4.5
      Why this song:
        • no strong matches

============================================================

============================================================
                     🎵  MUSIC RECOMMENDER                   
============================================================
  Profile: Tie Maker (blank genre/mood)
  Loaded 20 songs from the catalog.
  Your profile: genre=, mood=, energy=0.5, likes_acoustic=False
------------------------------------------------------------
  Top 5 recommendations:
============================================================

  #1  Velvet Whisper  —  Mara Sol
      r&b · romantic      Score: 1.32 / 4.5
      Why this song:
        • energy 0.52 vs target 0.50 (+0.98)
        • electronic feel (0.31), as you like (+0.34)

  #2  Island Time  —  Sunward Tide
      reggae · playful      Score: 1.25 / 4.5
      Why this song:
        • energy 0.61 vs target 0.50 (+0.89)
        • electronic feel (0.28), as you like (+0.39)

  #3  Stardust Reverie  —  Aurora Fields
      dream pop · dreamy      Score: 1.19 / 4.5
      Why this song:
        • energy 0.48 vs target 0.50 (+0.98)
        • electronic feel (0.58), as you like (+0.21)

  #4  Concrete Verses  —  Cypher Bloom
      hip hop · energetic      Score: 1.15 / 4.5
      Why this song:
        • energy 0.79 vs target 0.50 (+0.71)
        • electronic feel (0.12), as you like (+0.44)

  #5  Night Drive Loop  —  Neon Echo
      synthwave · moody      Score: 1.14 / 4.5
      Why this song:
        • energy 0.75 vs target 0.50 (+0.75)
        • electronic feel (0.22), as you like (+0.39)

============================================================

```


