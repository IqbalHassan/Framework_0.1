$(document).ready(function(){
    ButtonPreparation();
});
function ButtonPreparation(){
    $('#add').click(function(){
        var manager=[]
        $('.add_manager:checked').each(function(){
            manager.push($(this).val());
        });
        var tester=[];
        $('.add_tester:checked').each(function(){
            tester.push($(this).val());
        });
        var team_name=$('#name').text().trim();
        if(manager.length!=0 || tester.length!=0){
            alertify.confirm("Are you sure you want to add the selected to the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Add_Members',{
                        'manager':manager.join("|"),
                        'tester':tester.join("|"),
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
        var manager=[];
        $('.remove_manager:checked').each(function(){
            manager.push($(this).val());
        });
        var tester=[];
        $('.remove_tester:checked').each(function(){
            tester.push($(this).val());
        });
        var team_name=$('#name').text().trim();
        if(manager.length!=0 || tester.length!=0){
            alertify.confirm("Are you sure you want to remove the selected from the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Delete_Members',{
                        'manager':manager.join("|"),
                        'tester':tester.join("|"),
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
            alertify.error("None is selected from current team","",0);
            return false;
        }
    });
}