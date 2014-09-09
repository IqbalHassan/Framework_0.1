/**
 * Created by Admin on 9/9/14.
 */
$(document).ready(function(){
   get_all_data();
});

function get_all_data(){
    var project_id= $.session.get('project_id').trim();
    var team_id= $.session.get('default_team_identity').trim();
    $.get('get_browser_data/',{
        'project_id':project_id,
        'team_id':team_id
    },function(data){
        var browser_list=data;
        for(var i=0;i<browser_list.length;i++){
            $("input[name='browser']").each(function(){
               if($(this).val()==browser_list[i]){
                   $(this).attr("checked","checked");
               }
            });
        }
    });
}