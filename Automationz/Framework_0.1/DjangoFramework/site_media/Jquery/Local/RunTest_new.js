var dependency_list=[];
var global_version_list=[];
var dependency_classes=[];
var test_cases="";

var lowest_feature = 0;
var isAtLowestFeature = false;
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd" });
    AutoSuggestions(project_id,team_id);
    RunAutoCompleteTestSearch(project_id,team_id);
    DeleteSearchQueryText(project_id,team_id);
    ManageMilestone(project_id,team_id);
    SubmitRun(project_id,team_id);
    /*$('.edit_machine').on('click',function(){
        $('.tabs-div').removeClass('responsive-tabs__panel--active');

        $('.tabs-div').removeClass('responsive-tabs__list__item--active');
        $('.tabs-div').attr('aria-hidden','true');
        //$('.tabs-div').hide();

        $('.tabs-dive').prev().addClass('responsive-tabs__heading--active');
        $('.tabs-div:last').addClass('responsive-tabs__panel--active');
        $('.tabs-div:last').attr('aria-hidden','false');

        $('.tabs-div:last').addClass('responsive-tabs__list__item--active');
        //$('.tabs-div:last').show();
        $('.tabs-dive:last').prev().addClass('responsive-tabs__heading--active');
    });*/
    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val().trim());
        window.location.reload(true);
    });
    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val().trim());
        window.location.reload(true);
    });
});
function SubmitRun(project_id,team_id){
    $('#run_test').on('click',function(){
        var UserText="";
        if(test_cases){
            $("#AutoSearchResult #searchedtext").each(function() {
                UserText = $(this).find("td").text();
                UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "");
            });
            console.log(UserText);
        }
        else{
            alertify.error('No Test cases selected',1500);
            return false;
        }

        var temp=[]
        var message="";
        for(var i=0;i<dependency_classes.length;i++){
            if($('.'+dependency_classes[i].name+':checked').length>0){
                if(temp.indexOf($('.'+dependency_classes[i].name+':checked').val().trim())>-1){
                    continue;
                }
                else{
                    temp.push($('.'+dependency_classes[i].name+':checked').val().trim());
                }
            }
            else{
                alertify.error('No '+dependency_classes[i].name+' is selected',1500);
                return false;
            }
        }
        for(var i=0;i<temp.length;i++){
            message+=(temp[i].trim()+': ');
        }
        console.log(message);
        var start_date=$('#start_date').val();
        if(start_date==undefined){
            alertify.log("Starting Date Must be selected","",0);
            return false;
        }
        var end_date=$('#end_date').val();
        if(end_date==undefined){
            alertify.log("Ending Date Must be selected","",0);
            return false;
        }
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
        var RunTestQuery=UserText+message+machineQuery;
        $.get("Run_Test",
            {
                RunTestQuery : RunTestQuery,
                TesterIds:TesterQuery,
                EmailIds:EmailQuery,
                TestObjective:TestObjective,
                TestMileStone:milestoneQuery,
                project_id:project_id,
                team_id:team_id,
                //feature_path:newFeaturePath,
                start_date:start_date,
                end_date:end_date
            },
            function(data)
            {
                if(data['Result']){
                    //run_notify("RunID-'"+data['runid']+"' got executed!");
                    var location='/Home/RunID/'+data['runid']+'/';
                    window.location=location;
                }
                else{
                    MsgBox("Test Run Response",	"Your Test Run Request Has Been Submitted, Here is the result :"+ data['Result']);
                }

            });
    });
}
function AutoSuggestions(project_id,team_id){
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
            $.ajax({
                url:"AutoCompleteUsersSearch",
                dataType: "json",
                data:{ term: request.term,project_id:project_id,team_id:team_id},
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

function RunAutoCompleteTestSearch(project_id,team_id){
    $("#searchbox").autocomplete(
        {
            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearchOtherPages",
                    dataType: "json",
                    data:{ term: request.term,project_id:project_id,team_id:team_id},
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
                    PerformSearch(project_id,team_id);
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

function PerformSearch(project_id,team_id,predicate) {

    $("#AutoSearchResult #searchedtext").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        console.log(UserText);
        if(predicate!=undefined){
            UserText=UserText+predicate;
        }
        $.get("TableDataTestCasesOtherPages",{
            Query: UserText,
            test_status_request:true,
            project_id:project_id,
            team_id:team_id,
            total_time:'true'
        },function(data) {
            if (data['TableData'].length == 0)
            {
                $('#RunTestResultTable').html("");
                $('#RunTestResultTable').html("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $("#RunTestResultTable").fadeIn(1000);
                $('#time_panel').html("");
                $('#time_panel').css({'display':'none'});
                test_cases=false;
            }
            else
            {
                $('#time_panel').html('<b class="Text">Time Needed: '+data['time']+'</b> ');
                $('#time_panel').css({'display':'block'});
                ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");
                $("#RunTestResultTable").fadeIn(1000);
                test_cases=true;
                implementDropDown("#RunTestResultTable");
                if(predicate==undefined){
                    get_dependency(project_id,team_id,UserText);
                }


            }
        });
    });
}
function populate_parameter_div(array_list,div_name,project_id,team_id){
    var message="";
    for(var i=0;i<array_list.length;i++){
        var dependency=array_list[i][0];
        message+='<form id="tc_'+dependency+'" class="new_tc_form">';
        message+='<table>';
        message+='<tr>';
        message+='<td class="tc_form_label_col">'
        message+='<b class="Text">'+dependency+':</b>';
        message+='</td>';
        message+='<td class="tc_form_input_col">';
        message+='<table width="100%">';
        var equal_size=(100/array_list[i][1].length);
        var dep_name=[];
        message+='<tr>';
        for(var j=0;j<array_list[i][1].length;j++){
            message+='<td width="'+equal_size+'%">';
            message+='<input class="'+dependency+'" id="'+dependency+'_'+array_list[i][1][j]+'" type="radio" name="type" value="'+array_list[i][1][j]+'" style="width:auto" />';
            message+='<label for="'+dependency+'_'+array_list[i][1][j]+'">'+array_list[i][1][j]+'</label>';
            message+='</td>';
            dep_name.push(dependency+'_'+array_list[i][1][j]);
        }
        message+='</tr>';
        message+='</table>';
        message+='</td>';
        message+='<tr>';
        message+='</table>';
        message+='</form>';
        var temp={'name':dependency,'list':dep_name};
        dependency_classes.push(temp);
    }
    $('#'+div_name).html(message);
    for(var i=0;i<dependency_classes.length;i++){
        for(var j=0;j<dependency_classes[i].list.length;j++){
            $('#'+dependency_classes[i].list[j]).on('click',function(){
               PerformSearch(project_id,team_id,parseValue(dependency_classes));
            });
        }
    }
}
function parseValue(dependency_classes){
    var message="";
    for(var i=0;i<dependency_classes.length;i++){
        $('.'+dependency_classes[i].name+':checked').each(function(){
           message+=($(this).val().trim()+': ');
        });
    }
    return message;
}
function get_dependency(project_id,team_id,UserText){
    $.get('specific_dependency_settings',{
        Query: UserText,
        project_id:project_id,
        team_id:team_id
    },function(data){
        populate_parameter_div(data,"parameter_div",project_id,team_id);
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
function DeleteSearchQueryText(project_id,team_id){
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
        PerformSearch(project_id,team_id);

    });
}

function ManageMilestone(project_id,team_id){
    $.get('GetOS',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        dependency_list=data['dependency_list'];
        global_version_list=data['version_list'];
        populate_manual_div(dependency_list,global_version_list,project_id,team_id);
    });
}

function populate_manual_div(dependency_list,global_version_list,project_id,team_id){
    var message="";
    message+='<tr>';
    message+='<td align="right"><b class="Text">Machine Name:</b></td>';
    message+='<td align="left"><input class="textbox" id="machine_name"  placeholder="Machine Name Here.."></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Machine IP:</b></td>';
    message+='<td align="left"><input class="textbox" id="machine_ip"  placeholder="Machine IP Here.."></td>';
    message+='</tr>';
    for(var i=0;i<dependency_list.length;i++){
        message+='<tr>';
        message+='<td align="right"><b class="Text">'+dependency_list[i][0]+':</b></td>';
        message+='<td align="left"><table width="100%"><tr><td width="10%">';
        message+='<select id="'+dependency_list[i][0]+'_name">';
        message+='<option value="">Name</option>';
        var option_list=dependency_list[i][1];
        for(var j=0;j<option_list.length;j++){
            message+=('<option value="'+option_list[j][0]+'" >'+option_list[j][0]+'</option>');
        }
        message+='</select></td>';
        message+='<td width="10%"><select id="'+dependency_list[i][0]+'_bit" style="display:none;"></select></td><td width="33%"><select id="'+dependency_list[i][0]+'_version" style="display:none;"></select></td></tr></table></td>';
        message+='</tr>';
    }
    message+='<tr>';
    message+='<td align="right"><b class="Text">Version:</b></td>';
    message+='<td align="left"><table width="100%"><tr>';
    message+='<td width="19%"><select id="branch_name"><option value="">Branch</option>';
    for(var i=0;i<global_version_list.length;i++){
        message+='<option value="'+global_version_list[i][0]+'">'+global_version_list[i][0]+'</option> ';
    }
    message+='</select></td><td><select id="branch_version" style="display: none;"></select></td>'
    message+='</tr></table></td>'
    message+='</tr>';
    message+='<tr><td align="right">&nbsp;</td><td align="left"><input value="create" type="button" class="button primary" id="create_manual_machine"/></td></tr>';
    $('#manual_machine_body').html(message);
    for(var i=0;i<dependency_list.length;i++){
        $('#'+dependency_list[i][0]+'_name').on('change',function(){
            if($(this).val()!=""){
                generate_name(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
        });
        $('#'+dependency_list[i][0]+'_bit').on('change',function(){
            if($(this).val()!=""){
                generate_version(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
        });
    }
    $('#branch_name').on('change',function(){
        if($(this).val()!=""){
            for(var i=0;i<global_version_list.length;i++){
                if(global_version_list[i][0]==$(this).val()){
                    var version=global_version_list[i][1];
                    var message="";
                    message+='<option value="">Version</option>';
                    for(var j=0;j<version.length;j++){
                        message+='<option value="'+version[j]+'">'+version[j]+'</option>';
                    }
                    $('#branch_version').html(message);
                    $('#branch_version').css({'display':'block'});
                }
            }
        }
    });
    $('#create_manual_machine').on('click',function(){
        var machine_name=$('#machine_name').val().trim();
        var machine_ip=$('#machine_ip').val().trim();
        var dependency=[];
        for(var i=0;i<dependency_list.length;i++){
            var temp=[];
            var name=dependency_list[i][0];
            temp.push(name);
            if($('#'+name+'_name option:selected').val().trim()==""){
                alertify.error(name+' name is empty',1500);
                return false;
            }
            else{
                temp.push($('#'+name+'_name option:selected').val().trim());
            }
            if($('#'+name+'_bit option:selected').val()==null){
                temp.push('Nil');
            }
            else if($('#'+name+'_bit option:selected').val().trim()==""){
                alertify.error(name+' bit is empty',1500);
                return false;
            }
            else{
                temp.push($('#'+name+'_bit option:selected').val().trim());
            }
            if($('#'+name+'_bit option:selected').val()==null){
                temp.push('Nil');
            }
            else if($('#'+name+'_version option:selected').val().trim()==""){
                alertify.error(name+' version is empty',1500);
                return false;
            }
            else{
                temp.push($('#'+name+'_version option:selected').val().trim());
            }
            dependency.push(temp.join('|'));
        }
        if($('#branch_name').val().trim()==""){
            alertify.error('Branch name is empty',1500);
        }
        if($('#branch_version').val().trim()==""){
            alertify.error('Branch Version is empty',1500);
        }
        var branch_name=$('#branch_name').val().trim();
        var branch_version=$('#branch_version').val().trim();

        $.get('AddManualTestMachine',{
            'machine_name':machine_name,
            'machine_ip':machine_ip,
            'dependency':dependency.join('#'),
            'branch_name':branch_name,
            'branch_version':branch_version,
            'project_id':project_id,
            'team_id':team_id
        },function(data){
            if(data['message']){
                alertify.success(data['log_message'],1500)
                window.location.reload(true);
            }
            else{
                alertify.error(data['log_message'],1500);
                window.location.reload(true);
            }
        });
    });
    /*
    $("#machine_name").autocomplete({
        source:function(request,response){
            $.ajax({
                url:"Auto_MachineName",
                dataType:"json",
                data:{term:request.term,'project_id':project_id,'team_id':team_id},
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
                    var machine_ip=data[0][0];
                    var branch_version=data[0][1];
                    var dependency=data[0][2];
                    $('#machine_ip').val(machine_ip);
                    branch_version=branch_version.split(':');
                    var branch=branch_version[0].trim();
                    var version=branch_version[1].trim();
                    $('#branch_name').val(branch);
                    $('#branch_name').trigger('change');
                    $('#branch_version').val(version);
                    for(var i=0;i<dependency.length;i++){
                        var list=dependency[i].split('|');
                        $('#'+list[0]+'_name').val(list[1]);
                        $('#'+list[0]+'_name').trigger('change');
                        $('#'+list[0]+'_bit').val(list[2]);
                        $('#'+list[0]+'_bit').trigger('change');
                        $('#'+list[0]+'_version').val(list[3]);
                    }
                });
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };
    */
}
function generate_name(dependency_list,name,type){
    for (var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            for(var j=0;j<dependency_list[i][1].length;j++){
                if(dependency_list[i][1][j][0]==name){
                    var version_list=dependency_list[i][1][j][1];
                    if (version_list.length>0){
                        var message="";
                        message+='<option value="">Bit</option>';
                        for(var k=0;k<version_list.length;k++){
                            message+='<option value="'+version_list[k][0]+'">'+version_list[k][0]+' Bit</option>';
                        }
                        $('#'+type+'_bit').html(message);
                        $('#'+type+'_bit').css({'display':'block'});
                        break;
                    }
                }
            }
        }
    }
}

function generate_version(dependency_list,name,type){
    for(var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            var names=dependency_list[i][1];
            for(var j=0;j<names.length;j++){
                if(names[j][0]==$('#'+type+'_name option:selected').val()){
                    var bit_list=names[j][1];
                    for(var k=0;k<bit_list.length;k++){
                        if(bit_list[k][0]==name){
                            var version_list=bit_list[k][1];
                            console.log(version_list);
                            var message="";
                            message+='<option value="">Version</option>';
                            for(var l=0;l<version_list.length;l++){
                                message+='<option value="'+version_list[l]+'">'+version_list[l]+'</option>';
                            }
                            $('#'+type+'_version').html(message);
                            $('#'+type+'_version').css({'display':'block'});
                            break;
                        }
                    }
                }
            }
        }
    }
}