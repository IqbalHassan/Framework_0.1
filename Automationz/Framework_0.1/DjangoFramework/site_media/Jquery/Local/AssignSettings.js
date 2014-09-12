/**
 * Created by Admin on 9/9/14.
 */
$(document).ready(function(){
    get_all_data();
    set_button_behaviour();
});
function set_button_behaviour(){
    $('#new_browser_submit').on('click',function(){
        var browser_name=$('#new_browser_name').val().trim();
        var browser_version=$('#new_browser_version').val().trim();
        var project_id=$('#project_identity option:selected').val().trim();
        var team_id=$('#default_team_identity option:selected').val().trim();
        $.get("enlist_new_browsers/",{
            'project_id':project_id.trim(),
            'team_id':team_id.trim(),
            'browser_name':browser_name.trim(),
            'browser_version':browser_version.trim()
        },function(data){

        });
    });
    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val().trim());
        window.location=('/Home/AssignSettings/');
    });
    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val().trim());
        window.location=('/Home/AssignSettings/');
    });
    $('#new_browser_button').on('click',function(){
        $(this).css({'display':'none'});
        $('#name_row').css({'margin-left':'45%'});
        $('#name_row').slideDown('slow');
        $('#button_row').slideDown('slow');
    });
    $('#new_browser_cancel').on('click',function(){
        $('#button_row').css({'display':'none'});
        $('#name_row').css({'display':'none'});
        $('#new_browser_button').css({'display':'block'});
    });
    $('#select_browser').on('click',function(){
        var browser_list=[];
        $('input[name="browser"]:checked').each(function(){
            browser_list.push($(this).val());
        });
        console.log(browser_list);
        send_data_to_backend(browser_list);
    });
}

function send_data_to_backend(browser_list){
    $.get("enlist_browser_to_team_settings/",{
        'browser_list':browser_list.join("|"),
        'project_id': $('#project_identity option:selected').val().trim(),
        'team_id':$('#default_team_identity option:selected').val().trim()
    },function(data){
        if(data==='message'){
            window.location=('/Home/AssignSettings/');
        }
    });
}

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