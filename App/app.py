from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__, template_folder='/Users/preetipalakkaur/Desktop/Website/Music_Recommender/templates')

# Load the song data
df = pd.read_csv('Music_Dataset.csv')

@app.route('/')
def index():
    return render_template('music.html')

# Define functions for mood-based song recommendations
def filter_songs_by_mood(df, mood):
    filtered_songs = df[df['Mood'] == mood]
    # Count the number of songs for each artist
    artist_song_counts = filtered_songs['Artist'].value_counts()
    
    # Get the top 5 artists by song count
    top_artists = artist_song_counts.head(5).index
    
    # Initialize an empty list to store the selected songs and artists
    selected_songs = []
    
    # Select one song from each of the top 5 artists
    for artist in top_artists:
        artist_songs = filtered_songs[filtered_songs['Artist'] == artist]
        if not artist_songs.empty:
            selected_song = artist_songs.sample(1).to_dict(orient='records')[0]
            selected_songs.append(selected_song)
    
    return selected_songs

@app.route('/recommend', methods=['POST'])
def recommend_songs():
    # Get the selected mood from the request payload
    try:
        mood = request.json['mood']
        print("Received mood:", mood)  # Add print statement to debug
    except KeyError:
        return jsonify({'error': 'Please provide a "mood" in the request body.'}), 400

    # Get mood-based recommendations
    recommendations = filter_songs_by_mood(df, mood)

    # Return the recommendations as JSON response
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
