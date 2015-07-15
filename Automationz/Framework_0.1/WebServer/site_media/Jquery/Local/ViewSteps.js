/**
 * Created by J on 2/2/2015.
 */

var test_case_per_page=10;
var test_case_page_current=1;
var project_id = $.session.get('project_id');
var team_id = $.session.get('default_team_identity');

$(document).ready(function(){
	$("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });
    get_steps(project_id, team_id,test_case_per_page,test_case_page_current);

    test_case_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            test_case_per_page=$(this).val();
            test_case_page_current=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            get_steps(project_id, team_id,test_case_per_page,test_case_page_current);
        }
    });
});

var colors = {
    'pass' : '#65bd10',
    'fail' : '#fd0006',
    'block' : '#ff9e00',
    'submitted' : '#808080',
    'in-progress':'#0000ff',
    'skipped':'#cccccc',
    'dev': '#aaaaaa',
    'ready': '#65bd10'
};

function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table class="two-column-emphasis" id="table_vai_table">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        for(var j=0;j<data[i].length;j++){
            switch(data[i][j]){
                case 'Dev':
                    message+='<td style="background-color: ' + colors['dev'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                case 'Ready':
                    message+='<td style="background-color: ' + colors['ready'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                default :
                    message+='<td>'+data[i][j]+'</td>';
                    continue;
            }
        }
        message += '<td><span style="cursor:pointer;" class="hint--left hint--bounce hint--rounded" data-hint="Delete this step"><i class="fa fa-trash fa-fw fa-lg"></span></td>'
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);

    $("#table_vai_table tr td:nth-child(11)").each(function(){
        $(this).on('click',function(){
            var stepname = $(this).parent().find('td:first-child').text().trim();
            var hobe = $(this).parent().find('td:nth-child(10)').text().trim();
            //reset();
            if(hobe!="0"){
                //alertify.set({ delay: 300000 });
                alertify.log("This step cannot be deleted! Its being used in "+ hobe + " testcase(s).","",0);
            }
            else{
                var message='';
                message+='<div>';
                message+='<p style="font-size:140%">Are you sure to delete step <b>' + stepname + '</b>?</p>';
                message+='<br/>';
                message+='</div>';
                alertify.confirm(message, function (e) {
                    if (e) {
                        $.ajax({
                            url:"TestStep_Delete",
                            dataType:"json",
                            data:{term:stepname,project_id:project_id,team_id:team_id},
                            success:function(data){
                                var count=data[0];
                                console.log(count);
                                if(count>0){
                                    alertify.log("This test step can't be deleted. There are "+count+" test cases using this test step '"+name+"'","",0);
                                    //$("#delete_error").html("<p><b>This test step can't be deleted. There are "+count+" test cases using this test step '"+name+"'</b></p>");
                                }
                                if(count==0){
                                    alertify.set({ delay: 300000 });
                                    alertify.success("Test Step '"+stepname+"' deleted successfully!");
                                    get_steps(project_id, team_id,test_case_per_page,test_case_page_current);
                                }
                            }
                        });
                        
                    } else {
                        alertify.set({ delay: 300000 });
                        alertify.error("You've clicked Cancel");
                    }
                });
                return false;
            }
       });
    });
}

function get_steps(project_id,team_id,test_case_per_page,test_case_page_current){
    $.get("Steps_List",{'project_id':project_id ,'team_id':team_id,'test_case_per_page':test_case_per_page,'test_case_page_current':test_case_page_current},function(data){
        form_table("allsteps",data['Heading'],data['TableData'],data['Count'],"Test Steps");
        styling("allsteps");
        $('#pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:test_case_per_page,
            cssStyle: 'dark-theme',
            currentPage:test_case_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_steps(project_id,team_id,test_case_per_page,PageNumber);
            }
        });
    });
}
function styling(wheretoplace){
    $('#'+wheretoplace+" tr td:nth-child(1)").css({'color' : 'blue','cursor' : 'pointer'});
    $('#'+wheretoplace+" tr td:first-child").each(function(){
       $(this).on('click',function(){
            var step = $(this).text().trim();       
            window.location = '/Home/ManageTestCases/EditStep/' + step ;
       });
    });
    $('#'+wheretoplace+" tr td:nth-child(10)").css({'color' : 'blue','cursor' : 'pointer','cursor':'pointer'});
    $('#'+wheretoplace+" tr td:nth-child(10)").each(function(){
       $(this).on('click',function(){
            var step_name=$(this).parent().find('td:first-child').text().trim();
            get_test_cases(step_name,project_id,team_id,5,1);
       });
    });
}
function get_test_cases(stepname,project_id,team_id,itemPerPage,PageCurrent){
    $('#step_name').html("Test cases for step: "+ stepname);
    $.get("TestCase_Results",{
        Query: stepname,
        test_case_per_page:itemPerPage,
        test_case_page_current:PageCurrent,
        project_id:project_id,
        team_id:team_id,
        test_status_request:true
    },function(data) {
        form_table("usage_div",data['Heading'],data['TableData'],data['Count'],"Test Cases");
        implementDropDown('#usage_div');
        $('#usage_pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:test_case_per_page,
            cssStyle: 'dark-theme',
            currentPage:test_case_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_test_cases(stepname,project_id,team_id,itemPerPage,PageNumber);
            }
        });
        var indx = 0;
        $('#usage_div tr>td:nth-child(7)').each(function(){
            var ID = $("#usage_div tr>td:nth-child(1):eq("+indx+")").text().trim();

            $(this).after('<span style="cursor: pointer; margin-left: 8px;" class="hint--left hint--bounce hint--rounded" data-hint="Copy Test Case"><i class="fa fa-copy fa-2x templateBtn" id="'+ID+'" style="cursor:pointer"></i></span>');
            //$(this).after('&nbsp;&nbsp;');
            $(this).after('<span style="cursor: pointer; margin-left: 8px;" class="hint--left hint--bounce hint--rounded" data-hint="Edit Test Case"><i class="fa fa-pencil fa-2x editBtn" id="'+ID+'" style="cursor:pointer"></i></span>');

            indx++;
        });

        $(".editBtn").click(function (){
            window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
        });
        $(".templateBtn").click(function (){
            window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
        });
    });
}
function implementDropDown(wheretoplace){
    $(wheretoplace+" tr td:nth-child(1)").css({'color' : 'blue','cursor' : 'pointer'});
    $(wheretoplace+" tr td:nth-child(1)").each(function() {
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
