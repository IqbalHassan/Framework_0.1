$(document).ready(function(){
    $("#create_edit").click(function(event){
        //event.preventDefault();
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
            '<input type="text" placeholder="Enter the test set name" name="step_name"/>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Test Step Description:</b></label><br>' +
            '<textarea rows="2" cols="35" name="step_desc" placeholder="Describe the test step(within 180 letters)"></textarea>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Feature:</b></label><br>' +
            '<input type="text" name="test_feature" placeholder="Enter the feature"/>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Data Requirement:<b></label><br>' +
                '<select name="step_data">' +
                    '<option value="3" selected="selected">Select from the below choices:</option>' +
                    '<option value="1">True</option>' +
                    '<option value="0">False</option> ' +
                '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Test Step Type:</b></label><br>' +
                '<select name="step_type">' +
                    '<option value="0" selected="selected">Select from the below choices:</option>' +
                    '<option value="1">Automated</option> ' +
                    '<option value="2">Manual</option>' +
                    '<option value="3">Performance</option> ' +
                '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
            '<label><b>Driver:</b></label><br>' +
            '<input type="text" name="step_driver" placeholder="Enter the driver">' +
        '</div><br>'
    );
}
function populate_footer_div(){
    $('#footer_div').append('' +
        '<div>' +
            '<input type="button" id="delete_button" value="Delete"/>' +
            '<input type="button" id="get_cases" value="Get Test Cases"/>' +
            '<input type="submit" id="submit_button" name="submit_button" value="Submit">' +
        '</div>');
}