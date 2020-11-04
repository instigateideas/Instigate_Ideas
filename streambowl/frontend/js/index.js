"use strict";

var myInit = {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json'
	},
	body: JSON.stringify({"page_no": 3}),
	mode: 'no-cors',
	cache: 'default'
};

let myRequest = new Request("http://localhost:5001/prefered/movies_list", myInit);
var jsondata

fetch(myRequest)
	.then(function(resp) {
		return resp.text();
	})
	.then(function(data) {
			var jsondata = data;
			console.log(jsondata);
		}
	)