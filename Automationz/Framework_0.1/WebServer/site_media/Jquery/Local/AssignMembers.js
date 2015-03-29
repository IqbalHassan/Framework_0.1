/**
 * Created by 09 on 3/29/15.
 */
$(document).ready(function(){
    $("#user_name_suggestion").select2({
        placeholder: "Search User....",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "GetProjectOwner",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatTestCasesSearch
    }).on("change", function(e) {
            var user_id=$(this).select2('data')['id'];
            var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
            $('#tester').html('<tr><td class="deleteTester"><img title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td><td data-id="'+user_id+'">'+user_name+'</td></tr>');
            $(this).select2('val','');
            $('.deleteTester').on('click',function(){
                $('#assigned_projects').empty();
                $(this).parent().remove();
            });
            get_projects(user_id,user_name);
            return false;
        });
    function formatTestCasesSearch(test_case_details) {
        var markup ='<div><i class="fa fa-file-text-o"></i><span style="font-weight: bold;"><span>' + test_case_details.text + '</span></div>';
        return markup;
    }
});

function get_projects(user_id,user_name){
    $.get('get_projects',{'user_id':user_id},function(data){
        var message='';
        message+='<caption><b>'+user_name+'\'s Projects</b></caption>'
        var project_list=data['project_list'];
        if(project_list.length>0){
            for(var i=0;i<project_list.length;i++){
                message+='<tr><td>'+project_list[i][1]+'</td><td><input id="'+project_list[i][0]+'" class="cmn-toggle cmn-toggle-yes-no" type="checkbox" value="'+project_list[i][0]+'" style="width:auto" /><label for="'+project_list[i][0]+'"data-on="Yes" data-off="No"></label></td></tr>';
            }
        }
        else{
            message+='<tr><td><b>No Project is linked</b></td></tr>';
        }
        message+='<tr><td>&nbsp;</td><td><input type="button" class="m-btn green" value="save" id="save_projects"/></td></tr>';
        $('#assigned_projects').empty();
        $('#assigned_projects').html(message);
        if(project_list.length>0){
            for(var i=0;i<project_list.length;i++){
                if(project_list[i][2]){
                    $('#'+project_list[i][0]).attr('checked','checked');
                }
            }
        }
        $('#save_projects').on('click',function(){
            var project_list=[];
            $('#assigned_projects tr').each(function(){
                if($(this).find('td:nth-child(2)').find('input:eq(0)').attr('type')=='checkbox'){
                    var element=$(this).find('td:nth-child(2)').find('input:eq(0)');
                    var project_id=element.val();
                    if(element.is(":checked")){
                        var check=true;
                    }
                    else{
                        var check=false;
                    }
                    project_list.push([project_id,check]);
                }
            });
            $.get('update_team_project',{user_id:user_id,project_list:project_list.join("|")},function(data){
                if(data['message']){
                    window.location.reload(true);
                }
                else{
                    window.location.reload(false);
                }
            });
        });
    });
}
