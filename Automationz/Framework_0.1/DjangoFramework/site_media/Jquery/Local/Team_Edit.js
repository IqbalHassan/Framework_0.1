$(document).ready(function(){
    ButtonPreparation();
});
function ButtonPreparation(){
    $('#add').click(function(){
        var member=[];
        $('.add_manager:checked').each(function(){
            member.push($(this).val());
        });
        $('.add_tester:checked').each(function(){
            member.push($(this).val());
        });
        var team_name=$('#name').text().trim();
        if(member.length!=0 || tester.length!=0){
            alertify.confirm("Are you sure you want to add the selected to the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Add_Members',{
                        'member':member.join("|"),
                        'team_name':team_name.trim()
                    },function(data){
                        if(data.indexOf('Failed')!=0){
                            window.location=('/Home/Team/'+team_name.trim().replace(/ /g,'_').trim()+'/');
                        }
                        else{
                            window.location.reload(true);
                        }
                    });
                }
            });
        }
        else{
            alertify.error("None is selected from right column","",0);
            return false;
        }

    });
    $('#remove').click(function(){
        var member=[];
        $('.remove_manager:checked').each(function(){
            member.push($(this).val());
        });
        $('.remove_tester:checked').each(function(){
            member.push($(this).val());
        });
        var team_name=$('#name').text().trim();
        if(member.length!=0 || tester.length!=0){
            alertify.confirm("Are you sure you want to remove the selected from the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Delete_Members',{
                        'member':member.join("|"),
                        'team_name':team_name.trim()
                    },function(data){
                        if(data.indexOf('Failed')!=0){
                            window.location=('/Home/Team/'+team_name.trim().replace(/ /g,'_').trim()+'/');
                        }
                        else{
                            window.location.reload(true);
                        }
                    });
                }
            });
        }
        else{
            alertify.error("None is selected from right column","",0);
            return false;
        }

    });
}