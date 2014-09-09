/**
 * Created by J on 9/1/14.
 */

var operation = 1;

$(document).ready(function(){

    ActivateNecessaryButton();
    ButtonSet();

    TestCaseLinking();

    $("#submit").live('click',function(){

        var project = $("#project_identity").val();
        var bug_desc=$("#bug_desc").val();
        var start_date=$('#start_date').val();
        var end_date=$('#end_date').val();
        var team=$("#default_team_identity").val();
        var priority= 'P' + $('#priority').val();
        var milestone=$('#milestone').text();
        var title=$('#title').val();
        var creator = $("#created_by").val();
        var testers= $("#tester").text();
        /*$('.selected').each(function(){
            testers.push($(this).text().trim());
        });*/
        var status = $('#status').val();


        $.get("LogNewBug/",{
            title:title.trim(),
            description:bug_desc.trim(),
            status:status.trim(),
            start_date:start_date.trim(),
            end_date:end_date.trim(),
            team:team.trim(),
            tester:testers,
            priority:priority.trim(),
            milestone:milestone.trim(),
            project_id: project.trim(),
            user_name:$('#user_name').text().trim(),
            created_by:creator.trim()
        },function(data){
            window.location='/Home/ManageBug/';
        });

        /*if(operation=="0"||title==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_milestone').html(error_message);
            $('#error_milestone').css({'display':'block'});
        }
        else {
            var title_msg = "Bug Created!";

            $.get('BugOperation',{
                operation:operation,
                title:title.trim(),
                description:bug_desc.trim(),
                status:status.trim(),
                start_date:start_date.trim(),
                end_date:end_date.trim(),
                team:team.trim(),
                tester:testers.join("|").trim(),
                priority:priority.trim(),
                milestone:milestone.trim(),
                project_id: project.trim(),
                user_name:$('#user_name').text().trim(),
                created_by:creator.trim()
            },function(data){
                if(data['confirm_message']==""){
                    var color='red';
                    alertify.log(""+data['error_message']+"","",0);
                    milestone_notify(""+data['error_message']+"",""+data['error_message']+"","/site_media/noti2.ico");
                    $('#error_milestone').html('<b style="color:red;">'+data['error_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/ManageBug/';
                }
                else{
                    var color='green';
                    alertify.log(""+data['confirm_message']+"","",0);
                    milestone_notify(title_msg,""+data['confirm_message']+"","/site_media/noti.ico");
                    $('#error_milestone').html('<b style="color:green;">'+data['confirm_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/CreateBug/';
                }

            })
        }*/
    });
});

function TestCaseLinking(){

    $("#search_case").autocomplete({

        source:function(request,response){
            $.ajax({
                url:"TestCaseSearch",
                dataType:"json",
                data:{
                    term:request.term
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select : function(event, ui) {

            var value = ui.item[1]

            $("#linking").append('<tr><td><img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text selected">'
                + value
                + "&nbsp"
                + '</td></tr>');

            //$("#tester th").css('display', 'block');

            $("#search_case").val("");
            return false;

        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + " - "+item[1]+"<strong> - " + item[2] + "</strong></a>" )
            .appendTo( ul );
    };

    $("#search_case").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteCase").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
}

function ButtonSet(){

    $("#assigned_tester").autocomplete({

        source:function(request,response){
            $.ajax({
                url:"AutoCompleteTesterSearch",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select : function(request, ui, item) {

            var value = ui.item.value
            if(value!=''){
                $("#tester").html('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text selected">'
                    + value
                    //+ "&nbsp"
                    + '</td>');

                //$("#tester th").css('display', 'block');

                $("#assigned_tester").val("");
                return false;
            }

        }
    });
    $("#assigned_tester").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteTester").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();
    });
    $('#milestone_list').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"AutoMileStone",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                //$(this).val(value.trim());
                $("#milestone").html('<td><img class="delete" id = "DeleteMileStone" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text">'
                    + value
                    //+ "&nbsp"
                    + '</td>');

                //$("#MileStoneHeader th").css('display', 'block');

                $("#milestone_list").val("");
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $("#milestone_list").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteMileStone").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
}
function ActivateNecessaryButton(){
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#start_date').datepicker("option", "showAnim", "slide" );
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#end_date').datepicker("option", "showAnim", "slide" );
    $(".selectdrop").selectBoxIt();
}


function milestone_notify(title_msg,message,icon){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('submit');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification(title_msg,{body:message, icon:icon});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification(title_msg,{body:message, icon:icon});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }


}