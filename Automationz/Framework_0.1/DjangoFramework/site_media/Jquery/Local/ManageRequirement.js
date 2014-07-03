$(document).ready(function(){
    PopulateNewRequirementDiv($.session.get('project_id'));
    PrepareButtons();
});
function PopulateNewRequirementDiv(project_id){
    $.get('GetNewRequirementDetail',{'project_id': project_id},function(data){
        $('#project_id').val(project_id);
        var teams=data['teams'];
        var message="";
        for(var i=0;i<teams.length;i++){
            message+=('<option value="'+teams[i][0]+'">'+teams[i][0]+' - '+teams[i][1]+'</option>');
        }
        $('#team_id').html(message);
    });
}
function PrepareButtons(){
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#submit_button').click(function(){
        var project_id=$('#project_id').val().trim();
        var team_id=$('#team_id').val().trim();
        var title=$('#title').val().trim();
        var description=$('#description').val().trim();
        var start_date=$('#start_date').val().trim();
        var end_date=$('#end_date').val().trim();
        var priority=$('#priority').val().trim();
        var milestone=$('#milestone').val().trim();
        var status=$('#status').val().trim();
        var user_name= $.session.get('username');
        $.get('CreateRequirement',{
            'project_id':project_id,
            'team_id':team_id,
            'title':title,
            'description':description,
            'start_date':start_date,
            'end_date':end_date,
            'priority':priority,
            'milestone':milestone,
            'status':status,
            'user_name':user_name
        },function(data){

        });
    });
}