var express = require("express");
var app = express();

var formidable = require('formidable');
var fs = require('fs');

var uploadFilePath = 'C:\Users\Dylan';
//var uploadFilePath = '/mnt/glusterfs';

var downloadFilePath = __dirname;
//var downloadFilePath = '/mnt/glusterfs';

app.post('/upload', function(req, res){
	res.setHeader('Access-Control-Allow-Origin', '*');
	res.write("Upload demarré !");
	var form = new formidable.IncomingForm();
	form.parse(req, function (err, fields, files) {
		//console.log(files);
		var oldpath = files.maVideo.path;
		var newpath = uploadFilePath + files.maVideo.name;
		console.log(files.maVideo.name+" a ete uploade !");
		fs.rename(oldpath, newpath, function (err) {
			if (err) throw err;
			
			res.write("Upload reussi !");
			res.end();
		});
	});
});

app.get('/download', function(req, res){
	/*Essai pour le parsage des infos*/
	/*var form = new formidable.IncomingForm();
	console.log(form);
	form.parse(req, function (err, fields, files) {
		console.log(files);
		var filename = files.maVideo.path;
		var newpath = 'C:\Users\Dylan' + files.maVideo.name;
	});*/
	/*fin de l'essai*/
	var filename = 'test.jpg';
	console.log("Telechargement de "+filename+" lance !");
	var file = downloadFilePath+'/'+ filename;
	console.log(file);
	
	res.download(file, filename, function(err){
	  if (err) {
		console.log(err);
	  } else {
		  console.log("Telechargement de "+filename+" fini !");
		// decrement a download credit, etc.
	  }
	});	
});

app.listen(1881, function(){
		console.log("ServeurExpress lance !");
});

