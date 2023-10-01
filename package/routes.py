from flask import request, redirect, render_template, url_for, send_from_directory, jsonify
from package import db, app
from package.models import Video
import os
import datetime
from werkzeug.exceptions import BadRequestKeyError


# Set the upload folder
UPLOAD_FOLDER = '/home/Myusername/mysite/package/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024  # 250MB limit


@app.route('/')
def list_videos():
    videos = Video.query.all()
    return render_template('list_videos.html', videos=videos)


@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    file = request.files['video']

    # Check file size
    file_size = int(request.headers['Content-Length'])
    if file_size > app.config['MAX_CONTENT_LENGTH']:
        return "File size exceeds the limit of 250MB", 400

    video_name = file.filename
    date_uploaded = datetime.datetime.now()

    # Check if the file already exists on disk
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    if os.path.exists(file_path):
        return "File already exists", 400

    # Check if the file already exists in the database
    existing_video = Video.query.filter_by(video_name=video_name).first()
    if existing_video:
        return "File already exists in the database", 400

    # Save video to disk
    file.save(file_path)

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

# api routes

@app.route('/api/upload', methods=['POST'])
def api_upload_video():
    try:
        file = request.files['video']
    except BadRequestKeyError:
        return jsonify({'error': "No file part in the request with the key 'video'"}), 400

    # Check file size
    file_size = int(request.headers['Content-Length'])
    if file_size > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({'error': 'File size exceeds the limit of 250MB'}), 400

    video_name = file.filename
    date_uploaded = datetime.datetime.now()

    # Check if the file already exists on disk
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    if os.path.exists(file_path):
        return jsonify({'error': 'File already exists'}), 400

    # Check if the file already exists in the database
    existing_video = Video.query.filter_by(video_name=video_name).first()
    if existing_video:
        return jsonify({'error': 'File already exists in the database'}), 400

    # Save video to disk
    file.save(file_path)

    # Save video information to the database
    video = Video(video_name=video_name, date_uploaded=date_uploaded)
    db.session.add(video)
    db.session.commit()

    # Return success response
    return jsonify({'message': 'Video uploaded successfully', 'video_id': video.id}), 201

@app.route('/api/videos', methods=['GET'])
def api_list_videos():
    videos = Video.query.all()
    video_data = [{'id': video.id, 'video_name': video.video_name, 'date_uploaded': video.date_uploaded,
                   'video_url': url_for('send_video', filename=video.video_name)} for video in videos]
    return jsonify(video_data)

@app.route('/api/videos/<int:id>', methods=['GET'])
def get_video_by_id(id):
    video = Video.query.filter_by(id=id).first()
    if not video:
        return jsonify({"message" : "Video doesn't exist on disk"}), 400
    else:
        video_data = {"id" : video.id, "video_name" : video.video_name, 
        "date_uploaded" : video.date_uploaded,
        "video_url" : url_for('send_video', filename=video.video_name)
        }
        return jsonify(video_data) 