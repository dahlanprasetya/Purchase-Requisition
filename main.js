
//   untuk cookienya ///////////////////////////////////////////////////////////////////////////////////////////////////////////
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

// Menghapus Cookie///////////////////////////////////////////////////////////////////////////////////////////////////////////
function removeCookie() {
  document.cookie = 'token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  document.cookie = 'position=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  document.cookie = 'requester=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  window.location = '/login.html';
}

// Mengatur dashboard location ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function home() {
  var a = getCookie('requester')
  a == "true" ? window.location = "/employee.html" : window.location = "/scm.html"
}

function comment() {
  var a = getCookie('position')
  a == "3" ? window.location = "/comment.html" : window.location = "/manager.html"
}

// Login ke dalam home ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function login() {
  $.ajax({
    method: "POST",
    url: "http://localhost:9000/login",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json')
    },
    data: JSON.stringify({
      "email": document.getElementById('email').value,
      "password": document.getElementById('password').value
    }),
    success: function (res) {
      data = JSON.parse(res)
      if (data.position == 4) {
        var isRequest = true
      } else {
        var isRequest = false
      }
      alert("Login Success");
      document.cookie = `token=${data.token}`
      document.cookie = `position=${data.position}`
      document.cookie = `requester=${isRequest}`
      if (isRequest) {
        window.location = "/employee.html"
      } else {
        window.location = "/scm.html"
      }
    },
    error: function (err) {
      alert("email atau password salah: " + this.status);
      console.log(err)
    }
  })
}

// Menampilkan request dari requester
function getUserRequest(){
  $.ajax({
    method: 'GET',
    url : "http://localhost:9000/getUserRequest",
    beforeSend: function (req) {
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      JSON.parse(res).forEach(function (data) {
        // console.log(data)
        document.getElementById('table-request').insertAdjacentHTML("beforeend", `<tr>
        <td scope="row">${data.id}</td>
        <td>${data.person_name}</td>
        <td>${data.company}</td>
        <td>${data.status}</td>
        <form action="">
            <td id="table-action"><button onclick="redirectToDetail(${data.id})"
            type="submit" id="see-details-button">See details</button></td>
        </form>
    </tr>
        `)
      })
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// Memunculkan data ke home ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function getProfile() {
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      data = JSON.parse(res)
      // console.log(data)
      document.getElementById('dropdown').insertAdjacentHTML("afterbegin", `<div class="dropdown__user">
      <img class="dropbtn" href="#" src="${data.photoprofile}" alt="orang" />
      <a id="profile-name" href="profile.html"> ${data.fullname}</a>
      <div class="dropdown-content">
          <a href="edit.html"><i class="fas fa-cogs"></i> Setting and Privacy</a>
          <a href="#"><i class="far fa-question-circle"></i> Help Center</a>
          <a onclick="removeCookie()" href="login.html" id="logout-button"><i class="fas fa-power-off"></i> Log Out</a>
      </div>
  </div>`)
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// Mengambil nama employee //////////////////////////////////////////////////////////////////////////////////////////////////
function welcome() {
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      data = JSON.parse(res)
      // console.log(data)
      document.getElementById('home').insertAdjacentHTML("afterbegin", `<p class="lead text-center display-4">Hello, ${data.fullname}</p>
      <p class="lead text-center mb-5 display-4">Make a form request now ?</p>
      <button onclick="window.location = '/formReq.html'" type="button" class="btn btn-lg col-2 offset-5">Request </button>`)
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// mengambil task list //////////////////////////////////////////////////////////////////////////////////////////////////////// 
function getTaskList(){
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getTaskList",
    beforeSend: function (req) {
      req.setRequestHeader('Authorization', getCookie('token'))
      $('#loading').show()
    },
    success: function (res) {
      JSON.parse(res).forEach(function (data) {
        // console.log(data)
        document.getElementById('table-task-list').insertAdjacentHTML("beforeend", `
        <tr>
            <td scope="row">${data.id}</th>
            <td>${data.fullname}</td>
            <td>${data.company}</td>
            <td>${data.status}</td>
            <form action="">
            <td id="table-action"><button onclick="redirectToComment(${data.id})"
            type="submit" id="see-details-button">See details</button></td>
            </form>
        </tr>
        `)
      })
      $('#loading').hide()
    },
    error: function (err) {
      console.log(err)
      $('#loading').hide()
    }
  })
}
// mengambil request yang harus direvisi
function getTaskRevise(){
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getTaskList",
    beforeSend: function (req) {
      req.setRequestHeader('Authorization', getCookie('token'))
      $('#loading').show()
    },
    success: function (res) {
      JSON.parse(res).forEach(function (data) {
        // console.log(data)
        $('#table-revise').append(`
        <tr>
            <td scope="row">${data.id}</th>
            <td>${data.fullname}</td>
            <td>${data.company}</td>
            <td>${data.status}</td>
            <form action="">
            <td id="table-action"><button onclick="redirectToRevise(${data.id})"
            type="submit" id="see-details-button">See details</button></td>
            </form>
        </tr>
        `)
      })
      $('#loading').hide()
    },
    error: function (err) {
      console.log(err)
      $('#loading').hide()
    }
  })
}
// mencari request yg sudah di acc oleh owner////////////////////////////////////////////////////////////////////////////

function getAccRequest(){
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getAccRequest",
    beforeSend: function (req) {
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      JSON.parse(res).forEach(function (data) {
        // console.log(data)
        document.getElementById('table-acc-request').insertAdjacentHTML("beforeend", `
        <tr>
            <td scope="row">${data.id}</th>
            <td>${data.fullname}</td>
            <td>${data.company}</td>
            <td>${data.status}</td>
            <form action="">
            <td id="table-action"><a onclick="redirectToDetail(${data.id})"type="submit" id="see-details-button">See details</a></td>
            </form>
        </tr>
        `)
      })
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// loading function ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function loading(button) {

  console.log(button)
  $(button).addClass('hide')
  $('#loading').removeClass('hide')
  // document.getElementById("loading").style.display = "none";
}

// menampilkan detail request berdasarkan id ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function getRequestDetails() {
  var id = window.location.href.split("=")[1];
  $.ajax({
      method: 'POST',
      url: "http://localhost:9000/getRequestDetails",
      beforeSend: function (req) {
        req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
        $('#loading').show()
      },
      data: JSON.stringify({
        "id": id
      }),
      success: function (res) {
        // window.location = "/details.html";
        data = JSON.parse(res)
        document.getElementById('get-data-request').insertAdjacentHTML("afterbegin", `<h2 id="welcome" class="text-center">General Material Purchase Request Details</h2>
        <fieldset id="requester_info">
            <legend><i class="far fa-id-card"></i> Request Information</legend>

            <!-- Bagian Kiri -->
            <div id="all" class="row">
                <div id="left" class="col-md-6">
                    <label class="col-md-4" for="fullname">Fullname</label>
                    <span id="fullname" name="fullname">${data.requester_detail.fullname}</span>
                    <p></p>
                    <label class="col-md-4" for="email">Email</label>
                    <span id="email" name="email">${data.requester_detail.email}</span>
                    <p></p>
                    <label class="col-md-4" for="position">Postion</label>
                    <span id="position" name="position">${data.requester_detail.position}</span>
                    <p></p>
                    <label class="col-md-4" for="id">ID Number</label>
                    <span id="id_employee" name="id_employee">${data.requester_detail.id_number}</span>
                    <p></p>
                    <label class="col-md-4" for="company">Company</label>
                    <span id="company" name="company">${data.requester_detail.company}</span>
                    <p></p>
                    <label class="col-md-4" for="plant">Plant</label>
                    <span id="plant" name="plant">${data.requester_detail.plant}</span>
                    <p></p>
                </div>

                <!-- Bagian Kanan -->
                <div id="right" class="col-md-6">
                    <label class="col-md-4" for="payroll">Payroll Number</label>
                    <span id="payroll" name="payroll">${data.requester_detail.payroll}</span>
                    <p></p>
                    <label class="col-md-4" for="budget_type">Budget Type</label>
                    <span id="budget_type" name="${data.request_detail.budget_type}" />
                    Maintenance Order
                    </span>
                    <p></p>
                    <label class="col-md-4" for="currency">Currency</label>
                    <span id="currency" name="currency" />
                    ${data.request_detail.currency}
                    </span>
                    <p></p>
                    <label class="col-md-4" for="location">Receiving Location</label>
                    <span id="location" name="location" />
                    ${data.request_detail.location}
                    </span>
                    <p></p>
                    <label class="col-md-4" for="budget_source">Budget Source</label>
                    <span id="budget_source" name="budget_source" />
                    ${data.request_detail.budget_source}
                    </span>
                    <p></p>
                    <label class="col-md-4" for="expected_date">Expected Date</label>
                    <span id="expected_date" name="expected_date" >${data.request_detail.expected_date}</span> 
                </div>
            </div>
        </fieldset>

        <fieldset id="header_info">
            <legend><i class="fas fa-info"></i> Header Information</legend>

            <div id="all" class="row">
                <div id="justification-div" class="col-md-12">
                    <label class="col-md-2" for="justification">Justification</label>
                    <span id="justification" name="justification">${data.request_detail.justification}</span>
                </div>
            </div>
        </fieldset>`)
        var table_item = $('#table_item tbody'),
            data_table_item = data.items_detail
            row = $('#table_item').find('tr')
            // masukin data tabel item
            a = 0
            data_table_item.forEach(data => {
              a++
              table_item.append(`
              <tr>
              <th scope="row">${a}</th>
              <td id="tableDataItemDetail" >${data.material_name}</td>
              <td id="tableDataDescription">${data.description}</td>
              <td id="tableDataEstimatedPrice">${data.estimate_price}</td>
              <td id="tableDataQuantity">${data.quantity}</td>
              <td id="tableDataUnit">${data.unit_measurement}</td>
              <td id="tableDataSubTotal">${data.total}</td>
          </tr>
              `)
          })
          var table_comment = $('#table_comment_history tbody'),
          data_table_comment = data.comment_history
          // row = tbody.find('tr')
          // masukin data tabel item
          a = 0
          data_table_comment.forEach(data => {
            a++
            var str = data.date
            var tanggal = str.split("T")
            var res1 = tanggal[1].substr(0,5)
            var tes = tanggal[0] + " " +res1
            table_comment.append(`
            <tr>
                <td id="comment-fullname" scope="col" class="col-md-2">${data.user}</td>
                <td id="comment-position" scope="col" class="col-md-2">${data.position}</td>
                <td id="comment-activity" scope="col" class="col-md-1">approved</td>
                <td id="comment-time" scope="col" class="col-md-2">${tes}</td>
                <td id="comment-content" scope="col" class="col-md-5">${data.comment}</td>
            </tr>`)
          })
          $('#loading').hide()
      },
      error: function (err) {
        console.log(err)
        $('#loading').hide()
      }
    })
}

// Memunculkan data sebelumnya untuk direvisi ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function showReviseData() {
  var id = window.location.href.split("=")[1];
  $.ajax({
      method: 'POST',
      url: "http://localhost:9000/getRequestDetails",
      beforeSend: function (req) {
        req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
        $('#loading').show()
      },
      data: JSON.stringify({
        "id": id
      }),
      success: function (res) {
        // window.location = "/details.html";
        data = JSON.parse(res)
        $('#fullname').append(data['requester_detail']['fullname'])
        $('#email').append(data['requester_detail']['email'])
        $('#position').append(data['requester_detail']['position'])
        $('#id_employee').append(data['requester_detail']['id_number'])
        $('#company').append(data['requester_detail']['company'])
        $('#plant').append(data['requester_detail']['plant'])
        $('#payroll').append(data['requester_detail']['payroll'])
        $('#budget_type').val(`${data['request_detail']['budget_type']}`)
        $('#currency').val(`${data['request_detail']['currency']}`)
        $('#location').val(`${data['request_detail']['location']}`)
        $('#expected_date').val(`${data['request_detail']['expected_date']}`)
        $('#justification').val(`${data['request_detail']['justification']}`)
        

        var table_item = $('#table_item'),
            data_table_item = data['items_detail']
            row = $('#table_item').find('tr')
            // masukin data tabel item
            a = 0
            data_table_item.forEach(data => {
              a++
              table_item.append(`
              <tr id="${row.length + 1}">
              <th scope="row">${a}</th>
              <td id="tableDataItemDetail" >${data['material_name']}</td>
              <td id="tableDataDescription">${data['description']}</td>
              <td id="tableDataEstimatedPrice">${data['estimate_price']}</td>
              <td id="tableDataQuantity">${data['quantity']}</td>
              <td id="tableDataUnit">${data['unit_measurement']}</td>
              <td id="tableDataSubTotal">${data['total']}</td>
              <form action="">
                  <td id="table-action">
                      <button formaction="#" onclick=deleteTable(${row.length + 1}) type="submit" id="delete-button"><i class="far fa-trash-alt"></i></button>
                  </td>
              </form>
          </tr>
              `)
          })
          var table_comment = $('#table_comment_history'),
          data_table_comment = data['comment_history']
          // row = tbody.find('tr')
          // masukin data tabel item
          a = 0
          data_table_comment.forEach(data => {
            a++
            var str = data.date
            var tanggal = str.split("T")
            var res1 = tanggal[1].substr(0,5)
            var tes = tanggal[0] + " " +res1
            table_comment.append(`
            <tr>
                <td id="comment-fullname" scope="col" class="col-md-2">${data["user"]}</td>
                <td id="comment-position" scope="col" class="col-md-2">${data["position"]}</td>
                <td id="comment-activity" scope="col" class="col-md-1">approved</td>
                <td id="comment-time" scope="col" class="col-md-2">${tes}</td>
                <td id="comment-content" scope="col" class="col-md-5">${data["comment"]}</td>
            </tr>`)
          })
          $('#loading').hide()
      },
      error: function (err) {
        console.log(err)
        $('#loading').hide()
      }
    })
}
// menampilkan detail request untuk di acc atau ditolak ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function responseRequest() {
  var id = window.location.href.split("=")[1];
  $.ajax({
      method: 'POST',
      url: "http://localhost:9000/getRequestDetails",
      beforeSend: function (req) {
        req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
        $('#loading').show()
      },
      data: JSON.stringify({
        "id": id
      }),
      success: function (res) {
        // window.location = "/details.html";
        data = JSON.parse(res)
        $('#left ').append(`<label class="col-md-4" for="fullname">Fullname</label>
        <span id="fullname" name="fullname">${data.requester_detail.fullname}</span>
        <p></p>
        <label class="col-md-4" for="email">Email</label>
        <span id="email" name="email">${data.requester_detail.email}</span>
        <p></p>
        <label class="col-md-4" for="position">Postion</label>
        <span id="position" name="position">${data.requester_detail.position}</span>
        <p></p>
        <label class="col-md-4" for="id">ID Number</label>
        <span id="id_employee" name="id_employee">${data.requester_detail.id_number}</span>
        <p></p>
        <label class="col-md-4" for="company">Company</label>
        <span id="company" name="company">${data.requester_detail.company}</span>
        <p></p>
        <label class="col-md-4" for="plant">Plant</label>
        <span id="plant" name="plant">${data.requester_detail.plant}</span>
        <p></p>`)

        $('#right').append(`<label class="col-md-4" for="payroll">Payroll Number</label>
        <span id="payroll" name="payroll">${data.requester_detail.payroll}</span>
        <p></p>
        <label class="col-md-4" for="budget_type">Budget Type</label>
        <span id="budget_type" name="budget_type" />
        ${data.request_detail.budget_type}
        </span>
        <p></p>
        <label class="col-md-4" for="currency">Currency</label>
        <span id="currency" name="currency" />
        ${data.request_detail.currency}
        </span>
        <p></p>
        <label class="col-md-4" for="location">Receiving Location</label>
        <span id="location" name="location" />
        ${data.request_detail.location}
        </span>
        <p></p>
        <label class="col-md-4" for="budget_source">Budget Source</label>
        <span id="budget_source" name="budget_source" />
        ${data.request_detail.budget_source}
        </span>
        <p></p>
        <label class="col-md-4" for="expected_date">Expected Date</label>
        <span id="expected_date" name="expected_date" >${data.request_detail.expected_date}</span> `)
        
        $('#justification').append(`${data.request_detail.justification}`)

        var table_item = $('#table_item tbody'),
            data_table_item = data.items_detail
            // row = tbody.find('tr')
            // masukin data tabel item
            a = 0
            data_table_item.forEach(data => {
              a++
              table_item.append(`
              <tr>
              <th scope="row">${a}</th>
              <td id="tableDataItemDetail" >${data.material_name}</td>
              <td id="tableDataDescription">${data.description}</td>
              <td id="tableDataEstimatedPrice">${data.estimate_price}</td>
              <td id="tableDataQuantity">${data.quantity}</td>
              <td id="tableDataUnit">${data.unit_measurement}</td>
              <td id="tableDataSubTotal">${data.total}</td>
          </tr>
              `)
          })
          var table_comment = $('#table_comment_history tbody'),
          data_table_comment = data.comment_history
          // row = tbody.find('tr')
          // masukin data tabel item
          a = 0
          data_table_comment.forEach(data => {
            a++
            var str = data.date
            var tanggal = str.split("T")
            var res1 = tanggal[1].substr(0,5)
            var tes = tanggal[0] + " " +res1
            table_comment.append(`
            <tr>
                <td id="comment-fullname" scope="col" class="col-md-2">${data.user}</td>
                <td id="comment-position" scope="col" class="col-md-2">${data.position}</td>
                <td id="comment-activity" scope="col" class="col-md-1">approved</td>
                <td id="comment-time" scope="col" class="col-md-2">${tes}</td>
                <td id="comment-content" scope="col" class="col-md-5">${data.comment}</td>
            </tr>`)
          })
          $('#loading').hide()
      },
      error: function (err) {
        console.log(err)
        $('#loading').hide()
      }
    })
}
function sendResponseSCM(response, button){
  
  $("#approved-button").addClass('hide')
  $("#revised-button").addClass('hide')
  $('#loading').removeClass('hide')

  // /////////////////////////////////////////////

  var id = window.location.href.split("=")[1];
  $.ajax({
    method: 'POST',
    url: "http://localhost:9000/responseRequest",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data: JSON.stringify({
      "request_id": id,
      "comment": $('#comment-box').val(),
      "response": response
    }),
    success:function(res){
      alert("Success")
      window.location="/scm.html"
    },
    error:function(err){
      alert(err)
    }
  })
}

// send response dari manager dan owner
function sendResponse(){
  var id = window.location.href.split("=")[1];
  $.ajax({
    method: 'POST',
    url: "http://localhost:9000/responseRequest",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data: JSON.stringify({
      "request_id": id,
      "comment": $('#comment-box').val()
    }),
    success:function(res){
      alert("Success")
      window.location="/scm.html"
    },
    error:function(err){
      alert(err)
    }
  })
}

// function untuk pindah halaman ke detail.html berdasarkan id
function redirectToDetail(id){
  window.location = 'details.html?id=' + id
}

// function untuk pindah halaman ke formRebvise.html
function redirectToRevise(id){
  window.location = 'formRev.html?id=' + id
}

// funtion pindah halaman comment.html berdasarkan id
function redirectToComment(id){
  if (getCookie('position') == "3") {
    window.location = '/comment.html?id=' + id
  } else {
    window.location = '/manager.html?id=' + id
  }
}

// belum digunakan 
function getRequestInfo() {
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
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
              <span id="company" name="company">${data.company}</span>
              <p></p>
              <label class="col-md-4" for="plant">Plant</label>
              <span id="plant" name="plant">${data.plant}</span>
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
    error: function (err) {
      console.log(err)
    }
  })
}

// memunculkan material pada kolom select di request form /////////////////////////////////////////////////////////////////
function getMaterial() {
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getAllMaterial",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      JSON.parse(res).forEach(function (data) {
        // console.log(data)
        document.getElementById('materials').insertAdjacentHTML("beforeend", `
        <option id="${data.id}">${data.code} ${data.name}</option>
        `)
      })
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// Mengirim seluruh isi request form ke database ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function sendAllData(button) {
  console.log(button)
  $(button).addClass('hide')
  $('#loading').removeClass('hide')
  // //////////////////////////////// Request ////////////////////////////////////////

  // autoComplete
  var obj = new Object(),
    autoComplete = $('#right select').get()
  // autoComplete = document.querySelectorAll('.parent .child1');
  for (let i = 0; i < autoComplete.length; i++) {
    var id = $(autoComplete).eq(i).attr("id"),
      val = $(autoComplete).eq(i).val()
    // console.log(val)
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
    delete item_obj['table-action']
    array.push(item_obj)
  })

  // ///////////////////////////////// Data to send to Backend ///////////////////////////////////////
  var obj_data = new Object()
  obj_data["request_data"] = obj
  obj_data["array_item"] = array

  // /////////////////////////////// Kirim pake Ajax //////////////////////////////////////
  $.ajax({
    method: 'POST',
    url: 'http://localhost:9000/submitrequest',
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json')
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data: JSON.stringify(
      obj_data    
    ),
    success: function (res) {
      // console.log(res)
      alert('Data has been sent successfully')
      window.location = "/employee.html"
    },
    error: function (err) {
      console.log(err)
      alert('Data sent failed')
    }
  })
}

function sendRevise(button) {
  console.log(button)
  $(button).addClass('hide')
  $('#loading').removeClass('hide')
  // //////////////////////////////// Request ////////////////////////////////////////

  // autoComplete
  var obj = new Object(),
    autoComplete = $('#right select').get()
  // autoComplete = document.querySelectorAll('.parent .child1');
  for (let i = 0; i < autoComplete.length; i++) {
    var id = $(autoComplete).eq(i).attr("id"),
      val = $(autoComplete).eq(i).val()
    // console.log(val)
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
    delete item_obj['table-action']
    array.push(item_obj)
  })

  // ///////////////////////////////// Data to send to Backend ///////////////////////////////////////
  var obj_data = new Object()
  obj_data["request_data"] = obj
  obj_data["array_item"] = array
  console.log(obj_data)

  // /////////////////////////////// Kirim pake Ajax //////////////////////////////////////
  // $.ajax({
  //   method: 'POST',
  //   url: 'http://localhost:9000/submitrequest',
  //   beforeSend: function (req) {
  //     req.setRequestHeader('Content-Type', 'application/json')
  //     req.setRequestHeader('Authorization', getCookie('token'))
  //   },
  //   data: JSON.stringify(
  //     obj_data    
  //   ),
  //   success: function (res) {
  //     // console.log(res)
  //     alert('Data has been sent successfully')
  //     window.location = "/employee.html"
  //   },
  //   error: function (err) {
  //     console.log(err)
  //     alert('Data sent failed')
    // }
  // })
}

// Fungsi menambahkan item ke tabel ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function addItemToTabel() {
  var materials_value = $('#materials').val()
  var description_value = $('#description').val()
  var quantity_value = $('#quantity').val()
  var unit_measurement_value = $('#unit_measurement').val()
  var price_value = $('#price').val()

  // jQuery
  var table = $('table.table tbody#table_item'),
    row = table.find('tr')
  $('table.table tbody#table_item').append(
    `<tr id="${row.length + 1}">
  <th scope="row">${row.length + 1}</th>
  <td id="tableDataItemDetail">${materials_value} equipment</td>
  <td id="tableDataDescription"> ${description_value}</td>
  <td id="tableDataEstimatedPrice">${price_value}</td>
  <td id="tableDataQuantity">${quantity_value}</td>
  <td id="tableDataUnit">${unit_measurement_value}</td>
  <td id="tableDataSubTotal">${quantity_value * price_value}</td>
  <form action="">
      <td id="table-action">
          <button formaction="#" onclick=deleteTable(${row.length + 1}) type="submit" id="delete-button"><i class="far fa-trash-alt"></i></button>
      </td>
  </form>
</tr>`)
  $('#materials').val("Choose...")
  $('#description').val("")
  $('#quantity').val("")
  $('#unit_measurement').val("Piece")
  $('#price').val("")
}

// fungsi reset ditabel item ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function reset () {
  $('#materials').val("Choose...")
  $('#description').val("")
  $('#quantity').val("")
  $('#unit_measurement').val("Piece")
  $('#price').val("")
}

// fungsi delete tabel item ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function deleteTable(id) {
  $(`tr#${id}`).remove()
  // reset number
  var row = $('table.table tbody tr')
  for (var i = 0; i < row.length; i++) {
    $(row).eq(i).find('th').html(`${i + 1}`)
  }
}

// Memunculkan data ke tabel approval list ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function approvalList() {
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getAllMaterial",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      JSON.parse(res).forEach(function (data) {
        data = JSON.parse(res)
        // console.log(data)
        document.getElementById('materials').insertAdjacentHTML("beforeend", `
        <tr>
                <td scope="row">32132131</td>
                <td>Mark</td>
                <td>Astra</td>
                <td>Approved by Manager</td>
                <form action="">
                    <td id="table-action"><button formaction="/details.html" type="submit" id="see-details-button">See details</button></td>
                </form>
            </tr>
        `)
      })
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// Fungsi munculkan data ke comment html ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function commentProfile(){
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/getProfile",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
        req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      data = JSON.parse(res)
      // console.log(data)
      document.getElementById('comment-section').insertAdjacentHTML("afterbegin", 
      `<form>
      <div id="all" class="row">
          <div class="col-md-1">
              <img src="${data.photoprofile}" />
          </div>
          <div class="col-md-11">
              <textarea rows="4" id="comment-box" placeholder="Add a comment"></textarea>
          </div>
      </div>
  </form>`)
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// Fungsi menambahkan comment ke database ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function approvedComment(){
  var comment_value = $('#comment-box').val()
  var approved_value = $('#approved-button').text()

  // jQuery
  var table = $('#table_comment_history.table tbody'),
    row = table.find('tr')
  $('#table_comment_history.table tbody').prepend(
    `<tr>
    <td id="tableDataParticipant" scope="${row}">Oka Aryanta</td>
    <td id="tableDataPosition" >Supply Chain Management</td>
    <td id="tableDataActivity">${approved_value}</td>
    <td id="tableDataStart">5 Nov 2018 09:20</td>
    <td id="tableDataComment">${comment_value}</td>
</tr>`)
  $('#comment-box').val("")
}

//  ///////////////////////////////////////////////////////////////////////////////////////////////////
function revisedComment(){
  var comment_value = $('#comment-box').val()
  var revised_value = $('#revised-button').text()

  // jQuery
  var table = $('#table_comment_history.table tbody'),
    row = table.find('tr')
  $('#table_comment_history.table tbody').prepend(
    `<tr>
    <td id="tableDataParticipant" scope="row">Oka Aryanta</td>
    <td id="tableDataPosition" >Supply Chain Management</td>
    <td id="tableDataActivity">${revised_value}</td>
    <td id="tableDataStart">5 Nov 2018 09:20</td>
    <td id="tableDataComment">${comment_value}</td>
</tr>`)
  $('#comment-box').val("")
}

// Edit Profile ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function editPassword(){
  $.ajax({
    method: 'PUT',
    url: "http://localhost:9000/editPassword",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data: JSON.stringify({
      "current_password" : document.getElementById('current_password').value,
      "new_password" : document.getElementById('new_password').value,
      "verify_password" : document.getElementById('verify_password').value
    }),
    success: function(res) {
      alert(res)
      window.location = "/edit.html"
    },
    error: function(err) {
      alert("Error, either the current password is wrong, or the new password is not the same as the verify password")
    }
  })
}

// Menampilkan Data profile sebelumnya ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function showEditData() {
  $.ajax({
    method: 'GET',
    url: "http://localhost:9000/showEditData",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    success: function (res) {
      data = JSON.parse(res)
      // console.log(data)
      document.getElementById('fullname').value = data.fullname
      document.getElementById('email').value = data.email
      document.getElementById('profile_picture').value = data.photoprofile
    },
    error: function (err) {
      console.log(err)
    }
  })
}

// Edit Password ///////////////////////////////////////////////////////////////////////////////////////////////////////////
function editProfile(){
  $.ajax({
    method: 'PUT',
    url: "http://localhost:9000/editProfile",
    beforeSend: function (req) {
      req.setRequestHeader('Content-Type', 'application/json'),
      req.setRequestHeader('Authorization', getCookie('token'))
    },
    data: JSON.stringify({
      "fullname" : document.getElementById('fullname').value,
      "email" : document.getElementById('email').value,
      "profile_picture" : document.getElementById('profile_picture').value
    }),
    success: function(res) {
      alert(res)
      window.location = "/edit.html"
    },
    error: function(err) {
      alert("")
      console.log(err)
    }
  })
}