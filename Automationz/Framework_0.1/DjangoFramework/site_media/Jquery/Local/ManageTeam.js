/**
 * Created by lent400 on 5/27/14.
 */
$(document).ready(function(){
    GetAllTeam();
    CreateButtonInit();

});
function MainButtonPreparation(){
    $('.team').click(function(){
        var team_name=$(this).attr('id').replace(/_/g,' ').trim();
        $.get('GetTeamInfo',{'team':team_name.trim()},function(data){
            //alert(data['message']);
            if(data['message'].indexOf('No')!=0){
                $('#msg').slideUp('slow');
                $('#RunTestResultTable').html(initiateInfoDiv(data['data'],data['teamname']));
            };
        });

    });
}
function initiateInfoDiv(data,teamname){
    var message="";
    message+='<table width="100%" align="center">';
    message+='<tbody>';
    for(var i=0;i<data.length;i++){
        if(data[i][0]=='leader'){
            var type_tag="Managers:";
        }
        if(data[i][0]=='tester'){
            var type_tag="Tester:";
        }
        message+='<tr>';
        message+='<td align="right" class="Text" style="vertical-align: 0%;"><b>'+type_tag+'</b></td>';
        message+='<td><table width="100%">';
        for(var j=0;j<data[i][1].length;j++){
            message+='<tr><td>'+data[i][1][j].trim()+'</td></tr>';
        }
        message+='</table></td>';
        message+='</tr>';
    }
    message+='</tbody>';
    message+='</table>';
    return message;
}
function GetAllTeam(){
    $.get("GetAllTeam",{},function(data){
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

        });
    });
}
function initCreateDiv(data){
    var message="";
    if(data[0][0]=='assigned_tester'){
        var tester=data[0][1];
    }
    if(data[1][0]=='manager'){
        var manager=data[1][1];
    }
    message+='<table align="center" width="100%">';
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