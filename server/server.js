/*var express = require("express");
var bodyParser = require('body-parser');
var app = express();

app.post('/upload', function(req, res){
	console.log('Debut upload !');
	
});

app.listen(1881);
console.log('Serveur Demarré');

*/

var http = require('http');
var formidable = require('formidable');
var fs = require('fs');

http.createServer(function (req, res) {
	console.log("Fct !");
	if (req.url == '/upload') {
		var form = new formidable.IncomingForm();
		//console.log(form);
		form.parse(req, function (err, fields, files) {
			var oldpath = files.filetoupload.path;
			var newpath = 'C:\Users\Dylan' + files.filetoupload.name;
			fs.rename(oldpath, newpath, function (err) {
				if (err) throw err;
			});
		});
	}
}).listen(1881);

console.log("Serveur lancé !");