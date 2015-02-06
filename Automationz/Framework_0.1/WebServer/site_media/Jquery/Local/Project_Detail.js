$(document).ready(function(){
    StylePreparation();

    $('#add_selected').on('click',function(){
        var teams=[];
        $('input[name="rest_team"]:checked').each(function(){
           teams.push($(this).val().trim());
        });
        $.get('AddTeamtoProject',
            {'project_id':$('#project_id').text().trim(),
            'teams':teams.join("|")
            },
        function(data){
            var location=('/Home/Project/'+$('#project_id').text().trim()+'/');
            window.location=location;
        });
    });
});
function StylePreparation(){
    $('#id_comment').closest('tr').find('th:first').css({'vertical-align':'0%'});
    $('#id_commented_by').val($('#user_name').text().trim());
}