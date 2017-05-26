module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function ResolutionNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.resolution = config.resolution;
		
		/*Creation d'un listener qui permet de recuperer l'entre pour travailler dessus*/
		this.on('input', function(input) {
			// do something with 'input'
		});
		
		/*Traitement souhaite*/
		this.log("ResolutionNode work !");
		this.status({fill:"yellow",shape:"dot",text:this.resolution});
		
		
		/*Envoi d'un valeur sur la sortie*/
		var sortie = { payload:"hi" }
		this.send(sortie);
		
	}
	
	RED.nodes.registerType("resolution", ResolutionNode);
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

