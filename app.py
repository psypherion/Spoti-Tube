from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import secrets,subprocess

secret_key = secrets.token_urlsafe(32)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = secret_key

# Configure Google Blueprint
google_bp = make_google_blueprint(client_id='322111399517-cb0k7tq4diknd1o74r7iodu96p698mj6.apps.googleusercontent.com',
                                 client_secret='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',
                                 redirect_to='google_login')  # 'google_login' is just a placeholder

app.register_blueprint(google_bp, url_prefix='/google_login')

@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return render_template('index.html', google=google)


@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return redirect(url_for('index'))


@app.route('/google_logout')  # Change the endpoint to 'google_logout'
def google_logout():
    token = google.token.get('access_token')
    if token:
        # You may want to revoke the token or perform other cleanup here
        
        pass

    google_bp.storage.delete()

    return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download():
    try:
        if not google.authorized:
            return jsonify({'error': 'User not authenticated'}), 401

        data = request.get_json()
        playlist_link = data.get('playlistLink', '')
        print(f"Playlist Link : {playlist_link}")

        # Call spoti-tube.py using subprocess
        subprocess.run(['python', 'spoti-tube.py', playlist_link])

        return jsonify({'message': 'Download started successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0",ssl_context=('cert.pem', 'key.pem'))

