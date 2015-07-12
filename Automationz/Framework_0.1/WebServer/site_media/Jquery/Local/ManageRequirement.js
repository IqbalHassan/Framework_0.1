
var label_per_page=5;
var label_page_current=1;
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');
$(document).ready(function(){
    primarySettings();

    $("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val());
        window.location.reload(true);
    });

    /*$.get("Reqs_List",{project_id : project_id},function(data)
    {
        if(data['reqs'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr>'
            for (var i = 0; i < data['reqs'].length; i++) {
                message += '<tr>';
                for (var j = 0; j < data['reqs'][i].length; j++) {
                    message += '<td align="left">' + data['reqs'][i][j] + '</td>';


                }
                message += '</tr>';
            }
            message += '</table>';
            $('#allReqs').html(message);
            make_clickable('#allReqs');


        }
        else{
            $("#allReqs").html('<h2>No Data Available</h2>')
        }
    });*/


    get_labels(project_id,team_id,label_per_page,label_page_current);

    label_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            label_per_page=$(this).val();
            label_page_current=1;
            $('#pagination_div').pagination('destroy');
            window.location.hash = "#1";
            get_labels(project_id,team_id,label_per_page,label_page_current);
        }
    });

});

function primarySettings(){
    $('#project_code').text($.session.get('project_id'));
    $('#create_new_requirement').click(function(event){
        event.preventDefault();
        window.location=('/Home/'+ $.session.get('project_id')+'/CreateRequirement/');
    });
}

function make_clickable(divname) {
    $(divname + ' tr>td:first-child').each(function () {
        $(this).css({
            'color': 'blue',
            'cursor': 'pointer',
            'textAlign': 'left'
        });
        $(this).click(function(){
            window.location = '/Home/'+ $.session.get('project_id')+'/EditRequirement/'+$(this).text().trim()+'/';
        })
    });

    $(divname + ' tr>td:last-child').each(function () {
        /*if($(this).text()!=("None")){
         $(this).css({
         'color': 'blue',
         'cursor': 'pointer',
         'textAlign': 'left'
         });
         }*/
        //var divider = $(this).lastIndexOf("/");
        //console.log(divider);

    });
}

function get_labels(project_id,team_id,label_per_page,label_page_current){
    $.get("Show_Reqs",{'project_id':project_id ,'team_id':team_id,'label_per_page':label_per_page,'label_page_current':label_page_current},function(data){
        form_table("AllMSTable",data['Heading'],data['TableData'],data['Count'],"Requirements");
        
        $('#pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:label_per_page,
            cssStyle: 'dark-theme',
            currentPage:label_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_labels(project_id,team_id,label_per_page,PageNumber);
            }
        });
    });
}


function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table class="two-column-emphasis">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        for(var j=0;j<data[i].length;j++){
            switch(data[i][j]){
                case 'Dev':
                    message+='<td style="background-color: ' + colors['dev'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                case 'Ready':
                    message+='<td style="background-color: ' + colors['ready'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                default :
                    message+='<td>'+data[i][j]+'</td>';
                    continue;
            }
        }
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);
    make_clickable('#'+divname);
}

/*$(document).ready(function(){
   PopulateGeneralInfo();
    var config_object = {
        "core": {
            "themes" : { "variant" : "large" },

            "data" : {
                "url" : function(node) {
                    return ("/Home/"+ $.session.get('project_id')+"/getRequirements/");
                },

                "data" : function(node) {
                    return { "id" : node.id };
                }
            },

            "check_callback": true
        },

        "types" : {
            "#" : {
                "valid_children" : [ "parent_section" ]
            },

            "parent_section" : {
                "icon" : "fa fa-file fa-lg fa-fw",
                "valid_children" : [ "section" ]
            },

            "section" : {
                "icon" : "fa fa-file fa-fw fa-lg",
                "valid_children" : [ "section" ]
            }
        },

        "contextmenu" : {
            "select_node":true,
            "items" : function(node) {
                return {
                    "Create" : {
                        "separator_before": false,
                        "separator_after": false,
                        "label": "Create Sub Requirement",
                        "icon": "fa fa-plus",
                        "action": function(obj) {
                            /*try {
                                var x = node.text.split('<span style="display:none;">');
                                var y = x[1].split("</span>");
                                createNode(y[0] + ".");
                            } catch (TypeError) {
                                createNode(node.text + ".");
                            }*/
                            //create a child requirement under this requirement
                           /* window.location=('/Home/'+ $.session.get('project_id')+'/CreateRequirement/'+ node.text);
                        }
                    },
                    "Edit" : {
                        "separator_before": false,
                        "separator_after": false,
                        "label": "Edit",
                        "icon": "fa fa-edit",
                        "action": function(obj) {

                        }
                    },
                    "Delete" : {
                        "separator_before": true,
                        "separator_after": false,
                        "icon": "fa fa-trash-o",
                        "label": "Delete Requirement",
                        "action": function(obj) {

                        }
                    }
                }
            }
        },
        /*
        "checkbox" : {
            "keep_selected_style": false
        },*/

       /* "plugins" : [ "search", "types", "wholerow", "contextmenu", "sort" ]
    };
    //$('#tree').jstree(config_object);
    $("#tree").jstree(config_object)
        .on("select_node.jstree", function(e, data) {
            var selected_sections = JSON.stringify(data.selected);
            $(this).jstree(true).open_node(data.selected);
            $.get('SmallViewRequirements',{
                'selected_section_ids':selected_sections,
                'project_id': $.session.get('project_id')
            },function(data){
                var parent=data['parent_id'];
                var detail=data['requirement_detail'][0];
                $('#msg').css({'display':'none'});
                var message="";
                message+='<table width="100%" align="left">';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Requirement ID:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%"><b>'+detail[6]+'</b></td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Title:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%">'+detail[0]+'</td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Description:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%">'+detail[1]+'</td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Parent Requirement:</b></td>';
                if(parent instanceof(Array)){
                    message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%"><b>'+parent[0][0] +'</b> - '+parent[0][1]+'</td>');

                }else{
                    message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%">'+parent+'</td>');
                }
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Due Date:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%">'+detail[2]+'</td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Status:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%;color: '+detail[4]+';">'+detail[3]+'</td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Milestone:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%">'+detail[5]+'</td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;"><b class="Text" style="font-size: 150%;">Team Name:</b></td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%">'+detail[7]+'</td>');
                message+='</tr>';
                message+='<tr>';
                message+='<td width="45%" align="right" style="vertical-align: 0%;">&nbsp;</td>';
                message+=('<td width="55%" align="left" style="vertical-align: 0%;font-size: 125%"><table align="right"><tr><td align="right"><a href="/Home/'+$('#project_code').text().trim()+'/Requirements/'+detail[6]+'/"><b>See Details</b></a></td></tr></table></td>');
                message+='</tr>';
                message+='</table>';
                $('#RunTestResultTable').html(message);
            })
        });
    });

function PopulateGeneralInfo(){
    $('#project_code').html($.session.get('project_id'));
    $('#project_code').click(function(){
        window.location= ("/Home/Project/"+ $.session.get('project_id'));
    });
    $('#create_new_requirement').click(function(event){
        event.preventDefault();
        window.location=("/Home/"+ $.session.get('project_id')+"/CreateRequirement/");
    });
}*/