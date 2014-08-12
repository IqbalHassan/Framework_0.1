/*$(document).ready(function(){
    BasicPreparation();
});
function BasicPreparation(){
    //showing the dates in right format
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd" })

    $('#submit_button').click(function(){
        //alert('clicked');
        //Get all the info about the current requirement
        var project_id=$('#project_id option:selected').val().trim();
        var requirement_parent_id=$('#parent_req_id option:selected').val().trim();
        var team_id=$('#team_id option:selected').val().trim();
        var title=$('#title').val().trim();
        var description=$('#description').val().trim();
        var start_date=$('#start_date').val().trim();
        var end_date=$('#end_date').val().trim();
        var priority=$('#priority option:selected').val().trim();
        var status=$('#status option:selected').val().trim();
        var milestone=$('#milestone option:selected').val().trim();
        $.get('CreateRequirement',{
            'project_id':project_id.trim(),
            'requirement_id':requirement_parent_id.trim(),
            'team_id':team_id.trim(),
            'title':title.trim(),
            'description':description.trim(),
            'start_date':start_date.trim(),
            'end_date':end_date.trim(),
            'priority':priority.trim(),
            'status':status.trim(),
            'milestone':milestone.trim(),
            'user_name': $('#user_name').text().trim()
        },function(data){
            window.location=("/Home/ManageRequirement/");
        });
    });
    $('#project_id').on('change',function(){
        //get the required team info
        $.get('GetTeamInfoToCreateRequirement',{'project_id':$(this).val()},function(data){
            var message="";
            for(var i=0;i<data['teams'].length;i++){
                message+=('<option value="'+data['teams'][i][0]+'">'+data['teams'][i][1]+'</option>');
            }
            $('#team_id').html(message);
        });
    });
}*/
var createpath="CreateRequirement";
var editpath="EditRequirement";
$(document).ready(function(){
    var URL=window.location.pathname;
    var create_index=URL.indexOf(createpath);
    var edit_index=URL.indexOf(editpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    if(create_index != -1 || edit_index != -1){
        //Button Preparation
        status_button_preparation();
        $('#project_id').text($.session.get('project_id'));
        $('#starting_date').datepicker({ dateFormat: "yy-mm-dd" });
        $('#ending_date').datepicker({ dateFormat: "yy-mm-dd" });

        if(edit_index != -1 && template){

        }
        if(!template){
            $('#form_parent_selection').css({'display':'none'});
        }
        else{
            $('#form_parent_selection').css({'display':'block'});
        }
        $('#submit').click(function(){
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
            var requirement_description="";
            requirement_description=$('#description').val();
            var start_date="";
            start_date=$('#starting_date').val();
            var end_date="";
            end_date=$('#ending_date').val();
            var team=[];
            $('input[name="team"]:checked').each(function(){
               team.push($(this).val());
            });
            var priority="";
            priority=$('input[name="priority"]:checked').val();
            var milestone=$('#milestone option:selected').val();
            var title=$('#title').val();
            $.get("SubmitCreateRequirement/",{
                'title':title.trim(),
                'description':requirement_description.trim(),
                'status':status.trim(),
                'start_date':start_date.trim(),
                'end_date':end_date.trim(),
                'team':team.join("|").trim(),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$('#user_name').text().trim()
            },function(data){

            });
        });
    }
});
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