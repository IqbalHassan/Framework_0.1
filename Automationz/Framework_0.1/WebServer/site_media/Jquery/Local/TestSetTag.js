/**
 * Created by lent400 on 5/13/14.
 */
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    var test_case_per_page=5;
    var test_case_page_current=1;
    $.get('GetSetTag',{term:"",project_id:project_id,team_id:team_id},function(data){
        $('#set_tag').html(formTable(data));
        ClickButton(project_id,team_id,test_case_per_page,test_case_page_current);
    });
    GetTestSet(project_id,team_id);
    $("#createnewset").click(function(event){
        var temp=$(this).attr('data-id').trim();
        event.preventDefault();
        $('#inner_div').html(createDivInit(temp));
        $("#inner_div").dialog({
            
            show : {
                effect : 'drop',
                direction : "up"
            },
            modal : true,
            width : 400,
            height : 200,
            title:"Create New "+temp.toLocaleUpperCase()
        });
        $('#create').click(function(event){
            event.preventDefault();
            var new_name=$('#inputText').val().trim();
            //alert(temp.toLocaleUpperCase()+new_name);
            $.get("createNewSetTag",{type:'SET',name:new_name.trim(),project_id:project_id,team_id:team_id},function(data){
                var str=data;
                var substr='Failed'
                if(str.lastIndexOf(substr, 0) == 0){
                    alertify.set({ delay: 300000 });
                    alertify.error(data,"",0);
                }
                else{
                    alertify.set({ delay: 300000 });
                    alertify.success(data,"",0);
                }
                var location='/Home/ManageSetTag/';
                window.location=location;
            });
        });
    });
});
function createDivInit(temp){
    var message="";
    message+='<div align="center">';
    message+='<table align="center"><tr><td>Enter '+temp.toLocaleUpperCase()+' Name:</td><td><input id="inputText" type="text" class="Text"/></td></tr>' +
        '<tr><td>&nbsp;</td><td colspan="1" align="right"><input style="margin-right: 0%;" type="button" class="createnew" id="create" value="Create '+temp.toLocaleUpperCase()+'" /></td></tr></table>';
    message+='</div>';
    return message;
}
function renameDivInit(temp,name){
    var message="";
    message+='<div align="center">';
    message+='<table align="center">'+
        '<tr><td>Old '+temp.toLocaleUpperCase()+' Name:</td><td><span>'+name.trim()+'</span></td></tr>' +
        '<tr><td>Enter New '+temp.toLocaleUpperCase()+' Name:</td><td><input id="inputText" type="text" class="Text"/></td></tr>' +
        '<tr><td>&nbsp;</td><td colspan="1" align="right"><input style="margin-right: 0%;" type="button" class="createnew" id="create" value="Rename '+temp.toLocaleUpperCase()+'" /></td></tr></table>';
    message+='</div>';
    return message;
}
function configureLinks(temp,name,project_id,team_id){
    $('#rename').click(function(event){
        event.preventDefault();
        $('#inner_div').html(renameDivInit(temp,name));
        $("#inner_div").dialog({
            /*buttons : {
             "OK" : function() {
             $(this).dialog("close");
             }
             },
             */
            show : {
                effect : 'drop',
                direction : "up"
            },
            modal : true,
            width : 400,
            height : 200,
            title:"Rename: "+temp.toLocaleUpperCase()
        });
        $('#create').click(function(event){
            event.preventDefault();
            var new_name=$('#inputText').val().trim();
            var old_name=name.trim();
            //alert(temp.toLocaleUpperCase()+new_name);
            $.get("UpdateSetTag",{type:temp.toLocaleUpperCase(),new_name:new_name.trim(),old_name:old_name.trim()},function(data){
                var str=data;
                var substr='Failed'
                if(str.lastIndexOf(substr, 0) == 0){
                    alertify.set({ delay: 300000 });
                    alertify.error(data,"",0);
                }
                else{
                    alertify.set({ delay: 300000 });
                    alertify.success(data,"",0);
                }
                var location='/Home/ManageSetTag/';
                window.location=location;
            });
        });
    });
    $('#createNew').click(function(event){
        event.preventDefault();
        $('#inner_div').html(createDivInit(temp));
        $("#inner_div").dialog({
            /*buttons : {
                "OK" : function() {
                    $(this).dialog("close");
                }
            },
            */
            show : {
                effect : 'drop',
                direction : "up"
            },
            modal : true,
            width : 400,
            height : 200,
            title:"Create New "+temp.toLocaleUpperCase()
        });
        $('#create').click(function(event){
            event.preventDefault();
            var new_name=$('#inputText').val().trim();
            //alert(temp.toLocaleUpperCase()+new_name);
            $.get("createNewSetTag",{type:temp.toLocaleUpperCase(),name:new_name.trim(),project_id:project_id,team_id:team_id},function(data){
                var str=data;
                var substr='Failed'
                if(str.lastIndexOf(substr, 0) == 0){
                    alertify.set({ delay: 300000 });
                    alertify.error(data,"",0);
                }
                else{
                    alertify.set({ delay: 300000 });
                    alertify.success(data,"",0);
                }
                var location='/Home/ManageSetTag/';
                window.location=location;
            });
        });
    });
    $('#edit').click(function(event){
        event.preventDefault();
        var location='/Home/ManageSetTag/'+temp+'/'+name+'/';
        window.location=location;
    });
    $('#order').click(function(event){
        event.preventDefault();
        var location='/Home/ManageSetTag/'+temp+'/'+name+'/EditOrder/';
        window.location=location;
    });
    $('#delete').click(function(event){
        event.preventDefault();
        alertify.confirm("Are you sure you want to delete the test "+temp.toLocaleUpperCase().trim()+" named "+name.trim()+"?", function(e) {
            if (e) {
                $.get("DeleteSetTag",{type:temp.toLocaleUpperCase(),name:name.trim()},function(data){
                    alertify.set({ delay: 300000 });
                    alertify.success(data,"",0);
                    desktop_notify(data);
                    var location='/Home/ManageSetTag/';
                    window.location=location;
                });
            }
        });
    });
}
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

function PerformSearch(name,project_id,team_id,test_case_per_page,test_case_page_current){
    $.get('TableDataTestCasesOtherPages',{Query:name.trim(),test_status_request:true,total_time:true,project_id:project_id,team_id:team_id,test_case_per_page:test_case_per_page,test_case_page_current:test_case_page_current},function(data){
        if(data['TableData'].length!=0){
            //ResultTable("#RunTestResultTable",data['Heading'],data['TableData'],'Test Cases');
            var tooltip='Test Case Number';
            var message='';
            message+="<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + data['Count'];
            if(data['Count']>1){
                message+=" Test Cases</p>";
            }
            else{
                message+=' Test Case</p>';
            }
            message+='<table class="two-column-emphasis">';
            message+='<tr>';
            for(var i=0;i<data['Heading'].length;i++){
                message+='<th>'+data['Heading'][i]+'</th>';
            }
            message+='</tr>';
            for(var i=0;i<data['TableData'].length;i++){
                message+='<tr>';
                for(var j=0;j<data['TableData'][i].length;j++){
                switch(data['TableData'][i][j]){
                    case 'Dev':
                        message += '<td style="background-color: ' + colors['dev'] + '; color: #fff;">' + data['TableData'][i][j] + '</font></td>';
                        continue;
                    case 'Ready':
                        message += '<td style="background-color: ' + colors['ready'] + '; color: #fff;">' + data['TableData'][i][j] + '</font></td>';
                        continue;
                    }
                    message+='<td>'+data['TableData'][i][j]+'</td>';
                }
                message+='</tr>';
            }
            message+='</table> ';
            $('#RunTestResultTable').html(message);
            $('#pagination_div').pagination({
                items:data['Count'],
                itemsOnPage:test_case_per_page,
                cssStyle: 'dark-theme',
                currentPage:test_case_page_current,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    PerformSearch(name,project_id,team_id,test_case_per_page,PageNumber);
                }
            });
            $('#time').html('<b> - '+data['time']+'</b>')

            implementDropDown("#RunTestResultTable");
            var indx = 0;
            $('#RunTestResultTable tr>td:nth-child(7)').each(function(){
                var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

                $(this).after('<span class="hint--left hint--bounce hint--rounded" data-hint="Edit Test Case"><i class="fa fa-pencil fa-2x editBtn" id="'+ID+'"></i></span>');
                $(this).after('<span class="hint--left hint--bounce hint--rounded" data-hint="Copy Test Case"><i class="fa fa-copy fa-2x templateBtn" id="'+ID+'"></i></span>');


                indx++;
            });

            $(".editBtn").click(function (){
                window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
            });
            $(".templateBtn").click(function (){
                window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
            });
        }
        else{
            $('#RunTestResultTable').html('<p style="font-weight: bold; text-align: center;" class="Text">There is no test cases</p>');
            $('#pagination_div').pagination('destroy');
        }
    });
}
function ClickButton(project_id,team_id,test_case_per_page,test_case_page_current){
    $('.element').click(function(){
        $('.element').css({'background-color':'#ffffff'});
        $(this).css({'background-color':'#ccc'});
        var name=$(this).text().trim();
        $('#msg').css({'display':'none'});
        configureLinks($(this).attr('data-id').trim(),name,project_id,team_id);
        $('#type').html('<p style="color: #4183c4;font-weight: bold; text-align:left;" class="Text">'+$(this).attr('data-id').trim().toUpperCase()+' - </p>');
        $('#name').html('<p style="font-weight: bold; text-align: left;margin-left: -10%" class="Text">'+name+'<span id="time"></span></p>');
        name+=':';
        $('#infoDiv').css({'display':'block'});
        PerformSearch(name.trim(),project_id,team_id,test_case_per_page,test_case_page_current);
    });
    $('.new').click(function(event){
        var temp=$(this).attr('data-id').trim();
        event.preventDefault();
        $('#inner_div').html(createDivInit(temp));
        $("#inner_div").dialog({
            /*buttons : {
             "OK" : function() {
             $(this).dialog("close");
             }
             },
             */
            show : {
                effect : 'drop',
                direction : "up"
            },
            modal : true,
            width : 400,
            height : 200,
            title:"Create New "+temp.toLocaleUpperCase()
        });
        $('#create').click(function(event){
            event.preventDefault();
            var new_name=$('#inputText').val().trim();
            //alert(temp.toLocaleUpperCase()+new_name);
            $.get("createNewSetTag",{type:temp.toLocaleUpperCase(),name:new_name.trim()},function(data){
                var str=data;
                var substr='Failed'
                if(str.lastIndexOf(substr, 0) == 0){
                    alertify.set({ delay: 300000 });
                    alertify.error(data,"",0);
                }
                else{
                    alertify.set({ delay: 300000 });
                    alertify.success(data,"",0);
                }
                var location='/Home/ManageSetTag/';
                window.location=location;
            });
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
function formTable(data){
    var message="";
    message+='<table style="width: 100%;" class="two-column-emphasis">';
    for(var i=0;i<data.length;i++){
        if(data[i][1].length>0){
            for(var j=0;j<data[i][1].length;j++){
                message+='<tr><td class="element back" data-id="'+data[i][0]+'" style="cursor:pointer;width:100%;">'+data[i][1][j]+'</td></tr>';
            }
        }
    }
    message+='</table>';
    return message;
}
function GetTestSet(project_id,team_id){
    $('#searchbox').on('input',function(){
        $.get('GetSetTag',{term:$(this).val()},function(data){
            $('#set_tag').html(formTable(data));
            ClickButton(project_id,team_id,test_case_per_page,test_case_page_current);
        });
    });
};