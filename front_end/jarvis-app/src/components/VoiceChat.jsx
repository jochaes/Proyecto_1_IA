import React from "react"
import { useState, useEffect } from "react"
import VoiceRecorder from "./VoiceRecorder"
import "./VoiceChat.css"
import Form from "./Form"

import CircleLoader from "react-spinners/CircleLoader"
import BeatLoader from "react-spinners/BeatLoader"
import RingLoader from "react-spinners/RingLoader"

const VoiceChat = () => {
	const [text, setText] = useState("") //Texto del usuario
	const [answer, setAnswer] = useState("") //Respuesta de la AI
	const [isRecording, setIsRecording] = useState(false) //Grabando
	const [showForm, setShowForm] = useState(false) //Mostrar formulario
	const [waitingAnswer, setWaitingAnswer] = useState(false) //Esperando respuesta

	const [formFields, setFormFields] = useState([]) //Campos del formulario
	const [endPoint, setEndPoint] = useState("") //Endpoint de la API

	useEffect(() => {
		setWaitingAnswer(false)
		setAnswer("")
		setFormFields([])
		setEndPoint("")
		setShowForm(false)

		if (text !== "") {
			let instruction = getInstruction(text)

			if (instruction === "No se encontró instrucción") {
				setAnswer("No se encontró instrucción")
				return
			}

			let fields = getFormFields(instruction)
			let endpoint = getEndPoint(instruction)

			setFormFields(fields)
			setEndPoint(endpoint)
			setShowForm(true)
	
		}
	}, [text])

	const getEndPoint = instruction => {
		switch (instruction) {
			case "bitcoin":
				return "/prediccionBitcoin"
			case "acciones":
				return "/prediccionStockApple"
			case "venta":
				return "/prediccionVentasTienda"
			case "vino":
				return "/clasificacionCalidadVino"
			case "cardiovascular":
				return "/clasificacionStroke"
			case "masa":
				return "/prediccionBMI"
			case "bicicleta":
				return "/prediccionCostoViaje"
			case "hepatitis":
				return "/clasificacionHepatitis"
			case "cirrosis":
				return "/clasificacionCirrosis"
			case "aguacate":
				return "/prediccionAguacate"
			default:
				break
		}
	}

	const getFormFields = instruction => {
		switch (instruction) {
			case "bitcoin":
				return ["Dias"]
			case "acciones":
				return ["Dias"]
			case "venta":
				return ["Dias"]
			case "vino":
				return [
					"type",
					"fixed acidity",
					"volatile acidity",
					"citric acid",
					"residual sugar",
					"chlorides",
					"free sulfur dioxide",
					"total sulfur dioxide",
					"density",
					"pH",
					"sulphates",
					"alcohol"
				]
			case "cardiovascular":
				return [
					"gender",
					"age",
					"hypertension",
					"heart_disease",
					"ever_married",
					"work_type",
					"Residence_type",
					"avg_glucose_level",
					"bmi",
					"smoking_status"
				]

			case "masa":
				return [
					"Density",
					"Age",
					"Weight",
					"Height",
					"Neck",
					"Chest",
					"Abdomen",
					"Hip",
					"Thigh",
					"Knee",
					"Ankle",
					"Biceps",
					"Forearm",
					"Wrist"
				]
			case "bicicleta":
				return ["const", "driver_tip", "distance", "toll_amount"]

			case "hepatitis":
				return ["Age", "Sex", "ALB", "ALP", "ALT", "AST", "BIL", "CHE", "CHOL", "CREA", "GGT", "PROT"]

			case "cirrosis":
				return [
					"N_Days",
					"Status",
					"Drug",
					"Age",
					"Sex",
					"Ascites",
					"Hepatomegaly",
					"Spiders",
					"Edema",
					"Bilirubin",
					"Cholesterol",
					"Albumin",
					"Copper",
					"Alk_Phos",
					"SGOT",
					"Tryglicerides",
					"Platelets",
					"Prothrombin"
				]

			case "aguacate":
				return ["Dias"]

			default:
				break
		}
	}

	const getInstruction = userText => {
		userText = userText.toLowerCase()
		console.log("Get instruction - User Text:", userText);

		let instructions = [
			"bitcoin",
			"acciones",
			"venta",
			"vino",
			"cardiovascular",
			"masa",
			"bicicleta",
			"hepatitis",
			"cirrosis",
			"aguacate"
		]

		let instruction = instructions.find(instruction => text.includes(instruction))

		if (instruction) {
			return instruction
		} else {
			return "No se encontró instrucción"
		}
	}

	return (
		<div className="VC_Main_Component">
			{/* <button onClick={() => setShowForm(true)}>Show Form</button> */}

			<VoiceRecorder setText={setText} setIsRecording={setIsRecording} setLoading={setWaitingAnswer} />

			<div className="VC_Screens">
				<div className="VC_SPINNER_CONTAINER">
					{isRecording ? (
						<BeatLoader color={"#F16EF1"} loading={true} size={150} aria-label="Loading Spinner" data-testid="loader" />
					) : waitingAnswer ? (
						<RingLoader color={"#F16EF1"} loading={true} size={150} aria-label="Loading Spinner" data-testid="loader" />
					) : (
						<CircleLoader
							color={"#F16EF1"}
							loading={true}
							size={150}
							aria-label="Loading Spinner"
							data-testid="loader"
						/>
					)}
				</div>

				<div className="VC_Screen">
					<h3>Petición</h3>
					{text}
				</div>

				<div className="VC_Screen">
					<h3>Respuesta</h3>
					{answer}
				</div>
			</div>

			{showForm && <Form showForm={showForm} setShowForm={setShowForm} data={formFields} endpoint={endPoint} setAnswer={setAnswer} waitingAnswer={setWaitingAnswer} />}
		</div>
	)
}

export default VoiceChat
