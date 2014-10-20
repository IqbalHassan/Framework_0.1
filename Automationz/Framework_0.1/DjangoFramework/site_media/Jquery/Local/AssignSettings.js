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
        populate_div("unused_dependency",data['unused_dependency_list'],project_id,team_id,"add_dependency");
        populate_div("branch_body",data['branch_list'],project_id,team_id,'branch');
        populate_div("unused_branch",data['unused_branch_list'],project_id,team_id,'add_branch');
        populate_div("feature_body",data['feature_list'],project_id,team_id,'feature');
        populate_div("unused_feature",data['unused_feature_list'],project_id,team_id,'add_feature');
    });
}
function populate_div(div_name,array_list,project_id,team_id,type){
    var message="";
    message+='<tr>';
    if(type=='dependency'||type=='branch' ||type=='feature'){
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
        if(type=="add_dependency"|| type=="dependency"){
            message+='<td style="border-left: 2px solid #CCCCCC" align="center"><b>No Dependency Found</b></td>';
        }
        if(type=='branch'||type=='add_branch'){
            message+='<td style="border-left: 2px solid #CCCCCC" align="center"><b>No Branch Found</b></td>';
        }
        if(type=='feature'||type=='add_feature'){
            message+='<td style="border-left: 2px solid #CCCCCC" align="center"><b>No Feature Found</b></td>';
        }
    }
    $('#'+div_name).html(message);
    if(type=="dependency"){
        $('#name_dependency_tab').html("");
        $('#version_dependency_tab').html("");
        $('.'+type).on('click',function(){
            $('.'+type).removeClass('selected');
            $('.add_dependency').css({'background':'none'});
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
            $(this).addClass('selected');
            dep_value=$(this).attr('value');
            dep_name=$(this).text().trim();
            $.get('get_all_name_under_dependency',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
            },function(data){
                $('#version_dependency_tab').html("");
                populate_second_div("name_dependency_tab",data['dependency_list'],data['default_list'],"dependency_name",project_id,team_id);
            });
        });
    }
    if(type=='add_dependency'){
        $('.'+type).on('click',function(){
            $('#name_dependency_tab').html("");
            $('.dependency').css({'background':'none'});
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
        });
    }
    if(type=='add_branch'){
        $('.'+type).on('click',function(){
            $('#version_tab').html("");
            $('.branch').css({'background':'none'});
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
        });
    }
    if(type=='branch'){
        $('#version_tab').html("");
        $('.'+type).on('click',function(){
            $('.'+type).removeClass('selected');
            $('.add_branch').css({'background':'none'});
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
            $(this).addClass('selected');
            dep_value=$(this).attr('value');
            dep_name=$(this).text().trim();
            $.get('get_all_version_under_branch',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
            },function(data){
                $('#version_dependency_tab').html("");
                populate_second_div("version_tab",data['version_list'],data['default_list'],"version_name",project_id,team_id);
            });
        });
    }
    if(type=='add_feature'){
        $('.'+type).on('click',function(){
            $('#name_feature_tab').html("");
            $('.feature').css({'background':'none'});
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
        });
    }
    if(type=='feature'){
        $('#name_feature_tab').html("");
        $('.'+type).on('click',function(){
            $('.'+type).removeClass('selected');
            $('.add_feature').css({'background':'none'});
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
            $(this).addClass('selected');
            dep_value=$(this).attr('value');
            dep_name=$(this).text().trim();
            /*$.get('get_all_version_under_branch',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
            },function(data){
                $('#version_dependency_tab').html("");
                populate_second_div("version_tab",data['version_list'],data['default_list'],"version_name",project_id,team_id);
            });*/
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
        if( type=="add_dependency" || type=="dependency"||type=="add_branch"||type=='branch'||type=='add_feature'||type=='feature'){
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
function populate_second_div(div_name,array_list,default_list,type,project_id,team_id){
    if(type=='dependency_name'){
        if(default_list[0]!=null){
            var default_choices=default_list[0].split(",");
        }
        else{
            var default_choices=[];
        }
        var message="<table width=\"100%\" class='one-column-emphasis'>";

        if(array_list.length>0){
            for(var i=0;i<array_list.length;i++){
                message+='<tr><td align="left" value="'+array_list[i][0]+'" class="'+type+'" style="cursor:pointer" >'+array_list[i][1]+'</td>';
                if(default_choices.indexOf(array_list[i][0].toString())>-1){
                    message+='<td align="right" class="_status" style="cursor: pointer;"><a class="notification-indicator" data-gotokey="n"><span class="mail-status filled"></span></a></td>';
                }
                else{
                    message+='<td align="right" class="_status" style="cursor: pointer;"><a class="notification-indicator" data-gotokey="n"><span class="mail-status unfilled"></span></a></td>';
                }
                message+='</tr>';
            }
        }
        else{
            message+='<td><b>No Name Found</b></td>'
        }
        message+="</table>";

        $('#'+div_name).html(message);
        $('._status').click(function(){
            var tag="";
            var message="";
            message+='<table width="100%">';
            if($(this).find('span:eq(0)').hasClass('unfilled')){
                message+='<tr><td>Are you sure to make <b>\''+$(this).prev().text().trim()+'\'</b> default?</td></tr>';
                tag="make_default"
            }
            else{
                message+='<tr><td>Are you sure to remove <b>\''+$(this).prev().text().trim()+'\'</b> from default?</td></tr>';
                tag="remove_default"
            }
            message+='</table> ';
            var dependency=$(this).prev().attr('value');
            var selected="";
            $('.dependency').each(function(){
                if($(this).hasClass('selected')){
                    selected=$(this).attr('value');
                }
            });
            alertify.confirm(message,function(e){
                if(e){
                    if(selected!=""){
                        $.get('make_default_name',{
                            name:dependency.trim(),
                            dependency:selected.trim(),
                            project_id:project_id,
                            team_id:team_id,
                            tag:tag
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
                }
                else{

                }
            });
        });
        $('.'+type).on('click',function(){
            $('.'+type).css({'background':'none'});
            $(this).css({'background':'#CCCCCC'});
            dep_name=$(this).text().trim();
            dep_value=$(this).attr('value');
            if(type=='dependency_name'){
                $.get('get_all_version_bit',{
                    'value':dep_value
                },function(data){
                    var version_list=data['version_list'];
                    populate_third_div("version_dependency_tab",version_list,"version",project_id,team_id);
                });
            }
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
        $('.custom-menu-'+type+' li').click(function(){
            $('.custom-menu').hide();
            switch($(this).attr("data-action")){
                case "create_name": input_new_version(dep_name,project_id,team_id,dep_value);break;
                case "rename_name": input_rename_name(dep_name,project_id,team_id,dep_value);break;
                case "usage_name": alert("usage_name");break;
            }
        });

    }
    if(type=='version_name'){
        var message="<table width=\"100%\" class='one-column-emphasis'>";

        if(array_list.length>0){
            for(var i=0;i<array_list.length;i++){
                message+='<tr><td align="left" value="'+array_list[i][0]+'" class="'+type+'" style="cursor:pointer" >'+array_list[i][0]+'</td>';

                message+='</tr>';
            }
        }
        else{
            message+='<td><b>No Version Found</b></td>'
        }
        message+="</table>";

        $('#'+div_name).html(message);
    }
}
function input_rename_name(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<thead><tr><td colspan="2"><b>Rename</b></td></tr></thead>';
    message+='<tbody><tr><td align="right"><b>Old Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="old_name" value="'+dep_name+'"/></td></tr>';
    message+='<tr><td align="right"><b>New Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="new_name"/></td></tr></tbody>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var old_name=$('#old_name').val().trim();
            var new_name=$('#new_name').val().trim();

            if(old_name!="" && new_name!=""){
                $.get('rename_name',{
                    old_name:old_name,
                    new_name:new_name
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
function populate_third_div(div_name,version_list,type,project_id,team_id){
    var message='<table width="100%" class="one-column-emphasis">';
    if(version_list.length==0){
        message+='<tr><td>No Version Found</td></tr>'
    }
    else{
        for(var i=0;i<version_list.length;i++){
            if(version_list[i][1]!=""){
                message+='<tr><td>'+version_list[i][0]+'</td>';
                message+='<td><table width="100%">';
                var temp=version_list[i][1].split(",");
                for(var j=0;j<temp.length;j++){
                    message+='<tr><td class="'+type+'">'+temp[j]+'</td></tr>';
                }
                message+='</table></td>';
                message+='</tr>';
            }
        }
    }
    message+='</table>';
    $('#'+div_name).html(message);
}
function input_new_version(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<thead><tr><td colspan="2"><b>Input New Version</b></td></tr></thead>';
    message+='<tbody style="margin-top: 2%;"><tr><td align="right"><b>Name:</b></td><td align="left">'+dep_name+'</td></tr>';
    message+='<tr><td align="right"><b>Bit:</b></td><td align="left"><select id="bit"><option value="32">32 Bit</option><option value="64">64 Bit</option></select></td></tr>';
    message+='<tr><td align="right"><b>Version:</b></td><td align="left"><input style="width:100%;" id="version" class="textbox"/></td></tr>';
    message+='</tbody>;'
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var bit=$('#bit option:selected').val().trim();
            var version=$('#version').val().trim();
            if(bit!="" && version !=""){
                $.get('add_new_version',{
                    'bit':bit,
                    'version':version,
                    'value':dep_value
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
                alertify.error("Input Field Error",time_out);
            }
        }
        else{

        }
    });
}
function allow_binding(type,project_id,team_id){
    if(type=="dependency"){
        $(".custom-menu-dependency li").click(function(){
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "create":create_new_name_under_version(dep_name,project_id,team_id,dep_value); break;
                case "rename":rename_dependency(dep_name,project_id,team_id,dep_value); break;
                case "usage":alert('usage'); break;
                case "unlink":unlink_dependency(dep_name,project_id,team_id,dep_value); break;
            }
        });
    }
    if(type=="add_dependency"){
        $(".custom-menu-add_dependency li").click(function(e){
            //(project_id,team_id);
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "link": link_dependency(dep_name,project_id,team_id,dep_value);break;
                case "rename":rename_dependency(dep_name,project_id,team_id,dep_value); break;
                case "usage":alert('usage'); break;
                case "delete":alert("delete"); break;
            }
            //e.stopPropagation();
        });
    }
    if(type=='branch'){
        $(".custom-menu-branch li").click(function(){
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "create":create_new_version_under_branch(dep_name,project_id,team_id,dep_value);break;
                case "rename":rename_branch(dep_name,project_id,team_id,dep_value); break;
                case "usage":alert('usage'); break;
                case "unlink":unlink_branch(dep_name,project_id,team_id,dep_value); break;
            }
        });
    }
    if(type=="add_branch"){
        $(".custom-menu-add_branch li").click(function(e){
            //(project_id,team_id);
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "link": link_branch(dep_name,project_id,team_id,dep_value);break;
                case "rename":rename_branch(dep_name,project_id,team_id,dep_value); break;
                case "usage":alert('usage'); break;
                case "delete":alert("delete"); break;
            }
            //e.stopPropagation();
        });
    }
    if(type=='add_feature'){
        $(".custom-menu-add_feature li").click(function(e){
            //(project_id,team_id);
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "link": link_feature(dep_name,project_id,team_id,dep_value);break;
                case "rename":rename_feature(dep_name,project_id,team_id,dep_value); break;
                case "usage":alert('usage'); break;
                case "delete":alert("delete"); break;
            }
            //e.stopPropagation();
        });
    }
    if(type=='feature'){
        $(".custom-menu-feature li").click(function(){
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "create":alert('create_sub_feature');break;
                case "rename":rename_feature(dep_name,project_id,team_id,dep_value); break;
                case "usage":alert('usage'); break;
                case "unlink":unlink_feature(dep_name,project_id,team_id,dep_value); break;
            }
        });
    }
}
function rename_feature(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<thead><tr><td colspan="2"><b>Rename</b></td></tr></thead>';
    message+='<tbody><tr><td align="right"><b>Old Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="old_name" value="'+dep_name+'"/></td></tr>';
    message+='<tr><td align="right"><b>New Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="new_name"/></td></tr></tbody>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var old_name=$('#old_name').val().trim();
            var new_name=$('#new_name').val().trim();

            if(old_name!="" && new_name!=""){
                $.get('rename_feature',{
                    old_name:old_name,
                    new_name:new_name
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

function unlink_feature(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="center">Are you sure to unlink feature <b>\''+dep_name+'\'</b>?</td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            $.get('unlink_feature',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
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

        }
    });
}
function link_feature(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="center">Are you sure to link feature <b>\''+dep_name+'\'</b>?</td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            $.get('link_feature',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
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

        }

    });
}
function link_branch(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="center">Are you sure to link branch <b>\''+dep_name+'\'</b>?</td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            $.get('link_branch',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
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

        }

    });
}
function unlink_branch(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="center">Are you sure to unlink branch <b>\''+dep_name+'\'</b>?</td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            $.get('unlink_branch',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
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

        }
    });
}
function rename_branch(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<thead><tr><td colspan="2"><b>Rename</b></td></tr></thead>';
    message+='<tbody><tr><td align="right"><b>Old Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="old_name" value="'+dep_name+'"/></td></tr>';
    message+='<tr><td align="right"><b>New Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="new_name"/></td></tr></tbody>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var old_name=$('#old_name').val().trim();
            var new_name=$('#new_name').val().trim();

            if(old_name!="" && new_name!=""){
                $.get('rename_branch',{
                    old_name:old_name,
                    new_name:new_name
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
function create_new_version_under_branch(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td colspan="2" align="center"><b>Create New Version</b></td></tr>';
    message+='<tr><td align="right"><b>'+dep_name+' Version:</b></td><td align="left"><input class="textbox" id="new_name" style="width: 100%"/></td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var new_name=$('#new_name').val().trim();
            if(new_name!=""){
                $.get('add_new_version_branch',{
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
function unlink_dependency(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="center">Are you sure to unlink dependency <b>\''+dep_name+'\'</b>?</td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            $.get('unlink_dependency',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
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

        }
    });
}
function link_dependency(dep_name,project_id,team_id,dep_value){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="center">Are you sure to link dependency <b>\''+dep_name+'\'</b>?</td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            $.get('link_dependency',{
                value:dep_value,
                project_id:project_id,
                team_id:team_id
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

        }

    });
}
function rename_dependency(dep_name,project_id,team_id,dep_value){
   // alert(project_id+team_id);
    var message="";
    message+='<table width="100%">';
    message+='<thead><tr><td colspan="2"><b>Rename</b></td></tr></thead>';
    message+='<tbody><tr><td align="right"><b>Old Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="old_name" value="'+dep_name+'"/></td></tr>';
    message+='<tr><td align="right"><b>New Name:</b></td><td align="left"><input type="text" class="textbox" style="width:100%" id="new_name"/></td></tr></tbody>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var old_name=$('#old_name').val().trim();
            var new_name=$('#new_name').val().trim();

            if(old_name!="" && new_name!=""){
                $.get('rename_dependency',{
                    old_name:old_name,
                    new_name:new_name
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
    $('#create_new_branch').on('click',function(event){
        event.preventDefault();
        var message="";
        message+='<table width="100%">';
        message+='<tr><td align="center" colspan="2"><b class="Text">Create New Branch</b></td></tr>';
        message+='<tr style="margin-top: 2%;"><td align="right"><b class="Text">Branch:</b></td><td><input class="textbox" style="width: 100%" id="branch_name"></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var dependency_name=$('#branch_name').val().trim();
                if(dependency_name!=""){
                    $.get('add_new_branch',{
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
    $('#create_new_feature').on('click',function(event){
        event.preventDefault();
        var message="";
        message+='<table width="100%">';
        message+='<tr><td align="center" colspan="2"><b class="Text">Create New Feature</b></td></tr>';
        message+='<tr style="margin-top: 2%;"><td align="right"><b class="Text">Feature:</b></td><td><input class="textbox" style="width: 100%" id="feature_name"></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var feature_name=$('#feature_name').val().trim();
                if(feature_name!=""){
                    $.get('add_new_feature',{
                        feature_name:feature_name
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