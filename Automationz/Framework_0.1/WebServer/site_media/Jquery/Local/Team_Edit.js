var project_id= $.session.get('project_id')
var team_name=$('#name').text().trim();
$(document).ready(function(){
    $("#tester_search").select2({
        placeholder: "Available Testers...",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteTesterSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'all':'edit',
                    'team_name':team_name,
                    'project_id':project_id
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatUsers
    }).on("change", function(e) {
            var user_id=$(this).select2('data')['id'];
            var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
            $("#tester").append('<tr><td><img class="delete DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text" data-id="'+user_id+'">'
                + user_name
                + ":&nbsp"
                + '</td></tr>');
            $(this).select2('val','');
            return false;
        });

    function formatUsers(user_details) {
        var markup ='<div><i class="fa fa-user"></i><span style="font-weight: bold;"><span>' + ' ' + user_details.text + '</span></div>';

        return markup;
    }
    $(".DeleteTester").live('click', function() {

        //$(this).parent().next().remove();
        //$(this).remove();
        $(this).parent().parent().remove();

    });

    $("#manager_search").select2({
        placeholder: "Available Manager...",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "GetTesterManager/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'all':'edit',
                    'team_name':team_name.trim(),
                    'project_id':project_id.trim()
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatUsers
    }).on("change", function(e) {
            var user_id=$(this).select2('data')['id'];
            var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
            $("#manager").append('<tr><td><img class="delete DeleteManager" title = "ManagerDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text" data-id="'+user_id+'">'
                + user_name
                + ":&nbsp"
                + '</td></tr>');
            $(this).select2('val','');
            return false;
        });
    $(".DeleteManager").live('click', function() {
        $(this).parent().parent().remove();
    });

    $('#remove_user').on('click',function(){
        var user_list=[];

        $('.Manager:checked').each(function(){
           user_list.push($(this).val().trim());
        });

        $('.Tester:checked').each(function(){
           user_list.push($(this).val().trim());
        });
        if(user_list.length>0){
            alertify.confirm("Are you sure you want to remove the selected from the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Delete_Members',{
                        'member':user_list.join("|"),
                        'team_name':team_name.trim(),
                        'project_id':project_id
                    },function(data){
                        if(data.indexOf('Failed')!=0){
                            window.location=('/Home/'+project_id+'/Team/'+team_name.trim().replace(/ /g,'_').trim()+'/');
                        }
                        else{
                            window.location.reload(true);
                        }
                    });
                }
            });
        }
        else{
            alertify.error("None is selected","",0);
            return false;
        }
    });

    $('#add_user').on('click',function(){
        var member=[];
        $('.DeleteManager').each(function(){
           member.push($(this).parent().next().attr('data-id'));
        });

        $('.DeleteTester').each(function(){
            member.push($(this).parent().next().attr('data-id'));
        });
        if(member.length!=0){
            alertify.confirm("Are you sure you want to add the selected to the team '"+team_name.trim()+"'?", function(e) {
                if (e) {
                    $.get('Add_Members',{
                        'member':member.join("|"),
                        'team_name':team_name.trim(),
                        'project_id':project_id
                    },function(data){
                        if(data.indexOf('Failed')!=0){
                            window.location=('/Home/'+project_id.trim()+'/Team/'+team_name.trim().replace(/ /g,'_').trim()+'/');
                        }
                        else{
                            window.location.reload(true);
                        }
                    });
                }
            });
        }
        else{
            alertify.error("None is selected","",0);
            return false;
        }
    });
});