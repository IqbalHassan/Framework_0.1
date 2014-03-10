/**
 * Created by minar09 on 2/7/14.
 */

$(document).ready(function(){

    $('#jstree').jstree({
        "types" : {
            "#" : {
                "max_children" : 1,
                "max_depth" : 4,
                "valid_children" : ["root"]
            },
            "root" : {
                "icon" : "/site_media/tree_icon.png",
                "valid_children" : ["default"]
            },
            "default" : {
                "valid_children" : ["default","file"]
            },
            "file" : {
                "icon" : "glyphicon glyphicon-file",
                "valid_children" : []
            }
        },
        "plugins" : [ "checkbox", "contextmenu", "dnd", "search", "sort", "state", "types", "unique", "wholerow" ]
    });
    // 7 bind to events triggered on the tree
    /*$('#jstree').jstree({
        "core" : {
            "animation" : 0,
            "check_callback" : true,
            "themes" : { "stripes" : true },
            'data' : {
                'url' : function (node) {
                    return node.id === '#' ?
                        'ajax_demo_roots.json' : 'ajax_demo_children.json';
                },
                'data' : function (node) {
                    return { 'id' : node.id };
                }
            }
        },
        "types" : {
            "#" : {
                "max_children" : 1,
                "max_depth" : 4,
                "valid_children" : ["root"]
            },
            "root" : {
                "icon" : "tree_icon.png",
                "valid_children" : ["default"]
            },
            "default" : {
                "valid_children" : ["default","file"]
            },
            "file" : {
                "icon" : "glyphicon glyphicon-file",
                "valid_children" : []
            }
        },
        "plugins" : [
            "contextmenu", "dnd", "search",
            "state", "types", "wholerow"
        ]
    });*/
    $('#jstree').on("changed.jstree", function (e, data) {
        console.log(data.selected);
    });

    var to = false;
    $('#searchbox').keyup(function () {
        if(to) { clearTimeout(to); }
        to = setTimeout(function () {
            var v = $('#searchbox').val();
            $('#searchbox').jstree(true).search(v);
        }, 250);
    });


    $(".main").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"GetSections",
                dataType:"json",
                data:{
                    section : ''
                },
                success:function(data){
                    response(data);
                }
            });
        },
        /*select: function(request,ui){
         var tc_id_name = ui.item.value.split(" - ");
         var value = "";
         if (tc_id_name != null)
         value = tc_id_name[0];
         $("#input").val(value);
         return false;
         }*/
        select: function(request,ui){
            var value = ui.item[0];
            if(value!=""){
                $(".main").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "</a>" )
            .appendTo( ul );
    };

    $(".sub1").autocomplete({
        //var sect = $(".main").val();
        source: function(request,response){
            $.ajax({
                url:"GetSubSections",
                dataType:"json",
                data:{
                    section : ''
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value = ui.item[0];
            if(value!=""){
                $(".sub1").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "</a>" )
            .appendTo( ul );
    };
});

