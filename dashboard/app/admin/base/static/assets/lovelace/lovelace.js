
function saveSettings(key, value) {
  localStorage.setItem(key, value);
}

function getSettings(key) {
  return localStorage.getItem(key);
}

function removeSettings(key) {
  localStorage.removeItem(key);
}

function reloadPage(t) {
  setTimeout(function () {
    window.location.reload();
  }, t * 1000);
}

// Refresh token interval
window.onload = () => {
  setInterval(function () {
    api_v1.refresh_token()
  }, 1000 * 60);
}

// TODO: Clean bootstrap hidden modal form data
$('.modal').on('hidden.bs.modal', function () {
  $('#formUserModify').find('input[type=text], input[type=password], input[type=number], input[type=email], textarea').val('');
  // Register other form
})

/**
 * Get form object for specified id
 * @id: Form id
 * @return: Form object
 * 
 */
function getFormData(id) {
  let data = {};
  let value = $('#' + id).serializeArray();
  $.each(value, function (index, item) {
    data[item.name] = item.value;
  });
  return data;
}


// API implementations
class API {
  constructor(domain) {
      this.domain = domain;
      this.result = {};
      this.error = "";
      this.headers = this.authHeader();
  }

  request(url, method, headers, json, callback_success, callback_error) {
      this.headers = this.authHeader();
      $.ajax({
          type: method,
          url: this.domain + url,
          headers: headers,
          contentType: 'application/json;charset=UTF-8',
          data: json,
          success: callback_success,
          error: callback_error
      });
  }
  // :url: 
  jsonPost(url, json, callback_success, callback_error) {
      this.headers = this.authHeader();
      $.ajax({
          type: "POST",
          url: this.domain + url,
          dataType: 'json',
          contentType: 'application/json;charset=UTF-8',
          headers: this.headers,
          data: json, // json should be stringified, use JSON.stringify()
          success: callback_success,
          error: callback_error
      });
  }

  put(url, json, callback_success, callback_error) {
      this.headers = this.authHeader();
      $.ajax({
          type: "PUT",
          url: this.domain + url,
          dataType: 'json',
          contentType: 'application/json;charset=UTF-8',
          headers: this.headers,
          data: json, // json should be stringified, use JSON.stringify()
          success: callback_success,
          error: callback_error
      });
  }


  fromPost(url, formdata, callback_success, callback_error) {
      this.headers = this.authHeader();
      $.ajax({
          type: "POST",
          url: this.domain + url,
          headers: this.headers,
          data: formdata,
          success: callback_success,
          error: callback_error
      });
  }

  get(url, callback_success, callback_error) {
      this.headers = this.authHeader();
      $.ajax({
          url: this.domain + url,
          headers: this.headers,
          success: callback_success,
          error: callback_error
      })
  }

  authHeader() {
      return {
          'Authorization': 'Bearer ' + sessionStorage.getItem('access_token'),
          'accept': 'application/json'
      }
  }

  refresh_token() {
      let headers = {
          'Authorization': 'Bearer ' + sessionStorage.getItem('refresh_token'),
          'accept': 'application/json'
      };
      api_v1.request('/refresh', 'POST', headers, {}, function (result, status, xhr) {
          sessionStorage.setItem("access_token", result.access_token);
      }, function (xhr, status, error) {
          console.log(error);
      });
  }
};

// Gloabal API instance
let api_v1 = new API("/api/v1");

// User management
function userModify(userid, formid) {
    let formData = {};
    $.each($('#' + formid).serializeArray(), function (index, item) {
        formData[item.name] = item.value;
    });
    delete (formData['repassword']);
    formData['active'] = formData['active'] === "on" ? true : false;
    console.log(formData)

    let json = JSON.stringify(formData);
    api_v1.request('/users/' + userid, 'PUT', api_v1.authHeader(), json, function (result, status, xhr) {
        reloadPage(1);
        md.showNotification('top', 'right', 3, $('#msg_success').text());
    }, function (xhr, status, error) {
        console.log(error);
        md.showNotification('top', 'right', 2, $('#msg_failed').text());
    });

}

function userAdd(formid) {
    let formData = {};
    $.each($('#' + formid).serializeArray(), function (index, item) {
        formData[item.name] = item.value;
    });

    formData['active'] = formData['active'] === "on" ? true : false;
    console.log(formData)

    let json = JSON.stringify(formData);
    api_v1.request('/users', 'POST', api_v1.authHeader(), json, function (result, status, xhr) {
        reloadPage(1);
        md.showNotification('top', 'right', 3, $('#msg_success').text());
    }, function (xhr, status, error) {
        console.log(error);
        md.showNotification('top', 'right', 2, $('#msg_failed').text());
    });

}

function userDelete(userid) {
    api_v1.request('/users/' + userid, 'DELETE', api_v1.authHeader(), null, function (result, status, xhr) {
        reloadPage(1);
        md.showNotification('top', 'right', 3, $('#msg_success').text());
    }, function (xhr, status, error) {
        console.log(error);
        md.showNotification('top', 'right', 2, $('#msg_failed').text());
    });
}
