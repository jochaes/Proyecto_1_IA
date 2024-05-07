import React, { useState, useEffect } from 'react';

const  VoiceRecorder = (props) =>  {

    const API_URL = process.env.REACT_APP_API_URL;

    const [recorder, setRecorder] = useState(null);
    const [isRecording, setIsRecording] = useState(false);

    useEffect(() => {

        // Revisa si el navegador soporta MediaRecorder
        if (!window.MediaRecorder) {
            alert('MediaRecorder no está soportado en el navegador.');
            return;
        }

        // Pide permiso para acceder al microfono
        async function prepareRecorder() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                setRecorder(mediaRecorder);
            } catch (error) {
                console.error('Error accediento al microfono', error);
                alert('Error accediento al microfono');
            }
        }

        //Prepara el recorder
        prepareRecorder();

        // Limpiar el stream del recorder
        return () => {
            if (recorder) {
                recorder.stream.getTracks().forEach(track => track.stop());
            }
        };
    }, []);


    useEffect(() => {
        if (!recorder) return;

        //Limpia el texto del usuario
        props.setText("")

        let chunks = [];

        //Cuando se recibe data del recorder
        recorder.ondataavailable = e => {
            chunks.push(e.data);
        };

        //Cuando se detiene el recorder
        recorder.onstop = async() => {

            
            
            const blob = new Blob(chunks, { type: 'webm/opus' });
            chunks = [];
            

            //Crea un archivo de audio con el blob
            const audioFile = new File([blob], 'recording.ogg', { type: 'webm/opus' });

            //Crea un formData y le agrega el archivo de audio
            const formData = new FormData();

            //Agrega el archivo de audio al formData
            formData.append('voiceNote', audioFile);
            
            //Muestra el loading
            props.setLoading(true)

            //Envia el formData al servidor
            const t = await fetch(`${API_URL}/voiceChat`, {
                method: 'POST',
                body: formData
            });

            
            //Convierte la respuesta a JSON y la guarda en el estado text
            const json = await t.json();
            props.setText(json.transcription)
            props.setLoading(false)
            console.log(t);

        };

        if (isRecording) {
            recorder.start();
        } else {
            recorder.stop();
        }

        return () => {
            if (recorder) {
                recorder.ondataavailable = null;
                recorder.onstop = null;
            }
        };
    }, [isRecording, recorder]);

    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.code === "Space" && !isRecording) {
                props.setIsRecording(true);
                setIsRecording(true);
            }
        };

        const handleKeyUp = (event) => {
            if (event.code === "Space" && isRecording) {
                props.setIsRecording(false);
                setIsRecording(false);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
        };
    }, [isRecording]);

    return (
        <div>
            <h4>Presione y Mantenga la Barra Espaciadora Para Grabar</h4>
            {/* {isRecording && <p>Recording...</p>} */}
        </div>
    );
}

export default VoiceRecorder;
