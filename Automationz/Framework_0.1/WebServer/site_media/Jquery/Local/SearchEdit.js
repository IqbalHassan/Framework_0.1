var test_case_per_page=5;
var test_case_page_current=1;
$(document).ready(function(){
    test_case_per_page=$('#content_change option:selected').val().trim();
    RunAutoCompleteTestSearch();
    DeleteSearchQueryText(test_case_per_page,test_case_page_current);
    $('#content_change').on('change',function(){
        test_case_per_page=$(this).val().trim();
        window.location.hash='#1';
        PerformSearch(test_case_per_page,test_case_page_current);
    });
});
function RunAutoCompleteTestSearch(){
    $("#searchbox").autocomplete(
        {
            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearchOtherPages",
                    dataType: "json",
                    data:{ term: request.term,project_id:$('#project_identity option:selected').val().trim(),team_id:$('#default_team_identity option:selected').val().trim()},
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
                    $("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
                        + '<td name = "submitquery" class = "Text" style = "size:10">'
                        + value
                        + ":&nbsp"
                        + '</td>'
                    );
                    PerformSearch(test_case_per_page,test_case_page_current);
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

function PerformSearch(test_case_per_page,test_case_page_current) {
    $("#AutoSearchResult #searchedtext").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("TableDataTestCasesOtherPages",{
            Query: UserText,
            project_id:$('#project_identity option:selected').val().trim(),
            team_id:$('#default_team_identity option:selected').val().trim(),
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
                        PerformSearch(test_case_per_page,PageNumber);
                    }
                });
                $("#RunTestResultTable").fadeIn(1000);
                //$("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#RunTestResultTable");
                // add edit btn
                var indx = 0;
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
                $(".Buttons[title='Select User']").fadeOut();
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
function DeleteSearchQueryText(test_case_per_page,test_case_page_current){
    $("#AutoSearchResult td .delete").live('click', function() {

        if ($("#AutoSearchTextBoxLabel").text().trim() != "*Select Test Machine:") //If user is on select user page, do not allow him to delete the Test Data Set
        {
            console.log("clicked");
            console.log($(this).text());
            $(this).parent().next().remove();
            $(this).remove();
            if($('#AutoSearchResult #searchedtext td').text()==""){
                $('#DepandencyCheckboxes').css('display','none');
                $('.flip[title="DepandencyCheckBox"]').css('display','none');
                $('#RunTestResultTable').css('display','none');
            }
            $("#AutoSearchResult #searchedtext").each(function() {
                var UserText = $(this).find("td").text();
                if (UserText.length == 0)
                {
                    //$(".Buttons[title='Search Test Cases']").fadeOut(2000);
                    //$(".Buttons[title='Verify Query']").fadeOut(2000);
                    $(".Buttons[title='Select User']").fadeOut(2000);
                }
            });

        }

        else
        {

            $(".delete").css('cursor','default');
        }
        PerformSearch(test_case_per_page,test_case_page_current);

    });
}
