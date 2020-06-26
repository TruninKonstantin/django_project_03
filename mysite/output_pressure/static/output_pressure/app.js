// Links to files:
//
// * [[admin.py]]
// * [[apps.py]]
// * [[forms.py]]
// * [[models.py]]
// * [[tests.py]]
// * [[urls.py]]
// * [[views.py]]
// * [[app.js]]
// * [[constants.py]]

// Updates InterpolationPressure field with Ajax request and Json response based on PressureClass, MaterialId, InputTemperatureValue
function updatePressureInterpolation() {
    var url = $("#resultsPressureForm").attr("data-interpolated-pressure-url");

    var pressureClassId = $(document.getElementById("id_pressure_class")).val();
    var materialId = $(document.getElementById("id_material")).val();
    var inputTemperature = $(document.getElementById("id_temperature")).val();

    if (pressureClassId && materialId && inputTemperature) {
        $.ajax({
            url: url,
            data: {
                'pressure_class': pressureClassId,
                'material': materialId,
                'input_temperature': inputTemperature
            },
            dataType: 'json',
            success: function(data) {
                document.getElementById("id_interpolated_pressure").setAttribute('value', data.interpolated_pressure);
            }
        });
    } else {
        document.getElementById("id_interpolated_pressure").setAttribute('value', '----');
    }
}

// Updates Table field with Ajax request and Json response based on GroupId found with from MaterialId
function updateTable() {
    var url = $("#resultsPressureForm").attr("data-update-table-url");

    var materialId = $(document.getElementById("id_material")).val();

    if (materialId) {
        $.ajax({
            url: url,
            data: {
                'material': materialId,
            },
            dataType: 'json',
            success: function(data) {
                document.getElementById("id_table").setAttribute('value', data.str_table);
            }
        });
    } else {
        document.getElementById("id_table").setAttribute('value', '----');
    }
}

// Updates Notes field with Ajax request and Json response based on MaterialId and InputTemperatureValue
function updateNotes() {
    var url = $("#resultsPressureForm").attr("data-update-notes-url");

    var materialId = $(document.getElementById("id_material")).val();
    var temperatureValue = $(document.getElementById("id_temperature")).val();

    if (materialId && temperatureValue) {
        $.ajax({
            url: url,
            data: {
                'material': materialId,
                'temperature_value': temperatureValue,
            },
            dataType: 'json',
            success: function(data) {
                document.getElementById("id_notes").value = data.str_temperatures;
                document.getElementById("id_notes").className = data.textarea_class;
            }
        });
    } else {
        document.getElementById("id_notes").value = "----";
        document.getElementById("id_notes").className = 'color_white';
    }
}

// Re-Load all Materials with Ajax request and Html response
function reLoadMaterial() {
    var url = $("#resultsPressureForm").attr("data-re-load-materials-url");
    $.ajax({
        url: url,
        success: function(data) {
            $("#id_material").html(data);
        }
    });
}

// Updates Standard field with Ajax request and Html response based on MaterialId
function updateStandard() {
    var url = $("#resultsPressureForm").attr("data-standards-url");
    var materialId = $(document.getElementById("id_material")).val();
    $.ajax({
        url: url,
        data: {
            'material': materialId
        },
        success: function(data) {
            $("#id_standard").html(data);
        }
    });
}

// Updates Material field with Ajax request and Html response based on StandardId
function updateMaterial() {
    var url = $("#resultsPressureForm").attr("data-materials-url");
    var standardId = $(document.getElementById("id_standard")).val();
    $.ajax({
        url: url,
        data: {
            'standard': standardId
        },
        success: function(data) {
            $("#id_material").html(data);
        }
    });
}



// Initiates Material update on Standard change
$("#id_standard").change(function() {
    updateMaterial();
});

// Initiates Interpolation, Standard, Table and Notes update on InputTemperatureValue change
$("#id_material").change(function() {

    updateStandard();

    var materialId = $(this).val();
    if (materialId == '') {
        reLoadMaterial();
    }

    updateTable();
    updatePressureInterpolation();
    updateNotes();
});

// Initiates Interpolation update on PressureClass change
$("#id_pressure_class").change(function() {
    updatePressureInterpolation();
});


// Initiates Interpolation and Notes update on InputTemperatureValue change
$("#id_temperature").change(function() {
    updatePressureInterpolation();
    updateNotes();
});