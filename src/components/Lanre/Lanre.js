import React, { Component } from "react";
import { Link } from "react-router-dom";
import LanreWebcamCapture from "../Lanre/lanre_camera";
import "../App/App.css";

import Header from "../Header/Header";

class Lanre extends Component {
	render() {
		return (
			<div className="Lanre">
				<Header />
				<h1>Lanre's app</h1>
				<div>
					<div className="webcam-capture-holder">
						<p>Webcam capture below (to use flash please brighten your screen)</p>
						<LanreWebcamCapture />
						
					</div>
					<Link to="/home">
						<button> Back </button>
					</Link>
					<Link to="/lanre/dipstik-home">
						<button> Instructions </button>
					</Link>
				</div>
			</div>
		);
	}
}

export default Lanre;
