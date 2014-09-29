/**
 * Created by Admin on 9/9/14.
 */
var time_out=1500;
var name_field_error="Name field can't be empty";
var dep_value="";
var dep_name="";
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_all_data(project_id,team_id);
    DependencyTabButtons(project_id,team_id);

});
function get_all_data(project_id,team_id){
    $.get('get_all_data_dependency_page',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        populate_div("dependency_body",data['dependency_list'],project_id,team_id,"dependency");
        populate_div("unused_dependency",data['unused_dependency_list'],"","","add_dependency");
    });
}
function populate_div(div_name,array_list,project_id,team_id,type){
    var message="";
    message+='<tr>';
    if(project_id!="" && team_id!=""){
        message+='<td align="center">'+project_id+'<br>'+team_id+'</td>';
    }
    else{
        message+='<td align="center"><b>Global</b></td>';
    }
    if(array_list.length>0){
        message+='<td style="border-left: 2px solid #CCCCCC">';
        message+='<table id="'+type+'_list" class="one-column-emphasis">';
        for(var i=0;i<array_list.length;i++){
            message+='<tr><td align="center" class="'+type+'" value="'+array_list[i][0]+'" style="cursor:pointer;">'+array_list[i][1]+'</td></tr>';
        }
        message+='</table>';
        message+='</td>';
        message+='</tr>';
    }
    else{
        message+='<td style="border-left: 2px solid #CCCCCC" align="center"><b>No '+type+' Found</b></td>';
    }
    $('#'+div_name).html(message);
    if(type=="dependency"){
        $('#name_dependency_tab').html("");
        $('.'+type).on('click',function(){
            dep_value=$(this).attr('value');
            dep_name=$(this).text().trim();
            $.get('get_all_name_under_dependency',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
            },function(data){
                populate_second_div("name_dependency_tab",data['dependency_list'],"dependency_name",project_id,team_id);
            });
        });
    }
    $('.'+type).bind("contextmenu",function(eventy){
        eventy.preventDefault();
        $(this).trigger('click');
        $(".custom-menu-"+type).toggle(100).
            // In the right position (the mouse)
            css({
                top: event.pageY + "px",
                left: event.pageX + "px"
            });
        if( type=="add_dependency" || type=="dependency"){
            dep_name=$(this).text().trim();
            dep_value=$(this).attr('value');
        }
    });
    $(document).bind("mousedown", function (e) {
        console.log(!$(e.target).parents(".custom-menu").length > 0);
        if (!$(e.target).parents(".custom-menu").length > 0)
            $(".custom-menu").hide(100);
    });
    allow_binding(type,project_id,team_id);

}
function populate_second_div(div_name,array_list,type,project_id,team_id){
    var message="";
    if(array_list.length>0){
        for(var i=0;i<array_list.length;i++){
            message+='<tr><td value="'+array_list[i][0]+'" class="'+type+'" style="cursor:pointer" >'+array_list[i][1]+'</td></tr>';
        }
    }
    else{
        message+='<td><b>No Name Found</b></td>'
    }
    $('#'+div_name).html(message);
    $('.'+type).on('click',function(){

    });
    $('.'+type).bind("contextmenu",function(eventy){
        eventy.preventDefault();
        $(this).trigger('click');
        $(".custom-menu-"+type).toggle(100).
            // In the right position (the mouse)
            css({
                top: event.pageY + "px",
                left: event.pageX + "px"
            });
        dep_name=$(this).text().trim();
        dep_value=$(this).attr('value');
    });
    $('.custom-menu-dependency_name').click(function(){
        $('.custom-menu').hide();
        alert($(this));
    });
}
function allow_binding(type,project_id,team_id){
    if(type=="dependency"){
        $(".custom-menu-dependency li").click(function(){
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "create":create_new_name_under_version(dep_name,project_id,team_id,dep_value); break;
                case "rename":alert('rename'); break;
                case "usage":alert('usage'); break;
                case "unlink":alert("unlink"); break;
            }
        });
    }
    if(type=="add_dependency"){
        $(".custom-menu-add_dependency li").click(function(){
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "rename":alert('rename'); break;
                case "usage":alert('usage'); break;
                case "delete":alert("delete"); break;
            }
        });
    }
}

function create_new_name_under_version(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td colspan="2" align="center"><b>Create New Name</b></td></tr>';
    message+='<tr><td align="right"><b>'+dep_name+' Name:</b></td><td align="left"><input class="textbox" id="new_name" style="width: 100%"/></td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var new_name=$('#new_name').val().trim();
            if(new_name!=""){
                $.get('add_new_name_dependency',{
                    new_name:new_name.trim(),
                    new_value:dep_value
                },function(data){
                    if(data['message']==true){
                        alertify.success(data['log_message'],time_out);
                        get_all_data(project_id,team_id);
                    }
                    else{
                        alertify.error(data['log_message'],time_out);
                    }
                });
            }
            else{
                alertify.error(name_field_error,time_out);
            }

        }
        else{

        }
    });
}

function DependencyTabButtons(project_id,team_id){
    $('#create_new_dependency').on('click',function(event){
        event.preventDefault();
        var message="";
        message+='<table width="100%">';
        message+='<tr><td align="center" colspan="2"><b class="Text">Create New Dependency</b></td></tr>';
        message+='<tr style="margin-top: 2%;"><td align="right"><b class="Text">Dependency:</b></td><td><input class="textbox" style="width: 100%" id="dependency_name"></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var dependency_name=$('#dependency_name').val().trim();
                if(dependency_name!=""){
                    $.get('add_new_dependency',{
                        dependency_name:dependency_name
                    },function(data){
                        if(data['message']==true){
                            alertify.success(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }
                        else{
                            alertify.error(data['log_message'],time_out);
                        }
                    });
                }
                else{
                    alertify.error(name_field_error,time_out);
                }

                e.stopPropagation();
            }
            else{

            }
        })
    });
}