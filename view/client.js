function init() {
  // initialisation stuff here
}

//firt get all without id

function findAll() {
  $.ajax({
    url: "https://localhost:5001/api/Indici",
    type: "GET",
    contentType: "application/json",
    success: function (result) {
      console.log(result);
      readResult(JSON.stringify(result));
    },
    error: function (xhr, status, p3, p4) {
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    },
  });
}

function readResult(str)
{ document.getElementById('txtarea').value += str;
console.log(str);
}

function findById() {
  var id = $("#txtId").val();
  $.ajax({
    url: "https://localhost:5001/api/Indici/" + id,
    type: "GET",
    contentType: "application/json",
    data: "",
    success: function (result) {
      console.log(result);
      readResult(JSON.stringify(result));
    },
    error: function (xhr, status, p3, p4) {
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    },
  });
}

//post in the
function postItem() {
  var id = $("#txtId").val();
  var anno = $("#txtNewAnno").val();
  var options = {};
  options.url = "https://localhost:5001/api/Stagione/PostStagioneItem";
  options.type = "POST";
  options.data = JSON.stringify({
    id: Number(id),
    anno: Number(anno),
    serie: "C",
  });
  options.dataType = "json";
  options.contentType = "application/json";
  options.success = function (msg) {
    alert(msg);
  };
  options.error = function (err) {
    alert(err.responseText);
  };
  $.ajax(options);
}
//delete 
function deleteId() {
  var options = {};
  options.url = "https://localhost:5001/api/Stagione/"+ $("#txtId").val();
  options.type = "DELETE";
  options.contentType = "application/json";
  options.success = function (msg) {
  alert(msg);
  };
  options.error = function (err) { alert(err.statusText); };
  $.ajax(options);
  }

  //put
  function updateId() {
    var id = $('#txtId').val();
    var anno = $('#txtNewAnno').val();
    var options = {};
    options.url = "https://localhost:5001/api/Stagione/"+ $("#txtId").val();
    options.type = "PUT";
    options.data = JSON.stringify({
    "id": Number(id),
    "anno": Number(anno),
    "serie": 'C'
    });
    options.dataType = "json";
    options.contentType = "application/json";
    options.success = function (msg) { alert(msg); };
    options.error = function (err) { alert(err.responseText); };
    $.ajax(options);
    };

function getIndexById() {
      document.getElementById("indexButton").disabled = true;
      var id = document.getElementById("indices").value;
      $.ajax({
        url: "https://localhost:5001/api/Indici/" + id,
        type: "GET",
        contentType: "application/json",
        data: "",
        success: function(result) {
          showResult(JSON.parse(result));
        },
        error: function(xhr, status, p3, p4) {
          var err = "Error " + status + " " + p3;
          if (xhr.responseText && xhr.responseText[0] == "{") {
            err = JSON.parse(xhr.responseText).message;
          }
          alert(err);
        }
      });
}
function showResult(res) {
	document.getElementById('txtarea').value += res.text;
	renderImage(res.img);
	document.getElementById("indexButton").disabled = false;
}

function renderImage(images) {
	images.forEach(base64ImageString => {
		var baseStr64 = base64ImageString;
		baseStr64 = baseStr64.substring(0, baseStr64.length - 1);
		baseStr64 = baseStr64.substring(2, baseStr64.length);
		var image = new Image();
		image.style = "width: 100%";
		image.src = 'data:image/png;base64,' + baseStr64;
		document.getElementById("charts").appendChild(image);
	});
}
  