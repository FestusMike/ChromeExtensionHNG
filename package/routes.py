from flask import request, redirect, render_template, url_for, send_from_directory
from package import db, app
from package.models import Video
import os
import datetime


# Set the upload folder
UPLOAD_FOLDER = 'C:\\Users\\Micheal\\Desktop\\web_pictures'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def list_videos():
    videos = Video.query.all()
    return render_template('list_videos.html', videos=videos)
   
@app.route('/upload', methods=['GET','POST'])
def upload_video():
    file = request.files['video']
    video_name = file.filename
    date_uploaded = datetime.datetime.now()

    # Save video to disk
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_name))

    # Save video information to the database
    video = Video(video_name=video_name, date_uploaded=date_uploaded)
    db.session.add(video)
    db.session.commit()

    # Redirect to the list of videos
    return redirect(url_for('list_videos'))

@app.route('/play/<video_id>')
def play_video(video_id):
    video = Video.query.filter_by(id=video_id).first()
    if video:
        return render_template('play_video.html', video=video)
    else:
        return 'Video not found.'

@app.route('/video/<filename>')
def send_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

