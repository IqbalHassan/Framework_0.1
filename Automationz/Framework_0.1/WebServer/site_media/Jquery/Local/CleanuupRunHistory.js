/**
 * Created by 09 on 2/20/15.
 */
var current_page=1;
var run_per_page=10;
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_data(project_id,team_id,current_page,run_per_page);
    $('#delete_selected').on('click',function(){
        var run_id=[];
        $('.run_id:checked').each(function(){
            run_id.push($(this).val());
        });
        if(run_id.length<=0){
            alert('Run Id not selected');
            return false;
        }else{
            $.get('cleanup_data',{
                run_id_list:run_id.join('|')
            },function(data){
                if(data['message']){
                    alertify.set({ delay: 300000 });
                    alertify.success('Run Id erased successfully');
                    get_data(project_id,team_id,current_page,run_per_page);
                }
            });
        }
    });
});

function get_data(project_id,team_id,current_page,run_per_page){
    $.get('get_cleanup_data',{
        'project_id':project_id,
        'team_id':team_id,
        'current_page':current_page,
        'run_per_page':run_per_page
    },function(data){
        var run_list=data['data'];
        var message="";
        message+='<table class="two-column-emphasis">';
        message+='<tr>';
        for(var i=0;i<data['column'].length;i++){
            message+='<th>'+data['column'][i]+'</th>';
        }
        message+='</tr>'
        for(var i=0;i<run_list.length;i++){
            message+='<tr>';
            for(var j=0;j<run_list[i].length;j++){
                if(j==0){
                    message+='<td><a href="/Home/RunID/'+run_list[i][j]+'/" style="text-decoration: none;">'+run_list[i][j]+'</a></td>';
                }
                else{
                    message+='<td>'+run_list[i][j]+'</td>';
                }
            }
            message+='<td><input type="checkbox" class="run_id Buttons Add" value="'+run_list[i][0]+'"></td>';
            message+='</tr>';
        }
        message+='</table>';
        $('#run_history_table').empty();
        $('#run_history_table').html(message);
        $('#pagination_div').pagination({
            items:data['count'],
            itemsOnPage:run_per_page,
            cssStyle: 'dark-theme',
            currentPage:current_page,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_data(project_id,team_id,PageNumber,run_per_page)
            }
        });

    });
}

