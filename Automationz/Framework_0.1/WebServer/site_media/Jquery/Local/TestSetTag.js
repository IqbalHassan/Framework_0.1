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
                    alertify.error(data,"",0);
                }
                else{
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
                    alertify.error(data,"",0);
                }
                else{
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
    $('#delete').click(function(event){
        event.preventDefault();
        alertify.confirm("Are you sure you want to delete the test "+temp.toLocaleUpperCase().trim()+" named "+name.trim()+"?", function(e) {
            if (e) {
                $.get("DeleteSetTag",{type:temp.toLocaleUpperCase(),name:name.trim()},function(data){
                    alertify.success(data,"",5);
                    desktop_notify(data);
                    var location='/Home/ManageSetTag/';
                    window.location=location;
                });
            }
        });
    });
}
function ClickButton(project_id,team_id,test_case_per_page,test_case_page_current){
    $('.element').click(function(){
        $('.element').css({'background-color':'#ffffff'});
        $(this).css({'background-color':'#E7F4F9'});
        var name=$(this).text().trim();
        $('#msg').css({'display':'none'});
        configureLinks($(this).closest('table').attr('data-id').trim(),name,project_id,team_id);
        $('#type').html('<p style="color: #4183c4;font-weight: bold; text-align:left;" class="Text">'+$(this).closest('table').attr('data-id').trim().toUpperCase()+' - </p>');
        $('#name').html('<p style="font-weight: bold; text-align: left;margin-left: -10%" class="Text">'+name+'<span id="time"></span></p>');
        name+=':';
        $('#infoDiv').css({'display':'block'});
        $.get('TableDataTestCasesOtherPages',{Query:name.trim(),test_status_request:true,total_time:true,project_id:project_id,team_id:team_id,test_case_per_page:test_case_per_page,test_case_page_current:test_case_page_current},function(data){
            if(data['TableData'].length!=0){
                ResultTable("#RunTestResultTable",data['Heading'],data['TableData'],'Test Cases');
                $('#pagination_div').pagination({
                    items:data['Count'],
                    itemsOnPage:test_case_per_page,
                    cssStyle: 'dark-theme',
                    currentPage:test_case_page_current,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        PerformSearch(project_id,team_id,test_case_per_page,PageNumber);
                    }
                });
                $('#time').html('<b> - '+data['time']+'</b>')

                implementDropDown("#RunTestResultTable");
                var indx = 0;
                $('#RunTestResultTable tr>td:nth-child(7)').each(function(){
                    var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<span class="hint--left hint--bounce hint--rounded" data-hint="Edit Test Case"><i class="fa fa-copy fa-2x editBtn" id="'+ID+'"></i></span>');
                    $(this).after('<span class="hint--left hint--bounce hint--rounded" data-hint="Copy Test Case"><i class="fa fa-pencil fa-2x templateBtn" id="'+ID+'"></i></span>');
                    

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
                    alertify.error(data,"",0);
                }
                else{
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
    message+='<table style="width: 100%;border-collapse: separate;border-spacing: 1.5em 3em;">';
    for(var i=0;i<data.length;i++){
        message+='<tr><td colspan="2"><a class="m-btn purple" data-id="'+data[i][0]+'" href="">Create '+data[i][0]+'</a></td></tr>';
        if(data[i][1].length>0){
            message+='<td>';
            message+='<table data-id="'+data[i][0]+'">'
            for(var j=0;j<data[i][1].length;j++){
                message+='<tr><td class="element back" style="cursor:pointer;width:100%;">'+data[i][1][j]+'</td></tr>';
            }
            message+='</table>';
            message+='</td>'
            message+='</tr>';
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