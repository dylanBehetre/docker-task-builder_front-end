module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function InputVideoNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.video = config.video;
		
		/*Traitement souhaite*/
		this.log("InputVideoNode fct !");
		this.status({fill:"yellow",shape:"dot",text:this.video});
		
		this.on('change', function(input) {
			this.log("InputVideo change fct !");
		});
		
		
		/*Envoi d'un valeur sur la sortie*/
		var sortie = { payload:"hi" }
		this.send(sortie);
		
	}
	
	RED.nodes.registerType("input-video",InputVideoNode);
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
