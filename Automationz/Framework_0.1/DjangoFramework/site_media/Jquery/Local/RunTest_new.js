var platform_list=[
    {
        plaform:"Windows",
        value:"PC"
    },
    {
        plaform:"Mac",
        value:"Mac"
    }
];
$(document).ready(function(){
    PlatformSelect();
    AutoCompleteTestCases();
    DeleteFilterData();
    PressRunButton();
    ManageTestMachine();
});
function PressRunButton(){
    $('#run_test').click(function(){
        RunTest();
    });
}
function RunTest(){
    var RunTestQuery="";
    $("#searchedFilter").each( function()
    {
        RunTestQuery = $(this).find("td").text();
        RunTestQuery = RunTestQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
    });
    if(RunTestQuery.length==0){
        alertify.log("Test Case Filters is to be selected from Test Case Selection Tab","",0);
        return false;
    }
    //Get the browser selection
    var client="";
    client=$('input[name="dependency"]:checked').val();
    if (client==""){
        alertify.log("Dependency is to be selected from Parameter Tab","",0);
        return false;
    }
    client=client.trim()+":";
    client=client.trim();
    RunTestQuery=RunTestQuery.trim()+(" "+client);
    RunTestQuery=RunTestQuery.trim();
    var TesterQuery="";
    $("#tester").each( function()
    {
        TesterQuery = $(this).find("td").text();
        TesterQuery = TesterQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
    });
    if(TesterQuery.length==0){
        alertify.log("Testers is to be selected from suggestion","",0);
        return false;
    }
    var EmailQuery="";
    $("#email").each( function()
    {
        EmailQuery = $(this).find("td").text();
        EmailQuery = EmailQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
    });
    if(EmailQuery.length==0){
        alertify.log("Email Receipient is to be selected from suggestion","",0);
        return false;
    }
    var TestObjective=$('#testObjective').val().trim();
    if(TestObjective==""){
        alertify.log("Test Objective is empty","",0);
        return false;
    }
    var milestoneQuery="";
    $("#milestone").each( function()
    {
        milestoneQuery = $(this).find("td").text();
        milestoneQuery = milestoneQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
    });
    if(milestoneQuery.length==0){
        alertify.log("Milestone is to be selected from suggestion","",0);
        return false;
    }
    var machineQuery="";
    $("#machine").each( function()
    {
        machineQuery = $(this).find("td").text();
        machineQuery = machineQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
    });
    if(machineQuery.length==0){
        alertify.log("Machine is to be selected from suggestion","",0);
        return false;
    }
    RunTestQuery=RunTestQuery.trim()+" "+machineQuery;
    RunTestQuery=RunTestQuery.trim();
    var Env = GeneratePlatform();
    console.log(RunTestQuery);
    console.log(TesterQuery);
    console.log(EmailQuery);
    console.log(client);
    console.log(TestObjective);
    console.log(milestoneQuery);
    console.log(Env);
    var project_id=$('#project_identity option:selected').val().trim();
    var team_id=$('#default_team_identity option:selected').val().trim();
    $.get("Run_Test",
        {
            RunTestQuery : RunTestQuery,
            TesterIds:TesterQuery,
            EmailIds:EmailQuery,
            DependencyText:client,
            TestObjective:TestObjective,
            TestMileStone:milestoneQuery,
            Env: Env,
            project_id:project_id,
            team_id:team_id
        },
        function(data)
        {

            //MsgBox("Test Run Response",	"Your Test Run Request Has Been Submitted, Here is the result :"+ data['Result']);
            // alert(data['Result']);
            if(data['Result']){
                run_notify("RunID-'"+data['runid']+"' got executed!");
                var location='/Home/RunID/'+data['runid']+'/';
                window.location=location;
            }
            else{
                MsgBox("Test Run Response",	"Your Test Run Request Has Been Submitted, Here is the result :"+ data['Result']);
        }

    });
    return false;
}
function ManageTestMachine(){
    $.get("GetOS",
        {
            os:''
        },
        function(data){
            console.log(data['os']);
            console.log(data['browser']);
            console.log(data['productVersion']);
            populate_manual_test_div(data['os'],data['browser'],data['productVersion']);
        });
}
function populate_manual_test_div(environment,browserdata,productVersion){
    //populate the os names
    var message="";
    console.log(environment);
    for(var i=0;i<environment.length;i++){
        //console.log(message);
        message+='<option value="'+environment[i][0].trim()+'">'+environment[i][0]+'</option>';
    }
    $('#os_name').append(message);
    message="";
    for(var i=0;i<browserdata.length;i++){
        message+='<option value="'+browserdata[i][0].trim()+'">'+browserdata[i][0]+'</option>'
    }
    $('#browser').append(message);
    message="";
    for(var i=0;i<productVersion.length;i++){
        message+='<option value="'+productVersion[i].trim()+'">'+productVersion[i].trim()+'</option>'
    }
    $('#product_version').append(message);
    $('#os_name').live('change',function(){
        if($('#os_name').val()!=''){
            console.log($(this).val());
            var message="";
            for(var i=0;i<environment.length;i++){
                if($(this).val()==environment[i][0].trim()){
                    console.log(environment[i][1]);
                    var os_version=environment[i][1];
                    for(var j=0;j<os_version.length;j++){
                        message+='<option value="'+os_version[j]+'">'+os_version[j]+'</option>'
                    }
                }
            }
            $('#os_version').html(message);
            $('#version_bit').css({'display':'inline-block'});
        }
        else{
            $('#os_version').html("");
            $('#version_bit').css({'display':'none'});
        }
    });
    $('#browser').live('change',function(){
        if($('#browser').val()!=''){
            var message="";
            for(var i=0;i<browserdata.length;i++){
                if($(this).val()==browserdata[i][0].trim()){
                    browser_version=browserdata[i][1];
                    for(var j=0;j<browser_version.length;j++){
                        message+='<option value="'+browser_version[j].trim()+'">'+browser_version[j].trim()+'</option> '
                    }
                }
            }
            $('#browser_version').html(message);
            $('#b_version').css({'display':'inline-block'});
        }
        else{
            $('#browser_version').html("");
            $('#b_version').css({'display':'none'});
        }
    });
    AutoCompletionButton(environment,browserdata);
}
function AutoCompletionButton(environment,browserdata){
    //console.log('into the AutoCompleteing');
    $("#machine_name").autocomplete({
        source:function(request,response){
            $.ajax({
                url:"Auto_MachineName",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value = ui.item[0];
            console.log(value);
            if(value!=""){
                $("#machine_name").val(value);
                $.get("CheckMachine",{name:value},function(data){
                    console.log(data[0]);
                    var list=data[0];
                    $('#os_name').val(list[0]);
                    for(var i=0;i<environment.length;i++){
                        var message="";
                        if($('#os_name').val()==environment[i][0]){
                            for(var j=0;j<environment[i][1].length;j++){
                                message+='<option value="'+environment[i][1][j].trim()+'">'+environment[i][1][j]+'</option> '
                            }
                            $('#os_version').html(message);
                            break;
                        }
                    }
                    $('#os_version').val(list[1]);
                    $('#os_bit').val(list[2]);
                    $('#version_bit').css({'display':'inline-block'});
                    $('#machine_ip').val(list[3]);
                    var browsers=list[4].split(";")[0].split("(");
                    for(var i=0;i<browserdata.length;i++){
                        var message="";
                        if(browsers[0].trim()==browserdata[i][0]){
                            var browser_version=browserdata[i][1];
                            for(var j=0;j<browser_version.length;j++){
                                message+='<option value="'+browser_version[j].trim()+'">'+browser_version[j]+'</option> ';
                            }
                            $('#browser_version').html(message);
                            $('#browser_version').val(browsers[1]);
                            break;
                        }
                    }
                    $('#b_version').css({'display':'inline-block'});
                    $('#browser').val(browsers[0].trim());
                    $('#product_version').val(list[5]);
                    console.log(browsers);
                })
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };
    $('#machine_name').live('click',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#os_name').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#os_version').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#os_bit').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#machine_ip').live('click',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#browser').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");

    });
    $('#browser_version').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#product_version').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#submit_button').live('click',function(){
        var machine_name=$('#machine_name').val();
        var os_name=$('#os_name option:selected').val();
        var os_version=$('#os_version option:selected').val();
        var os_bit=$('#os_bit option:selected').val();
        var browser=$('#browser option:selected').val();
        var browser_version=$('#browser_version option:selected').val();
        var machine_ip=$('#machine_ip').val();
        var product_version=$('#product_version option:selected').val();
        if(machine_name==''||os_name==''||browser==''||machine_ip==''||product_version==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_message').html(error_message);
            $('#error_message').css({'display':'block'});
        }
        else{
            $.get("AddManualTestMachine",{
                machine_name:machine_name,
                os_name:os_name,
                os_version:os_version,
                os_bit:os_bit,
                browser:browser,
                browser_version:browser_version,
                machine_ip:machine_ip,
                product_version:product_version
            },function(data){
                //console.log(data);
                alertify.log(""+data+"","",0);
                machine_notify(""+data+"");
                $('#error_message').html('<b style="color: #109F40">'+data+'<br>Page will be refreshed to change effect</b>');
                $('#error_message').slideDown('slow');
                //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                window.location = '/Home/RunTest/';
            });
        }
    });
}
function machine_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('submit_button');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Manual Test Machine Added!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Manual Test Machine Added!",{body:message, icon:"/site_media/noti.ico"});
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
function run_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('run_test');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Run Executed!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Run Executed!",{body:message, icon:"/site_media/noti.ico"});
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
function FilterData(){
    $('.dependency').click(function(){
       var client=$(this).val();
       client=client.trim()+":";
       FilterByDependency(GeneratePlatform(),client.trim());
    });
}
function PlatformSelect(){
    $('.buttonPic').click(function(){
       var selected_id=$(this).attr('id').trim();
       var platform_name=$('#'+selected_id).find('table:eq(0)').find('td:nth-child(2)').text().trim();
       $('.buttonPic').css({'display':'none'});
       $('#'+selected_id).css({'height':'200%','width':'50%'});
       $('#'+selected_id).css({'display':'block'});
       $('#msg').find('a:eq(0)').text(platform_name+ " Platfrom is selected");
       AvailableMachine();
    });
}
function AvailableMachine(){
    var Env = GeneratePlatform();
    var SearchUser = "True"
    $.get("Table_Data_UserList",{UserListRequest : SearchUser, Env: Env},function(data) {
        ResultTable('#available_machine', data['Heading'],data['TableData'], "Available User(s)", "Number of users available");
    });
}
function AutoCompleteTestCases(){
    $('#searchbox').autocomplete({
        source : function(request, response) {
            var Env=GeneratePlatform();
            $.ajax({
                url:"AutoCompleteTestCasesSearch",
                dataType: "json",
                data:{ term: request.term, Env: Env },
                success: function( data ) {
                    response( data );
                }
            });
        },
        select : function(event, ui) {
            var tc_id_name = ui.item[0].split(" - ");
            console.log(tc_id_name);
            var value = "";
            if (tc_id_name != null)
                value = tc_id_name[0]
            console.log(value);
            var platform=GeneratePlatform();
            if(value!=""){
                $("#searchedFilter").append('<td><img class="delete" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td name = "submitquery" class = "Text" style = "size:10">'
                    + value
                    + ":&nbsp"
                    + '</td>');
                PerformSearch(platform);
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };
    $("#assigned_tester").autocomplete({

        source : 'AutoCompleteTesterSearch',
        select : function(event, ui) {

            var value = ui.item.value
            $("#tester").append('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text">'
                + value
                + ":&nbsp"
                + '</td>');

            //$("#tester th").css('display', 'block');

            $("#assigned_tester").val("");
            return false;

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
    $("#email_list").autocomplete({

        source : 'AutoCompleteEmailSearch',
        select : function(event, ui) {

            var value = ui.item.value
            $("#email").append('<td><img class="delete" id = "DeleteEmail" title = "EmailDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text">'
                + value
                + ":&nbsp"
                + '</td>');

            //$("#SelectedEmail th").css('display', 'block');

            $("#email_list").val("");
            return false;

        }
    });

    $("#email_list").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });


    //Delete Seleted Email Ids
    $("#DeleteEmail").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
    $('#milestone_list').autocomplete({
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
                    + ":&nbsp"
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

    });

    $("#machine_list").autocomplete({

        //source : 'AutoCompleteUsersSearch',

        source : function(request, response) {
            var Env = GeneratePlatform();
            $.ajax({
                url:"AutoCompleteUsersSearch",
                dataType: "json",
                data:{ term: request.term, Env: Env },
                success: function( data ) {
                    response( data );
                }
            });
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                //$(this).val(value.trim());
                $("#machine").html('<td><img class="delete" id = "DeleteMachine" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text">'
                    + value
                    + ":&nbsp"
                    + '</td>');

                //$("#MileStoneHeader th").css('display', 'block');

                $("#milestone_list").val("");
                $('#run_test').slideDown("slow");
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $("#DeleteMachine").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();
        $('#run_test').slideUp("slow");

    });
}
function GeneratePlatform(){
    var selected_plaform="";
    var Env="";
    $('.buttonPic').each(function(){
        if($(this).css('display')=='block'){
            selected_plaform=$(this).find('table:eq(0)').find('td:nth-child(2)').text().trim();
        }
    });
    for (var i=0;i<platform_list.length;i++){
        if(platform_list[i].plaform==selected_plaform){
            Env=platform_list[i].value;
        }
    }
    return Env;
}
function FilterByDependency(Env,client){
    $("#searchedFilter").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "");
        UserText+=(" "+client);
        $.get("Table_Data_TestCases",{Query: UserText, Env: Env},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#RunTestResultTable').children().remove();
                $('#RunTestResultTable').html('<p align="center" style="font-size:150%;font-weight: bold;color:#003bb3;">There is no test cases for this filter</p>');
                $('#timeRequired').fadeOut(500);
                $('#timeRequired').html("");

            }
            else
            {
                ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

                $("#RunTestResultTable").fadeIn(1000);
                var message=('<p align="center" style="font-size:150%;font-weight: bold;color:#003bb3;">TimeRequired:&nbsp;&nbsp;<b style="font-size: 150%;font-weight:bolder; color: #000000;">'+data['TimeEstimated']+'</b></p>');
                $('#timeRequired').html(message);
                $('#timeRequired').fadeIn(1000);
                implementDropDown('#RunTestResultTable');
                //VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                //$(".Buttons[title='Select User']").fadeOut();
            }

        });

    });
}
function PerformSearch(Env){
    $("#searchedFilter").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get("Table_Data_TestCases",{Query: UserText, Env: Env},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#RunTestResultTable').children().remove();
                $('#RunTestResultTable').html('<p align="center" style="font-size:150%;font-weight: bold;color:#003bb3;">There is no test cases for this filter</p>');
                $('#timeRequired').fadeOut(500);
                $('#timeRequired').html("");

            }
            else
            {
                ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

                $("#RunTestResultTable").fadeIn(1000);
                var message=('<p align="center" style="font-size:150%;font-weight: bold;color:#003bb3;">TimeRequired:&nbsp;&nbsp;<b style="font-size: 150%;font-weight:bolder; color: #000000;">'+data['TimeEstimated']+'</b></p>');
                $('#timeRequired').html(message);
                $('#timeRequired').fadeIn(1000);
                implementDropDown('#RunTestResultTable');
                VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                //$(".Buttons[title='Select User']").fadeOut();
            }

        });

    });
}
function VerifyQueryProcess(){
    $("#searchedFilter").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        var Env = GeneratePlatform();
        $.get("Verify_Query", {Query : UserText, Env: Env}, function(data) {
            console.log(data);
            var list=data['DepandencyList'];
            var message="";
            for(var i=0;i<list.length;i++){
                for(var j=1;j<list[i].length;j++){
                    message+=('<td><input name="dependency" class="dependency" value="'+list[i][j].trim()+'" type="radio"/></td><td><b class="Text">'+list[i][j]+'</b></td>');
                }
            }
            $('#dependency').html(message);
            $('#dependency_label').css({'display':'block'});
            $('#dependency').css({'display':'block'});
            FilterData();
        });
    });
};
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
    $('#searchedFilter td .delete').live('click',function(){
        $(this).parent().next().remove();
        $(this).remove();
        PerformSearch(GeneratePlatform());
    });
}