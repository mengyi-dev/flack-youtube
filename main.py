from flask import Flask, request, jsonify, request, send_file, make_response
from werkzeug.exceptions import RequestURITooLarge
from werkzeug.wrappers import Response
import youtube_dl
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your secret secret key"
CORS(app) # avoiding  CORS error

@app.route('/audio', methods=['GET'])
def download_mp3():
    # getting a get request from client 
    url = request.args.get('url')
    
    # function call for downloding
    mp3_file_name = get_mp3(url)
    
    #sending file as response
    resp = make_response(
        send_file("./song.mp3", mimetype='audio/wav', as_attachment=True, attachment_filename="audio.mp3"))

    return resp

def get_mp3(url):
  
  #gets video information from url
    video_info = youtube_dl.YoutubeDL().extract_info(
        url, download=False
    )
    file_name = "song.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': file_name,
        # conversion
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    
    #downloads song with above parameters
    with youtube_dl.YoutubeDL(options) as download:
        download.download([url])

    return file_name

if __name__ == '__main__':
    app.run(debug=True)
