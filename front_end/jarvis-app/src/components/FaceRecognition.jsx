import React, { useState, useRef, useEffect } from "react"

import "./FaceRecognition.css"
import RingLoader from "react-spinners/RingLoader"

const FaceRecognition = () => {
	const API_URL = process.env.REACT_APP_API_URL
	const videoRef = useRef(null)
	const [imageData, setImageData] = useState(null)
	const [response, setResponse] = useState("")
	const [loading, setLoading] = useState(false)

	// useEffect(() => {
	// 	startCamera();
	// }, []);

	const startCamera = async () => {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ video: true })
			videoRef.current.srcObject = stream
		} catch (error) {
			console.error("Error accessing camera:", error)
		}
	}

	const stopCamera = async () => {
		videoRef.current.srcObject = null
	}

	const handleTakePicture = async () => {
		try {
			const video = videoRef.current
			const canvas = document.createElement("canvas")
			canvas.width = video.videoWidth
			canvas.height = video.videoHeight
			canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height)

			const dataURL = canvas.toDataURL("image/png")
			setImageData(dataURL)
		} catch (error) {
			console.error("Error taking picture:", error)
		}
	}

	const handleFileInputChange = event => {
		const file = event.target.files[0]
		const reader = new FileReader()

		reader.onload = () => {
			setImageData(reader.result)
		}

		reader.readAsDataURL(file)
	}

	const handleSendImage = async () => {
		setLoading(true)

		try {
			const formData = new FormData()
			//Send imageData as an image file blob with form data
			const imagePromise = await fetch(imageData)
				.then(response => response.blob())
				.then(blob => {
					const file = new File([blob], "image.jpeg", { type: "image/jpeg" })
					formData.append("image", file)
				})

			Promise.all([imagePromise]).then(async () => {
				const response = await fetch(`${API_URL}/faceRecognition`, {
					method: "POST",
					body: formData
				})

				const data = await response.json()
				
				const responseString = JSON.stringify(data.message, null, 2)


				setResponse(responseString)
				setLoading(false)
			})
		} catch (error) {
			setLoading(false)
			console.error("Error sending image:", error)
		}
	}

	return (
		<div className="FC_Component">
			<h4>Reconocimiento de Sentimientos</h4>
			<div className="FC_Container">
				<div className="FC_Video_Component">
					<video ref={videoRef} autoPlay playsInline style={{ width: "100%", maxWidth: "500px" }} />
					<div className="FC_Buttons_1">
						<button onClick={handleTakePicture}>Tomar Fotografía</button>
						<button onClick={stopCamera}>Detener</button>
						<button onClick={startCamera}>Iniciar</button>
					</div>
				</div>

				<div className="FC_Image_Container">
					<div className="FC_Image_Component">
						{imageData && <img src={imageData} alt="Captured" style={{ maxWidth: "500px" }} />}
					</div>

					<div className="FC_Buttons_2">
						<label htmlFor="file-upload" className="custom-file-upload">
							Buscar Imágen
						</label>
						<input id="file-upload" type="file" accept="image/*" onChange={handleFileInputChange} />
						<button onClick={handleSendImage}>Enviar</button>
					</div>
				</div>
			</div>

			<div className="FC_Response">
				{loading && <RingLoader color={"#BA00BA"} loading={true} size={150} aria-label="Loading Spinner" data-testid="loader" />}
				<p>{response}</p>
			</div>
		</div>
	)
}

export default FaceRecognition
