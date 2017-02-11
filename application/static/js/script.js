// For those who are looking at this, i am really sorry.
// I wish the code could be a lot easier to read and understand
// but we are tired and we just don't care anymore.
//
$(document).ready(function () {
    // display a message to #file help p tag when a file is chosen
    var data_map = {
        'add': {
            'form': '#add-form',
            'operation': '#add-op',
            'btn': '#add-btn'
        },
        'delete': {
            'form': '#delete-form',
            'operation': '#delete-op',
            'btn': '#delete-btn'
        },
        'edit': {
            'form': '#edit-form',
            'operation': '#edit-op',
            'btn': '#edit-btn'
        },
        'search': {
            'form': '#search-form',
            'operation': '#search-op',
            'btn': '#search-btn'
        },
        'import': {
            'form': '#import-form',
            'operation': '#import-op',
            'btn': '#import-btn'
        },
        'export': {
            'form': '#export-form',
            'operation': '#export-op',
            'btn': '#export-btn'
        }
    };

    // All the rows that are currently selected in the table
    row_indexs = [];
    var selected_rows = {};
    var row_index = 0;
    var POST_URL = window.location.pathname;

    $datatable = $("#datatable").dataTable();
    var $add_form = $(data_map['add']['form']);
    var $edit_form = $(data_map['edit']['form']);
    var $delete_form = $(data_map['delete']['form']);
    // For every operation, confirm that the user intends to do the operation
    function showConfirmDialog(operation) {
        return confirm('Are you sure you want to ' + operation.split('-')[0].split('#')[1]);
    }

    function validate(json) {
        for (var property in json) {
            if (!json[property] || json[property].length === 0) {
                alert("There are missing fields");
                return false;
            }
        }
        return true;
    }

    function editRecord(row, json) {
        for (col in json) {
            row.find("#" + col).text(json[col]);
        }
        $(row).removeClass("selected_row");
        $(row).effect("highlight", {
            color: '#8CEB84'
        }, 1000, function () {
            $(row).addClass("selected_row");
        });
        x = row;
        console.log(row);
        console.log(json);
    }

    function addrow(data) {
        var $tr = $("<tr>");
        var $first_td = $("<td>");
        var $input = $("<input name='row_selct' type='checkbox'>");
        $first_td.append($input);
        $tr.append($first_td);

        bindEvent($input);
        for (var i in columns) {
            var str = columns[i];
            $tr.append("<td id='" + i + "'>" + data[str] + "</td>");
        }
        $("#datatable tbody:last").append($tr);
        $tr.effect("highlight", {
            color: '#8CEB84'
        }, 1000);

    }

    function postDataAsync(operation) {
        // show color to show that is was changed }); // Attach click listeners to all the buttons
        json = {};
        var success;
        var fail;

        var valid = false;
        if (operation === data_map['add']['operation']) {
            for (var col in columns) {
                var col_name = columns[col];
                json[col_name] = $add_form.find('#' + col_name).val();
            }

            delete json['id'];
            if (validate(json)) {
                success = function (data) {
                    addrow(data);
                    $table = $("#datatable");
                };
                valid = true;
            }

        } else if (operation === data_map['edit']['operation']) {
            for (var col in columns) {
                var col_name = columns[col];
                json[col_name] = $edit_form.find('#' + col_name).val();
            }
            delete json['id'];
            delete json['date'];
            if (validate(json)) {
                json['id'] = row_indexs[row_index];
                valid = true;
                success = function (data) {
                    tableRow = $("td").filter(function () {
                        return $(this).text() == json['id'];
                    }).closest("tr");
                    editRecord(tableRow, data);
                };
            }

        } else if (operation === data_map['delete']['operation']) {
            json['id'] = row_indexs[row_index];
            valid = true;
            if (!json['id']) {valid = false; alert("You can't delete an empty record!");}
            success = function (data) {
                tableRow = $("td").filter(function () {
                    return $(this).text() == json['id'];
                }).closest("tr");
                tableRow.effect("effect", {
                    color: "red"
                }, 1000);
                $datatable.fnDeleteRow(tableRow.index());
                row_indexs.pop(row_indexs.indexOf(json['id']));
                location.reload();
            };

        } else if (operation === data_map['import']['operation']) {

        } else if (operation === data_map['export']['operation']) {

        }

        if (valid) {
            if (showConfirmDialog(operation)) {
                json['method'] = operation;
                $.ajax({
                    'type': 'POST',
                    'contentType': "application/json",
                    'dataType': 'json',
                    'url': POST_URL,
                    'data': JSON.stringify(json),
                    'statusCode': {
                        200: function (json) {
                            setRecord(operation);
                            success(json);
                        },
                        400: function () {
                            fail();
                        }
                    }
                });
            } else {
                // the action doesn't get performed
            }
        }
    }


    function bindEvent() {
        var bind_to = 'input[name="row_select"]';
        $(document).on('click', bind_to, function (event) {
            var $tr = $(this).parent().parent();
            $tr.toggleClass("selected_row");
            var id = $tr.find('#id').text();
            if ($(this).is(":checked")) {
                selected_rows[id] = $(this);
                row_indexs.push(parseInt(id));
                for (col in columns) {
                    var col_name = columns[col];
                    selected_rows[id][col_name] = $tr.find("#" + col_name).text();
                }
                setRecord(data_map['edit']['operation']);
                setRecord(data_map['delete']['operation']);
            } else {
                var index = row_indexs.indexOf(id);
                row_indexs.splice(index, 1);
                delete selected_rows[id];
                setRecord(data_map['edit']['operation']);
                setRecord(data_map['delete']['operation']);
            }
        });
    };

    bindEvent();

    function setRecord(operation) {
        if (operation === data_map['edit']['operation']) {
            if (row_indexs.length != 0) {
                for (col in columns) {
                    var col_name = columns[col];
                    var row = selected_rows[row_indexs[row_index]];
                    $edit_form.find('#' + col_name).val(row[col_name]);
                }
            } else {
                for (col in columns) {
                    var col_name = columns[col];
                    $edit_form.find('#' + col_name).val("");
                }

            }
        } else if (operation == data_map['delete']['operation']) {
            if (row_indexs.length != 0) {
                for (col in columns) {
                    var col_name = columns[col];
                    var row = selected_rows[row_indexs[row_index]];
                    $delete_form.find('#' + col_name).text(row[col_name]);
                }
            } else {
                for (col in columns) {
                    var col_name = columns[col];
                    $delete_form.find('#' + col_name).text("");
                }

            }

        }
    }

    $("#edit-op").click(function (event) {
        var len = Object.keys(selected_rows).length;
        if (len != 0) {
            setRecord($(this));
        } else {
            for (col in columns) {
                var col_name = columns[col];
                var row = selected_rows[row_index];
                $edit_form.find('#' + col_name).val("");
            }

        }

    });
    $("#edit-previous, #delete-previous").click(function () {
        var len = Object.keys(selected_rows).length;
        if (len != 0) {
            row_index = parseInt((row_index - 1) % row_indexs.length);
            if (row_index == -1) {
                row_index = row_indexs.length - 1;
            }
            var op = "#" + $(this).attr('id').split('-')[0] + '-op';
            setRecord(op);
        }
    });
    $("#edit-next, #delete-next").click(function () {
        var len = Object.keys(selected_rows).length;
        if (len != 0) {
            row_index = parseInt((row_index + 1) % row_indexs.length);
            var op = "#" + $(this).attr('id').split('-')[0] + '-op';
            setRecord(op);
        }
    });

    $("#delete-op").click(function (event) {
        var len = Object.keys(selected_rows).length;
        if (len != 0) {
            setRecord(data_map['delete']['operation']);
        } else {
            for (col in columns) {
                var col_name = columns[col];
                var row = selected_rows[row_index];
                $edit_form.find('#' + col_name).val("");
            }

        }
    });

    $.each(data_map, function (index, prop) {
        $(prop['operation']).on('click', function () {
            $(prop['form']).slideToggle();
            $(this).toggleClass('active');
            closeAll(prop['form']);
            $(prop['btn']).click(function () {
                postDataAsync(prop['operation']);
            });
        });
    });

    function closeAll(op) {
        for (var prop in data_map) {
            if (data_map[prop]['form'] !== op) {
                $(data_map[prop]['form']).hide();
                $(data_map[prop]['operation']).removeClass('active');
            }
        }
    }

    $("#print-op").click(function () {
        window.print();
    });
});
