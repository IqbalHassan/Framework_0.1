function RunAutoCompleteTestSearch(project_id,team_id){
    $("#searchbox").select2({
        placeholder: "Search Test Cases....",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteTestCasesSearchOtherPages",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id'),
                    'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatTestCasesSearch
    }).on("change", function(e) {
        var tag_id=$(this).select2('data')['id'];
        $("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
            + '<td class="Text" data-id="'+user_id+'">'
            + tag_id
            + ":&nbsp"
            + '</td>');
        DeleteSearchQueryText(project_id,team_id);
        PerformSearch(1,project_id,team_id);
        $(this).select2('val','');
        return false;
    });
    function formatTestCasesSearch(test_case_details) {
        var tag_select=test_case_details.text.split(' - ');
        tag_select=tag_select[tag_select.length-1].trim();
        if (tag_select=='Test Case'){
            var markup ='<div><i class="fa fa-file-text-o"></i><span style="font-weight: bold;"><span>' + '  ' + test_case_details.text + '</span></div>';
        }
        else if(tag_select=='Section'){
            var markup ='<div><i class="fa fa-folder-o"></i><span style="font-weight: bold;"><span>' + '  ' + test_case_details.text.replace('Section','Folder') + '</span></div>';
        }
        else{
            var markup ='<div><i class="fa fa-file"></i><span style="font-weight: bold;"><span>' + '  ' + test_case_details.text + '</span></div>';
        }
        return markup;
    }
}
function PerformSearch(pageNumber,project_id,team_id,predicate) {

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
            total_time:'true',
            test_case_per_page:test_case_per_page,
            test_case_page_current:pageNumber
        },function(data) {
            if (data['TableData'].length == 0)
            {
                $('#RunTestResultTable').html("");
                $('#RunTestResultTable').html("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                $("#RunTestResultTable").fadeIn(1000);
                $('#time_panel').html("");
                $('#time_panel').css({'display':'none'});
                test_cases=false;
                $('#parameter_div').empty();
                $('#pagination_div').pagination('destroy');
            }
            else
            {
                $('#time_panel').html('<b class="Text">Time Needed: '+data['time']+'</b> ');
                $('#time_panel').css({'display':'block'});
                ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");
                $('#RunTestResultTable').find('p:eq(0)').html(data['Count']+' Test Cases');
                $('#pagination_div').css({'display':'block'});
                $('#pagination_div').pagination({
                    items:data['Count'],
                    itemsOnPage:test_case_per_page,
                    cssStyle: 'dark-theme',
                    currentPage:pageNumber,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        PerformSearch(PageNumber,project_id,team_id);
                    }
                });
                //$("#RunTestResultTable .one-column-emphasis").addClass('two-column-emphasis');
                //$("#RunTestResultTable .one-column-emphasis").removeClass('one-column-emphasis');
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
function get_dependency(project_id,team_id,UserText){
    $.get('specific_dependency_settings',{
        Query: UserText,
        project_id:project_id,
        team_id:team_id
    },function(data){
        populate_parameter_div(data,"parameter_div",project_id,team_id);
    });
}
function populate_parameter_div(array_list,div_name,project_id,team_id){
    dependency_classes=[];
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
            message+='<input class="'+dependency.split(" ").join("_")+' cmn-toggle cmn-toggle-yes-no" id="'+dependency.split(" ").join("_")+'_'+array_list[i][1][j]+'" type="radio" name="type" value="'+array_list[i][1][j]+'" style="width:auto" />';
            message+='<label for="'+dependency.split(" ").join("_")+'_'+array_list[i][1][j]+'" data-on="'+array_list[i][1][j]+'" data-off="'+array_list[i][1][j]+'"></label>';
            message+='</td>';
            dep_name.push(dependency.split(" ").join("_")+'_'+array_list[i][1][j]);
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
                PerformSearch(1,project_id,team_id,parseValue(dependency_classes));
            });
        }
    }
}

function parseValue(dependency_classes){
    var message="";
    for(var i=0;i<dependency_classes.length;i++){
        $('.'+dependency_classes[i].name.split(' ').join('_')+':checked').each(function(){
            message+=($(this).val().trim()+': ');
        });
    }
    return message;
}
var dependency_list=[];
var global_version_list=[];
var dependency_classes=[];
var test_cases="";

var lowest_feature = 0;
var isAtLowestFeature = false;
var machinePerPage=10;
var machinePageCurrent=1;
var test_case_per_page=5;
var test_case_page_current=1;
var colors_list={
    'online':'#00ff00',
    'offline':'#ff0000'
}
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd",minDate:$.datepicker.formatDate('yy-mm-dd', new Date()) });
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd",minDate: $.datepicker.formatDate('yy-mm-dd', new Date())});

    $('#next').on('click',function(){
        if(test_cases==''||test_cases){
            tc_status=false;
        }
        if(test_cases){
            tc_status=true;
        }
        if(tc_status){
            var temp=[];
            var dep_stat=true;
            for(var i=0;i<dependency_classes.length;i++){
                if($('.'+dependency_classes[i].name.split(' ').join('_')+':checked').length>0){
                    if(temp.indexOf($('.'+dependency_classes[i].name.split(' ').join('_')+':checked').val().trim())>-1){
                        continue;
                    }
                    else{
                        //temp.push($('.'+dependency_classes[i].name.split(' ').join('_')+':checked').val().trim());
                        continue;
                    }
                }
                else{
                    dep_stat= false;
                    break;
                }
            }
            if(dep_stat){
                $('#choice_div').css({'display':'none'});
                $('#dependency_tab').css({'display':'block'});
                $('#prev').css({'display':'block'});
                $(this).css({'display':'none'});
            }else{
                alertify.error(dependency_classes[i].name+ ' is not selected');
                return false;
            }

        }
        else{
            alertify.error('Test case is not selected.');
            return false;
        }

    });
    $('#prev').on('click',function(){
        $('#choice_div').css({'display':'block'});
        $('#dependency_tab').css({'display':'none'});
        $('#next').css({'display':'block'});
        $(this).css({'display':'none'});
    });
    $('#create_new').on('click',function(){
        //window.location="/Home/Machine/create_new_machine/";
        url="/Home/Machine/create_new_machine/";
        window.open(url, '_blank');

    });
    RunAutoCompleteTestSearch(project_id,team_id);
    AutoSuggestions(project_id,team_id);
    SubmitRun(project_id,team_id);
    getAllmachine(machinePerPage,machinePageCurrent,project_id,team_id);
});

function AutoSuggestions(project_id,team_id){
    $("#assigned_tester").select2({
        placeholder: "Assigned Testers...",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteTesterSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id'),
                    'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatUsers
    }).on("change", function(e) {
        var user_id=$(this).select2('data')['id'];
        var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
        $("#tester").append('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
            + '<td class="Text" data-id="'+user_id+'">'
            + user_name
            + ":&nbsp"
            + '</td>');
        $(this).select2('val','');
        return false;
    });

    // Should be used for formatting results, LATER
    function formatUsers(user_details) {
        var markup ='<div><i class="fa fa-user"></i><span style="font-weight: bold;"><span>' + ' ' + user_details.text + '</span></div>';

        return markup;
    }
    $("#DeleteTester").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });

    $("#email_list").select2({
        placeholder: "Send Emails...",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteEmailSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id'),
                    'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatEmails
    }).on("change", function(e) {
        var user_id=$(this).select2('data')['id'];
        var user_name=$(this).select2('data')['text'].split(' - ')[0].trim();
        $("#email").append('<td><img class="delete" id = "DeleteEmail" title = "EmailDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
            + '<td class="Text" data-id="'+user_id+'">'
            + user_name
            + ":&nbsp"
            + '</td>');
        $(this).select2('val','');
        return false;
    });
    function formatEmails(user_details) {
        var markup ='<div><i class="fa fa-user"></i><span style="font-weight: bold;"><span>' + ' ' + user_details.text + '</span></div>';

        return markup;
    }
    $("#DeleteEmail").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
    $("#milestone_list").select2({
        placeholder: "Search Milestone...",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteMilestoneSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id'),
                    'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatMilestone
    }).on("change", function(e) {
        var milestone_name=$(this).select2('data')['text'].split(' - ')[0].trim();
        $("#milestone").html('<td><img class="delete" id = "DeleteMileStone" title = "MileStoneDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
            + '<td class="Text">'
            + milestone_name
            + ":&nbsp"
            + '</td>');
        $(this).select2('val','');
        return false;
    });
    function formatMilestone(milestone) {
        var markup ='<div><i class="fa fa-file"></i><span style="font-weight: bold;"><span>' + ' ' +milestone.text + '</span></div>';
        return markup;
    }
    $("#DeleteMileStone").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
    $("#machine_list").select2({
        placeholder: "Select Machines.. ",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteUsersSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id'),
                    'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatMachine
    }).on("change", function(e) {
        var machine_name=$(this).select2('data')['text'].split(' - ')[0].trim();
        $("#machine").html('<td><img class="delete" id = "DeleteMachine" title = "MachineDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
            + '<td class="Text">'
            + machine_name
            + ":&nbsp"
            + '</td>');
        $(this).select2('val','');
        $('#run_test').slideDown('slow');
        return false;
    });
    function formatMachine(machine) {
        var markup ='<div><i class="fa fa-machine"></i><span style="font-weight: bold;"><span>'+ " " +machine.text + '</span></div>';
        return markup;
    }

    $("#DeleteMachine").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();
        $('#run_test').slideUp("slow");

    });

    $("#testObjective").select2({
        placeholder: "Run Objective.. ",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteObjectiveSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': project_id,
                    'team_id': team_id
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        createSearchChoice: function(term) {
            return {id: term};
        },
        createSearchChoicePosition: "top",
        formatResult: formatObjectives,
        formatSelection: formatObjectives
    }).on("change", function(e) {
        $(this).select2("val");
        return false;
    });

    function formatObjectives(obj_details) {
        //var start = obj_details.text.indexOf(":") + 1;
        //var length = obj_details.text.length;

        //var obj = step_details.text.substr(start, length - 1);
        //var title = step_details.text.substr(0,start-1);

        var markup =
            '<div>' +
            '<i class="fa fa-file-text fa-fw"></i> <span style="font-weight: bold;">' + obj_details.id + '</span>' +
            '</div>';

        return markup;
    }
}
function DeleteSearchQueryText(project_id,team_id){
    $("#AutoSearchResult td>img.delete").on('click', function() {
        console.log('clicked');
        $(this).parent().next().remove();
        $(this).parent().remove();
        setTimeout(function(){
            PerformSearch(1,project_id,team_id);
        }, 1000);
    });
}
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
            alertify.set({ delay: 300000 });
            alertify.error('No Test cases selected');
            return false;
        }

        var temp=[]
        var message="";
        for(var i=0;i<dependency_classes.length;i++){
            if($('.'+dependency_classes[i].name.split(' ').join('_')+':checked').length>0){
                if(temp.indexOf($('.'+dependency_classes[i].name.split(' ').join('_')+':checked').val().trim())>-1){
                    continue;
                }
                else{
                    temp.push($('.'+dependency_classes[i].name.split(' ').join('_')+':checked').val().trim());
                }
            }
            else{
                alertify.set({ delay: 300000 });
                alertify.error('No '+dependency_classes[i].name+' is selected');
                return false;
            }
        }
        for(var i=0;i<temp.length;i++){
            message+=(temp[i].trim()+': ');
        }
        console.log(message);
        var start_date=$('#start_date').val();
        if(start_date==undefined || start_date==""){
            alertify.log("Starting Date must be selected","",0);
            return false;
        }
        var end_date=$('#end_date').val();
        if(end_date==undefined || end_date==""){
            alertify.log("Ending Date must be selected","",0);
            return false;
        }
        var TesterQuery=[];
        $("#tester").find('td').each( function()
        {
            var temp = $(this).attr('data-id');
            //TesterQuery = TesterQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "");
            if(TesterQuery.indexOf(temp)==-1 && temp!=undefined){
                TesterQuery.push(temp);
            }
        });
        if(TesterQuery.length==0){
            alertify.log("Testers is to be selected from suggestion","",0);
            return false;
        }
        var EmailQuery=[];
        $("#email").find('td').each( function()
        {
            var temp = $(this).attr('data-id');
            //EmailQuery = EmailQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "");
            if(EmailQuery.indexOf(temp)==-1 && temp!=undefined){
                EmailQuery.push(temp);
            }
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
                TesterIds:TesterQuery.join('|'),
                EmailIds:EmailQuery.join('|'),
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
function getAllmachine(machinePerPage,machinePageCurrent,project_id,team_id){
    $.get('get_all_machine',{'machinePerPage':machinePerPage ,'machinePageCurrent':machinePageCurrent,project_id:project_id,team_id:team_id},function(data){
        var message="";
        message+='<tr>';
        for(var i=0;i<data['column'].length;i++){
            message+='<td><b>'+data['column'][i]+'</b></td>';
        }
        message+='</tr>';
        for(var i=0;i<data['machine'].length;i++){
            message+='<tr>';
            var status=data['machine'][i][data['machine'][i].length-1];
            if(status=='online'){
                var color=colors_list['online'];
            }
            else{
                var color=colors_list['offline'];
            }
            for(var j=0;j<data['machine'][i].length;j++){
                if(data['machine'][i][j] instanceof Array){
                    if(data['machine'][i][j].length!=0){
                        message+='<td><table>';
                        for(var k=0;k<data['machine'][i][j].length;k++){
                            message+='<tr>';
                            message+='<td>'+data['machine'][i][j][k]+'</td>';
                            message+='</tr>';
                        }
                        message+='</table></td>';
                    }
                    else{
                        message+='<td>N/A</td>';
                    }

                }
                else{
                    if(data['machine'][i][j]==''||data['machine'][i][j]==null){
                        message+='<td>N/A</td>';
                    }
                    else{
                        if(j==0){
                            message+='<td style="border-left: 4px solid  '+color+'"><a href="/Home/Machine/'+data['machine'][i][j].split(' ').join('_')+'/">'+data['machine'][i][j]+'</a></td>';
                        }
                        else{
                            message+='<td>'+data['machine'][i][j]+'</td>';
                        }

                    }
                }
            }
            message+='</tr>';
        }
        $('#machine_listing').html(message);
        $('#machine_pagination').pagination({
            items:data['count'],
            itemsOnPage:machinePerPage,
            cssStyle: 'dark-theme',
            currentPage:machinePageCurrent,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                //PerformSearch(project_id,team_id,user_text,itemPerPage,PageNumber);
                getAllmachine(machinePerPage,PageNumber,project_id,team_id);
            }
        });
    });
}

