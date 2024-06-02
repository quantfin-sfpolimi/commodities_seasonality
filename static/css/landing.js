url = "http://127.0.0.1:8000/" + "aapl"

let start_year = document.getElementById("startYear").value
let end_year = document.getElementById("endYear").value
let ticker = document.getElementById("ticker").value

url = "/"+ticker+"?start="+start_year.toString() + "&end=" + end_year.toString()

function redirect(){
    console.log("entrato in redirect")
    
    let start_year = document.getElementById("startYear").value
    let end_year = document.getElementById("endYear").value
    let ticker = document.getElementById("ticker").value
    if (start_year && end_year){
        url = "/"+ticker+"?start="+start_year.toString() + "&end=" + end_year.toString()
    }
    else{
        url = "/"+ticker
    }
    window.location.assign(url)

}


var button = document.getElementById("submit-btn");


console.log(button)

button.addEventListener("click", redirect);









