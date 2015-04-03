var user_id=$.session.get('user_id')
$(document).ready(function(){
    GetAllTeam(user_id,project_id);
});
function GetAllTeam(user_id,project_id){
    $.get('GetAllTeam',{
        'project_id':project_id,
        'user_id':user_id
    },function(data){
        var owner=data['owner'];
        var team_list=data['team_list'];
        var global_team_list=data['global_team_list'];
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b>Assigned Teams</b></caption>';
        if(team_list.length>0){
            for(var i=0;i<team_list.length;i++){
                message+='<tr><td data-id="'+team_list[i][0]+'" class="team" style="cursor: pointer;">'+team_list[i][1]+'</td></tr>'
            }
        }
        else{
            message+='<tr><td><b>No Team is Present</b></td></tr>';
        }
        message+='</table>';
        if(owner){
            message+='<table class="two-column-emphasis">';
            message+='<caption><b>Global Teams</b></caption>';
            if(global_team_list.length>0){
                for(var i=0;i<global_team_list.length;i++){
                    message+='<tr><td>'+global_team_list[i][1]+'</td><td data-id="'+global_team_list[i][0]+'" class="global_team"><img src="/site_media/plus1.png" style="cursor: pointer" width="20px" height="20px"/></td></tr>';
                }
            }
            else{
                message+='<tr><td><b>No Global Team is present</b></td></tr>';
            }
            message+='</table>';
            message+='<table width="100%">';
            message+='<tr>';
            message+='<td><input type="button" value="Create Team" class="m-btn green" id="create_button"/></td>';
            message+='</tr>';
            message+='</table>';
        }
        $('#table_div').html(message);
        if(owner){
            var project_name=data['project_name'];
            $('.global_team').on('click',function(){
                var team_id=$(this).attr('data-id');
                var team_text=$(this).prev().text().trim();
                var message="Do you want Team <b>'"+team_text+"'</b> to  project <b>'"+project_name+"'</b>??";
                alertify.confirm(message,function(e){
                    if(e){
                        $.get('link_team',{'team_name':team_text.trim(),'team_id':team_id,project_id:project_id},function(data){
                            if(data['message']){
                                alertify.success(data['log_message'],1500);
                                window.location.reload(true);
                            }
                            else{
                                alertify.error(data['log_message'],1500);
                                window.location.reload(true);
                            }
                        });
                    }
                    else{
                        alertify.alert().close_all();
                    }
                });
            });
            $('#create_button').on('click',function(){
                $('.team').css({'background-color':'#fff'});
                $('#mainbody').empty();
                var message='';
                message+='<table width="100%" class="two-column-emphasis"><caption><b>Team Details</b></caption>';
                message+='<tr><td align="right"><b>Team Name:</b></td><td align="left"><input class="textbox" id="team_name" placeholder="Team name here"/> </td><td>&nbsp;</td></tr>';
                message+='<tr><td align="right" style="vertical-align: 0%"><b>Manager:</b></td><td  style="vertical-align: 0%" align="left"><input type="hidden"  placeholder="Search Managers" id="search_manager"/> </td><td><table id="manager"></table></td></tr>';
                message+='<tr><td align="right" style="vertical-align: 0%"><b>Tester:</b></td><td  style="vertical-align: 0%" align="left"><input type="hidden" placeholder="Search Testers" id="search_tester"/> </td><td><table id="tester"></table></td></tr>';
                message+='<tr><td align="right" style="vertical-align: 0%">&nbsp;</td><td  style="vertical-align: 0%" align="left"><input class="m-btn green" value="Submit" id="submit_team" type="button"/> </td><td>&nbsp;</td></tr>';
                message+='</table>';
                $('#mainbody').html(message);
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
                                'all':'all',
                                'project_id':project_id
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
                                'all':'all',
                                'project_id':project_id
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
            $('.team').on('click',function(){
                $('.team').css({'background-color':'#fff'});
                $(this).css({'background-color':'#ccc'});
                var team_id=$(this).attr('data-id');
                var project_id=data['project_id'];
                var team_name=$(this).text().trim();
                $.get('GetTeamInfo',{'team':team_name.trim(),'team_id':team_id.trim(),'project_id':project_id.trim()},function(data){
                    var team_name=data['teamname'];
                    var message=data['message'];
                    var team_list=data['data'];
                    var message='';
                    message+='<table width="100%" class="two-column-emphasis"><caption><b>Team: '+team_name+'</b></caption>';
                    for(var i=0;i<team_list.length;i++){
                        message+='<tr><td align="right" style="vertical-align: 0%;">'+team_list[i][0]+': </td>';
                        if(team_list[i][1].length>0){
                            message+='<td align="left"><table>';
                            for(var j=0;j<team_list[i][1].length;j++){
                                message+='<tr><td data-id="'+team_list[i][1][j][0]+'">'+team_list[i][1][j][1]+'</td></tr>';
                            }
                            message+='</table></td>';
                        }
                        else{
                            message+='<td><b>No '+team_list[i][0].trim()+' is found</b></td>';
                        }
                        message+='</tr>';
                    }
                    message+='<tr><td colspan="2">';
                    message+='<input type="button" value="Rename" id="rename_button" class="m-btn blue"/>';
                    message+='<input type="button" value="Edit" id="edit_button" class="m-btn green"/>';
                    message+='<input type="button" value="Delete" class="m-btn red"/>';
                    message+='</td></tr>';

                    message+='</table>';
                    $('#mainbody').html(message);

                    $('#rename_button').on('click',function(){
                        //var team_name=$(this).text().trim();
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
                                        window.location.reload(true);
                                    }else{
                                        alertify.error(data['log_message'],1500);
                                        window.location.reload(true);
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
                        //var team_name=$(this).text().trim();
                        window.location='/Home/'+project_id+'/Team/'+team_name.replace(/ /g,'_')+'/';
                    });
                    $('#delete_button').on('click',function(){

                    });


                });
            });
        }
        else{
            $('.team').on('click',function(){
                var team_id=$(this).attr('data-id');
                var project_id=data['project_id'];
                var team_name=$(this).text().trim();
                $.get('GetTeamInfo',{'team':team_name.trim(),'team_id':team_id.trim(),'project_id':project_id.trim()},function(data){
                    var team_name=data['teamname'];
                    var message=data['message'];
                    var team_list=data['data'];
                    var message='';
                    message+='<table width="100%" class="two-column-emphasis"><caption><b>Team: '+team_name+'</b></caption>';
                    for(var i=0;i<team_list.length;i++){
                        message+='<tr><td align="right" style="vertical-align: 0%;">'+team_list[i][0]+': </td>';
                        if(team_list[i][1].length>0){
                            message+='<td align="left"><table>';
                            for(var j=0;j<team_list[i][1].length;j++){
                                message+='<tr><td data-id="'+team_list[i][1][j][0]+'">'+team_list[i][1][j][1]+'</td></tr>';
                            }
                            message+='</table></td>';
                        }
                        else{
                            message+='<td><b>No '+team_list[i][0].trim()+' is found</b></td>';
                        }
                        message+='</tr>';
                    }
                    $('#mainbody').html(message);
                });
            });
        }
    });
}