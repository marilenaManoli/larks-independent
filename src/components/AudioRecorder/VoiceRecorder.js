import RecordRTC, { StereoAudioRecorder, invokeSaveAsDialog } from "recordrtc";
import React, { useState, useEffect } from "react";
import axios from "axios";

let BASEURL = "";
process.env.NODE_ENV === "development"
	? (BASEURL = process.env.REACT_APP_DEV)
	: (BASEURL = process.env.REACT_APP_PROD);

const VoiceRecorder = (props) => {
	var audio = document.querySelector("audio");
	var audioBlob;

	var isEdge =
		navigator.userAgent.indexOf("Edge") !== -1 &&
		(!!navigator.msSaveOrOpenBlob || !!navigator.msSaveBlob);
	var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

	var recorder;
	var microphone;

	const captureMicrophone = (callback) => {
		if (microphone) {
			callback(microphone);
			return;
		}

		if (typeof navigator.mediaDevices === "undefined" || !navigator.mediaDevices.getUserMedia) {
			alert("This browser does not supports WebRTC getUserMedia API.");

			if (!!navigator.getUserMedia) {
				alert("This browser seems supporting deprecated getUserMedia API.");
			}
		}

		navigator.mediaDevices
			.getUserMedia({
				audio: isEdge
					? true
					: {
							echoCancellation: false,
					  },
			})
			.then(function (mic) {
				callback(mic);
			})
			.catch(function (error) {
				alert("Unable to capture your microphone. Please check console logs.");
				console.error(error);
			});
	};

	const addAudioElement = (src) => {
		audio = document.querySelector("audio");
		var newAudio = document.createElement("audio");
		newAudio.controls = true;

		if (src) {
			newAudio.src = src;
		}

		var parentNode = audio.parentNode;
		parentNode.innerHTML = "";
		parentNode.appendChild(newAudio);

		audio = newAudio;
	};

	const stopRecordingCallback = () => {
		addAudioElement(URL.createObjectURL(recorder.getBlob()));
		audioBlob = recorder.getBlob();
		setTimeout(function () {
			if (!audio.paused) return;

			setTimeout(function () {
				if (!audio.paused) return;
				audio.play();
			}, 1000);

			audio.play();
		}, 300);

		audio.play();
	};

	const initRecorder = () => {
		if (!microphone) {
			captureMicrophone(function (mic) {
				microphone = mic;

				if (isSafari) {
					addAudioElement();

					audio.muted = true;
					audio.srcObject = microphone;

					alert(
						"Please click startRecording button again. First time we tried to access your microphone. Now we will record it."
					);
				}
			});
		}
	};

	initRecorder();

	/////////////////////////////////////////////////
	// Button functions

	const startRecording = () => {
		addAudioElement();

		audio.muted = true;
		audio.srcObject = microphone;

		var options = {
			type: "audio",
			mimeType: "audio/wav",
			recorderType: StereoAudioRecorder,
			numberOfAudioChannels: isEdge ? 1 : 2,
			checkForInactiveTracks: true,
			bufferSize: 16384,
		};

		if (isSafari || isEdge) {
			options.recorderType = StereoAudioRecorder;
		}

		if (isSafari) {
			options.sampleRate = 44100;
			options.bufferSize = 4096;
			options.numberOfAudioChannels = 2;
		}

		if (recorder) {
			recorder.destroy();
			recorder = null;
		}

		recorder = RecordRTC(microphone, options);
		recorder.startRecording();
	};

	const stopRecording = () => {
		recorder.stopRecording(stopRecordingCallback);
	};

	const stopMicrophone = () => {
		if (microphone) {
			microphone.stop();
			microphone = null;
		}
	};

	const btnDownloadRecording = () => {
		if (!recorder || !recorder.getBlob()) return;

		if (isSafari) {
			recorder.getDataURL(function (dataURL) {
				SaveToDisk(dataURL, getFileName("wav"));
			});
			return;
		}

		var blob = recorder.getBlob();
		var file = new File([blob], getFileName("wav"), {
			type: "audio/wav",
		});
		invokeSaveAsDialog(file);
	};

	function getRandomString() {
		if (
			window.crypto &&
			window.crypto.getRandomValues &&
			navigator.userAgent.indexOf("Safari") === -1
		) {
			var a = window.crypto.getRandomValues(new Uint32Array(3)),
				token = "";
			for (var i = 0, l = a.length; i < l; i++) {
				token += a[i].toString(36);
			}
			return token;
		} else {
			return (Math.random() * new Date().getTime()).toString(36).replace(/\./g, "");
		}
	}

	function getFileName(fileExtension) {
		var d = new Date();
		var year = d.getFullYear();
		var month = d.getMonth();
		var date = d.getDate();
		return "RecordRTC-" + year + month + date + "-" + getRandomString() + "." + fileExtension;
	}

	function SaveToDisk(fileURL, fileName) {
		// for non-IE
		if (!window.ActiveXObject) {
			var save = document.createElement("a");
			save.href = fileURL;
			save.download = fileName || "unknown";
			save.style = "display:none;opacity:0;color:transparent;";
			(document.body || document.documentElement).appendChild(save);

			if (typeof save.click === "function") {
				save.click();
			} else {
				save.target = "_blank";
				var event = document.createEvent("Event");
				event.initEvent("click", true, true);
				save.dispatchEvent(event);
			}

			(window.URL || window.webkitURL).revokeObjectURL(save.href);
		}

		// for IE
		else if (!!window.ActiveXObject && document.execCommand) {
			var _window = window.open(fileURL, "_blank");
			_window.document.close();
			_window.document.execCommand("SaveAs", true, fileName || fileURL);
			_window.close();
		}
	}

	const sendTestAudio = async (e) => {
		e.preventDefault();

		const blob = recorder.getBlob();

		let metadata = {
			type: "audio/wav",
		};
		let file = new File([blob], "test.wav", metadata);

		var formData = new FormData();
		formData.append("audio", file);
		try {
			const response = await axios.post(BASEURL + "ramat/audio", formData, {
				headers: {
					"Access-Control-Allow-Origin": "*",
					"Content-Type": "multipart/form-data",
				},
			});
			console.log(response);
		} catch (error) {
			console.error(error);
		}
	};

	const handleSubmit = (e) => {
		e.preventDefault();

		//props.returnAudio();
		props.returnFinished(recorder.getBlob());

		stopMicrophone();
	};

	return (
		<>
			<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0" />

			<br />

			<button id="btn-start-recording" onClick={startRecording}>
				Start Recording
			</button>
			<button id="btn-stop-recording" onClick={stopRecording}>
				Stop Recording
			</button>
			<button id="btn-submit" onClick={handleSubmit}>
				Submit
			</button>
			<button id="btn-test" onClick={sendTestAudio}>
				Test
			</button>

			<div>
				<audio controls autoPlay playsInline></audio>
			</div>
		</>
	);
};

export default VoiceRecorder;
