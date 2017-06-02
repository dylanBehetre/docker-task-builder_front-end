module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function CustomNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.nomImage = config.nomImage;
		this.commandeRun = config.commandeRun;
		
		/*Traitement souhaite*/
		this.on('input', function(msg) {
			this.send(msg);
		});
		this.log("CustomNode executed !");
		
	}
	
	RED.nodes.registerType("custom",CustomNode);
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

