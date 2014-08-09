/**
 * Created by J on 6/15/14.
 */
$(document).ready(function(){

    var user = $(".welcome").text();
    $(".logged_user").text($.session.get('fullname'));
    $(".test_count").text($.session.get('testing'));

    /*$("#GetAssignedTests").click(function(){
        $.get("GetAssignedTasks",{user : user},function(data)
        {
            //$("#test_count").text(data['TableData'].length);
            ResultTable(ass_tasks,data['Heading'],data['TableData'],"Assigned Tasks");
        });
    });*/

    /*$.get("GetAssignedTests",{user : user},function(data)
    {
        $("#test_count").text(data['TableData'].length);
        //ResultTable(ass_tasks,data['Heading'],data['TableData'],"Assigned Tasks");
    });*/

    /*$("#assigned_tasks").click(function(){
        $("#task_prompt").html(
            '<p style="text-align: center">You have selected ' +
                tc_id +'-'+ tc_name + '.' +
                '<br/> What do you want to do?' +
                '</p>' +
                '<div style="padding-left: 15%">' +
                '<a class="github" href="/Home/ManageTestCases/Edit/'+tc_id+'">Edit</a>' +
                '<a class="twitter" href="/Home/ManageTestCases/CreateNew/'+tc_id+'">Copy</a>' +
                '<a class="dribble" href="#" rel="modal:close">Close</a>' +
                '</div>'

        );
        $("#task_prompt").modal();
        $.get("GetAssignedTests",{user : user},function(data)
        {
            ResultTable(task_prompt,data['Heading'],data['TableData'],"Assigned Tasks");

        });
    });*/
});