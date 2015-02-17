var test_case_per_page=10;
var test_case_page_current=1;
var project_id = $.session.get('project_id');
var team_id = $.session.get('default_team_identity');

$(document).ready(function(){
    ActivateAutoComplete();
    DeleteFilterData();
    ClickButton();
});
function ClickButton(){
    $('#deleteButton').on('click',function(){
        var tc_list=[]
        $('input[type="checkbox"]').each(function(){
            if($(this).attr('checked')==='checked'){
                var tc_id=$(this).attr('id').trim();
                tc_list.push(tc_id);
            }
        });
        $.get("DeleteTestCase",{Query:tc_list.join('|')},function(data) {
            alertify.success(data+' deleted successfully');
            PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current);
        });
    });
}
function ActivateAutoComplete(){
    $('#searchbox').autocomplete({
        source:function(request,response){
            $.ajax({
                url:'AutoCompleteTestCasesSearchTestSet',
                dataType:'json',
                data:{term: request.term,project_id:project_id, team_id:team_id},
                success:function(data){
                    response(data);
                }
            });
        },
        select : function(event, ui) {

            var tc_id_name = ui.item[0].split(" - ");
            var value = "";
            if (tc_id_name != null)
                value = tc_id_name[0].trim();

            if(value != "")
            {
                $("#filteredText").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
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
}

function PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current) {
    $("#filteredText").each(function() {
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
                $('#resultDiv').children().remove();
                $('#resultDiv').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $('#buttonDiv').css({'display':'none'});
                $('#pagination_div').pagination('destroy');
            }
            else
            {
                ResultTable('#resultDiv',data['Heading'],data['TableData'],"Test Cases");
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

                $("#resultDiv").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#resultDiv");
                // add edit btn
                var indx = 0;
                $('#resultDiv tr>td:nth-child(6)').each(function(){
                    var ID = $("#resultDiv tr>td:nth-child(1):eq("+indx+")").text().trim();

                    //$(this).after('<input type="checkbox" id="'+ID+'"/>');
                    $(this).after('<div><input id="'+ID+'" type="checkbox" class="Buttons add"/></div>')
                    indx++;
                });
                $('#buttonDiv').css({'display':'block'});
            }
        });
    });
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
            ResultTable('#'+ID+'detail',column,data_list,"");
            $('#'+ID+'detail tr').each(function(){
                $(this).css({'textAlign':'left'});
            });
        });
        $(this).live('click',function(){
            $('#'+ID+'detail').slideToggle("slow");
        });
    });
}
function DeleteFilterData(){
    $('#filteredText td .delete').live('click',function(){
        $(this).parent().next().remove();
        $(this).remove();
        PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current);
    });
}
