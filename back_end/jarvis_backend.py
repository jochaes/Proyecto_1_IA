from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import speech_recognition as sr
from werkzeug.utils import secure_filename
import os
import subprocess
import boto3

#Para los modelos 
import pickle
import pandas as pd
from statsmodels.tsa.arima_model import SARIMAX


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})



class VoiceChat(Resource):

    def transcribe_audio(self, audioPath):
        recognizer = sr.Recognizer()

        if not os.path.exists(audioPath):
          return "File not found"

        if os.path.getsize(audioPath) == 0:
          return "File is empty"

        # Load Audio File from Disk
        with sr.AudioFile(audioPath) as source:
            audio = recognizer.record(source)
        # Recognize Speech

        try:
            text = recognizer.recognize_google(audio, language='es-ES')
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Error: {0}".format(e)

    def post(self):
        if 'voiceNote' not in request.files:
          return {'error': 'No file part'}, 400
        file = request.files['voiceNote']
        if file.filename == '':
          return {'error': 'No selected file'}, 400

        # Save the original MP4 file
        filename = secure_filename(file.filename)
        directory = './voice'  # Make sure this directory exists
        ogg_path = os.path.join(directory, filename)
        file.save(ogg_path)

        #Convert ogg to wav
        wav_path = ogg_path.replace('.ogg', '.wav')
        subprocess.run(['ffmpeg', '-y', '-i', ogg_path, wav_path], check=True, text=True)

        text = self.transcribe_audio(wav_path)

        return {'transcription': text}, 200


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class FaceRecognition(Resource):
    

    def __init__(self):

    def post(self):
     
        try:
            file = request.files.getlist('image')[0]
            
            filename = secure_filename(file.filename)

            directory = './img'
            image_path = os.path.join(directory, filename)
            file.save(image_path)

        except:
            return {'error': 'No selected file'}, 400
        

        # Load image data
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Initialize a Rekognition client
        client = boto3.client('rekognition')

        # Call Amazon Rekognition to detect faces
        response = client.detect_faces(
            Image={'Bytes': image_data},
            Attributes=['ALL']  # Requesting all facial attributes
        )

        emotions = []
        # Print detected face details and emotions
        for faceDetail in response['FaceDetails']:
            print('Emotions:')
            for emotion in faceDetail['Emotions']:
                emotions.append({emotion['Type']: emotion['Confidence']})
                print(f"{emotion['Type']}: {emotion['Confidence']:.2f}%")
        return {'message': emotions }, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class BitcoinPricePredictor(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(VoiceChat, '/voiceChat')
api.add_resource(FaceRecognition, '/faceRecognition')

#Modelos 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
