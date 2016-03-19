var congressmen;
var votes;
var test;

function getCongressmanData(lname){
    var dataString = "lname=" + lname; 
    $.ajax({
        url:  "getCongressmanData.php",
        type: "POST",
        data: dataString,
        success: function(html) {
            votes = JSON.parse(html);
            $("#results").empty();
            $("#explanation").remove();
            for (var i = 1; i <= Object.keys(votes).length; i++) {
                $("#results")[0].appendChild(new VoteRecord(votes[i]));
            };
        },
        error: function (jqXHR, status, err) {
            throw new("Error: retrieve.php connect failure.");
        }
    });
}

function cleanUpCongressmen(str){
    var barIndex = str.indexOf("|");
    var lname = str.substring(barIndex + 1, str.length)

    var junior = false;
    var jrIndex = str.indexOf("Jr.,");
    if(jrIndex != -1){
        str = str.substring(jrIndex + 5, str.length);
        junior = true;
    }

    var commaIndex = str.indexOf(",");
    if(commaIndex != -1)
        str = str.substring(0, commaIndex);

    if(junior)
        str += "|Jr.";

    str = lname + "|" + str;
    return str.split("|");
}

function fillCongressmen(){
    $.ajax({
        url:  "getCongressmen.php",
        type: "POST",
        success: function(html) {
            congressmen = JSON.parse(html);
            for(var i = 0; i < congressmen.length; i++){
                var ele = document.createElement("option");
                var congressman = cleanUpCongressmen(congressmen[i]);
                ele.value = congressman[0];
                var fullName = congressman[1] + " " + congressman[2];
                if(congressman[3])
                    fullName += " " + congressman[3]
                ele.innerHTML = fullName;
                $("#congressmanSelect").append(ele);
            }
            $('.chosen-select').chosen();
            $('.chosen-select').on('change', function(e, params) {
                getCongressmanData(params.selected)
            });
        },
        error: function (jqXHR, status, err) {
            throw new("Error: getLastFileId.php connect failure.");
        }
    });
}

$(document).ready(function() {
    fillCongressmen();
    $("#searchButton").on('click', function(){
        getCongressmanData($("#congressmanSelect").val());
    });
});