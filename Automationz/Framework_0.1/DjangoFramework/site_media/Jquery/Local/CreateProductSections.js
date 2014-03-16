/**
 * Created by minar09 on 2/7/14.
 */

$(document).ready(function(){
    /*$('#jstree_container').jstree({ 'core' : {
        /*'data' : [
            { "id" : "ajson1", "parent" : "#", "text" : "Simple root node" },
            { "id" : "ajson2", "parent" : "#", "text" : "Root node 2" },
            { "id" : "ajson3", "parent" : "ajson2", "text" : "Child 1" },
            { "id" : "ajson4", "parent" : "ajson2", "text" : "Child 2" },
        ]
            "ajax":{
                "url":'getProductSection',
                "data":function(data){
                    console.log(data);
                }
            }
        }
    });*/
    var dataList=[];
    $.get('GetProductSection/',{section:""},function(data){
        dataList=configure_data(data);
        $('#jstree_container').tree({
            data:dataList,
            dragAndDrop:true,
            autoOpen:0
        });
    });
    $('#jstree_container').bind('tree.click',function(event){
        var node=event.node;
        //alert(node.name);
        $.get('GetSections/',{section:node.name.trim()},function(data){
            var node1 = $('#tree1', 'getNodeByName', node.name.trim());
            for(var i=0;i<data.length;i++){
                $('#jstree_container').tree('addNodeAfter',{
                    label:data[i]
                },node1);
            }
        })
    })
    /*var data = [
        {
            label: 'node1',
            children: [
                { label: 'child1' },
                { label: 'child2' }
            ]
        },
        {
            label: 'node2',
            children: [
                { label: 'child3' }
            ]
        }
    ];*/
    /*$('#jstree_container').tree({
        dataUrl:'GetProductSection/',
        dataFilter:function(data){
            dataList=configure_data(data);
        },
        data:dataList
    });*/
});
function configure_data(data){
    dataList=[];
    for(var i=0;i<data.length;i++){
        var object={label:data[i]};
        dataList.push(object);
    }
    return dataList;
}