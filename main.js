// untuk login
const axios = require('axios')

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

function removeCookie() {
  document.cookie = 'token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  document.cookie = 'requester=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  window.location = '/login.html';
}

function home(){
  var a= getCookie('requester')
  a == "true" ? window.location = "/employee.html" : window.location = "/scm.html"
}

function login() {
  $.ajax({
    method: "POST",
    url: "http://localhost:9000/login",
    beforeSend: function(req) {
      req.setRequestHeader('Content-Type', 'application/json')
    },
    data: JSON.stringify ({
      "email" : document.getElementById('email').value,
      "password" : document.getElementById('password').value
    }),
    success : function(res) {
      data = JSON.parse(res)
      if (data.position == 4) {
        var isRequest = true
      } else {
        var isRequest = false
      }
      alert("Login Success");
      document.cookie = `token=${data.token}`
      document.cookie = `requester=${isRequest}`
      if (isRequest){
        window.location = "/employee.html"
      }else{
        window.location = "/scm.html"
      }
    },
    error : function(err) {
      alert ("email atau password salah: "+this.status);
      console.log(err)
    }
  })
}

function getProfile() {
  $.ajax({
    method : 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function(req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success : function(res) {
      data = JSON.parse(res)
      console.log(data)
      document.getElementById('dropdown').insertAdjacentHTML("afterbegin", `<div class="dropdown__user">
      <img class="dropbtn" href="#" src="${data.photoprofile}" alt="orang" />
      <a id="profile-name" href="profile.html"> ${data.fullname}</a>
      <div class="dropdown-content">
          <a href="edit.html"><i class="fas fa-cogs"></i> Setting and Privacy</a>
          <a href="#"><i class="far fa-question-circle"></i> Help Center</a>
          <a onclick="removeCookie()" href="Login.html" id="logout-button"><i class="fas fa-power-off"></i> Log Out</a>
      </div>
  </div>`)
    },
    error : function(err) {
      console.log(err)
    }
  })
}

function welcome() {
  $.ajax({
    method : 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function(req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success : function(res) {
      data = JSON.parse(res)
      console.log(data)
      document.getElementById('home').insertAdjacentHTML("afterbegin", `<p class="lead text-center display-4">Hello, ${data.fullname}</p>
      <p class="lead text-center mb-5 display-4">Make a form request now ?</p>
      <button onclick="window.location = '/formReq.html'" type="button" class="btn btn-lg col-2 offset-5">Request </button>`)
    },
    error : function(err) {
      console.log(err)
    }
  })
}

function getRequestInfo() {
  $.ajax({
    method : 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function(req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success : function(res) {
      data = JSON.parse(res)
      // console.log(data)
      document.getElementById('requester_info').insertAdjacentHTML("afterbegin", `<legend><i class="far fa-id-card"></i> Request Information</legend>
                    
      <!-- Bagian Kiri -->
      <div id="all" class="row">
          <div id="left" class="col-md-6">
              <label class="col-md-4" for="fullname">Fullname</label>
              <span id="fullame" name="fullname">${data.fullname}</span>
              <p></p>
              <label class="col-md-4" for="email">Email</label>
              <span id="email" name="email">${data.email}</span>
              <p></p>
              <label class="col-md-4" for="position">Position</label>
              <span id="position" name="position">${data.position}</span>
              <p></p>
              <label class="col-md-4" for="id">ID Number</label>
              <span id="id_employee" name="id_employee">${data.id}</span>
              <p></p>
              <label class="col-md-4" for="company">Company</label>
              <span id="company" name="company"></span>
              <p></p>
              <label class="col-md-4" for="plant">Plant</label>
              <span id="plant" name="plant"></span>
              <p></p>
          </div>

          <!-- Bagian Kanan -->
          <div id="right" class="col-md-6">
              <label class="col-md-4" for="payroll">Payroll Number</label>
              <span id="payroll" name="payroll">${data.payroll}</span>
              <p></p>
              <label class="col-md-4" for="budget_type">Budget Type</label>
              <select id="budget_type" name="budget_type" />
                  <option selected>Project</option>
                  <option>Maintenance Order</option>
              </select>
              <p></p>
              <label class="col-md-4" for="currency">Currency</label>
              <select id="currency" name="currency" />
                  <option selected>USD</option>
                  <option>IDR</option>
                  <option>EUR</option>
                  <option>YEN</option>
              </select>
              <p></p>
              <label class="col-md-4" for="location">Receiving Location</label>
              <select id="location" name="location" />
                  <option selected>Jakarta</option>
                  <option>Bandung</option>
                  <option>Cikarang</option>
                  <option>Surabaya</option>
              </select>
              <p></p>
              <label class="col-md-4" for="budget_source">Budget Source</label>
              <select id="budget_source" name="budget_source" />
                  <option selected>Cost center</option>
                  <option>Foreign loans</option>
                  <option>Others</option>
              </select>
              <p></p>
              <label class="col-md-4" for="expected_date">Expected Date</label>
              <input type="date" id="expected_date" name="expected_date" />
          </div>
      </div>`)
    },
    error : function(err) {
      console.log(err)
    }
  })
}

function getMaterial(){
  $.ajax({
    method : 'GET',
    url: "http://localhost:9000/getAllMaterial",
    beforeSend: function(req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success : function(res) {
      JSON.parse(res).forEach(function(data){
        // console.log(data)
        document.getElementById('materials').insertAdjacentHTML("beforeend", `
        <option id="${data.id}">${data.code} ${data.name}</option>
        `)
      })
    },
    error : function(err) {
      console.log(err)
    }
  })
}

function sendRequest(){
  $.ajax({
    method: 'POST',
    url: 'http://localhost:9000/sendRequest',
    beforeSend : function(req){
      req.setRequestHeader('Content-Type', 'application/json')
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data : JSON.stringify({
      "fullname" : document.getElementById('fullname').value,
      "budget_type" : document.getElementById('budget_type').value,
      "currency": document.getElementById('currenct').value,
      "expected_date": document.getElementById('expected_date').value,
      "location" : document.getElementById('location').value,
      "budget_source" : document.getElementById('budget_source').value,
      "justification" : document.getElementById('justification').value,
      "materials" : document.getElementById('materials').value,
      "description" : document.getElementById('description').value,
      "quantity" : document.getElementById('quantity').value,
      "unit_measurement" : document.getElementById('unit_measurement').value,
      "material_picture" : document.getElementById('material_picture').value
    }),
    success: function(res){    
      alert('berhasil')
  },
    error: function(err){
      alert('gagal')
    }
  })
}

// FUNGSI BIKINAN NAUFAL
function getAllData() {
  
  // //////////////////////////////// Request ////////////////////////////////////////
  // autoComplete
  var obj = new Object(),
      autoComplete = $('#right select').get()
      // autoComplete = document.querySelectorAll('.parent .child1');

  for (let i = 0; i < autoComplete.length; i++) {
    var id = $(autoComplete).eq(i).attr("id"),
        val = $(autoComplete).eq(i).val()
    console.log(val)
    obj[`${id}`] = val
  }
  // input (date)
  var date = $('#expected_date').val()
  obj['expected_date'] = date
  // justification
  var just = $('#justification').val()
  obj['justification'] = just


  // //////////////////////////////// Item ////////////////////////////////////////
  var array = new Array(),
      rows = $('table.table tbody tr').get()
  rows.forEach(row => {
    var tds = $(row).find('td').get(),
        item_obj = new Object()
    tds.forEach(td => {
      var id = $(td).attr("id"),
          text = $(td).text()
      item_obj[`${id}`] = text
    })
    array.push(item_obj)
  })  

  // ///////////////////////////////// Data to send to Backend ///////////////////////////////////////
  var obj_data = new Object()
  obj_data["request_data"] = obj
  obj_data["array_item"] = array

  // /////////////////////////////// Kirim pake Ajax //////////////////////////////////////
  $.ajax({
    method: 'POST',
    url: 'http://localhost:9000/sendRequest',
    beforeSend : function(req){
      req.('Content-Type', 'application/json')
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data : obj_data,
    success: function(res){
      alert('berhasil')
    },
    error: function(res){
      alert('gagal')
    }
  })
}

function addItemToTabel(){
  
  <tr>
      <th scope="row">2</th>
      <td id="tableDataItemDetail">Machine equipment</td>
      <td id="tableDataDescription"> Baut</td>
      <td id="tableDataEstimatedPrice">50</td>
      <td id="tableDataQuantity">10</td>
      <td id="tableDataUnit">Piece</td>
      <td id="tableDataSubTotal">500</td>
      <form action="">
          <td id="table-action">
              <!-- <button formaction="#" type="submit" id="edit-button"><i class="fas fa-pen"></i></button> -->
              <button formaction="#" type="submit" id="delete-button"><i class="far fa-trash-alt"></i></button>
          </td>
      </form>
  </tr>
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