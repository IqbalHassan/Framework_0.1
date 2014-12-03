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
}
function DeleteSearchQueryText(){
    $('#owner_list td .delete').live('click',function(){
        $(this).parent().parent().remove();
        $(this).remove();
        //PerformSearch(project_id,team_id);
    });
}