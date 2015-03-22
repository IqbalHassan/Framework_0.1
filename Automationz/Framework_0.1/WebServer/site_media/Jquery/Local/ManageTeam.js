/**
 * Created by lent400 on 5/27/14.
 */
/*
var project_id= $.session.get('project_id');
$(document).ready(function(){
    $('body').css({'font-size':'100%'});
    GetAllTeam();
    $('#create_team').on('click',function(){
        $('.team').css({'background-color':'#fff'});
        $('.team').removeClass('selected');
        $('#control_panel').css({'display':'none'});
        $('#main_body').html(team_crate());
        $("#search_tester").select2({
            placeholder: "Assigned Testers...",
            width: 460,
            quietMillis: 250,
            ajax: {
                url: "AutoCompleteTesterSearch/",
                dataType: "json",
                queitMillis: 250,
                data: function(term, page) {
                    return {
                        'term': term,
                        'page': page,
                        'all':'all'
                    };
                },
                results: function(data, page) {
                    return {
                        results: data.items,
                        more: data.more
                    }
                }
            },
            formatResult: formatUsers
        }).on("change", function(e) {
                var user_id=$(this).select2('data')['id'];
                var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
                $("#tester").append('<tr><td><img class="delete DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text" data-id="'+user_id+'">'
                    + user_name
                    + ":&nbsp"
                    + '</td></tr>');
                $(this).select2('val','');
                return false;
            });

        function formatUsers(user_details) {
            var markup ='<div><i class="fa fa-user"></i><span style="font-weight: bold;"><span>' + ' ' + user_details.text + '</span></div>';

            return markup;
        }
        $(".DeleteTester").live('click', function() {

            //$(this).parent().next().remove();
            //$(this).remove();
            $(this).parent().parent().remove();

        });

        $("#search_manager").select2({
            placeholder: "Assigned Manager...",
            width: 460,
            quietMillis: 250,
            ajax: {
                url: "GetTesterManager/",
                dataType: "json",
                queitMillis: 250,
                data: function(term, page) {
                    return {
                        'term': term,
                        'page': page,
                        'all':'all'
                    };
                },
                results: function(data, page) {
                    return {
                        results: data.items,
                        more: data.more
                    }
                }
            },
            formatResult: formatUsers
        }).on("change", function(e) {
                var user_id=$(this).select2('data')['id'];
                var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
                $("#manager").append('<tr><td><img class="delete DeleteManager" title = "ManagerDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text" data-id="'+user_id+'">'
                    + user_name
                    + ":&nbsp"
                    + '</td></tr>');
                $(this).select2('val','');
                return false;
            });
        $(".DeleteManager").live('click', function() {
            $(this).parent().parent().remove();
        });

        $('#submit_team').on('click',function(){
            var team_name=$('#team_name').val().trim();
            var member=[];
            $('.DeleteManager').each(function(){
               member.push($(this).parent().next().attr('data-id'));
            });
            $('.DeleteTester').each(function(){
                member.push($(this).parent().next().attr('data-id'));
            });
            //alert(member);
            if(member.length==0 || team_name.trim()==""){
                alertify.log("Some of the fields are empty","",0);
                return false;
            }else{
                $.get("Create_Team",{'project_id':project_id.trim(),'member':member.join("|"),'team_name':team_name},function(data){
                    if(data.indexOf('Failed')!=0){
                        window.location=('/Home/'+project_id+'/Team/'+team_name.trim().replace(/ /g,'_').trim()+'/');
                    }
                    else{
                        window.location.reload(true);
                    }
                });
            }

        });
});
    //CreateButtonInit();
    //Other();
});
function team_crate(){
    var message='';
    message+='<table class="two-column-emphasis"><caption><b style="font-size: 150%;">Team Details</b></caption>';
    message+='<tr><td align="right"><b>Team Name:</b></td><td align="left"><input class="textbox" id="team_name" placeholder="Team name here"/> </td><td>&nbsp;</td></tr>';
    message+='<tr><td align="right" style="vertical-align: 0%"><b>Manager:</b></td><td  style="vertical-align: 0%" align="left"><input type="hidden"  placeholder="Search Managers" id="search_manager"/> </td><td><table id="manager"></table></td></tr>';
    message+='<tr><td align="right" style="vertical-align: 0%"><b>Tester:</b></td><td  style="vertical-align: 0%" align="left"><input type="hidden" placeholder="Search Testers" id="search_tester"/> </td><td><table id="tester"></table></td></tr>';
    message+='<tr><td align="right" style="vertical-align: 0%">&nbsp;</td><td  style="vertical-align: 0%" align="left"><input class="m-btn green" value="Submit" id="submit_team" type="button"/> </td><td>&nbsp;</td></tr>';
    message+='</table>';
    return message;
}
function GetAllTeam(){
    $("#main_body").empty();
    $('#control_panel').empty();
    $.get('GetAllTeam',{'project_id':project_id},function(data){
        var team_list=data['all_team'];
        var global_list=data['global_team'];
        var message='';
        message+='<table class="two-column-emphasis"><caption><b>Team Assigned</b></caption>';
        if(team_list.length>0){
            for(var i=0;i<team_list.length;i++){
                message+='<tr><td class="team" data-id="'+team_list[i][0]+'">'+team_list[i][1]+'</td></tr>';
            }
        }
        else{
            message+='<tr><td>No Team Assigned</td></tr>';
        }
        message+='</table>';
        $('#team_list').html(message);
        var message='';
        message+='<table class="two-column-emphasis"><caption><b>Team Left</b></caption>';
        if(global_list.length>0){
            for(var i=0;i<global_list.length;i++){
                message+='<tr><td>'+global_list[i][1]+'</td>';
                message+='<td class="global_team"data-id="'+global_list[i][0]+'"><img src="/site_media/plus1.png" style="cursor: pointer" width="20px" height="20px"/></td></tr>';
            }
        }
        else{
            message+='<tr><td>No Team Left</td></tr>';
        }
        message+='</table>';
        $('#global_team_list').html(message);
        $('.global_team').on('click',function(){
            var team_id=$(this).attr('data-id');
            var team_text=$(this).prev().text().trim();
            var project_name=$('#project_identity option:selected').text().trim();
            var message="Do you want Team <b>'"+team_text+"'</b> to  project <b>'"+project_name+"'</b>??";
            alertify.confirm(message,function(e){
                if(e){
                    $.get('link_team',{'team_name':team_text.trim(),'team_id':team_id,project_id:project_id},function(data){
                        if(data['message']){
                            alertify.success(data['log_message'],1500);
                            GetAllTeam();
                        }
                        else{
                            alertify.error(data['log_message'],1500);
                            GetAllTeam();
                        }
                    });
                }
                else{
                    alertify.alert().close_all();
                }
            });
        });
        $('.team').on('click',function(){
            $('.team').css({'background-color':'#fff'});
            $(this).css({'background-color':'#ccc'});
            $('.team').removeClass('selected');
            $(this).addClass('selected');
            getAlldata(project_id,$(this).text().trim(),$(this).attr('data-id'));
        });
    });
}

function getAlldata(project_id,team_name,team_id){
    $.get('GetTeamInfo',{'team':team_name.trim(),'team_id':team_id.trim(),'project_id':project_id.trim()},function(data){
        var message='';
        var team_name=data['teamname'];
        var user_list=data['data'];
        message+='<table class="two-column-emphasis"><caption><b>'+team_name+'</b></caption>';
        for(var i=0;i<user_list.length;i++){
            var user_type=user_list[i][0];
            var users=user_list[i][1];
            message+='<tr><td style="vertical-align: 0%;"><b>'+user_type+'</b></td>';
            if(users.length>0){
                message+='<td><table>';
                for(var j=0;j<users.length;j++){
                    message+='<tr><td>'+users[j][1]+'</td></tr>';
                }
                message+='</table>';
                message+='</td>';
            }
            else{
                message+='<td>No '+user_type+' in this team</td>';
            }
            message+='</tr>';
        }
        message+='</table>';
        $('#main_body').html(message);
        var message='';
        message+='<input type="button" id="rename_button" class="m-btn blue" value="Rename"/> ';
        message+='<input type="button" id="edit_button" class="m-btn purple" value="Add/Remove"/> ';
        message+='<input type="button" class="m-btn red" value="Delete"/> ';
        $('#control_panel').html(message);
        $('#rename_button').on('click',function(){
            var team_name=$('.team.selected').text().trim();
            var message='';
            message+='<table class="two-column-emphasis"><caption><b>Rename Team</b></caption>';
            message+='<tr><td><b>Old Name:</b></td><td>'+team_name+'</td></tr>';
            message+='<tr><td><b>New Name:</b></td><td><input type="text" id="new_team" class="textbox" style="width: 100%;"/> </td></tr>';
            message+='</table>';
            alertify.confirm(message,function(){
                var new_name=$('#new_team').val().trim();
                if(new_name!=''){
                    $.get('UpdateTeamName',{'new_name':new_name,'old_name':team_name,project_id:project_id},function(data){
                        if(data['message']){
                            alertify.success(data['log_message'],1500);
                            GetAllTeam();
                        }else{
                            alertify.error(data['log_message'],1500);
                            GetAllTeam();
                        }
                    });
                }
                else{
                    alertify.error('Team Name empty',1500);
                    return false;
                }

            });
        });

        $('#edit_button').on('click',function(){
            var team_name=$('.team.selected').text().trim();
            window.location='/Home/'+project_id+'/Team/'+team_name.replace(/ /g,'_')+'/';
        });
        $('#delete_button').on('click',function(){

        });
    });
}
*/

$(document).ready(function(){
    $('body').css({'font-size':'100%;'});
});
