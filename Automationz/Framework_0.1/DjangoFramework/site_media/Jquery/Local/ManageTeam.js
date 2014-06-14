/**
 * Created by lent400 on 5/27/14.
 */
$(document).ready(function(){
    GetAllTeam();
    CreateButtonInit();
    Other();
});
function Other(){
    $('#searchbox').on('input',function(){
        $.get("GetAllTeam",{term:$(this).val().trim()},function(data){
            $('#team').html(initTeamName(data));
            MainButtonPreparation();
        });

    });
}
function MainButtonPreparation(){
    $('.team').click(function(){
        var team_name=$(this).attr('id').replace(/_/g,' ').trim();
        $.get('GetTeamInfo',{'team':team_name.trim()},function(data){
            //alert(data['message']);
            if(data['message'].indexOf('No')!=0){
                $('#msg').slideUp('slow');
                $('#RunTestResultTable').html(initiateInfoDiv(data['data'],data['teamname']));
                $('#RunTestResultTable').slideDown('slow');
            };
        });
    });
    OtherButtonPreparation();
}
function OtherButtonPreparation(){
    $('#createNew').click(function(event){
        event.preventDefault();
        $.get('GetTesterManager',{},function(data){
            $('#type').css({'display':'none'});
            $('#name').css({'display':'none'});
            $('#RunTestResultTable').html("");
            $('#RunTestResultTable').html(initCreateDiv(data));
            $('#RunTestResultTable').css({'display':'block'});
            ButtonPreparation();
        });
    });
    $('#edit').click(function(event){
        event.preventDefault();
        var team_name=$('#name').text().trim().replace(/ /g,'_').trim();
        if(team_name!=""){
            window.location='/Home/Team/'+team_name.trim()+'/';
        }

    });
    $('#delete').click(function(event){
       event.preventDefault();
        var team_name=$('#name').text();
        if(team_name!=""){
            alertify.confirm("Are you sure you want to add the selected to the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Delete_Team',{
                        'team_name':team_name.trim()
                    },function(data){
                        if(data.indexOf('Failed')!=0){
                            window.location=('/Home/ManageTeam/');
                        }
                        else{
                            window.location.reload(true);
                        }
                    });
                }
            });
        }
    });
    $('#rename').click(function(event){
        event.preventDefault();
        var temp='Team';
        var name=$('#name').text().trim();
        $('#inner_div').html(renameDivInit(temp,name));
        $("#inner_div").dialog({
            /*buttons : {
             "OK" : function() {
             $(this).dialog("close");
             }
             },
             */
            show : {
                effect : 'drop',
                direction : "up"
            },
            modal : true,
            width : 400,
            height : 200,
            title:"Rename: "+temp.toLocaleUpperCase()
        });
        $('#create').click(function(event){
            event.preventDefault();
            var new_name=$('#inputText').val().trim();
            var old_name=name.trim();
            //alert(temp.toLocaleUpperCase()+new_name);
            $.get("UpdateTeamName",{type:temp.toLocaleUpperCase(),new_name:new_name.trim(),old_name:old_name.trim()},function(data){
                if(data.indexOf('Failed')!=0){
                    window.location=('/Home/ManageTeam/');
                }
                else{
                    window.location.reload(true);
                }
            });
        });
    });
}
function initiateInfoDiv(data,teamname){

    $('#type').html('<b class="Text" style="color: #4183c4">Team:</b>');
    $('#name').html('<b class="Text">'+teamname+'</b> ');
    $('#infoDiv').slideDown('slow');
    $('#new_team').slideUp('slow');
    var message="";
    message+='<table style="margin-left: 3%;">';
    for(var i=0;i<data.length;i++){
        if(data[i][0]=='leader'){
            var type_tag="Managers";
        }
        if(data[i][0]=='tester'){
            var type_tag="Tester";
        }
        message+='<tr>';
        if(data[i][1].length==0){
            message+=('<td align="left" colspan="2"><b class="Text" style="color: #4183c4">No'+type_tag+' in this team</b></td>');
        }
        else{
            message+='<td width="25%" align="left" class="Text" style="vertical-align: 0%;color: #4183c4"><b>'+type_tag+':</b></td>';
            message+='<td><table width="100%"   style="margin-top: -2%;">';
            for(var j=0;j<data[i][1].length;j++){
                message+='<tr><td width="65%" data-id="'+data[i][1][j].replace(/ /g,'_')+'"><b class="Text">'+data[i][1][j].trim()+'</b></td>';
                //message+='<td align="center" width="10%"><i class="fa fa-minus-square fa-fw fa-lg remove" style="cursor: pointer;"></i></td></tr>';
            }
            message+='</table></td>';

        }
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function GetAllTeam(){
    $.get("GetAllTeam",{term:''},function(data){
        $('#team').html(initTeamName(data));
        MainButtonPreparation();
    });

};
function initTeamName(team){
    var message="";
    message+='<table width="100%">';
    message+='<tr style="margin-right: 2%;"><td align="center" style="width: 22%; border-right: 2px solid #ccc;"><b class="Text">Teams</b></td>';
    message+='<td><table>'
    for(var i=0;i<team.length;i++){
        message+='<tr><td>&nbsp;</td><td class="team" style="cursor: pointer;" id="'+team[i].replace(/ /g,'_').trim()+'">'+team[i].trim()+'</td></tr>'
    }
    message+='</table></td></tr>';
    message+='</table>';
    return message;
}
function CreateButtonInit(){
  $('#new_team').click(function(event){
      event.preventDefault();
      $.get('GetTesterManager',{},function(data){
          $('#RunTestResultTable').html(initCreateDiv(data));
          $('#RunTestResultTable').css({'display':'block'});
          ButtonPreparation();
      });
  });
};
function ButtonPreparation(){
    $('#submit_team').click(function(){
        var manager=[];
        var tester=[];
        var team_name=$('#team_name').val().trim();
        $('input[class="manager"]:checked').each(function(){
            manager.push($(this).val().replace(/_/g,' ').trim());
        });
        $('input[class="tester"]:checked').each(function(){
            tester.push($(this).val().replace(/_/g,' ').trim());
        });
        if(manager.length==0 || tester.length==0 || team_name.trim()==""){
            alertify.log("Some of the fields are empty","",0);
        }
        $.get("Create_Team",{'manager':manager.join("|"),'tester':tester.join("|"),'team_name':team_name},function(data){
            if(data.indexOf('Failed')!=0){
                window.location=('/Home/Team/'+team_name.trim().replace(/ /g,'_').trim()+'/');
            }
            else{
                window.location.reload(true);
            }
        });
    });
}
function initCreateDiv(data){
    $('#msg').css({'display':'none'});

    var message="";
    if(data[0][0]=='assigned_tester'){
        var tester=data[0][1];
    }
    if(data[1][0]=='manager'){
        var manager=data[1][1];
    }
    message+='<table align="center" width="100%"style="margin-top:2%;">';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Team Name:</b></td>';
    message+='<td align="left"><input type="text" class="textbox" placeholder="Team Name Here" id="team_name"/></td>';
    message+='</tr>';
    message+='<tr><td>&nbsp;</td><td>&nbsp;</td></tr>'
    message+='<tr>';
    message+='<td align="right" style="vertical-align: 0%;"><b class="Text">Select Managers:</b></td>';
    message+='<td align="left">';
    message+='<table>';
    for(var i=0;i<manager.length;i++){
        message+='<tr><td><input type="checkbox" class="manager" value="'+manager[i].replace(/ /g,'_')+'"/>'+manager[i]+'</td></tr>';
    }
    message+='</table>';
    message+='</td>';
    message+='</tr>';
    message+='<tr><td>&nbsp;</td><td>&nbsp;</td></tr>'
    message+='<tr>';
    message+='<td align="right" style="vertical-align: 0%;"><b class="Text">Select Tester:</b></td>';
    message+='<td align="left">';
    message+='<table>';
    for(var i=0;i<tester.length;i++){
        message+='<tr><td><input type="checkbox" class="tester" value="'+tester[i].replace(/ /g,'_')+'"/>'+tester[i]+'</td></tr>';
    }
    message+='</table>';
    message+='</td>';
    message+='</tr>';
    message+='<tr><td>&nbsp;</td><td align="center"><input class="createnew" value="Create Team" type="button" id="submit_team"/></td></tr>';
    message+='</table>';
    return message;
};
function renameDivInit(temp,name){
    var message="";
    message+='<div align="center">';
    message+='<table align="center">'+
        '<tr><td>Old '+temp.toLocaleUpperCase()+' Name:</td><td><span>'+name.trim()+'</span></td></tr>' +
        '<tr><td>Enter New '+temp.toLocaleUpperCase()+' Name:</td><td><input id="inputText" type="text" class="Text"/></td></tr>' +
        '<tr><td>&nbsp;</td><td colspan="1" align="right"><input style="margin-right: 0%;" type="button" class="createnew" id="create" value="Rename '+temp.toLocaleUpperCase()+'" /></td></tr></table>';
    message+='</div>';
    return message;
}