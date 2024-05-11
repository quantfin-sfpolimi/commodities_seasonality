let inputForm = document.getElementById('inputForm')

inputForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let start = document.getElementById("startYear").value
  let end = document.getElementById("endYear").value
    
    let input = {
        "start": parseInt(start),
        "end": parseInt(end),
    }


    console.log(input)

    url = 'https://127.0.0.1:8000/' + 'get-year/' + start + end
    window.location.href = url
})