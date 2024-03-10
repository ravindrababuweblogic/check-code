from flask import Flask, request
import whisper
import numpy as np
import librosa
from flask_cors import CORS, cross_origin
import os
app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form['name']
    email = request.form['email']
    audio_file = request.files['audioFile']
    if os.path.exists('email_data.txt'):
        with open('email_data.txt', 'r') as f:
            existing_emails = f.read().splitlines()
            if email in existing_emails:
                return 'Email already exists. Sign up declined.'

    # Save the audio file to a desired location
    audio_file.save(audio_file.filename)

    # Process the data as needed
    print('Name:', name)
    print('Email:', email)
    print('Audio File Name:', audio_file.filename)

    # Load model and transcribe audio
    model = whisper.load_model('base')
    result = model.transcribe(audio_file.filename)
    print("Result:", result['text'])    

    # Read audio data and sample rate
    audio_data, sample_rate = librosa.load(audio_file.filename, sr=None)

    # Write data to a text file
    with open('audio_data.txt', 'a') as f:
        f.write(f"Name: {name}\n")
        f.write(f"Text: {result['text']}\n")

        f.write(f"Email: {email}\n")
        f.write(f"Audio File Name: {audio_file.filename}\n")
        f.write(f"Sample rate: {sample_rate}\n")
        f.write(f"Number of samples: {len(audio_data)}\n")
        f.write("\n")  # Add a new line after each entry
    with open('email_data.txt', 'a') as f:
        f.write(f"{email}\n")
        f.write("\n")  # Add a new line after each entry


    return 'Registeration Successful'
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    audio_file = request.files['audioFile']
    audio_file.save(audio_file.filename)

    # Check if the email exists in the database (text file)
    with open('audio_data.txt', 'r') as file:
        lines = file.readlines()
    
    user_data = {}
    users = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(': ')
            key = parts[0]
            value = ': '.join(parts[1:])
            if key == 'Name':
                users.append(user_data)  # Save the previous user data
                user_data = {}
            user_data[key] = value
    users.append(user_data)  # Save the last user data

    # Search for the provided email in the user data
    for user in users:
        if user.get('Email') == email:
            # Retrieve the corresponding name

            Text = user.get('Text', 'Name not found')
            name = user.get('Name', 'Name not found')

            Sample_rate = user.get('Sample rate', 'Name not found')
            Number_of_samples = user.get('Number of samples', 'Name not found')

            model = whisper.load_model('base')
            result = model.transcribe(audio_file.filename)
            print("Result:", result['text'])    
            print("Text:",Text)    

            # if(Text==result['text']):
            if(Text==result['text']):

                print("Voice Match Success!")

                return 'OK, Voice Match Success! Welcome ' + name
            else:
                return 'Username Found But Voice Authentation Failed ' + name



            # Perform audio file processing or verification here
            # For simplicity, let's just return 'OK' if email exists

    # If the email is not found in any user data
    return 'Error: Email not found'

if __name__ == '__main__':
    app.run(debug=True)
