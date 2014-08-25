/**
 * Created by lent400 on 5/21/14.
 */
var operation = 1;
$(document).ready(function(){
   //MileStoneTab();

    New_UI();
});

function New_UI(){
    status_button_preparation();

    $.get("GetMileStones",{term : ''},function(data)
    {
        ResultTable(all_milestones,data['Heading'],data['TableData'],"Milestones");
    });

    $('#starting_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#ending_date').datepicker({ dateFormat: "yy-mm-dd" });

    $('#msinput').autocomplete({
        source:function(request,response){
            if($('#operation_milestone option:selected').val()!="0"){
                $.ajax({
                    url:"AutoMileStone",
                    dataType:"json",
                    data:{term:request.term},
                    success:function(data){
                        response(data);

                    }
                });
            }
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                $(this).val(value.trim());
                operation = 2;
                $("#renamebox").show();
                if(ui.item[1]=="not_started")
                {
                    $('a[value="not_started"]').addClass('selected')
                    $('a[value="started"]').removeClass('selected')
                    $('a[value="complete"]').removeClass('selected')
                    $('a[value="over_due"]').removeClass('selected')
                }
                else if(ui.item[1]=="started")
                {
                    $('a[value="not_started"]').removeClass('selected')
                    $('a[value="started"]').addClass('selected')
                    $('a[value="complete"]').removeClass('selected')
                    $('a[value="over_due"]').removeClass('selected')
                }
                else if(ui.item[1]=="complete")
                {
                    $('a[value="not_started"]').removeClass('selected')
                    $('a[value="started"]').removeClass('selected')
                    $('a[value="complete"]').addClass('selected')
                    $('a[value="over_due"]').removeClass('selected')
                }
                else if(ui.item[1]=="over_due")
                {
                    $('a[value="not_started"]').removeClass('selected')
                    $('a[value="started"]').removeClass('selected')
                    $('a[value="complete"]').removeClass('selected')
                    $('a[value="over_due"]').addClass('selected')
                }
                $("#ms_desc").val(ui.item[2]);
                $("#starting_date").val(ui.item[3]);
                $("#ending_date").val(ui.item[4]);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1] +"</a>" )
            .appendTo( ul );
    };


    $('#msinput2').autocomplete({
        source:function(request,response){
            if($('#operation_milestone option:selected').val()!="0"){
                $.ajax({
                    url:"AutoMileStone",
                    dataType:"json",
                    data:{term:request.term},
                    success:function(data){
                        response(data);
                    }
                });
            }
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                $(this).val(value.trim());
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };

    $('#ms_button').live('click',function(){

        //get the statuses
        var status="";
        if($('a[value="not_started"]').hasClass('selected'))
            status = "not_started";
        if($('a[value="started"]').hasClass('selected'))
            status = "started";
        if($('a[value="complete"]').hasClass('selected'))
            status = "complete";
        if($('a[value="over_due"]').hasClass('selected'))
            status = "over_due";

        var description = $("#ms_desc").val();
        var created_by = "";
        var modified_by = "";

        var team=[];
        $('input[name="team"]:checked').each(function(){
            team.push($(this).val());
        });

       // var operation=$('#operation_milestone option:selected').val();
        if(operation==1){
            var new_name=$('#msinput').val();
            var start_date = $("#starting_date").val();
            var end_date = $("#ending_date").val();
            created_by = $.session.get('fullname');

        }
        else if(operation==2){
            var new_name=$('#msinput2').val();
            var old_name=$('#msinput').val();
            var start_date = $("#starting_date").val();
            var end_date = $("#ending_date").val();
            modified_by = $.session.get('fullname');
        }
        else{
            var new_name=$('#msinput').val();
            var old_name="";
            var start_date = "";
            var end_date = "";
        }
        if(operation=="0"){
            var title_msg = "Fields are Empty!"
        }
        else if(operation=="1"){
            title_msg = "Milestone Created"
        }
        else if(operation=="2"){
            title_msg = "Milestone Modified"
        }
        else if(operation=="3"){
            title_msg = "Milestone Deleted"
        }
        if(operation=="0"||new_name==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_milestone').html(error_message);
            $('#error_milestone').css({'display':'block'});
        }
        else {
            $.get('MileStoneOperation',{status:status,description:description.trim(),old_name:old_name,new_name:new_name,operation:operation,'team':team.join("|").trim(),start_date:start_date.trim(),end_date:end_date.trim(),created_by:created_by,modified_by:modified_by},function(data){
                if(data['confirm_message']==""){
                    var color='red';
                }
                else{
                    var color='green';
                }
                if(data['confirm_message']==""){
                    alertify.log(""+data['error_message']+"","",0);
                    milestone_notify(""+data['error_message']+"",""+data['error_message']+"","/site_media/noti2.ico");
                    $('#error_milestone').html('<b style="color:red;">'+data['error_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/ManageMilestone/';
                }
                else{
                    alertify.log(""+data['confirm_message']+"","",0);
                    milestone_notify(title_msg,""+data['confirm_message']+"","/site_media/noti.ico");
                    $('#error_milestone').html('<b style="color:green;">'+data['confirm_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/ManageMilestone/';
                }

            })
        }
    });

}

function status_button_preparation(){
    $("#not_started").click(function(){
        $(this).addClass("selected");
        $('#started').removeClass("selected");
        $('#over_due').removeClass("selected");
        $('#complete').removeClass("selected");
    });
    $("#started").click(function(){
        $(this).addClass("selected");
        $('#not_started ').removeClass("selected");
        $('#over_due').removeClass("selected");
        $('#complete').removeClass("selected");
    });
    $("#over_due").click(function(){
        $(this).addClass("selected");
        $('#complete').removeClass("selected");
        $('#not_started').removeClass("selected");
        $('#started').removeClass("selected");
    });
    $("#complete").click(function(){
        $(this).addClass("selected");
        $('#started').removeClass("selected");
        $('#over_due').removeClass("selected");
        $('#not_started').removeClass("selected");
    });
}

/*function MileStoneTab(){
    $('#msinput').autocomplete({
        source:function(request,response){
            if($('#operation_milestone option:selected').val()!="0"){
                $.ajax({
                    url:"AutoMileStone",
                    dataType:"json",
                    data:{term:request.term},
                    success:function(data){
                        response(data);

                    }
                });
            }
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                $(this).val(value.trim());
                $("#starting_date").val(ui.item[1]);
                $("#ending_date").val(ui.item[2]);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+ " - " + item[2] +"</a>" )
            .appendTo( ul );
    };
    $('#operation_milestone').live('change',function(){
        // autoCompleteMilestone();
        var selection=$('#operation_milestone option:selected').val();
        if(selection==1 || selection==2){
            $("#start_field").css({'display':'inline-block'});
            $("#end_field").css({'display':'inline-block'});
            $('#starting_date').datepicker({ dateFormat: "yy-mm-dd" });
            $('#ending_date').datepicker({ dateFormat: "yy-mm-dd" });
        }
        else {
            $("#start_field").css({'display':'none'});
            $("#end_field").css({'display':'none'});
            //$('#starting_date').datepicker('disable');
            //$('#ending_date').datepicker('disable');
        }
        if(selection==2){
            $('#renamebox').css({'display':'inline-block'});
            $('#msinput2').autocomplete({
                source:function(request,response){
                    if($('#operation_milestone option:selected').val()!="0"){
                        $.ajax({
                            url:"AutoMileStone",
                            dataType:"json",
                            data:{term:request.term},
                            success:function(data){
                                response(data);
                            }
                        });
                    }
                },
                select:function(request,ui){
                    var value=ui.item[0].trim();
                    if (value!=""){
                        $(this).val(value.trim());
                        return false;
                    }
                }
            }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li></li>" )
                    .data( "ui-autocomplete-item", item )
                    .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
                    .appendTo( ul );
            };
        }
        else{
            $('#renamebox').css({'display':'none'});
        }
    });
    $('#ms_button').live('click',function(){
        var operation=$('#operation_milestone option:selected').val();
        if(operation==1){
            var new_name=$('#msinput').val();
            var start_date = $("#starting_date").val();
            var end_date = $("#ending_date").val();
        }
        else if(operation==2){
            var new_name=$('#msinput2').val();
            var old_name=$('#msinput').val();
            var start_date = $("#starting_date").val();
            var end_date = $("#ending_date").val();
        }
        else{
            var new_name=$('#msinput').val();
            var old_name="";
            var start_date = "";
            var end_date = "";
        }
        if(operation=="0"){
            var title_msg = "Fields are Empty!"
        }
        else if(operation=="1"){
            title_msg = "Milestone Created"
        }
        else if(operation=="2"){
            title_msg = "Milestone Modified"
        }
        else if(operation=="3"){
            title_msg = "Milestone Deleted"
        }
        if(operation=="0"||new_name==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_milestone').html(error_message);
            $('#error_milestone').css({'display':'block'});
        }
        else {
            $.get('MileStoneOperation',{old_name:old_name,new_name:new_name,operation:operation,start_date:start_date.trim(),end_date:end_date.trim()},function(data){
                if(data['confirm_message']==""){
                    var color='red';
                }
                else{
                    var color='green';
                }
                if(data['confirm_message']==""){
                    alertify.log(""+data['error_message']+"","",0);
                    milestone_notify(""+data['error_message']+"",""+data['error_message']+"","/site_media/noti2.ico");
                    $('#error_milestone').html('<b style="color:red;">'+data['error_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/ManageMilestone/';
                }
                else{
                    alertify.log(""+data['confirm_message']+"","",0);
                    milestone_notify(title_msg,""+data['confirm_message']+"","/site_media/noti.ico");
                    $('#error_milestone').html('<b style="color:green;">'+data['confirm_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/ManageMilestone/';
                }

            })
        }
    });
}*/
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

    var button = document.getElementById('ms_button');

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