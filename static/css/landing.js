<<<<<<< HEAD
url = "http://127.0.0.1:8000/" + "aapl"

let start_year = document.getElementById("startYear").value
let end_year = document.getElementById("endYear").value
let ticker = document.getElementById("ticker").value

url = "/"+ticker+"?start="+start_year.toString() + "&end=" + end_year.toString()

=======
>>>>>>> 37c8ef0fc617875c7d5d31bc22b826afef6d9d90
function redirect(){
    /**
     * Redirects the user to a URL based on input field values for start year, end year, and ticker.
     *
     * This function retrieves values from input fields with IDs "startYear", "endYear", and "ticker",
     * constructs a URL with query parameters for the start and end years if they are provided,
     * and redirects the user to the constructed URL.
     */

    // Pick parameters from input fields
    let start_year = document.getElementById("startYear").value
    let end_year = document.getElementById("endYear").value
    let ticker = document.getElementById("ticker").value

    // Add query parameters only if needed (needed = user wrote start and end)
    if (start_year && end_year)
        url = "/" + ticker + "?start=" + start_year.toString() + "&end=" + end_year.toString()
    else
        url = "/" + ticker

    window.location.assign(url)
}


<<<<<<< HEAD
var button = document.getElementById("submit-btn");


console.log(button)

button.addEventListener("click", redirect);









=======
// Call the redirect function
let button = document.getElementById("submit-btn");
button.addEventListener("click", redirect);
>>>>>>> 37c8ef0fc617875c7d5d31bc22b826afef6d9d90
