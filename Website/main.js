// JavaScript Document

// Importing templates
var templatesImport = document.getElementById('templates');
var templates = templatesImport.import;

var listing = templates.getElementById('reportListing');
var navbar = templates.getElementById('navbar');



// Responsive Shit
function updateColumns(x) {
    if (x.matches) { // If media query matches
		console.log("add");
        $("#content .seven").addClass("columns");
        $("#content .five").addClass("columns");
    } else {
		console.log("remove");
        $("#content .seven").removeClass("columns");
        $("#content .five").removeClass("columns");
    }
}

var x = window.matchMedia("(min-width: 900px)")
updateColumns(x) // Call listener function at run time
x.addListener(updateColumns) // Attach listener function on state changes


// Constants

const mainEndpoint = "http://trace-api.herokuapp.com/report"
const url = mainEndpoint + "?pageNumber=0&pageSize=10";
var ul = document.getElementById("searchResults");
var ul2 = document.getElementById("another-one");
var ul3 = document.getElementById("another-one-two");
var results = document.getElementById("searchResults");
var tables = [ul, ul2, ul3, results];


// Initialize

$('document').ready(function(){
	console.log("Ready");
	var c = document.importNode(navbar.content, true);
	document.getElementById('navbar').appendChild(c);
});

// Helper Functions

function clearTables() { // Remove all table rows from all tables
	for (t in tables) {
		tables[t].innerHTML = "";
	}
}




// Search Input

var input = document.getElementById("searchInput");

input.addEventListener("keyup", function (event) {
	event.preventDefault();
	if (event.keyCode === 13) {
		console.log("print");
		document.getElementById("searchButton").click();
	}
});


// Display Search Results
function sendSearch() {
	var search = document.getElementById("searchInput");
	sendRequest(url + "&search=" + search.value);
}


console.log(ul);

function sendRequest(url) {
	const options = {
		method: 'GET'
	};
	fetch(url, options)
		.then((resp) => resp.json())
		.then(function (data) {
			clearTables();
			return data.result.map(function (report) {
				var clone = document.importNode(listing.content, true);
				clone.querySelector('.report-name').innerText = report.name;
				clone.querySelector('.report-subject').innerText = report.subject;
				clone.querySelector('.report-instr').innerText = report.instructor.lastName + ", " + report.instructor.firstName;
				clone.querySelector('.report-term').innerText = report.term.title;
				clone.querySelector('.report-view a').setAttribute("onclick", "viewReport('" + report._id.$oid + "')");
				document.getElementById('searchResults').appendChild(clone);
//				var html =
//					'<tr>' +
//					'<td>' + report.name + '</td>' +
//					'<td>' + report.subject + '</td>' +
//					'<td>' + report.instructor.lastName + ", " + report.instructor.firstName + '</td>' +
//					'<td>' + report.term.title + '</td>' +
//					'<td><a onclick=\"viewReport(\'' + report._id.$oid + '\')\">View</a></td>' +
//					'</tr>';
//				ul.innerHTML += html;
			});
		})
		.catch(function (error) {
			console.log(error);
		});
}





function viewReport(id) {
	console.log(id);
	sendReport(mainEndpoint + "/" + id);
}

function sendReport(url) {
	const options = {
		method: 'GET'
	};
	fetch(url, options)
		.then((resp) => resp.json())
		.then(function (data) {
			console.log("here");
			clearTables();
			//		  console.log(data.result);
			report = data.result;
			var html =
				'<tr>' +
				'<td>' + report.name + '</td>' +
				'<td>' + report.subject + '</td>' +
				'<td>' + report.instructor.lastName + ", " + report.instructor.firstName + '</td>' +
				'<td>' + report.term.title + '</td>' +
				'<td><a onclick=\"viewReport(\'' + report._id.$oid + '\')\">View</a></td>' +
				'</tr>';
			ul.innerHTML += html;
			Object.keys(report.data[0]).map(function (key) {
				ul.innerHTML +=
					'<p>' + key + " : " + report.data[0][key] + '</p>';
			})

			var header = "";
			Object.keys(report.data[1]).map(function (key) {
				header += '<th>' + key + '</th>';
			})

			ul.innerHTML += '<tr>' + header + '</tr>';
			report.data.slice(1, report.data.length - 2).map(function (stat) {
				console.log(stat);
				body = "";
				Object.keys(stat).map(function (key) {
					body += '<td>' + stat[key] + '</td>';
				})
				ul.innerHTML += '<tr>' + body + '</tr>';
			});
			report.data.slice(report.data.length - 2, report.data.length - 1).map(function (stat) {
				console.log(stat);
				header = "";
				body = "";
				Object.keys(stat).map(function (key) {
					header += '<th>' + key + '</th>';
				})
				Object.keys(stat).map(function (key) {
					body += '<td>' + stat[key] + '</td>';
				})
				header = '<tr>' + header + '</tr>';
				body = '<tr>' + body + '</tr>';
				ul2.innerHTML += header + body;
			});
			report.data.slice(report.data.length - 1).map(function (stat) {
				console.log(stat);
				header = "";
				body = "";
				Object.keys(stat).map(function (key) {
					header += '<th>' + key + '</th>';
				})
				Object.keys(stat).map(function (key) {
					body += '<td>' + stat[key] + '</td>';
				})
				header = '<tr>' + header + '</tr>';
				body = '<tr>' + body + '</tr>';
				ul3.innerHTML += header + body;
			});
		})
		.catch(function (error) {
			console.log(error);
		});
}
