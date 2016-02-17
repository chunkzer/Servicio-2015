$(document).ready(function(){
    $("a.order_menu").click(function(){
        $.ajax({
            url: '/flaskapp/order',
            data: JSON.stringify({criteria: $(this).attr("id")}),
            type: "POST",
            dataType: "json",
            success: function(response, status, xhr) {
                $("#first_row").nextAll().remove();
                // alert("respuesta >> " + response.users[0][1])
                for (var user in response.users) {
                    user_row = "<tr>\
                    <td>\
                        <a href=\"/flaskapp/datos/"+encodeURIComponent(response.users[user][2])+"\">"+response.users[user][1]+"</a>\
                    </td>\
                    <td>\
                        "+response.users[user][2]+"\
                    </td>\
                    <td>\
                        "+response.users[user][8]+"\
                    </td>\
                    <td>\
                        "+response.users[user][13]+"\
                    </td>\
                    </tr>"
                    $(user_row).insertAfter("#first_row")
                }
            },
            error: function(xhr, status, error) {
                alert("Error. Status >> " + status + " Error >> " + error);
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });
    });
});
$(document).ready(function(){
    $("#search").click(function(){
        if ($("#usr").val() != '') {
            $.ajax({
                url: 'order',
                data: JSON.stringify({nombre: $("#usr").val()}),
                type: "POST",
                dataType: "json",
                success: function(response, status, xhr) {
                    $("#first_row").nextAll().remove();
                    // alert("respuesta >> " + response.users[0][1])
                    for (var user in response.users) {
                        user_row = "<tr>\
                        <td>\
                            <a href=\"/flaskapp/datos/"+encodeURIComponent(response.users[user][2])+"\">"+response.users[user][1]+"</a>\
                        </td>\
                        <td>\
                            "+response.users[user][2]+"\
                        </td>\
                        <td>\
                            "+response.users[user][8]+"\
                        </td>\
                        <td>\
                            "+response.users[user][13]+"\
                        </td>\
                        </tr>"
                        $(user_row).insertAfter("#first_row")
                    }
                },
                error: function(xhr, status, error) {
                    alert("Error. Status >> " + status + " Error >> " + error);
                },
                contentType: "application/json; charset=utf-8",
                dataType: "json"
            });
        }
    });
});
