var express = require("express");
var app = express();

var formidable = require('formidable');
var fs = require('fs');

app.post('/upload', function(req, res){
	res.setHeader('Access-Control-Allow-Origin', '*');
	res.write("Upload demarré !");
		var form = new formidable.IncomingForm();
		form.parse(req, function (err, fields, files) {
			console.log(files);
			var oldpath = files.maVideo.path;
			var newpath = 'C:\Users\Dylan' + files.maVideo.name;
			//var newpath = '/mnt/glusterfs' + files.maVideo.name;
			console.log(files.maVideo.name+" a ete uploade !");
			fs.rename(oldpath, newpath, function (err) {
				if (err) throw err;
				res.write("Upload reussi !");
				res.end();
				
			});
		});
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

app.listen(1881, function(){
		console.log("ServeurExpress lance !");
});

