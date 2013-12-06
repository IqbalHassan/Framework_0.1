$(document).ready(function(){
    $("#create_edit").click(function(event){
        //event.preventDefault();
        console.log("clicked");
        $('#search').hide();
        $('#create_edit').hide();
        $("#choice").append("<p style='font-size:1.5em;'><b>Action</b>: Create/Edit</p>");
        populate_info_div();
        populate_footer_div();
    });
    $("#search").click(function(){
        $("#choice_div").hide();
        $("#create_edit_div").hide();
        $("#search_choice").append("<p style='font-size:1.5em;'><b>Action</b>: Search Test Step</p>");
        $('#search_div').append('' +
            '<div>' +
                '<label><b>Search for the Test Steps:</b></label>' +
                '<input type="text" name="search_query" placeholder="enter the keywords"/>' +
            '</div>');
    });
});

function populate_info_div(){
    $('#info_div').append('' +
        '<div style="float: left;margin-right: 15px;margin-left: 15px;">' +
            '<label><b>Test Step Name:</b></label><br>' +
            '<input type="text" placeholder="Enter the test set name" id="step_name" name="step_name"/>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Test Step Description:</b></label><br>' +
            '<textarea rows="2" cols="35" id="step_desc" name="step_desc" placeholder="Describe the test step(within 180 letters)"></textarea>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Feature:</b></label><br>' +
            '<input type="text" id="step_feature" name="step_feature" placeholder="Enter the feature"/>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Data Requirement:<b></label><br>' +
                '<select id="step_data" name="step_data">' +
                    '<option value="3" selected="selected">Select from the below choices:</option>' +
                    '<option value="1">True</option>' +
                    '<option value="0">False</option> ' +
                '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Test Step Type:</b></label><br>' +
                '<select id="step_type" name="step_type">' +
                    '<option value="0" selected="selected">Select from the below choices:</option>' +
                    '<option value="1">Automated</option> ' +
                    '<option value="2">Manual</option>' +
                    '<option value="3">Performance</option> ' +
                '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Driver:</b></label><br>' +
            '<input type="text" id="step_driver" name="step_driver" placeholder="Enter the driver">' +
        '</div><br>'
    );
    $("#step_name").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"TestStep_Auto",
                dataType:"json",
                data:{term:request.term},
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
            if(value!=""){
                $("#step_name").val(value);
                $.ajax({
                    url:"Populate_info_div",
                    dataType:"json",
                    data:{term:value},
                    success:function(data){
                        //info_div(data[0]);
                        var row=data[0];
                        $("#step_desc").val(row[2]);
                        $("#step_driver").val(row[3]);
                        if(row[5]==null){
                            $("#step_data").val(0);
                        }
                        if(row[5]==true){
                            $("#step_data").val(1);
                        }
                        if(row[4]=="manual"){
                            $("#step_type").val(2);
                        }
                        if(row[4]=="automated"){
                            $("#step_type").val(1);
                        }
                        if(row[4]=="performance"){
                            $("#step_type").val(3);
                        }
                        $("#step_feature").val(row[6]);
                    }
                });
                return false;
            }
        }
    });
}
function populate_footer_div(){
    $('#footer_div').append('' +
        '<div>' +
            '<input type="button" id="delete_button" value="Delete"/>' +
            '<input type="button" id="get_cases" value="Get Test Cases"/>' +
            '<input type="submit" id="submit_button" name="submit_button" value="Submit">' +
        '</div>'
    );
    $("#get_cases").click(function(){
        var UserText=$("#step_name").val();
        console.log(UserText);
        Env = "PC"
        $.get("TestCase_Results",{Query: UserText, Env: Env},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#search_result').children().remove();
                $('#search_result').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                //$("#DepandencyCheckboxes").children().remove();
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                ResultTable('#search_result',data['Heading'],data['TableData'],"Test Cases");

                $("#search_result").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);

                // add edit btn
                var indx = 0;
                $('#search_result tr>td:nth-child(2)').each(function(){
                    var ID = $("#search_result tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonCustom" id="'+ID+'" src="/site_media/template.png" height="50"/>');
                    $(this).after('<img class="editBtn buttonCustom" id="'+ID+'" src="/site_media/edit_case.png" height="50"/>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Create/'+ $(this).attr("id");
                });
                VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                $(".Buttons[title='Select User']").fadeOut();
            }

        });

    });
}
function info_div(data){

}