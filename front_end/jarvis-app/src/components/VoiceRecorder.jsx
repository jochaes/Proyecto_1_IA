import React, { useState, useEffect } from 'react';

const  VoiceRecorder = (props) =>  {

    const API_URL = process.env.REACT_APP_API_URL;

    const [recorder, setRecorder] = useState(null);
    const [isRecording, setIsRecording] = useState(false);

    useEffect(() => {
        // Check for MediaRecorder support
        if (!window.MediaRecorder) {
            alert('MediaRecorder not supported on this browser.');
            return;
        }

        // Request permissions and create recorder
        async function prepareRecorder() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                setRecorder(mediaRecorder);
            } catch (error) {
                console.error('Error accessing microphone', error);
                alert('Error accessing microphone');
            }
        }

        prepareRecorder();

        // Cleanup on component unmount
        return () => {
            if (recorder) {
                recorder.stream.getTracks().forEach(track => track.stop());
            }
        };
    }, []);


    useEffect(() => {
        if (!recorder) return;

        let chunks = [];

        recorder.ondataavailable = e => {
            chunks.push(e.data);
        };

        recorder.onstop = async() => {

            console.log(recorder.mimeType);
            const blob = new Blob(chunks, { type: 'webm/opus' });
            chunks = [];
            // const audioURL = URL.createObjectURL(blob);

            //Store audio file in ./audio without document 
            const audioFile = new File([blob], 'recording.ogg', { type: 'webm/opus' });

            //save audioFile in ./audio
            const formData = new FormData();

            formData.append('voiceNote', audioFile);
            
            props.setLoading(true)

            const t = await fetch(`${API_URL}/voiceChat`, {
                method: 'POST',
                body: formData
            });

            
            //Convert t to json and extract text
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
                setIsRecording(true);
            }
        };

        const handleKeyUp = (event) => {
            if (event.code === "Space" && isRecording) {
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
            <h1>Press and hold spacebar to record</h1>
            {isRecording && <p>Recording...</p>}
        </div>
    );
}

export default VoiceRecorder;
