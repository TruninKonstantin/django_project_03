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

$("#id_standard").change(function() {
    var url = $("#resultsPressureForm").attr("data-materials-url");
    var standardId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'standard': standardId
        },
        success: function(data) {
            $("#id_material").html(data);
        }
    });
    updatePressureInterpolation();
});

$("#id_material").change(function() {
    var url = $("#resultsPressureForm").attr("data-groups-url");
    var materialId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'material': materialId
        },
        success: function(data) {
            $("#id_group").html(data);
        }
    });


    var url = $("#resultsPressureForm").attr("data-standards-url");
    var materialId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'material': materialId
        },
        success: function(data) {
            $("#id_standard").html(data);
        }
    });

    var materialId = $(this).val();
    if (materialId == '') {
        var url = $("#resultsPressureForm").attr("data-re-load-materials-url");
        $.ajax({
            url: url,
            success: function(data) {
                $("#id_material").html(data);
            }
        });
    }
    updateTable();
    updatePressureInterpolation();
    updateNotes();
});

$("#id_pressure_class").change(function() {
    updatePressureInterpolation();
});

$("#id_temperature").change(function() {
    updatePressureInterpolation();
    updateNotes();
});