var dependency_list=[];
var global_version_list=[];
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    ManageMilestone(project_id,team_id);
});

function ManageMilestone(project_id,team_id){
    $.get('GetOS',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        dependency_list=data['dependency_list'];
        global_version_list=data['version_list'];
        populate_manual_div(dependency_list,global_version_list);
    });
}

function populate_manual_div(dependency_list,global_version_list){
    var message="";
    message+='<tr>';
    message+='<td align="right"><b class="Text">Machine Name:</b></td>';
    message+='<td align="left"><input class="textbox" id="machine_name"  placeholder="Machine Name Here.."></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Machine IP:</b></td>';
    message+='<td align="left"><input class="textbox" id="machine_ip"  placeholder="Machine IP Here.."></td>';
    message+='</tr>';
    for(var i=0;i<dependency_list.length;i++){
        message+='<tr>';
        message+='<td align="right"><b class="Text">'+dependency_list[i][0]+':</b></td>';
        message+='<td align="left"><table width="100%"><tr><td width="10%">';
        message+='<select id="'+dependency_list[i][0]+'_name">';
        message+='<option value="">Name</option>';
        var option_list=dependency_list[i][1];
        for(var j=0;j<option_list.length;j++){
            message+=('<option value="'+option_list[j][0]+'" >'+option_list[j][0]+'</option>');
        }
        message+='</select></td>';
        message+='<td width="10%"><select id="'+dependency_list[i][0]+'_bit" style="display:none;"></select></td><td width="33%"><select id="'+dependency_list[i][0]+'_version" style="display:none;"></select></td></tr></table></td>';
        message+='</tr>';
    }
    message+='<tr>';
    message+='<td align="right"><b class="Text">Version:</b></td>';
    message+='<td align="left"><table width="100%"><tr>';
    message+='<td width="19%"><select id="branch_name"><option value="">Branch</option>';
    for(var i=0;i<global_version_list.length;i++){
        message+='<option value="'+global_version_list[i][0]+'">'+global_version_list[i][0]+'</option> ';
    }
    message+='</select></td><td><select id="branch_version" style="display: none;"></select></td>'
    message+='</tr></table></td>'
    message+='</tr>';
    message+='<tr><td align="right">&nbsp;</td><td align="left"><input value="create" class="button primary"/></td></tr>';
    $('#manual_machine_body').html(message);
    for(var i=0;i<dependency_list.length;i++){
        $('#'+dependency_list[i][0]+'_name').on('change',function(){
            if($(this).val()!=""){
                generate_name(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
        });
        $('#'+dependency_list[i][0]+'_bit').on('change',function(){
            if($(this).val()!=""){
                generate_version(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
        });
    }
    $('#branch_name').on('change',function(){
        if($(this).val()!=""){
            for(var i=0;i<global_version_list.length;i++){
                if(global_version_list[i][0]==$(this).val()){
                    var version=global_version_list[i][1];
                    var message="";
                    message+='<option value="">Version</option>';
                    for(var j=0;j<version.length;j++){
                        message+='<option value="'+version[j]+'">'+version[j]+'</option>';
                    }
                    $('#branch_version').html(message);
                    $('#branch_version').css({'display':'block'});
                }
            }
        }
    });
}
function generate_name(dependency_list,name,type){
    for (var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            for(var j=0;j<dependency_list[i][1].length;j++){
                if(dependency_list[i][1][j][0]==name){
                    var version_list=dependency_list[i][1][j][1];
                    var message="";
                    message+='<option value="">Bit</option>';
                    for(var k=0;k<version_list.length;k++){
                        message+='<option value="'+version_list[k][0]+'">'+version_list[k][0]+' Bit</option>';
                    }
                    $('#'+type+'_bit').html(message);
                    $('#'+type+'_bit').css({'display':'block'});
                    break;

                }
            }
        }
    }
}

function generate_version(dependency_list,name,type){
    for(var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            var names=dependency_list[i][1];
            for(var j=0;j<names.length;j++){
                if(names[j][0]==$('#'+type+'_name option:selected').val()){
                    var bit_list=names[j][1];
                    for(var k=0;k<bit_list.length;k++){
                        if(bit_list[k][0]==name){
                            var version_list=bit_list[k][1];
                            console.log(version_list);
                            var message="";
                            message+='<option value="">Version</option>';
                            for(var l=0;l<version_list.length;l++){
                                message+='<option value="'+version_list[l]+'">'+version_list[l]+'</option>';
                            }
                            $('#'+type+'_version').html(message);
                            $('#'+type+'_version').css({'display':'block'});
                            break;
                        }
                    }
                }
            }
        }
    }
}