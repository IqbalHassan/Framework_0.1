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
            PerformSearch();
        });
    });
}
function ActivateAutoComplete(){
    $('#searchbox').autocomplete({
        source:function(request,response){
            $.ajax({
                url:'AutoCompleteTestCasesSearchOtherPages',
                dataType:'json',
                data:{term: request.term},
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
}

function PerformSearch() {
    $("#filteredText").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("TableDataTestCasesOtherPages",{Query: UserText},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#resultDiv').children().remove();
                $('#resultDiv').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $('#buttonDiv').css({'display':'none'});
            }
            else
            {
                ResultTable('#resultDiv',data['Heading'],data['TableData'],"Test Cases");

                $("#resultDiv").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#resultDiv");
                // add edit btn
                var indx = 0;
                $('#resultDiv tr>td:nth-child(5)').each(function(){
                    var ID = $("#resultDiv tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<input type="checkbox" id="'+ID+'"/>');
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
        PerformSearch();
    });
}
