module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function CustomNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.attribut1 = config.attribut1;
		this.attribut2 = config.attribut2;
		
		/*Creation d'un listener qui permet de recuperer l'entre pour travailler dessus*/
		this.on('input', function(input) {
			// do something with 'input'
		});
		
		/*Traitement souhaite*/
		this.log("CustomNode work !");
		
		
		/*Envoi d'un valeur sur la sortie*/
		var sortie = { payload:"hi" }
		this.send(sortie);
		
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
