$(document).ready(function(){
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
                            window.location=('/Home/'+ $.session.get('project_id')+'/CreateRequirement/'+ node.text);
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

        "plugins" : [ "search", "types", "wholerow", "contextmenu", "sort" ]
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
}