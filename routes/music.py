from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
import pandas as pd

music_bp = Blueprint('music', __name__)
songs_df = pd.read_csv("songs.csv")

# In-memory user library (replace with database logic in production)
user_libraries = {}

@music_bp.route("/music", methods=["GET", "POST"])
@login_required
def music():
    query = request.form.get("query", "")
    song_id = request.form.get("song_id")

    user_id = current_user.id
    if user_id not in user_libraries:
        user_libraries[user_id] = []

    # Add song to user library
    if song_id:
        song_row = songs_df[songs_df["id"] == int(song_id)]
        if not song_row.empty and song_row.to_dict("records")[0] not in user_libraries[user_id]:
            user_libraries[user_id].append(song_row.to_dict("records")[0])

    # Search logic
    if query:
        results = songs_df[
            songs_df["track_name"].str.contains(query, case=False, na=False) |
            songs_df["artist_name"].str.contains(query, case=False, na=False)
        ]
    else:
        results = pd.DataFrame()

    return render_template("music.html",
                           songs=results.to_dict("records"),
                           library=user_libraries[user_id],
                           query=query)
