module.exports = function(RED) {
	/*Fonction servant de constructeur*/
	function OutputVideoNode(config) {
		/*Initialisation des fonctionnalités de bases*/
		RED.nodes.createNode(this, config);
		
		/*Recupération des parametres configurer dans le noeud*/
		this.video = config.video;
		this.priority = config.priority;
		
		/*Creation d'un listener qui permet de recuperer l'entre pour travailler dessus*/
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
		this.on('input', function(input) {
			// do something with 'input'
		});
		
		/*Traitement souhaite*/
		this.log("OutputVideo work !");
		
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

