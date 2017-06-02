var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var FormData = require('form-data');

module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function OutputVideoNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.videoName = config.videoName;
		this.priority = config.priority;
		
		var priorityString = "";
		switch (this.priority) {
			case "0" : 
				priorityString = "Normal";
				break;
			case "1" : 
				priorityString = "High";
				break;
			default:
				priorityString = "inconnue";
				break;
		}
		
		this.status({fill:"yellow",shape:"dot",text:"Priority : "+priorityString});
		
		/*Traitement souhaite*/
		var videoOriginalName="";
		this.on('input', function(msg) {
			videoOriginalName = msg.payload;
			this.log(msg);
		});
		this.log(videoOriginalName);
		this.log(this.videoName);
		/*The download*/ //TODO: Reussier déclencher le téléchargement via XMLHttpRequest
		var xhr = new XMLHttpRequest();
 		xhr.open('GET', 'http://localhost:1881/download', true);
		
		var form = new FormData();
 		form.append('originalName', "2013-07-13 20.12.14.jpg");
 		form.append('finalName', this.videoName);
 		//xhr.send(form.toString());
 		xhr.send();
		
		this.send("http://localhost:1881/download");
		
		this.log("OutputVideoNode executed !");
	}
	
	RED.nodes.registerType("output-video",OutputVideoNode);
}

/*
Fonction d'affichage de message :
	this.log("Something happened");
	this.warn("Something happened you should know about");
	this.error("Oh no, something bad happened");
	
Fonction modifiant le status :
	this.status({fill:"red, green, yellow, blue or grey",shape:"ring or dot",text:"disconnected"});
	
	this.status({fill:"green",shape:"dot",text:"connected"});
	this.status({fill:"red",shape:"ring",text:"disconnected"});
*/

