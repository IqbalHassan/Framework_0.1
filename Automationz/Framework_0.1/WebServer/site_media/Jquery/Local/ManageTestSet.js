/*$(document).ready(function(){
    $("#type").click(function(event){
        event.preventDefault();
        console.log($("#type").val());
        if($("#type").val()!="0"){
            $("#button_place").html("<input type=\"submit\" name=\"submit_button\" id=\"submitButton\" value=\"Search\"/>");
        }
        else{
            $("#button_place").html("")
        }

    });
    $("#input").autocomplete({
        source: function(request,response){
            if($("#type").val()==1){
                var url="TestSet_Auto";
            }
            if($("#type").val()==2){
                var url="TestTag_Auto"
            }
            if($("#type").val()==3){
                var url="AutoCompleteTestCasesSearch"
            }
            env="PC"
            $.ajax({
                url:"AutoCompleteTestCasesSearch",
                dataType:"json",
                data:{term:request.term,Env:env},
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var tc_id_name = ui.item.value.split(" - ");
            var value = "";
            if (tc_id_name != null)
                value = tc_id_name[0];
            $("#input").val(value);
            return false;
        }
    });
});*/
$(document).ready(function(){
    AddAutoCompleteSearchBox("#searchBox","Search Test Cases Data By Keywords:");
    RunAutoCompleteTestSearch("PC");
});
function AddAutoCompleteSearchBox(wheretoplace,label){
    $(wheretoplace).append(
        "<form method = 'get' >"

            +"<table id='AutoSearchResult' style='display: block;' >"
            + "<tbody>"

            + "<tr>"
            + "<td>"
            + "<label > <b id = 'AutoSearchTextBoxLabel' class = 'Text'>"
            +   label
            + " </b></label>"
            + "<input class = 'ui-corner-all textbox' id='searchbox' type='text' title = 'Please Type Keyword and Click On that to add to query' name='searchboxname' />"
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
function RunAutoCompleteTestSearch(env){
    $("#searchbox").autocomplete(
        {
            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearchOtherPages",
                    dataType: "json",
                    data:{ term: request.term, Env: env },
                    success: function( data ) {
                        response( data );
                    }
                });
            },
            select : function(event, ui) {

                var tc_id_name = ui.item[0].split(" - ");
                var value = "";
                if (tc_id_name != null)
                    value = tc_id_name[0];
                if(value!=""){
                    $("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
                        +'<td name = "submitquery" class = "Text" style = "size:10">'
                        + value
                        + ":&nbsp"
                        + '</td>');
                    PerformSearch();
                    $("#searchbox").val("");
                    return false;
                }

            }
        }
    ).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
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
function PerformSearch(){
    $("#AutoSearchResult #searchedtext").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        //Env = Get_Selected_Env_Name()
        $.get("TableDataTestCasesOtherPages",{Query: UserText},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#right_div').children().remove();
                $('#right_div').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $("#DepandencyCheckboxes").children().remove();
                $(".delete").click(function(){
                    $(this).parent().next().remove();
                    $(this).remove();
                });
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                console.log(data);

                /*ResultTable('#right_div',data['Heading'],data['TableData'],"Test Cases");

                $("#right_div").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);

                // add edit btn
                var indx = 0;
                $('#right_div tr>td:nth-child(2)').each(function(){
                    var ID = $("#right_div tr>td:nth-child(1):eq("+indx+")").text().trim();

                    //$(this).after('<img class="templateBtn buttonCustom" id="'+ID+'" src="/site_media/template.png" height="50"/>');
                    //$(this).after('<img class="editBtn buttonCustom" id="'+ID+'" src="/site_media/edit_case.png" height="50"/>');

                    //var value=;
                    $(this).after('<input id="'+ ID +'" type="checkbox" name="selectTCAdd" value="'+ID+'"/>');
                    indx++;
                });

                /*$(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Create/'+ $(this).attr("id");
                });*/
                //VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                //$(".Buttons[title='Select User']").fadeOut();
                var message="";
                message+='<p align="center" style="font-weight: bolder;font-size: 1.2em;">Select Test Case(s) To Add</p>';
                message+='<hr style="width: 80%">';


                message+='<table class="one-column-emphasis" style="border-collapse: collapse"><tr>';
                for(var i=0;i<data['Heading'].length;i++){
                    message+='<th align="center" style="font-weight: bold;padding: 2px;">'+data['Heading'][i]+'</th>';
                }
                message+='<th align="center">&nbsp</th>';
                message+='</tr>';
                for(var i=0;i<data['TableData'].length;i++){
                    message+='<tr>';
                    for(var j=0;j<(data['TableData'][i]).length;j++){
                        message+='<td>'+data['TableData'][i][j]+'</td> ';
                    }
                    message+='<td><input id="'+data['TableData'][i][0]+'" value="'+data['TableData'][i][0]+'" name="selectTCAdd" type="checkbox" /></td> '
                    message+='</tr>';
                }
                message+='</table>';
                message+='<br/>';
                message+='<button type="submit" id="addBtn" class="button minibutton primary">Add Selected TCs</button>';
                $('#right_div').html(message);
                $(".delete").click(function(){
                   $(this).parent().next().remove();
                   $(this).remove();
                   PerformSearch();
                });
            }

        });

    });

}