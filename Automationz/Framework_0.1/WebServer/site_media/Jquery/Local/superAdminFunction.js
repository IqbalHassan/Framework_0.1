/**
 * Created by 09 on 12/3/14.
 */
$(document).ready(function(){
    var url=window.location.pathname;
    url=url.split("/");
    for(var i=0;i<url.length;i++){
        if(url[i]==""){
            if(url.indexOf(url[i])>-1){
                url.splice(url.indexOf(url[i]),1);
            }
        }
    }
    console.log(url[url.length-1]);
    populate_mainBody_div(url[url.length-1]);
});

function populate_mainBody_div(type_tag){
    var message="";
    if(type_tag=='Project'){
        message+='<div align="center" style="font-size: 150%;font-weight: bolder">New Project Creation</div>';
        message+='<table style="margin-top: 2%;"><tr><td><b>Project Name:</b></td><td><input class="textbox" id="project_name" placeholder="project name"/> </td><td>&nbsp;</td></tr>';
        message+='<tr style="vertical-align: 0%;"><td><b>Project Owner:</b></td><td><input class="textbox" id="project_owner" placeholder="project owner"/> </td><td id="owner_list" style="vertical-align: 0%;"></td></tr></table>';
        message+='<div align="center"><input class="primary button" type="button" id="create_project" value="Create Project"/> </div>';
        $('#mainBody').html(message);
        DeleteSearchQueryText();
        $('#project_owner').autocomplete({
            source:function(request,response){
                $.ajax({
                    url:"GetProjectOwner",
                    dataType:"json",
                    data:{
                        term:request.term
                    },
                    success:function(data){
                        response(data);
                    }
                });
            },
            select:function(request,ui){
                var value=ui.item[0];
                if(value!=''){
                    $('#owner_list').append('<tr><td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /><b>'+ui.item[1].trim()+':<span style="display: none;">'+value+'</span>&nbsp;</b></td></tr>');
                }
            }
        }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
            return $( "<li></li>" )
                .data( "ui-autocomplete-item", item )
                .append( "<a><strong>" + item[1] + "</strong> - "+item[2]+"</a>" )
                .appendTo( ul );
        };
        $('#create_project').on('click',function(){
            var project_name=$('#project_name').val().trim();
            if(project_name==""){
                alertify.error('Project Name is empty',1500);
            }
            var project_owner=[];
            $('#owner_list td').each(function(){
               if(project_owner.indexOf($(this).find('span:eq(0)').text().trim())==-1){
                   project_owner.push($(this).find('span:eq(0)').text().trim());
               }
            });
            $.get('Create_New_Project',{
                user_name:'Admin',
                project_name:project_name,
                project_owner:project_owner.join(',')
            },function(data){
                if(data['message']=='Success'){
                    window.location='/Home/superAdmin/';
                }
            })
        });
    }
    if(type_tag=='AddUser'){
        message+='<div align="center" style="font-size: 150%;font-weight: bolder">New User Registration</div>';
        message+='<table style="margin-top: 2%;"><tr><td align="right"><b>Full Name:</b></td><td><input class="textbox" id="full_name" placeholder="Full Name"/></td></tr><tr><td align="right"><b>User Name:</b></td><td><input class="textbox" id="user_name" placeholder="User Name"/></td></tr>';
        message+='<tr><td align="right"><b>Email:</b></td><td><input class="textbox" id="email" placeholder="Email Here"/></td></tr>';
        message+='<tr><td align="right"><b>Designation:</b></td><td><select id="user_level">' +
            '<option value="" selected>Select User Level</option>' +
            '<option value="assigned_tester">Tester</option>' +
            '<option value="manager">Manager</option>' +
            '<option value="admin">Admin</option>' +
            '</select></td></tr>';
        message+='<tr><td align="right"><b>Password:</b></td><td><input class="textbox" id="password" placeholder="Password Here"/></td></tr>';
        message+='<tr><td align="right"><b>Confirm Password:</b></td><td><input class="textbox" id="confirm_password" placeholder="Confirm Password"/></td></tr>';
        message+='</table>';
        message+='<div align="center"><input class="primary button" type="button" id="create_user" value="Register User"/> </div>';
        $('#mainBody').html(message);
        $('#create_user').on('click',function(){
            var user_name=$('#user_name').val().trim();
            var full_name=$('#full_name').val().trim();
            var email=$('#email').val().trim();
            var password=$('#password').val().trim();
            var confirm_password=$('#confirm_password').val().trim();
            var user_level=$('#user_level option:selected').val().trim();
            if(user_name=='' || full_name==''||email==''||user_level==''){
                alertify.error('Check Input Fields',1500)
            }
            if(password!=confirm_password){
                alertify.error('Password don\'t match',1500);
            }
            $.get('Create_New_User',{
                user_name:user_name.trim(),
                email:email.trim(),
                password:password.trim(),
                full_name:full_name.trim(),
                user_level:user_level
            },function(data){
                if(data==true){
                    window.location='/Home/superAdmin/';
                }
            });
        });
    }
    if(type_tag=='ListUser'){
        $.get('ListAllUsers',{},function(data){
            var column=data['column'];
            var user_list=data['user_list'];
            var message="";
            message+='<div align="center" style="font-size: 150%;font-weight: bolder">Current Users</div>';
            message+='<table style="margin-top: 3%;" width="100%;" align="center">';
            message+='<tr>';
            for(var i=0;i<column.length;i++){
                message+=('<th>'+column[i]+'</th>');
            }
            message+='</tr>';
            for(var i=0;i<user_list.length;i++){
                message+='<tr>';
                for(var j=0;j<user_list[i].length;j++){
                    message+=('<td align="center">'+user_list[i][j]+'</td>');
                }
                message+='</tr>';
            }
            message+='</table>';
            $('#mainBody').html(message);
        });
    }
    if(type_tag=='ListProject'){
        $.get('ListProjects',{},function(data){
            var project_list=data['project_detail'];
            var column_list=data['column'];
            var message='';
            message+='<table class="two-column-emphasis"><caption><b style="font-size: 150%">Projects</b></caption>';
            message+='<tr>';
            for(var i=0;i<column_list.length;i++){
                message+='<th><b>'+column_list[i]+'</b></th>';
            }
            message+='</tr>';
            for(var i=0;i<project_list.length;i++){
                message+='<tr>';
                for(var j=0;j<project_list[i].length;j++){
                    message+='<td>'+project_list[i][j]+'</td>';
                }
                message+='</tr>';
            }
            message+='</table>'
            $('#mainBody').html(message);
        });
    }
}
function DeleteSearchQueryText(){
    $('#owner_list td .delete').live('click',function(){
        $(this).parent().parent().remove();
        $(this).remove();
        //PerformSearch(project_id,team_id);
    });
}