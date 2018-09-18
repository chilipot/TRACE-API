// JavaScript Document

// Get the input field
var input = document.getElementById("searchInput");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Cancel the default action, if needed
  event.preventDefault();
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
	  console.log("print");
    // Trigger the button element with a click
    document.getElementById("searchButton").click();
  }
});


  var ul = document.getElementById("test");
console.log(ul);
//  const url = "http://trace-api.herokuapp.com/report?pageNumber=0&pageSize=10";
  const mainEndpoint = "http://trace-api.herokuapp.com/report"
  const url = mainEndpoint + "?pageNumber=0&pageSize=10";

function sendSearch() {
	var search = document.getElementById("searchInput");
	console.log(search);
	console.log(search.value);
//	sendRequest(url + "&search=" + "\"" + search.value + "\"");
	sendRequest(url + "&search=" + search.value );
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
	  .then(function(data) {
		  console.log("here");
		  ul.innerHTML = "";
//		  console.log(data.result);
		  report = data.result; 
			var html = 
				'<tr>' +
					'<td>' + report.name + '</td>' +
					'<td>' + report.subject + '</td>' +
					'<td>' + report.instructor.lastName + ", " + report.instructor.firstName+ '</td>' +
					'<td>' + report.term.title + '</td>' +
					'<td><a onclick=\"viewReport(\'' + report._id.$oid + '\')\">View</a></td>' +
				'</tr>';
			ul.innerHTML += html;
		  ul.innerHTML += '<tr><td>' + report.data[0].Enrollment + '</tr></td>';
			report.data.map(function(stat) {
				console.log(stat);
				var html = 
					'<tr>' +
						'<td>' + stat + '</td>'
					'</tr>';
				ul.innerHTML += html;
			});
		  })
	  .catch(function(error) {
		console.log(error);
	  });
}
			

function sendRequest(url) {
	const options = {
	  method: 'GET'
	};
	  fetch(url, options)
	  .then((resp) => resp.json())
	  .then(function(data) {
		  console.log("here");
		  ul.innerHTML = ""

		  
		return data.result.map(function(report) {
				var html = 
					'<tr>' +
						'<td>' + report.name + '</td>' +
						'<td>' + report.subject + '</td>' +
						'<td>' + report.instructor.lastName + ", " + report.instructor.firstName+ '</td>' +
						'<td>' + report.term.title + '</td>' +
						'<td><a onclick=\"viewReport(\'' + report._id.$oid + '\')\">View</a></td>' +
					'</tr>';
				ul.innerHTML += html;
		});
	  })
	  .catch(function(error) {
		console.log(error);
	  }); 
}  

