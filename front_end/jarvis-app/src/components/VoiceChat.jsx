import React from "react"
import { useState, useEffect } from "react"
import VoiceRecorder from "./VoiceRecorder"
import "./VoiceChat.css"




const VoiceChat = () => {

	const [text, setText] = useState("Transcript will appear here")
	const [loading, setLoading] = useState(false)

	useEffect(() => {
		setLoading(false)
	}, [text])


	return (
		<div className="VC_Main_Component">
			<h2>Voice Chat</h2>
      
      <VoiceRecorder setText={setText} setLoading={setLoading} />

			
			<div className="VC_Screens">
				<div className="VC_Screen">
					<h3>Transcript</h3>

					{loading ? <p>Loading...</p> : <p>{text}</p>}

				</div>

				<div className="VC_Screen">
					<h3>AI</h3>
					<p>Answer will appear here</p>
				</div>
			</div>

		</div>
	)
}

export default VoiceChat
