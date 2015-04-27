$(document).ready(function(){
    var pathname=window.location.pathname;
    var type=pathname.split('/')[3].trim();
    var name=pathname.split('/')[4].trim();
    var str="%20";
    var re=new RegExp(str,'g');
    name=name.replace(re,' ');
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    var test_case_per_page=5;
    var test_case_page_current=1;
    LoadGenInfo(type,name);

    GetExisting(name,project_id,team_id,test_case_per_page,test_case_page_current);
    //PerformSearch();
    Suggestion(project_id,team_id,test_case_per_page,test_case_page_current);
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
                alertify.success(data,1500);
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
function GetExisting(name,project_id,team_id,test_case_per_page,test_case_page_current){
    name=name+':';
    name=name.trim();
    $.get('TableDataTestCasesOtherPages',{Query:name.trim(),test_status_request:false,project_id:project_id,team_id:team_id,test_case_per_page:test_case_per_page,test_case_page_current:test_case_page_current,total_time:true},function(data){
        if(data['TableData'].length!=0){
            //ResultTable("#existing",data['Heading'],data['TableData'],'Test Cases');
            var message='';
            message+='<table id="existing_test_cases" class="two-column-emphasis">';
            message+='<tr>';
            for(var i=0;i<data['Heading'].length;i++){
                message+='<th><b>'+data['Heading'][i]+'</b></th>';
            }
            message+='</tr>'
            for(var i=0;i<data['TableData'].length;i++){
                message+='<tr>';
                for(var j=0;j<data['TableData'][i].length;j++){
                    message+='<td>'+data['TableData'][i][j]+'</td>';
                }
                message+='</tr>';
            }
            message+='</table>';
            $('#existing').html(message);
            $('#pagination').pagination({
                    items:data['Count'],
                    itemsOnPage:test_case_per_page,
                    cssStyle: 'dark-theme',
                    currentPage:test_case_page_current,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        GetExisting(name,project_id,team_id,test_case_per_page,PageNumber);
                    }
                });
            implementDropDown("#existing");
            $('#existing tr>td:nth-child(8)').each(function(){
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
            $('#pagination').pagination('destroy');
        }
    });
}

/*function PerformSearch(project_id,team_id){
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
}*/
function Suggestion(project_id,team_id,test_case_per_page,test_case_page_current){
    $("#searchbox").autocomplete(
        {
            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearchTestSet",
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
                    PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current);
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

function PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current) {
    $("#searchedFilter").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("TableDataTestCasesOtherPages",{
            Query: UserText,
            project_id:project_id,
            team_id:team_id,
            test_case_per_page:test_case_per_page,
            test_case_page_current:test_case_page_current
        },function(data) {

            if (data['TableData'].length == 0)
            {
                $('#RunTestResultTable').children().remove();
                $('#RunTestResultTable').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $("#DepandencyCheckboxes").children().remove();
                $('#pagination_div').pagination('destroy');
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");
                $('#RunTestResultTable').find('p:eq(0)').html(data['Count']+' Test Cases');
                $('#pagination_div').pagination({
                    items:data['Count'],
                    itemsOnPage:test_case_per_page,
                    cssStyle: 'dark-theme',
                    currentPage:test_case_page_current,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        PerformSearch(project_id,team_id,test_case_per_page,PageNumber);
                    }
                });
                $("#RunTestResultTable").fadeIn(1000);
                //$("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#RunTestResultTable");
                $('#RunTestResultTable tr>td:nth-child(7)').each(function(){
                    var id=$(this).closest('tr').find('td:first-child').text().trim();
                    $(this).after('<div><input id="'+id+'" type="checkbox" class="Buttons add"/></div>');
                });
                //$('#RunTestResultTable').css({'display':'block'});
                $('#add_button').css({'display':'block'});
                // add edit btn
                /*var indx = 0;
                $('#RunTestResultTable tr>td:nth-child(6)').each(function(){
                    var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25" width="25" />');
                    $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25" width="25"/>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id")+'/';
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id")+'/';
                });
                //VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                $(".Buttons[title='Select User']").fadeOut();*/
            }
        });
    });
}