/**
 * Created by gengzl on 14-11-26.
 */
var selected_path = "/static1/img/selected_seat.jpg";
var unselected_path = "/static1/img/unselected_seat.jpg";
var myseat_path = "/static1/img/myseat.gif";
function draw_seats(seat_matrix) {
    $(".seat_tr").children().remove();
    var table = $("#seat_plan");
    var rows = seat_matrix.length
    var cols = seat_matrix[0].length
    for (var i = 1; i <= rows; i++) {
        var tr = $("<tr>").attr('class', 'seat_tr').attr('id', 'tr'+i);

        var td2 = $("<td>");
        td2.attr("id", "row" + i);

        for (var j = 1; j <= cols; j++) {
            var s = $("<span>");
            if (seat_matrix[i-1][j-1] == 1){
                s.attr("class", "seat selected").append($('<img>').attr('src', selected_path));
            }
            else if (seat_matrix[i-1][j-1] == 2){
                s.attr("class", "seat hasSold");
            }
            else if (seat_matrix[i-1][j-1] == 3){
                s.attr("class", "seat myseat").append($('<img>').attr('src', myseat_path));
            }
            else if (seat_matrix[i-1][j-1] == 4){
                s.attr("class", "seat unselected").append($('<img>').attr('src', unselected_path));
            }
            else{
                s.attr("class", "seat");
            }

            s.appendTo(td2);
        }
        td2.appendTo(tr);

        table.append(tr);
        var w = window.innerWidth;
        var l = Math.min(30,(w-50) / cols);
        $('.seat').css('width', l).css('height', l);
        $('.seat img').css('width', l).css('height', l);
    }
}

function chooseSeat(rows, cols)
{
    $('.unselected').click(function () {
        reverseChoices($(this))
    })
    $('.selected').click(function () {
        reverseChoices($(this))
    })

    for (var i = 1; i <= rows; i++) {
        var tr = $("#tr"+i);
        var td1 = $("<td>");
        var div = $("<div>");

        div.attr({ class: "checkbox", style: "margin-right:30px" });

        var label = $("<label>");

        var input = $("<input>");
        input.attr({id: "check_row" + i, name: "row" + i, onchange: "check_row(" + i + ")",
            type: "checkbox", value: "x"});
        input.appendTo(label);

        var span = $("<span>");
        span[0].innerHTML = "第" + i + "排";
        span.appendTo(label);

        label.appendTo(div);
        div.appendTo(td1);
        td1.prependTo(tr);
    }
    $('<td>').prependTo($('tr#tr_stage'));

}

function reverseChoices(temp) {
    if (temp.hasClass("selected")) {
        temp.removeClass("selected");
        temp.addClass("unselected");
    } else if (temp.hasClass("unselected")) {
        temp.removeClass("unselected");
        temp.addClass("selected");
    }
}

function reverseAll(rows, cols) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            var temp = $('s' + i + '_' + j);
            reverseChoices(temp)
        }
    }
}

function check_row(n) {
    var l = $("#row" + n).children().length;
    if ($("#check_row" + n)[0].checked == true) {
        //将座位选中
        for (var i = 0; i < l; i++) {
            $($("#row" + n).children()[i]).removeClass("unselected");
            $($("#row" + n).children()[i]).addClass("selected");
        }
    }
    else {
        for (var i = 0; i < l; i++) {
            $($("#row" + n).children()[i]).removeClass("selected");
            $($("#row" + n).children()[i]).addClass("unselected");
        }
    }
}