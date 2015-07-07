var dependency_list=[];
var global_version_list=[];
var dependency_classes=[];
var test_cases="";
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    var location_name=window.location.pathname;
    location_name=location_name.split("/")[3].replace(/_/g,' ');
    //alert(location_name);
    if(location_name=='create new machine') {
        $('#create').html('Create');
        location_name = "";
        $.get('GetOS', {
            project_id: project_id,
            team_id: team_id
        }, function (data) {
            dependency_list = data['dependency_list'];
            global_version_list = data['version_list'];
            branch_list = data['branch_list'];
            populate_manual_div(dependency_list, branch_list, global_version_list, project_id, team_id);
        });
    }
    else{
        ManageMilestone(project_id,team_id,location_name);
    }
    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val().trim());
        window.location.reload(true);
    });
    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val().trim());
        window.location.reload(true);
    });
});
function ManageMilestone(project_id,team_id,location_name){
    $.get('GetOS',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        dependency_list=data['dependency_list'];
        global_version_list=data['version_list'];
        branch_list=data['branch_list'];
        populate_manual_div(dependency_list,branch_list,global_version_list,project_id,team_id);
        $.get("CheckMachine",{name:location_name},function(data){
            $('#machine_name').val(location_name);
            if(data.length>0){
                var machine_ip=data[0][0];
                var branch_version=data[0][1];
                var dependency=data[0][2];
                $('#machine_ip').val(machine_ip);
                branch_version=branch_version.split(':');
                var branch=branch_version[0].trim();
                var version=branch_version[1].trim();
                $('#branch_name').val(branch);
                $('#branch_name').trigger('change');
                $('#branch_version').val(version);
                for(var i=0;i<dependency.length;i++){
                    var list=dependency[i].split('|');
                    $('#'+list[0]+'_name').val(list[1]);
                    $('#'+list[0]+'_name').trigger('change');
                    $('#'+list[0]+'_bit').val(list[2]);
                    $('#'+list[0]+'_bit').trigger('change');
                    $('#'+list[0]+'_version').val(list[3]);
                }
            }

        });
    });
}

function populate_manual_div(dependency_list,branch_list,global_version_list,project_id,team_id){
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
    for(var i=0;i<branch_list.length;i++){
        message+='<option value="'+branch_list[i][0]+'">'+branch_list[i][0]+'</option> ';
    }
    /*for(var i=0;i<global_version_list.length;i++){
        message+='<option value="'+global_version_list[i][0]+'">'+global_version_list[i][0]+'</option> ';
    }*/
    message+='</select></td><td><select id="branch_version" style="display: none;"></select></td>'
    message+='</tr></table></td>'
    message+='</tr>';
    message+='<tr><td align="right">&nbsp;</td><td align="left"><input value="Edit" type="button" class="button primary" id="create_manual_machine"/></td></tr>';
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
    $('#create_manual_machine').on('click',function(){
        var machine_name=$('#machine_name').val().trim();
        if(machine_name==''){
            alertify.error('Machine name can not be empty');
            return false;
        }
        var machine_ip=$('#machine_ip').val().trim();
        if(machine_ip==''){
            alertify.error('Machine ip can not be empty');
            return false;
        }
        var dependency=[];
        for(var i=0;i<dependency_list.length;i++){
            var temp=[];
            var name=dependency_list[i][0];
            temp.push(name);
            if($('#'+name+'_name option:selected').val().trim()==""){
                alertify.set({ delay: 300000 });
                alertify.error(name+' name is empty');
                return false;
            }
            else{
                temp.push($('#'+name+'_name option:selected').val().trim());
            }
            if($('#'+name+'_bit option:selected').val()==null){
                temp.push('Nil');
            }
            else if($('#'+name+'_bit option:selected').val().trim()==""){
                alertify.set({ delay: 300000 });
                alertify.error(name+' bit is empty');
                return false;
            }
            else{
                temp.push($('#'+name+'_bit option:selected').val().trim());
            }
            if($('#'+name+'_bit option:selected').val()==null){
                temp.push('Nil');
            }
            else if($('#'+name+'_version option:selected').val().trim()==""){
                alertify.set({ delay: 300000 });
                alertify.error(name+' version is empty');
                return false;
            }
            else{
                temp.push($('#'+name+'_version option:selected').val().trim());
            }
            dependency.push(temp.join('|'));
        }
        if($('#branch_name').val().trim()==""){
            alertify.set({ delay: 300000 });
            alertify.error('Branch name is empty');
        }
        var branch_version = "";
        if($('#branch_version').is(":visible")){
            if($('#branch_version').val().trim()==""){
                alertify.set({ delay: 300000 });
                alertify.error('Branch Version is empty');
            }
            branch_version=$('#branch_version').val().trim();
        }
        var branch_name=$('#branch_name').val().trim();
        //var branch_version=$('#branch_version').val().trim();

        $.get('AddManualTestMachine',{
            'machine_name':machine_name,
            'machine_ip':machine_ip,
            'dependency':dependency.join('#'),
            'branch_name':branch_name,
            'branch_version':branch_version,
            'project_id':project_id,
            'team_id':team_id
        },function(data){
            if(data['message']){
                alertify.set({ delay: 300000 });
                alertify.success(data['log_message'])
                window.location='/Home/Machine/'+machine_name.replace(/ /g, '_')+'/';
            }
            else{
                alertify.set({ delay: 300000 });
                alertify.error(data['log_message']);
                window.location.reload(true);
            }
        });
    });
    /*
    $("#machine_name").autocomplete({
        source:function(request,response){
            $.ajax({
                url:"Auto_MachineName",
                dataType:"json",
                data:{term:request.term,'project_id':project_id,'team_id':team_id},
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value = ui.item[0];
            console.log(value);
            if(value!=""){
                $("#machine_name").val(value);
                $.get("CheckMachine",{name:value},function(data){
                    var machine_ip=data[0][0];
                    var branch_version=data[0][1];
                    var dependency=data[0][2];
                    $('#machine_ip').val(machine_ip);
                    branch_version=branch_version.split(':');
                    var branch=branch_version[0].trim();
                    var version=branch_version[1].trim();
                    $('#branch_name').val(branch);
                    $('#branch_name').trigger('change');
                    $('#branch_version').val(version);
                    for(var i=0;i<dependency.length;i++){
                        var list=dependency[i].split('|');
                        $('#'+list[0]+'_name').val(list[1]);
                        $('#'+list[0]+'_name').trigger('change');
                        $('#'+list[0]+'_bit').val(list[2]);
                        $('#'+list[0]+'_bit').trigger('change');
                        $('#'+list[0]+'_version').val(list[3]);
                    }
                });
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };
    */
}
function generate_name(dependency_list,name,type){
    for (var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            for(var j=0;j<dependency_list[i][1].length;j++){
                if(dependency_list[i][1][j][0]==name){
                    var version_list=dependency_list[i][1][j][1];
                    if (version_list.length>0){
                        var message="";
                        message+='<option value="">Bit</option>';
                        for(var k=0;k<version_list.length;k++){
                            message+='<option value="'+version_list[k][0]+'">'+version_list[k][0]+' Bit</option>';
                        }
                        $('#'+type+'_bit').html(message);
                        $('#'+type+'_bit').css({'display':'block'});
                        break;
                    }
                    else{
                        $('#'+type+'_bit').empty();
                        $('#'+type+'_version').empty();
                        $('#'+type+'_bit').css({'display':'none'});
                        $('#'+type+'_version').css({'display':'none'});

                    }
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