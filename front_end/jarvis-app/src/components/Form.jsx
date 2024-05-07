import React from "react"
import { useState, useEffect } from "react"
import './Form.css'

const Form = props => {

	const API_URL = process.env.REACT_APP_API_URL;	
	const [formData, setFormData] = useState({})


  //Use effect para llenar el objeto form con los campos del formulario
  //Se ejecuta cuando se muestra el formulario
	useEffect(() => {
		
		let data = props.data     //Los campos del formulario
		let form = {}             //El objeto que se va a llenar con los campos del formulario

    //Iterar sobre los campos del formulario y agregarlos al objeto form
		data.forEach(item => {
			form[item] = ""
		})

    //Colocar el objeto form en el estado formData
		setFormData(form)
	}, [props.showForm])

  //Funcion para manejar los cambios en los inputs del formulario
	const handleChange = e => {
		let key = e.target.placeholder
		let value = e.target.value

    //Actualizar el estado formData con el valor del input
    setFormData({ ...formData, [key]: value })
	}

  //Funcion para manejar el envio del formulario
	const handleSubmit = async (e) => {
		e.preventDefault()
		console.log("Form Data:", formData)

		//Enviar los datos al servidor
		
		const response = await fetch(`${API_URL}${props.endpoint}`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(formData)
		})

		const data = await response.json()

		console.log("Response:", data)


    //Limpia y cierra el formulario
		setFormData({})
		props.setShowForm(false)
	}

	return (
		<div className="overlay">
			<div className="form-container">
				<h2>Ingrese los Datos</h2>
				<form onSubmit={handleSubmit}>

          <div className="input-container">

          {/* Por cada llave del formulario crea  un input */}
					{Object.keys(formData).map((key, index) => {
						return <input required key={index} type="number" placeholder={key} onChange={handleChange} />
					})}
          </div>
          
					<button type="submit">Enviar</button>
				</form>
			</div>
		</div>
	)
}

export default Form