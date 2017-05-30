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

var express = require("express");
var app = express();

var server = http.createServer(function (req, res) {
	res.setHeader('Access-Control-Allow-Origin', '*');
	
	if (req.url == '/upload') {
		var form = new formidable.IncomingForm();
		form.parse(req, function (err, fields, files) {
			console.log(files);
			var oldpath = files.maVideo.path;
			//var newpath = 'C:\Users\Dylan' + files.maVideo.name;
			var newpath = 'C:\Users\Dylan' + files.maVideo.name;
			console.log(files.maVideo.name+" a ete uploade !");
			fs.rename(oldpath, newpath, function (err) {
				if (err) throw err;
				res.write("Upload reussi !");
				res.end();
			});
		});
	}

	res.writeHead(200);
	res.end('Ok !');
});

server.listen(1881, function(){
		console.log("Serveur lancé !");
});

app.get('/download', function(req, res){
		var filename = 'test.jpg';
		console.log("Telechargement de "+filename+" lance !");
		var file = __dirname +'/'+ filename;
		
		res.download(file, filename, function(err){
		  if (err) {
			console.log(err);
		  } else {
			// decrement a download credit, etc.
		  }
		});
		
});

app.listen(1882, function(){
		console.log("ServeurExpress");
});

