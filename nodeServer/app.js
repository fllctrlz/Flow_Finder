const express = require('express');
const app = express();
const mysql = require('mysql');
const path = require('path');
const port = 3000;
const htmlPath = path.join(__dirname, 'index.html');

app.set('views', './views');
app.set('view engine', 'ejs');

app.get('/danger/danger/delete', (request, response) => {
	connectToDatabase((connection) => {
		connection.connect();
		connection.query("truncate table showerData", (err, result) => {
			if (err) throw err;
			response.render('delete.ejs');			
		});
	});
});

app.get('/magnet/total', (request, response) =>{
	connectToDatabase((connection) => {
		connection.connect();
		connection.query("create temporary table temp as (select userInfo.name, showerData.litres from userInfo inner join showerData on userInfo.id=showerData.id); select name, sum(litres) as totalLitres from temp group by name;", (err, result) => {
			if (err) throw err;
			console.log(result[1]);
		        response.end(JSON.stringify(result[1]));
		});
	});
});

app.get('/magnet/average', (request, response) =>{
	response.end("hello there");
});

app.get('/average', (request, response) => {
	connectToDatabase((connection) => {
		connection.connect();
		connection.query("create temporary table temp as (select userInfo.name, showerData.litres from userInfo inner join showerData on userInfo.id=showerData.id); select name, avg(litres) as avgLitres from temp group by name;", (err, result) => {
			if (err) throw err;
			console.log(result[1]);
			response.render('average.ejs', {data: result[1]});
		});
	});
});

app.get('/total', (request, response) => {
	connectToDatabase((connection) => {
		connection.connect();
		connection.query("create temporary table temp as (select userInfo.name, showerData.litres from userInfo inner join showerData on userInfo.id=showerData.id); select name, sum(litres) as totalLitres from temp group by name;", (err, result) => {
			if (err) throw err;
			console.log(result[1]);

			response.render('total.ejs', {data: result[1]});
		});
	});
});

app.get('*', (request, response) => {
	response.render('index.ejs');
});

app.listen(port, (err) => {	
	if (err) {
		return console.log('something went wrong');
	}
	console.log('server is listening on '+port);
});

function connectToDatabase(callback) {
	const connection = mysql.createConnection({
		host : 'localhost',
		user : 'main',
		password : 'ctrlzfll',
		database : 'flowFinder',
		multipleStatements: true
	});
	callback(connection);
}



