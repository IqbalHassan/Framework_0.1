$(document).ready(function(){
    var pathname=window.location.pathname;
    var type=pathname.split('/')[3].trim();
    var name=pathname.split('/')[4].trim();
    var str="%20";
    var re=new RegExp(str,'g');
    name=name.replace(re,' ');
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    LoadGenInfo(type,name);

    GetExisting(name,project_id,team_id);
    //PerformSearch();
    Suggestion(project_id,team_id);
    DeleteFilterData(project_id,team_id);
    Buttons(type,name);
});
function Buttons(type,name){
    $('#add_button').click(function(event){
        event.preventDefault();
        var list=[]
        $('.add:checked').each(function(){
            list.push($(this).attr('id').trim());
        });
        if(list.length==0){
            alert('No Test Case selected');
            return false;
        }
        else{
            $.get('AddTestCasesSetTag',{type:type.toLocaleUpperCase().trim(),name:name.trim(),list:list.join('|')},function(data){
                alertify.success(data,"",3);
                var location='/Home/ManageSetTag/'+type+'/'+name+'/';
                window.location=location;
            });

        }

    });
    $('#delete_button').click(function(event){
        event.preventDefault();
        var list=[]
        $('.remove:checked').each(function(){
            list.push($(this).attr('id').trim());
        });
        if(list.length==0){
            alert('No Test Case selected');
            return false;
        }
        else{
            alertify.confirm("Are you sure you want to delete test cases "+list.join(",")+" from test "+type.toLocaleUpperCase().trim()+" named "+name.trim()+"?", function(e) {
                if (e) {
                    $.get('DeleteTestCasesSetTag',{type:type.toLocaleUpperCase().trim(),name:name.trim(),list:list.join('|')},function(data){
                        alertify.success(data,"",3);
                        var location='/Home/ManageSetTag/'+type+'/'+name+'/';
                        window.location=location;
                    });
                }
            });

        }

    });
}
function GetExisting(name,project_id,team_id){
    name=name+':';
    name=name.trim();
    $.get('TableDataTestCasesOtherPages',{Query:name.trim(),test_status_request:false,project_id:project_id,team_id:team_id,total_time:true},function(data){
        if(data['TableData'].length!=0){
            ResultTable("#existing",data['Heading'],data['TableData'],'Test Cases');
            implementDropDown("#existing");
            $('#existing tr>td:nth-child(7)').each(function(){
                var id=$(this).closest('tr').find('td:first-child').text().trim();
                $(this).after('<div><input id="'+id+'" type="checkbox" class="Buttons remove"/></div>');
            });
            $('#time').html('<b> - '+data['time']+'</b>')
            $('#existing').css({'display':'block'});
            $('#delete_button').css({'display':'block'});
        }
        else{
            $('#existing').html('<p style="font-weight: bold; text-align: center;" class="Text">There is no test cases</p>');
            $('#existing').css({'display':'block'});
            $('#delete_button').css({'display':'none'});
        }
    });
}

function PerformSearch(project_id,team_id){
    $("#searchedFilter").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get('TableDataTestCasesOtherPages',{Query:UserText,test_status_request:false,project_id:project_id,team_id:team_id},function(data){
        if(data['TableData'].length!=0){
            ResultTable("#RunTestResultTable",data['Heading'],data['TableData'],'Test Cases');
            implementDropDown("#RunTestResultTable");
            $('#RunTestResultTable tr>td:nth-child(6)').each(function(){
                var id=$(this).closest('tr').find('td:first-child').text().trim();
                $(this).after('<div><input id="'+id+'" type="checkbox" class="Buttons add"/></div>');
            });
            $('#RunTestResultTable').css({'display':'block'});
            $('#add_button').css({'display':'block'});

        }
        else{
            $('#RunTestResultTable').html('<p style="font-weight: bold; text-align: center;" class="Text">There is no test cases for this filter</p>');
            $('#RunTestResultTable').css({'display':'block'});
            $('#add_button').css({'display':'none'});
        }
    });
    });
}
function Suggestion(project_id,team_id){
    $("#searchbox").autocomplete(
        {
            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearchOtherPages",
                    dataType: "json",
                    data:{ term: request.term,project_id:project_id,team_id:team_id},
                    success: function( data ) {
                        response( data );
                    }
                });
            },

            //source : 'AutoCompleteTestCasesSearch?Env = ' +Env,
            select : function(event, ui) {

                var tc_id_name = ui.item[0].split(" - ");
                var value = "";
                if (tc_id_name != null)
                    value = tc_id_name[0].trim();

                if(value != "")
                {
                    $("#searchedFilter").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
                        + '<td name = "submitquery" class = "Text" style = "size:10">'
                        + value
                        + ":&nbsp"
                        + '</td>'
                    );
                    PerformSearch(project_id,team_id);
                }
                $("#searchbox").val("");
                return false;
            }
        }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };

    $("#searchbox").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });

}
function DeleteFilterData(project_id,team_id){
    $('#searchedFilter td .delete').live('click',function(){
        $(this).parent().next().remove();
        $(this).remove();
        PerformSearch(project_id,team_id);
    });
}
function LoadGenInfo(type,name){
    $('#type').html(type);
    $('#name').html(name);
}

function implementDropDown(wheretoplace){
    $(wheretoplace+" tr td:nth-child(2)").css({'color' : 'blue','cursor' : 'pointer'});
    $(wheretoplace+" tr td:nth-child(2)").each(function() {
        var ID=$(this).closest('tr').find('td:nth-child(1)').text().trim();
        var name=$(this).text().trim();
        $(this).html('<div id="'+ID+'name">'+name+'</div><div id="'+ID+'detail" style="display:none;"></div>');
        $.get("TestStepWithTypeInTable",{RunID: ID},function(data) {
            var data_list=data['Result'];
            var column=data['column'];
            ResultTable(wheretoplace+ ' #'+ID+'detail',column,data_list,"");
            $(wheretoplace+' #'+ID+'detail tr').each(function(){
                $(this).css({'textAlign':'left'});
            });
        });
        $(this).live('click',function(){
            $(wheretoplace+' #'+ID+'detail').slideToggle("slow");
        });
    });
}
