// untuk login
const axios = require('axios')

function login() {
   // debugger
  email = document.getElementById("email").value;
  password = document.getElementById("password").value;

  var xmlRequest = new XMLHttpRequest();
  xmlRequest.open("POST", "http://localhost:5000/login");
  xmlRequest.setRequestHeader("Content-Type", "application/json");
  xmlRequest.send(
    JSON.stringify({
      email: email,
      password: password
    })
  );
  xmlRequest.onreadystatechange = function () {
    // alert(this.response)
    if (this.readyState == 4 && this.status == 200) {
      let data = JSON.parse(this.response)
      debugger
      // alert(this.response)
      document.cookie = "email=" + data.token;
      if(data.position == '4'){
        window.location = "/employee.html"
      }else window.location = "/scm.html"
    } else if (this.readyState == 4) {
      alert("SignIn gagal dengan status code :" + this.status);
    }
  };
}


//   untuk cookienya
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}



function form1() {
  // debugger
 fullname = document.getElementById("fullname").value;
 email = document.getElementById("email").value;
 position = document.getElementById("position").value;
 id_employee = document.getElementById("id_employee").value;
 company = document.getElementById("company").value;
 plant = document.getElementById("plant").value;
 payroll = document.getElementById("payroll").value;
 budget_type = document.getElementById("budget_type").value;
 currency = document.getElementById("currency").value;
 location = document.getElementById("location").value;
 budget_source = document.getElementById("budget_source").value;
 justification = document.getElementById("justification").value;

 var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "http://localhost:5000/form");
  xmlHttp.setRequestHeader("Content-Type", "application/json");
  xmlHttp.send(
    JSON.stringify({
      fullname : fullname,
      email : email,
      position : position,
      id_employee : id_employee,
      company : company,
      plant : plant,
      payroll : payroll,
      budget_type : budget_type,
      currency : currency,
      location : location,
      budget_source : budget_source,
      justification : justification
    })
  );
  /* debugger */
  xmlHttp.onreadystatechange = function () {
    /* debugger */
    if (this.readyState == 4 && this.status == 201) {
      debugger
      alert("Data Has Been Added");
      window.location = "/loginTwitter.html";
    } else if (this.readyState == 4) {
      alert("Please Try Again");
    }
  };
}



function form2() {
  materials = document.getElementByname("materials").value;
  description = document.getElementById("description").value;
  quantity = document.getElementByname("quantity").value;
  unit_measurement = document.getElementsByName("unit_measurement").value;
  price = document.getElementById("price").value;
  material_picture = document.getElementById("material_picture").value;
}