$(document).ready(function(){
    AddAutoCompleteSearchBox("#Place_AutoComplete_Here","Search Test Cases Data By Keywords:");
    RunTestAutocompleteSearch();
    PerformSearch();
    DeleteSearchQueryText();
});

function AddAutoCompleteSearchBox(WhereToPlaceId, Label)
{

    $(WhereToPlaceId).append(


        "<form method = 'get' >"

            +"<table id='AutoSearchResult' style='display: block;' >"
            + "<tbody>"

            + "<tr>"
            + "<td>"
            + "<label > <b id = 'AutoSearchTextBoxLabel' class = 'Text'>"
            //+ Label
            + " </b></label>"
            + "<input class = 'ui-corner-all textbox' id='searchbox' style = 'margin:5px' type='text' title = 'Please Type Keyword and Click On that to add to query' name='searchboxname' placeholder='" +
            Label +
            "'/>"
            + "</td>"
            + "</tr>"


            + "</tbody>"
            + "</table>"


            +"<table id = 'AutoSearchResult' >"
            + "<tbody>"

            + "<tr id = 'searchedtext'>"
            +"<p> </p>"
            + "<th class = 'Text' style= 'text-align: left'> Test Data Set: </th>"
            + "</tr>"

            + "</tbody>"
            + "</table>"
            + "</form>"



    );
}
function RunTestAutocompleteSearch()

{

    $("#searchbox").autocomplete(
        {
            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearchOtherPages",
                    dataType: "json",
                    data:{ term: request.term},
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
                    PerformSearch();
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
function PerformSearch() {
    $("#AutoSearchResult #searchedtext").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("TableDataTestCasesOtherPages",{Query: UserText},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#RunTestResultTable').children().remove();
                $('#RunTestResultTable').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $("#DepandencyCheckboxes").children().remove();
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

                $("#RunTestResultTable").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#RunTestResultTable");
                // add edit btn
                var indx = 0;
                $('#RunTestResultTable tr>td:nth-child(5)').each(function(){
                    var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25"/>');
                    $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25"/>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
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
function DeleteSearchQueryText()

{

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
        PerformSearch();

    });
}
