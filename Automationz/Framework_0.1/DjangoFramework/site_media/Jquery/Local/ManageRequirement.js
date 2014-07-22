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

        /*"contextmenu" : {
            "items" : function(node) {
                return {
                    "Create" : {
                        "separator_before": false,
                        "separator_after": false,
                        "label": "Create Section",
                        "icon": "fa fa-plus",
                        "action": function(obj) {
                            try {
                                var x = node.text.split('<span style="display:none;">');
                                var y = x[1].split("</span>");
                                createNode(y[0] + ".");
                            } catch (TypeError) {
                                createNode(node.text + ".");
                            }
                        }
                    },
                    "Rename" : {
                        "separator_before": false,
                        "separator_after": false,
                        "label": "Rename Section",
                        "icon": "fa fa-edit",
                        "action": function(obj) {
                            renameNode(node, node.id);
                        }
                    },
                    "Delete" : {
                        "separator_before": true,
                        "separator_after": false,
                        "icon": "fa fa-trash-o",
                        "label": "Delete Section",
                        "action": function(obj) {
                            deleteNode(node);
                        }
                    }
                }
            }
        },

        "checkbox" : {
            "keep_selected_style": false
        },*/

        "plugins" : [ "search", "types", "wholerow", "contextmenu", "sort" ]
    };
    //$('#tree').jstree(config_object);
    $("#tree").jstree(config_object)
        .on("changed.jstree", function(e, data) {
            var selected_sections = JSON.stringify(data.selected);
            $(this).jstree(true).open_node(data.selected);
        });
    });

function PopulateGeneralInfo(){
    //Setting the project code dynamically
    $('#project_code').html($.session.get('project_id'));

    //setting the newRequirementLocation dynamically
    var newRequirementLocation=("/Home/"+ $.session.get('project_id')+"/CreateNewRequirement/");
    $('#create_new_requirement').attr('href',newRequirementLocation);

    $('#project_code').click(function(){
        window.location= ("/Home/ManageRequirement/");
    });
}