/*
*Author: CTRL-Z Robotics
*
*This program will take information from the raspberry pi via the MySql database and create a web server
*The information on the server will be used by the display program to be displayed on the E-Ink screen
*This server will be accessible from any device on the same Wi-Fi network
*/


// initializing various constents by require different libraries
const express = require('express');
const app = express();
const mysql = require('mysql');
const path = require('path');
const port = 3000;
const htmlPath = path.join(__dirname, 'index.html');

app.set('views', './views');
app.set('view engine', 'ejs');

//if the server gets a request with the '/danger/danger/delete' the server will delete all data from the database
app.get('/danger/danger/delete', (request, response) => {
	connectToDatabase((connection) => {
		connection.connect();
		connection.query("truncate table showerData", (err, result) => {
			if (err) throw err;
			response.render('delete.ejs');			
		});
	});
});
//if the server gets a request with the '/magnet/total' from the fridge magnet, this function will return an array with the 
//data requested for in the universal JSON format so that it is readable from any language 
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

//if the server gets a request with the '/average' the server display a table with each users average water usage
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

//if the server gets a request with the '/total' the server display a table with each users total water usage
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
//if the server gets a request with the default url the server will display the home webpage
app.get('*', (request, response) => {
	response.render('index.ejs');
});

//starting the server 
app.listen(port, (err) => {	
	if (err) {
		return console.log('something went wrong');
	}
	console.log('server is listening on '+port);
});
//connecting to the MySql database
function connectToDatabase(callback) {
	const connection = mysql.createConnection({
		host : 'localhost',
		user : 'main',
		password : '*****',
		database : 'flowFinder',
		multipleStatements: true
	});
	callback(connection);
}



