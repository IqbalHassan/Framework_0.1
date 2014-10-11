/**
 * Created by J on 9/1/14.
 */

var operation = 1;
var bugid;

$(document).ready(function(){

    ActivateNecessaryButton();
    ButtonSet();
    BugSearchAuto();
    TestCaseLinking();

    $('.scrollbox1').enscroll({
        verticalTrackClass: 'track1',
        verticalHandleClass: 'handle1',
        drawScrollButtons: true,
        scrollUpButtonClass: 'scroll-up1',
        scrollDownButtonClass: 'scroll-down1'
    });


    $("#submit").live('click',function(){

        var project = $("#project_identity").val();
        var bug_desc=$("#bug_desc").val();
        var start_date=$('#start_date').val();
        var end_date=$('#end_date').val();
        var team=$("#default_team_identity").val();
        var priority= 'P' + $('#priority').val();
        var milestone=$("#milestone").val();
        var title=$('#title').val();
        //var creator = $("#created_by").val();
        var testers= $("#tester").text();
        /*$('.selected').each(function(){
            testers.push($(this).text().trim());
        });*/
        var status = $('#status').val();

        var test_cases=[];
        $('input[name="test_cases"]:checked').each(function(){
            test_cases.push($(this).val());
        });

        var labels=[];
        $('input[name="labels"]:checked').each(function(){
            labels.push($(this).val());
        });


        if(title!=""){
            if(operation==1){
                $.get("LogNewBug/",{
                    title:title.trim(),
                    description:bug_desc.trim(),
                    status:status.trim(),
                    start_date:start_date.trim(),
                    end_date:end_date.trim(),
                    team:team.trim(),
                    tester:testers,
                    priority:priority.trim(),
                    milestone:milestone.trim(),
                    project_id: project.trim(),
                    user_name:$.session.get('fullname'),
                    test_cases:test_cases.join("|"),
                    labels:labels.join("|")
                    //created_by:creator.trim()
                },function(data){
                    bug_notify("Bug Created!", "Bug with title '"+title+"' is created!","/site_media/noti.ico");
                    window.location='/Home/ManageBug/';
                });
            }
            else if(operation==2){
                $.get("ModifyBug/",{
                    bug_id:bugid,
                    title:title.trim(),
                    description:bug_desc.trim(),
                    status:status.trim(),
                    start_date:start_date.trim(),
                    end_date:end_date.trim(),
                    team:team.trim(),
                    tester:testers,
                    priority:priority.trim(),
                    milestone:milestone.trim(),
                    project_id: project.trim(),
                    user_name:$.session.get('fullname'),
                    test_cases:test_cases.join("|"),
                    labels:labels.join("|")
                    //created_by:creator.trim()
                },function(data){
                    bug_notify("Bug Modified!", "Bug with title '"+title+"' is modified!","/site_media/noti.ico");
                    window.location='/Home/ManageBug/';
                });
            }
        }
        else{
            alertify.log("Title is empty","",0);
        }

        /*if(operation=="0"||title==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_milestone').html(error_message);
            $('#error_milestone').css({'display':'block'});
        }
        else {
            var title_msg = "Bug Created!";

            $.get('BugOperation',{
                operation:operation,
                title:title.trim(),
                description:bug_desc.trim(),
                status:status.trim(),
                start_date:start_date.trim(),
                end_date:end_date.trim(),
                team:team.trim(),
                tester:testers.join("|").trim(),
                priority:priority.trim(),
                milestone:milestone.trim(),
                project_id: project.trim(),
                user_name:$('#user_name').text().trim(),
                created_by:creator.trim()
            },function(data){
                if(data['confirm_message']==""){
                    var color='red';
                    alertify.log(""+data['error_message']+"","",0);
                    milestone_notify(""+data['error_message']+"",""+data['error_message']+"","/site_media/noti2.ico");
                    $('#error_milestone').html('<b style="color:red;">'+data['error_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/ManageBug/';
                }
                else{
                    var color='green';
                    alertify.log(""+data['confirm_message']+"","",0);
                    milestone_notify(title_msg,""+data['confirm_message']+"","/site_media/noti.ico");
                    $('#error_milestone').html('<b style="color:green;">'+data['confirm_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/CreateBug/';
                }

            })
        }*/
    });
});

function BugSearchAuto(){
    $('#title').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"BugSearch",
                dataType:"json",
                data:{
                    term:request.term
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(event,ui){
            var bug_id=ui.item[0].trim();
            var bug_name=ui.item[1].trim();
            if(bug_id!=""){
                $(this).val(bug_name);
                operation = 2;
                bugid = bug_id;
                PopulateBugInfo(bug_id);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] +"<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };
}

function PopulateBugInfo(bug_id){
    $.get("Selected_BugID_Analaysis",{Selected_Bug_Analysis : bug_id},function(data){
        $("#bug_desc").val(data['Bug_Info'][0][2]);
        $("#start_date").val(data['Bug_Info'][0][3]);
        $("#end_date").val(data['Bug_Info'][0][4]);
        $("#tester").html('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
        + '<td class="Text selected">'
        + data['tester']
            //+ "&nbsp"
        + '</td>');
        $('#status').val(data['Bug_Info'][0][11]);
        if(data['Bug_Info'][0][5]=='P1')
            $('#priority').val('1');
        else if(data['Bug_Info'][0][5]=='P2')
            $('#priority').val('2');
        else if(data['Bug_Info'][0][5]=='P3')
            $('#priority').val('3');
        else if(data['Bug_Info'][0][5]=='P4')
            $('#priority').val('4');
        $('#milestone').val(data['Bug_Info'][0][6]);
        $("#ms_info").show();
        $("#created_by").text(data['Bug_Info'][0][7]);
        $("#created_date").text(data['Bug_Info'][0][8]);
        $("#modified_by").text(data['Bug_Info'][0][9]);
        $("#modified_date").text(data['Bug_Info'][0][10]);


        $('input[name="labels"]').each(function(){
            $(this).prop('checked',false);
        });
        $('input[name="labels"]').each(function(){
           if(data['Bug_Labels'].indexOf($(this).val())>-1){
               $(this).prop('checked',true);
           }
        });

        $(".linking").html("");
        $(data['Bug_Cases']).each(function(i){
            $(".linking").append('<tr>' +
            '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
            + '<td>'
            + '<input type="checkbox" checked="true" name="test_cases" value="'
            + data['Bug_Cases'][i][0]
            + '"/>' +
            '</td><td>'
            + data['Bug_Cases'][i][1]
            + "</td>" +
            "</tr>");
        });

        $("#suggestion").show();
        $("#normal_sugg").hide();

        $(data['Failed_Cases']).each(function(i){
            $("#nobug_failed").append('<tr>' +
            '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
            + '<td>'
            + '<input type="checkbox" name="test_cases" value="'
            + data['Failed_Cases'][i][0]
            + '"/>' +
            '</td><td>'
            + data['Failed_Cases'][i][1]
            + "</td>" +
            '<td></td>' +
            '<td></td>' +
            '<td>' +
            data['Failed_Cases'][i][2] +
            '</td>' +
            "</tr>");
        });

    });

}

function TestCaseLinking(){

    $(".search_case").autocomplete({

        source:function(request,response){
            $.ajax({
                url:"AutoCompleteTestCasesSearchOtherPages",
                dataType:"json",
                data:{
                    term:request.term
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select : function(event, ui) {

            //var value = ui.item[0]
            //var name = ui.item[1]

            var tc_id_name = ui.item[0].split(" - ");
            var value = "";
            if (tc_id_name != null)
            {
                value = tc_id_name[0].trim();
                name = tc_id_name[1].trim();
            }

            if(value!=""){
                $(".linking").append('<tr>' +
                '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
                + '<td>'
                + '<input type="checkbox" checked="true" name="test_cases" value="'
                + value
                + '"/>' +
                '</td><td>'
                + name
                + "</td>" +
                "</tr>");
            }

            //$(".search_case").remove();

            /*$("#test_cases").append('<tr class="linking">' +
                '<td><input class="search_case textbox" placeholder="Search Test Case" style="width: auto" /></td>' +
            '</tr>');
            TestCaseLinking();*/

            //$("#tester th").css('display', 'block');

            $(".search_case").val("");
            return false;

        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };

    $(".search_case").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteCase").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
}

function PerformSearch() {
    $("#AutoSearchResult #searchedtext").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("TableDataTestCasesOtherPages",{
            Query: UserText,
            project_id:$('#project_identity option:selected').val().trim(),
            team_id:$('#default_team_identity option:selected').val().trim()
        },function(data) {

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
                $('#RunTestResultTable tr>td:nth-child(6)').each(function(){
                    var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25"/>');
                    $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25"/>');

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


function ButtonSet(){

    $("#assigned_tester").autocomplete({

        source:function(request,response){
            $.ajax({
                url:"AutoCompleteTesterSearch",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select : function(request, ui, item) {

            var value = ui.item.value
            if(value!=''){
                $("#tester").html('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text selected">'
                    + value
                    //+ "&nbsp"
                    + '</td>');

                //$("#tester th").css('display', 'block');

                $("#assigned_tester").val("");
                return false;
            }

        }
    });
    $("#assigned_tester").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteTester").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();
    });
    /*$('#milestone_list').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"AutoMileStone",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                //$(this).val(value.trim());
                $("#milestone").html('<td><img class="delete" id = "DeleteMileStone" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text">'
                    + value
                    //+ "&nbsp"
                    + '</td>');

                //$("#MileStoneHeader th").css('display', 'block');

                $("#milestone_list").val("");
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $("#milestone_list").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteMileStone").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });*/
}
function ActivateNecessaryButton(){
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#start_date').datepicker("option", "showAnim", "slide" );
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#end_date').datepicker("option", "showAnim", "slide" );
    $(".selectdrop").selectBoxIt();
}


function bug_notify(title_msg,message,icon){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('submit');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification(title_msg,{body:message, icon:icon});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification(title_msg,{body:message, icon:icon});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }


}

function PerformSearch() {
    $("#AutoSearchResult #searchedtext").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("TableDataTestCasesOtherPages",{
            Query: UserText,
            project_id:$('#project_identity option:selected').val().trim(),
            team_id:$('#default_team_identity option:selected').val().trim()
        },function(data) {

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
                $('#RunTestResultTable tr>td:nth-child(6)').each(function(){
                    var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25"/>');
                    $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25"/>');

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