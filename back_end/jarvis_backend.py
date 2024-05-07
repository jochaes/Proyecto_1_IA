from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import speech_recognition as sr
from werkzeug.utils import secure_filename
import os
import subprocess
import boto3
import datetime

#Para los modelos 
import pickle
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import make_pipeline


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
            return "No se pudo entender el audio"
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
class ModeloSerieTiempoBitcoin(Resource):
    def post(self):
        # Print the request body

        days = int(request.json['Dias'])
        
        
        with open('./../Trained_Models/Modelo_Prediccion_Bitcoin.pkl', 'rb') as f:
            model = pickle.load(f)
        
        tomorrow = datetime.date.today() + datetime.timedelta(days=days)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        print(tomorrow)

        #Startdate es la fecha inicial del DataSet
        startDate = pd.to_datetime('2015-01-01').date()
        startDate = startDate.strftime('%Y-%m-%d')

        #Predice el precio del bitcoin para mañana
        prediction = model.get_prediction(start=startDate, end=tomorrow)
        forecast = prediction.predicted_mean[-1]
        return {'date':tomorrow, 'result': forecast, 'message': f'El precio estimado del bitcoin para {tomorrow} es de {forecast}'}, 200
      

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloSerieTiempoStockApple(Resource):
    def post(self):
        
        days = int(request.json['Dias'])

        with open('./../Trained_Models/Modelo_Prediccion_StockApple.pkl', 'rb') as f:
            model = pickle.load(f)
        
        tomorrow = datetime.date.today() + datetime.timedelta(days)
        print(tomorrow)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        print(tomorrow)

        #Startdate es la fecha inicial del DataSet
        startDate = pd.to_datetime('2015-01-01').date()
        startDate = startDate.strftime('%Y-%m-%d')

        #Predice el precio del bitcoin para mañana
        prediction = model.get_prediction(start=startDate, end=tomorrow)
        forecast = prediction.predicted_mean[-1]
        return {'date':tomorrow, 'result': forecast, 'message': f'El precio de las acciones de Apple para el {tomorrow} serán de {forecast}'}, 200
    
#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloSerieTiempoVentasTienda(Resource):
    def post(self):
        days = int(request.json['Dias'])

        with open('./../Trained_Models/Modelo_Prediccion_VentasTienda.pkl', 'rb') as f:
            model = pickle.load(f)
        
        tomorrow = datetime.date.today() + datetime.timedelta(days)
        print(tomorrow)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        print(tomorrow)

        #Startdate es la fecha inicial del DataSet
        startDate = pd.to_datetime('2015-01-01').date()
        startDate = startDate.strftime('%Y-%m-%d')

        #Predice el precio del bitcoin para mañana
        prediction = model.get_prediction(start=startDate, end=tomorrow)
        forecast = prediction.predicted_mean[-1]
        return {'date':tomorrow, 'result': forecast, 'message': f'La cantidad de ventas del producto 1 para el {tomorrow} serán de {forecast}'}, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloSerieTiempoAguacate(Resource):
    def post(self):

        days = int(request.json['Dias'])
        
        with open('./../Trained_Models/Modelo_Prediccion_StockApple.pkl', 'rb') as f:
            model = pickle.load(f)
        
        tomorrow = datetime.date.today() + datetime.timedelta(days)
        print(tomorrow)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        print(tomorrow)

        #Startdate es la fecha inicial del DataSet
        startDate = pd.to_datetime('2015-01-01').date()
        startDate = startDate.strftime('%Y-%m-%d')

        #Predice el precio del bitcoin para mañana
        prediction = model.get_prediction(start=startDate, end=tomorrow)
        forecast = prediction.predicted_mean[-1]
        return {'date':tomorrow, 'result': forecast, 'message': f'El precio del aguacate para {tomorrow} será de {forecast/100}'}, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloRegresionMultipleBMI(Resource):
    def post(self):

        dataPerson = request.json
        print(dataPerson)
        
        with open('./../Trained_Models/Modelo_Prediccion_BMI.pkl', 'rb') as f:
            modelo = pickle.load(f)
        
        # Datos de una nueva persona
        # new_person = {
        #     'Density': [dataPerson['Density']],
        #     'Age': [45],
        #     'Weight': [180],  # en lbs
        #     'Height': [70],   # en pulgadas
        #     'Neck': [38],     # en cm
        #     'Chest': [100],   # en cm
        #     'Abdomen': [90],  # en cm
        #     'Hip': [95],      # en cm
        #     'Thigh': [55],    # en cm
        #     'Knee': [35],     # en cm
        #     'Ankle': [25],    # en cm
        #     'Biceps': [32],   # en cm
        #     'Forearm': [28],  # en cm
        #     'Wrist': [18]     # en cm
        # }

        new_person = {
            'Density': [dataPerson['Density']],
            'Age': [dataPerson['Age']],
            'Weight': [dataPerson['Weight']],  # en lbs
            'Height': [dataPerson['Height']],   # en pulgadas
            'Neck': [dataPerson['Neck']],     # en cm
            'Chest': [dataPerson['Chest']],   # en cm
            'Abdomen': [dataPerson['Abdomen']],  # en cm
            'Hip': [dataPerson['Hip']],      # en cm
            'Thigh': [dataPerson['Thigh']],    # en cm
            'Knee': [dataPerson['Knee']],     # en cm
            'Ankle': [dataPerson['Ankle']],    # en cm
            'Biceps': [dataPerson['Biceps']],   # en cm
            'Forearm': [dataPerson['Forearm']],  # en cm
            'Wrist': [dataPerson['Wrist']]     # en cm
        }

        # Convertir el diccionario en DataFrame
        new_person_df = pd.DataFrame(new_person)

        # Añadir constante
        new_person_df = sm.add_constant(new_person_df)

        # Hacer la predicción
        predicted_body_fat = modelo.predict(new_person_df)
        print(f"Predicted Body Fat Percentage: {predicted_body_fat[0]:.2f}%")
        return {'new_person':new_person, 'result': predicted_body_fat[0], 'message': f'El BMI estimado es de {predicted_body_fat[0]}'}, 200



#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloRegresionMultipleCostoViaje(Resource):
    def post(self):

        dataTrip = request.json
        print(dataTrip)
        
        with open('./../Trained_Models/Modelo_Prediccion_CostoViaje.pkl', 'rb') as f:
            modelo = pickle.load(f)
        
        # Datos de un nuevo viaje
        # new_trip = {
        #     'const':[1.0],
        #     'driver_tip': [13],
        #     'distance': [45],
        #     'toll_amount': [180],
        # }

        new_trip = {
            'const':[dataTrip['const']],
            'driver_tip': [dataTrip['driver_tip']],
            'distance': [dataTrip['distance']],
            'toll_amount': [dataTrip['toll_amount']],
        }

        # Convertir el diccionario en DataFrame
        new_trip_df = pd.DataFrame(new_trip)

        # Hacer la predicción
        prediccion = modelo.predict(new_trip_df)
        print(f"Predicted Total trip amount: {prediccion[0]:.2f}")
        return {'new_trip':new_trip, 'result': prediccion[0], 'message': f'El costo estimado del viaje será de {prediccion[0]}'}, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloRegresionLogisticaCalidadVino(Resource):
    def post(self):

        dataWine = request.json
        print(dataWine)
        
        with open('./../Trained_Models/Modelo_Clasificacion_CalidadVino.pkl', 'rb') as f:
            modelo = pickle.load(f)
        
        # prompt: predecir la calidad de un vino con datos aleatorios
        # newWine = {
        # 'type'                 : [1],    # (1 white) (0 Red)
        # 'fixed acidity'        : [4],    # Entre 3 y 16
        # 'volatile acidity'     : [1.3],    # Entre 0 y 2
        # 'citric acid'          : [0.98],    # Entre 0 y 2
        # 'residual sugar'       : [30],    # Entre 0 y 66
        # 'chlorides'            : [0.58],    # Entre 0 y 1
        # 'free sulfur dioxide'  : [0],    # Entre 1 y 290
        # 'total sulfur dioxide' : [300],    # Entre 6 y 440
        # 'density'              : [0.99],    # Entre 0 y 1.1
        # 'pH'                   : [3.2],    # Entre 2 y 4
        # 'sulphates'            : [1.3],    # Entre 0 y 2
        # 'alcohol'              : [14],    # Entre 8 y 15
        # }

        newWine = {
        'type'                 : [dataWine['type']],    # (1 white) (0 Red)
        'fixed acidity'        : [dataWine['fixed acidity']],    # Entre 3 y 16
        'volatile acidity'     : [dataWine['volatile acidity']],    # Entre 0 y 2
        'citric acid'          : [dataWine['citric acid']],    # Entre 0 y 2
        'residual sugar'       : [dataWine['residual sugar']],    # Entre 0 y 66
        'chlorides'            : [dataWine['chlorides']],    # Entre 0 y 1
        'free sulfur dioxide'  : [dataWine['free sulfur dioxide']],    # Entre 1 y 290
        'total sulfur dioxide' : [dataWine['total sulfur dioxide']],    # Entre 6 y 440
        'density'              : [dataWine['density']],    # Entre 0 y 1.1
        'pH'                   : [dataWine['pH']],    # Entre 2 y 4
        'sulphates'            : [dataWine['sulphates']],    # Entre 0 y 2
        'alcohol'              : [dataWine['alcohol']],    # Entre 8 y 15
        }

        X_test = pd.DataFrame(newWine)
        y_pred_pipeline = modelo.predict(X_test)
        result = y_pred_pipeline.tolist()[0]

        print(f"Predicted quality: {result}")
        return {'new_wine':newWine, 'result': result, 'message': f'La calidad del vino es {result}'}, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloRegresionLogisticaStroke(Resource):
    def post(self):

        dataPacient = request.json
        print(dataPacient)
        
        with open('./../Trained_Models/Modelo_Clasificacion_Stroke.pkl', 'rb') as f:
            modelo = pickle.load(f)
        
        # prompt: predecir la calidad de un vino con datos aleatorios
        # newPacient = {
        # 'gender'             :[ 0  ],  # (1 Male) (0 Female) (2 Other)
        # 'age'                 :[ 25 ],   # Edad
        # 'hypertension'        :[ 1  ],  # (0 No) (1 Yes)
        # 'heart_disease'       :[ 1  ],  # (0 No) (1 Yes)
        # 'ever_married'        :[ 1  ],  # (0 No) (1 Yes)
        # 'work_type'          :[ 3  ],  # (2 Private) (3 Self-employed)
        # 'Residence_type'     :[ 1  ],  # (1 Urban) (0 Rural)
        # 'avg_glucose_level'   :[ 250],    #55 - 272
        # 'bmi'                 :[ 68 ],
        # 'smoking_status'      :[ 3  ]  # (3 Smokes) (1 Formerly) (2 never)
        # }

        newPacient = {
        'gender'              :[dataPacient['gender']],  # (1 Male) (0 Female) (2 Other)
        'age'                 :[dataPacient['age']],   # Edad
        'hypertension'        :[dataPacient['hypertension']],  # (0 No) (1 Yes)
        'heart_disease'       :[dataPacient['heart_disease']],  # (0 No) (1 Yes)
        'ever_married'        :[dataPacient['ever_married']],  # (0 No) (1 Yes)
        'work_type'           :[dataPacient['work_type']],  # (2 Private) (3 Self-employed)
        'Residence_type'      :[dataPacient['Residence_type']],  # (1 Urban) (0 Rural)
        'avg_glucose_level'   :[dataPacient['avg_glucose_level']],    #55 - 272
        'bmi'                 :[dataPacient['bmi']],
        'smoking_status'      :[dataPacient['smoking_status']]  # (3 Smokes) (1 Formerly) (2 never)
        }

        X_test = pd.DataFrame(newPacient)
        y_pred_pipeline = modelo.predict(X_test)
        result = y_pred_pipeline.tolist()[0]

        print(f"Predicted quality: {result}")
        return {'new_pacient':newPacient, 'result': result, 'message': f'El paciente va a tener un problema cardiovascular: {result}'}, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloNaiveBayesHepatitis(Resource):
    def post(self):

        dataHEP = request.json
        print(dataHEP)
        
        with open('./../Trained_Models/Modelo_Clasificacion_Hepatitis.pkl', 'rb') as f:
            model = pickle.load(f)
        
                # Creamos un caso de hepatitis
        #['Age', 'Sex', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE','CHOL', 'CREA', 'GGT', 'PROT']
        # caso_hepatitis = [30, 1, 4.9, 85, 20, 30, 1.5, 1.2, 4.5, 1.2, 48, 7.2]
        caso_hepatitis = [dataHEP['Age'], dataHEP['Sex'], dataHEP['ALB'], dataHEP['ALP'], dataHEP['ALT'], dataHEP['AST'], dataHEP['BIL'], dataHEP['CHE'], dataHEP['CHOL'], dataHEP['CREA'], dataHEP['GGT'], dataHEP['PROT']]


        # Escalamos el caso
        caso_hepatitis_escalado = [caso_hepatitis]

        # Hacemos la predicción
        prediccion = model.predict(caso_hepatitis_escalado)
        print("Prediccion")
        print(prediccion)

        result = prediccion.tolist()[0]
        # Imprimimos la predicción
        print(result)

        return {'patient':caso_hepatitis, 'result': result, 'message': f'Hepatitis tipo : {result}'}, 200

#Modelo para predecir el precio del bitcoin en una fecha 
class ModeloNaiveBayesCirrosis(Resource):
    def post(self):

        dataCirr = request.json
        print(dataCirr)
        
        with open('./../Trained_Models/Modelo_Clasificacion_Cirrosis.pkl', 'rb') as f:
            model = pickle.load(f)
        
                # Creamos un caso de hepatitis
        # cirrosis_case = {
        # 'N_Days': 100,
        # 'Status': 1,
        # 'Drug': 1,
        # 'Age': 50,
        # 'Sex': 1,
        # 'Ascites': 1,
        # 'Hepatomegaly': 1,
        # 'Spiders': 1,
        # 'Edema': 1,
        # 'Bilirubin': 1.5,
        # 'Cholesterol': 200,
        # 'Albumin': 3.5,
        # 'Copper': 100,
        # 'Alk_Phos': 100,
        # 'SGOT': 100,
        # 'Tryglicerides': 100,
        # 'Platelets': 100,
        # 'Prothrombin': 10
        # }

        cirrosis_case = {
        'N_Days': dataCirr['N_Days'],
        'Status': dataCirr['Status'],
        'Drug': dataCirr['Drug'],
        'Age': dataCirr['Age'],
        'Sex': dataCirr['Sex'],
        'Ascites': dataCirr['Ascites'],
        'Hepatomegaly': dataCirr['Hepatomegaly'],
        'Spiders': dataCirr['Spiders'],
        'Edema': dataCirr['Edema'],
        'Bilirubin': dataCirr['Bilirubin'],
        'Cholesterol': dataCirr['Cholesterol'],
        'Albumin': dataCirr['Albumin'],
        'Copper': dataCirr['Copper'],
        'Alk_Phos': dataCirr['Alk_Phos'],
        'SGOT': dataCirr['SGOT'],
        'Tryglicerides': dataCirr['Tryglicerides'],
        'Platelets': dataCirr['Platelets'],
        'Prothrombin': dataCirr['Prothrombin'],
        }

        # Convertir el diccionario a un dataframe
        cirrosis_case_df = pd.DataFrame(cirrosis_case, index=[0])

        # Predecir el caso
        predicted_stage = model.predict(cirrosis_case_df).tolist()[0]

        # Imprimir el resultado
        print(f'Predicted stage for the cirrosis case: {predicted_stage}')

        return {'patient':cirrosis_case, 'result': predicted_stage, 'message': f'Etapa de Cirrosis tipo: {predicted_stage}'}, 200


#Endpoints para los modelos
api.add_resource(HelloWorld, '/')
api.add_resource(VoiceChat, '/voiceChat')
api.add_resource(FaceRecognition, '/faceRecognition')

#Modelos 
api.add_resource(ModeloSerieTiempoBitcoin, '/prediccionBitcoin')
api.add_resource(ModeloSerieTiempoStockApple, '/prediccionStockApple')
api.add_resource(ModeloSerieTiempoVentasTienda, '/prediccionVentasTienda')
api.add_resource(ModeloSerieTiempoAguacate, '/prediccionAguacate')

api.add_resource(ModeloRegresionMultipleBMI, '/prediccionBMI')
api.add_resource(ModeloRegresionMultipleCostoViaje, '/prediccionCostoViaje')

api.add_resource(ModeloRegresionLogisticaCalidadVino, '/clasificacionCalidadVino')
api.add_resource(ModeloRegresionLogisticaStroke, '/clasificacionStroke')
api.add_resource(ModeloNaiveBayesHepatitis, '/clasificacionHepatitis')
api.add_resource(ModeloNaiveBayesCirrosis, '/clasificacionCirrosis')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
