$(document).ready(function(){
    DeleteSearchQueryText();
    $('#project_owner').select2({
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
            $('#owner_list').append('<tr><td class="deleteTester"><img title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td><td data-id="'+user_id+'">'+user_name+'</td></tr>');
            $(this).select2('val','');
            $('.deleteTester').on('click',function(){
                //$('#assigned_projects').empty();
                $(this).parent().remove();
            });
            return false;
    });

    function formatTestCasesSearch(test_case_details) {
        var markup ='<div><i class="fa fa-file-text-o"></i><span style="font-weight: bold;"><span>' + test_case_details.text + '</span></div>';
        return markup;
    }

    $('#create_project').on('click',function(){
        var project_name=$('#project_name').val().trim();
        if(project_name==""){
            alertify.set({ delay: 300000 });
            alertify.error('Project Name is empty');
        }
        var project_owner=[];
        $('#owner_list td').each(function(){
            if(project_owner.indexOf($(this).attr('data-id'))==-1 && $(this).attr('data-id') != undefined){
                project_owner.push($(this).attr('data-id').trim());
            }
        });
        //alert(project_owner);
        $.get('Create_New_Project',{
            user_name:'Admin',
            project_name:project_name,
            project_owner:project_owner.join(',')
        },function(data){
            if(data['message']){
                alertify.set({ delay: 300000 });
                alertify.success('Project: '+project_name+' is created successfully');
                window.location='/Home/superAdminFunction/ListProject/';
            }
            else{
                alertify.set({ delay: 300000 });
                alertify.error('Project: '+project_name+' exists')
                return false;
            }
        });
    });
});

function DeleteSearchQueryText(){
    $('#owner_list td .delete').on('click',function(){
        $(this).parent().parent().remove();
        $(this).remove();
    });
}