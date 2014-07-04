var color={
    'Started':'#0000ff',
    'Complete':'#00ff00',
    'Overdue':'#ff0000'
};
$(document).ready(function(){
    GetAllRequirements($.session.get('project_id'));
    PopulateNewRequirementDiv($.session.get('project_id'));
    PrepareButtons();
});

function GetAllRequirements(project_id){
    $.get('GetAllRequirements',{'project_id':project_id.trim()},function(data){
        var message="";
        var requirements=data['requirement'];
        for(var i=0;i<requirements.length;i++){
            message+=(
                '<tr>'+
                    '<td width="90%" style="border-bottom: 2px solid #cccccc;">' +
                        '<table width="100%">' +
                            '<tr>' +
                                '<td><b class="Text requirement"style="cursor: pointer"> '+requirements[i][0]+'</b></td>' +
                            '</tr>' +
                            '<tr style="display: none;">' +
                                '<td>' +
                                    '<table width="100%" style="border-collapse: collapse;border-top: 1px solid #003bb3;margin-bottom: 5%;margin-top: 1%;font-size: 125%;">' +
                                        '<tr>' +
                                            '<td align="right" width="10%"><b style="color:#4183c4">Description:</b></td>' +
                                            '<td align="left" style="margin-left: 2%;">'+requirements[i][1]+'</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<td align="right" width="10%"><b style="color:#4183c4">Due In:</b></td>' +
                                            '<td align="left" style="margin-left: 2%;">'+requirements[i][2]+'</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<td align="right" width="10%"><b style="color:#4183c4">Milestone:</b></td>' +
                                            '<td align="left" style="margin-left: 2%;">'+requirements[i][6]+'</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<td align="right" width="10%"><b style="color:#4183c4">Status:</b></td>' +
                                            '<td align="left" style="margin-left: 2%;color: '+color[requirements[i][3]]+'">'+requirements[i][3]+'</td>' +
                                        '</tr>' +
                                    '</table>' +
                                '</td>' +
                            '</tr>' +
                        '</table>' +
                    '</td>'+
                    '<td width="10%;" align="right" style="border-bottom: 2px solid #cccccc;vertical-align: 0%;">' +
                        '<a href="/Home/'+requirements[i][4]+'/Requirements/'+requirements[i][5]+'/">See Details</a>' +
                    '</td>'+
                '</tr>'
            );
        }
        $('#requirements').html(message);
        EnableClicking();
    });
}
function EnableClicking(){
    $('.requirement').on('click',function(){
        $(this).closest('tr').next().slideToggle('slower');
    });
}
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
        var user_name= $('#user_name').text().trim();
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
            window.location=('/Home/ManageRequirement/');
        });
    });
}