# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real world music recommendation systems generally combine collaborative filtering, which learns from the listening habits of users with similar music taste, and content-based filtering, which recommends songs with similar characteristics. For my music recommender, I plan to use content-based filtering by utilizing a song's genre, energy, mood, and acousticness. These features help describe the overall characteristics of a song, allowing my system to recommend music that closely matches a user's preferences.

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

============================================================
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

============================================================

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



