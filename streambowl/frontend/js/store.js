const proxyurl = "https://cryptic-headland-94862.herokuapp.com/";
let path = "http://127.0.0.1:5001/health_check";

var init_var = {method: 'GET',
				mode: 'no-cors',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
					'Access-Control-Allow-Origin':  'http://127.0.0.1:5001',
					'Access-Control-Allow-Methods': 'POST',
					'Access-Control-Allow-Headers': 'Content-Type'
				}
			};

const GetHealthStatus = (async() => {
		 const response = await fetch(path, init_var);
		 const myJson = await response.text(); //extract JSON from the http response
		 console.log(myJson)
		 return myJson
		})();

console.log(GetHealthStatus);
console.log("Hello world")

let path = "http://127.0.0.1:5001/prefered/movies_list";
var init_var = {method: 'POST',
				mode: 'no-cors',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json',
					'Access-Control-Allow-Origin':  'http://127.0.0.1:5001',
					'Access-Control-Allow-Methods': 'POST',
					'Access-Control-Allow-Headers': 'Content-Type'
				},
				body: JSON.stringify({"page_no": 1})
			};

const PreferedMovieData = (async() => {
		 const response = await fetch(path, init_var);
		 const myJson = await response.text(); //extract JSON from the http response
		 return myJson
		});
PreferedMovieData().then(data => console.log(data));

function PreferedMovieData() {
	fetch("http://127.0.0.1:5001/prefered/movies_list", {
					method: 'POST',
					mode: 'no-cors',
					headers: {
						'Content-Type': 'application/json',
						'Accept': 'application/json',
						'Access-Control-Allow-Origin':  'http://127.0.0.1:5001',
						'Access-Control-Allow-Methods': 'POST',
						'Access-Control-Allow-Headers': 'Content-Type'
					},
					body: JSON.stringify({"page_no": 1})}).then(
		response => response.text()).then(function(responseText)).then({console.log(responseText);})
}
PreferedMovieData();







let path = "http://127.0.0.1:5001/prefered/movies_list";
function PreferedMovieData() {
	var init_var = {method: 'POST',
					mode: 'no-cors',
					headers: {
						'Content-Type': 'application/json',
						'Accept': 'application/json',
						'Access-Control-Allow-Origin':  'http://127.0.0.1:5001',
						'Access-Control-Allow-Methods': 'POST',
						'Access-Control-Allow-Headers': 'Content-Type'
					},
					body: JSON.stringify({"page_no": 1})
				};
	fetch("http://127.0.0.1:5001/prefered/movies_list", init_var).then(
		response => response.json()
		).then(
		data => {console.log(data)});
}
PreferedMovieData();

const proxyurl = "https://cors-anywhere.herokuapp.com/";
const url = "https://127.0.0.1:5001/health_check"; // site that doesn’t send Access-Control-*
fetch(proxyurl + url) // https://cors-anywhere.herokuapp.com/https://example.com
.then(response => response.text())
.then(contents => console.log(contents))
.catch(() => console.log("Can’t access " + url + " response. Blocked by browser?"))
