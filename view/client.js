function init() {
  // initialisation stuff here
}

//firt get all without id

function findAll() {
  $.ajax({
    url: "http://localhost:5000/api/Stagione",
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

function findById() {
  var id = $("#txtId").val();
  $.ajax({
    url: "https://localhost:5001/api/Stagione/" + id,
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
