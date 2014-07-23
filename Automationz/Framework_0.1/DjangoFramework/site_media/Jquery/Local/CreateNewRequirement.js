$(document).ready(function(){
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
}