/**
 * Created by minar09 on 2/7/14.
 */

$(document).ready(function(){
    $.get("GetProductSection/",{section:""},function(data){
        console.log(data);
        var levelNumber=data[0][0];
        message="";
        message+='<ul>';
        for(var i=1;i<data.length;i++){
            message+='<li data-level="'+levelNumber+'">'+data[i][0]+'</li>';
        }
        message+='</ul>';
        $('#jstree_container').html(message);
        $('#jstree_container').on(
            'changed.jstree',function(event,data){
                var i, j, r = [];
                for(i = 0, j = data.selected.length; i < j; i++) {
                    r.push(data.instance.get_node(data.selected[i]).text);
                }
                console.log('selected:'+r.join(','));
                $.get("GetProductSection/",{section: r.join(',')},function(data){
                    message="";
                    message+='<ul>';
                    for(var i=1;i<data.length;i++){
                        message+='<li data-level="'+levelNumber+'">'+data[i][0]+'</li>';
                    }
                    message+='</ul>';
                });
            }
        ).jstree();
    });
});

