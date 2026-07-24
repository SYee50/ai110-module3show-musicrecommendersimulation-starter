# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SongFinder 1.0**

A simple recommender that discovers songs that fit your preferences.

---

## 2. Intended Use  

SongFinder is built for a class project. It is a way to explore how recommender systems work. It takes a short list of preferences from a user and suggests songs from a file that includes a set collection of songs. It assumes the user profile will have a genre, a mood, a target energy level, and whether they like acoustic music. The recommender works best when those preferences match the songs in the catalog.

---

## 3. How the Model Works  

The model gives every song a score and then ranks them. The song with the highest score goes first. Each song earns points in four ways. It gets the most points, two points, if its genre matches what the user asked for. It gets one point if its mood matches. It gets points for how close its energy is to the user's target energy, so a closer match means more points. And it gets points if its acoustic feel lines up with whether the user likes acoustic music. All four are added together to make the final score. The user tells the model their favorite genre, their mood, a target energy from 0 to 1, and whether they like acoustic songs. The main change from the starter logic was implementing the scoring and ranking, and adding a short explanation for each song selection so the results are easy to understand.

---

## 4. Data  

The catalog has 20 songs. Each song has a title, artist, genre, mood, and a few number scores like energy, tempo, valence, danceability, and acousticness There are 17 different genres and about 16 different moods, so most genres and moods only show up once or twice. I added 10 songs to the starter data to cover more genres and moods. The catalog is still very small and does not cover all music. It leans toward calmer, low-energy songs, and there is a gap in the middle energy range. Due to the small selection of songs in the catalog, whole styles of music are missing or only have one example.

---

## 5. Strengths  

The system works well when a user has a clear taste that the catalog covers. If someone asks for happy pop with high energy, the top pick is a happy pop song with high energy. That matched my intuition every time I tried it. It is good at combining signals. A song that matches genre, mood, and energy at once rises to the top, which is what you would want. The energy score also works correctly. When two songs are close, the one nearer the user's target energy ranks higher. The "why this song" explanations are a nice strength too. They make it easy to see exactly why a song was picked, so how the results were determined is transparent.

---

## 6. Limitations and Bias 

One clear weakness I found is that genre is matched on an all-or-nothing basis, which creates a "filter bubble" for anyone with niche or adjacent taste. The catalog has 17 distinct genres across only 20 songs, so most genres appear just once, and genre is worth the largest single point value (+2.0). Because the match is exact, a user who likes "pop" gets nothing from the "indie pop" song, and a user whose genre is not spelled exactly like a catalog entry loses that +2.0 entirely. When that happens, the ranking depends on the energy and acousticness terms, which award points to every song regardless of genre, so the same handful of low-energy acoustic tracks (like "Library Rain") get recommended again and again. In effect the system can only recommend the exact genres a user already named. It reinforces existing preferecnces rather than helping users discover anything new.

---

## 7. Evaluation  

I checked the recommender in three ways. First, I ran a set of normal profiles ("High-Energy Pop," "Chill Lofi," "Deep Intense Rock") and confirmed the top results made intuitive sense. The pop-happy profile put "Sunrise City" first, which matched genre, mood, and energy all at once. Second, I ran adversarial and edge-case profiles designed to try to confuse the scoring mechanism using a profile with conflicting preferences (chill mood but energy 1.0), a profile with an out-of-range energy value (5.0), a genre and mood that exist in no song, an empty profile, and a profile with the wrong data type for energy. For each run I looked at whether the top five songs actually reflected what the user asked for, and I also tallied which songs showed up across all the runs to see if anything was being over-recommended.

The results showed a few things I did not expect. The energy 5.0 profile produced negative scores and silently ranked songs anyway instead of raising an error, and the wrong data type profile crashed with a ValueError, which showed the scoring has no input validation. The frequency tally revealed that "Library Rain" and a small cluster of low-energy acoustic tracks appeared far more often than anything else, which is what led me to the filter-bubble bias described above. Finally, I ran a small sensitivity experiment on a temporary copy of the code, doubling the weight of energy and halving the weight of genre, and compared it to the original on the starter profile; the change only swapped two adjacent ranks and moved no songs in or out of the top five, which told me the system is fairly insensitive to weight changes when a profile already has a strong genre and mood match.

Comparing the three normal profiles against each other shows the preferences are testing for what they should. High-Energy Pop vs. Chill Lofi is the greatest differing profiles. The pop profile returns bright, electronic, high-energy tracks ("Sunrise City," "Gym Hero," energy 0.82–0.93, acousticness under 0.20), while the lofi profile shifts entirely to calm, acoustic tracks ("Library Rain," "Midnight Coding," energy 0.35–0.42, acousticness above 0.70). This makes sense because the two profiles ask for opposite genres, opposite energy targets, and opposite acoustic preferences, so almost none of their scoring signals overlap. High-Energy Pop vs. Deep Intense Rock is a subtler comparison: both want high energy (0.9 vs. 0.95) and non-acoustic songs, so they share "Gym Hero" in their top three, but the genre and mood terms still pull them apart — pop puts the happy pop song first while rock puts "Storm Runner" (rock/intense) first. Chill Lofi vs. Deep Intense Rock is the most extreme pair, with zero overlap in their results, because low-energy acoustic and high-energy electronic sit at opposite ends of every feature the model scores. Overall these differences look valid. Profiles that differ on many features produce completely different lists, and profiles that share a feature (like high energy) overlap only on the songs that satisfy that shared feature.

---

## 8. Future Work  

If I kept working on this, I would change three things.Right now genre is all-or-nothing. I would give partial points for related genres, so "pop" and "indie pop" count as close instead of a total miss. This would help niche tastes and reduce the filter bubble. The model crashes on bad input and gives negative scores on out-of-range energy. I would set the energy value to 0–1 and check the input types so it doesn't raise an error. Lastly, the same calm acoustic songs show up a lot. I would add a rule that spreads out the top results, so the list has more variety instead of five similar songs.

---

## 9. Personal Reflection  

Building this taught me that a recommender is just a set of small scoring rules, and the weights on those rules decide what to recommend. The most interesting thing I found was how one design choice, such as making genre worth the most points and matching it exactly, created a filter bubble that kept suggesting the same few songs. I was also surprised by how easy it was to break the recommend with a strange input, like an energy value of 5.0 or the wrong data type. Now when I use an actual music app, I think more about why it keeps showing me similar songs, and I realize those patterns come from choices someone made in the scoring and ranking algorithms.