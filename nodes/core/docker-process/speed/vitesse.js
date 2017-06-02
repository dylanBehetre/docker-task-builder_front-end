module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function SpeedNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.vitesseVideo = config.vitesseVideo;
		this.vitesseSon = config.vitesseSon;

		/*Traitement souhaite*/
		this.status({fill:"yellow",shape:"dot",text:"Video:"+this.vitesseVideo+"\r\n"+"Son:"+this.vitesseSon});
		
		this.on('input', function(msg) {
			this.send(msg);
		});
		
		this.log("SpeedNode executed !");
	}
	
	RED.nodes.registerType("speed",SpeedNode);
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

