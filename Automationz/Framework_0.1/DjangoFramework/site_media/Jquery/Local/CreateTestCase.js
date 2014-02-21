/**
 * Created by minar09 on 2/10/14.
 */


var indx=0;
var indx2=0;
var URL="";
var step_num = 1;
var step_num_data_num = new Array();
var tag_list = new Array();
var Env = "PC"
var lowest_section = 0;
var isAtLowestSection = false;

$(document).ready(function() {

    add_step_teble_row();
    show_data_dialog();
    check_required_data();

    URL = window.location.pathname
    console.log("url:"+URL);
    indx = URL.indexOf("Create");
    console.log("Create Index:"+indx);
    indx2 = URL.indexOf("Edit");
    console.log("Edit Index:"+indx2);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf("Create") != -1;
    console.log("Url Length:"+URL.length);
    console.log("Template:"+template);
    if (indx != -1 || indx2 != -1) {
        $('#add_test_step').click(function() {
            addStep();
        });

        $('#remove_test_step').click(function() {
            if (step_num > 0) {
                /*$('#AutoSearchResult' + step_num).fadeOut().remove();
                step_num--;
                 RunTestAutocompleteSearch(Env, step_num);*/
                var table = document.getElementById("steps_table");
                var rowCount = table.rows.length;

                table.deleteRow(rowCount -1);
                step_num--;
            }
        });
        $('.remove_img').live('click',function(){
            var val=$(this).attr('id');
            //console.log('step_'+val);
            var tr=$(this).closest('tr');
            tr.css({'background-color':'#FF3700'});
            tr.css({'fadeOut':'500'});
            tr.remove();
            step_num--;
            resetNumber();
            //console.log(step_num);
            return false;
        });
        $('.add_after_img').live('click',function(){
            var row=$(this).closest('tr').attr('id').trim();
            console.log(row);
            var currentrow=$(this).closest('tr');
            step_num++;
            var message=add_new_row();
            console.log(message);
            currentrow.after(message);
            resetNumber();
            return false;
        });
        $("input[name=platform]").change(function () {
            Env = $(this).val();
        });

        //Sections
        $.ajax({
            url:'GetSections/',
            dataType : "json",
            data : {
                section : ''
            },
            success: function( json ) {
                if(json.length > 1)
                    for(var i = 1; i < json.length; i++)
                        json[i] = json[i][0].replace(/_/g,' ')
                $.each(json, function(i, value) {
                    if(i == 0)return;
                    $(".section[data-level='']").append($('<option>').text(value).attr('value', value));
                });
            }
        });
        $(".section[data-level='']").change(function(){
            isAtLowestSection = false;
            recursivelyAddSection(this);
        });

        //Browsers
        $.ajax({
            url:'GetBrowsers/',
            dataType : "json",
            data : {
                browser : ''
            },
            success: function( json ) {
                if(json.length > 1)
                    for(var i = 1; i < json.length; i++)
                        json[i] = json[i][0].replace(/_/g,' ')
                $.each(json, function(i, value) {

                    //$(".browser[data-level='']").append($('<option>').text(value).attr('value', value));
                    $(".browser").append('<td width="25%">' +
                        '<input id=' +
                        value +
                        ' type="checkbox" name="dependancy" value=' +
                        value +
                        '>' +
                        '<label for=' +
                        value +
                        '>' +
                        value +
                        '</label>' +
                        '</td>');
                });
            }
        });

        // Make tags autofill
        AddAutoCompleteToTag();
        DeleteSearchQueryText();
        if(indx2 != -1 || template){
            $.get("TestCase_EditData", {
                TC_Id : URL.substring(URL.lastIndexOf("/")+1,URL.length)
            }, function(data) {
                //Edit finish button text
                $("p.new_tc_form.buttonCustom").html($("p.new_tc_form.buttonCustom").html().substring(0,$("p.new_tc_form.buttonCustom").html().indexOf('<br>')) + '<br>Submit Edit')

                var enabledStatus = data['Status']
                var sections = data['Section_Path']
                var auto_id = data['TC_Id']
                var req_id = data['Requirement Ids']
                var assoc_bugs = data['Associated Bugs']
                var tc_id = data['Manual_TC_Id']
                var dependancy_list = data['Dependency List']
                var manual_tc_id = data['TC_Id']
                var platform = data['Platform']
                var priority = data['Priority']
                var status = data['Status']
                var steps_and_data = data['Steps and Data']
                var tc_types = data['TC Type']
                var tc_creator = data['TC_Creator']
                var name = data["TC_Name"]
                var tags = data['Tags List']


                //Section path
                var sectionArray = sections.split('.');
                var dataId ="";
                var handlerString = ""
                for(var index in sectionArray){
                    if(sectionArray[index] == "")
                        continue;
                    $.ajax({
                        url:'GetSections/',
                        dataType : "json",
                        data : {
                            section : dataId.replace(/^\.+|\.+$/g, "").replace(/ /g,'_')
                        },
                        success: function( json ) {
                            if(json.length != 1){
                                var realItemIndex = parseInt(json[0][0])
                                var handlerString = ""
                                for(var i = 0; i < realItemIndex; i++)
                                    handlerString+=sectionArray[i]+'.'

                                if(realItemIndex == 0){
                                    $(".section[data-level='']").find('option').each(function(){$(this).remove();});
                                    $(".section[data-level='']").append("<option>Choose...</option>");

                                    for(var i = 0; i < json.length; i++)
                                        json[i] = json[i][0].replace(/_/g,' ')
                                    $.each(json, function(i, value) {
                                        if(i == 0)return;
                                        $(".section[data-level='']").append($('<option>').text(value).attr('value', value));
                                    });
                                    $(".section[data-level='']").val(sectionArray[realItemIndex].replace(/_/g,' '))
                                }else{
                                    var tag = jQuery('<select/>',{
                                        'class':'section',
                                        'data-level':handlerString,
                                        'id':realItemIndex+1,
                                        change: function(){
                                            isAtLowestSection = false;
                                            recursivelyAddSection(this);
                                        }
                                    })
                                    if($('#sectiongroup select[id='+realItemIndex+']').length != 0)
                                        $('#sectiongroup select[id='+realItemIndex+']').after(tag)
                                    else
                                        $('#sectiongroup select[id=1]').after(tag)

                                    $(".section[data-level='"+handlerString+"']").append("<option>Choose...</option>");

                                    var once = true;
                                    for(var i = 0; i < json.length; i++)
                                        json[i] = json[i][0].replace(/_/g,' ')
                                    $.each(json, function(i, value) {
                                        if(i == 0)return;
                                        if(once){
                                            lowest_section+=1
                                            once = false
                                        }
                                        $(".section[data-level='"+handlerString+"']").append($('<option>').text(value).attr('value', value));
                                    });
                                    $(".section[data-level='"+handlerString+"']").val(sectionArray[realItemIndex].replace(/_/g,' '))
                                }
                                isAtLowestSection = true;
                            }
                        }
                    });

                    dataId += sectionArray[index] + '.'
                }

                //auto id
                if(!template){
                    $('#TC_Id').html("<b>Automation ID: "+auto_id +"</b>")
                    $('#TC_Id').css('display','block');
                }

                //enabled_status
                if(!template){
                    if(enabledStatus == "Ready")
                        $('input[value="Production"]').attr('checked', true);
                    else if(enabledStatus == "Dev")
                        $('input[value="Development"]').attr('checked', true);
                    else if(enabledStatus == "Forced")
                        $('input[value="Forced-Manual"]').attr('checked', true);
                    $('#tc_enable').css('display','block');
                }

                //assoc id
                $('#defectid_txtbox').val(assoc_bugs)
                //tcid
                $('#id_txtbox').val(tc_id)
                //req id
                $('#reqid_txtbox').val(req_id)
                //name
                $('#title_txtbox').val(name)
                //platform
                if(platform == 'PC') $('#PC_radio').attr('checked', true);
                else $('#MAC_radio').attr('checked', true);
                //dependancy
                for(var dependancy in dependancy_list){
                    if(dependancy_list[dependancy] == 'Outlook') $('input[value="Outlook"]').attr('checked', true);
                    else if(dependancy_list[dependancy] == 'MacNative') $('input[value="MacNative"]').attr('checked', true);
                    else if(dependancy_list[dependancy] == 'iTunes') $('input[value="iTunes"]').attr('checked', true);
                    else if(dependancy_list[dependancy] == 'iPhoto') $('input[value="iPhoto"]').attr('checked', true);
                    else if(dependancy_list[dependancy] == 'Chrome') $('input[value="Chrome"]').attr('checked', true);
                    else if(dependancy_list[dependancy] == 'FireFox') $('input[value="FireFox"]').attr('checked', true);
                    else if(dependancy_list[dependancy] == 'IE') $('input[value="IE"]').attr('checked', true);
                }
                //Type
                for(var type in tc_types){
                    if(tc_types[type].toLowerCase() == 'smoke') $('#smoke_check').attr('checked', true);
                    else if(tc_types[type].toLowerCase() == 'si') $('#si_check').attr('checked', true);
                    else if(tc_types[type].toLowerCase() == 'svv') $('#svv_check').attr('checked', true);
                }
                //Priority
                $("#priotiy_select").val(parseInt(priority.substring(1,2)));
                //Tags
                for(var tag in tags)
                    if(tags[tag] != "")
                        AddToListTag(tags[tag]);
                //test data
                for(var step_indx in steps_and_data){
                    var id = addStep();
                    var colour="";
                    var step_type=steps_and_data[step_indx][2];
                    if(step_type=="automated"){
                        colour="green";
                    }
                    if(step_type=="manual"){
                        colour="red";
                    }
                    if(step_type=="performance"){
                        colour="blue";
                    }
                    $('#' + id).val(steps_and_data[step_indx][0]);
                    $('#' + id+'info').val(steps_and_data[step_indx][3]);
                    $('#' + id+'expected').val(steps_and_data[step_indx][4]);
                    if(steps_and_data[step_indx][5]=="yes"){
                        $('#'+id+'verify').attr('checked',true);
                    }
                    $("#" + id + "step_type").html("<b style='color:"+colour+"'>"+step_type+"</b>");
                    //check if step has data
                    if(steps_and_data[step_indx][1].length > 0){
                        $("#" + id + "data").fadeIn(500);

                        for(var data in steps_and_data[step_indx][1]){
                            addDataToStep('#'+(parseInt(step_indx)+1) +'.add_test_data',steps_and_data[step_indx][1][data]);
                        }
                    }
                }
            });
        }


        $('#submit').click(function(){
            //Check section is at lowest
            if(!isAtLowestSection){
                alert("Section name is not set to a proper selection (must be lowest possible level).")
                return;
            }

            //if($("#sectiongroup select.section:last-child").attr("data-level").replace(/ /g,'_').indexOf("PIM.") == -1){
            //	alert("Work in progress. For more information contact automationsolutionz.com")
            //	return;
            //}

            //Validate Data
            for(var j = 1; j <= step_num; j++){
                if($("#searchbox"+j+"info").val()=="" || $("#searchbox"+j+"expected").val()==""){
                    alert("No Test Step Description or Expected Results is filled for step number#"+j);
                    return;
                }
                for(var i = 0; i < $("#searchbox"+j+"data textarea").length; i++){
                    if($("#searchbox"+j+"data textarea:eq("+i+")").attr("data-id") == 'edit'){
                        if(!validate_data($("#searchbox"+j+"data textarea:eq("+i+")").val())){
                            $(".searchbox"+j+(i+1)+"data").css('background','#ff0000')
                            $('html,body').animate({
                                scrollTop: $(".searchbox"+j+(i+1)+"data").offset().top
                            },500,function(){
                                //$(".searchbox"+j+(i+1)+"data").effect("pulsate", { times:2 }, 500);
                                $(".searchbox"+j+(i+1)+"data").stop().css("background-color", "transparent")
                                    .animate({ backgroundColor: "#F00"}, 150)
                                    .animate({ backgroundColor: "transparent"}, 150)
                                    .animate({ backgroundColor: "#f00"}, 150)
                                    .animate({ backgroundColor: "transparent"}, 150);
                            });
                            alert("There was an error in the FROM field of Step #"+j+", Data #" +(i+1));
                            return;
                        }
                        if(!validate_data($("#searchbox"+j+"data div textarea:eq("+(i+1)+")").val())){
                            $(".searchbox"+j+(i+1)+"data").css('background','#ff0000')
                            $('html,body').animate({
                                scrollTop: $(".searchbox"+j+(i+1)+"data").offset().top
                            },500,function(){
                                //$(".searchbox"+j+(i+1)+"data").effect("pulsate", { times:2 }, 500);
                                $(".searchbox"+j+(i+1)+"data").stop().css("background-color", "transparent")
                                    .animate({ backgroundColor: "#F00"}, 150)
                                    .animate({ backgroundColor: "transparent"}, 150)
                                    .animate({ backgroundColor: "#f00"}, 150)
                                    .animate({ backgroundColor: "transparent"}, 150);
                            });
                            alert("There was an error in the TO field of Step #"+j+", Data #" +(i+1));
                            return;
                        }
                        i++;
                    }else{
                        if(!validate_data($("#searchbox"+j+"data textarea:eq("+i+")").val())){
                            $('html,body').animate({
                                scrollTop: $(".searchbox"+j+(i+1)+"data").offset().top
                            },1000,function(){
                                //$(".searchbox"+j+(i+1)+"data").effect("pulsate", { times:2 }, 500);
                                $(".searchbox"+j+(i+1)+"data").stop().css("background-color", "transparent")
                                    .animate({ backgroundColor: "#F00"}, 150)
                                    .animate({ backgroundColor: "transparent"}, 150)
                                    .animate({ backgroundColor: "#f00"}, 150)
                                    .animate({ backgroundColor: "transparent"}, 150);
                            });
                            alert("There was an error in Step #"+j+", Data #" +(i+1));
                            return;
                        }
                    }
                }
            }

            //Assoc bugs list
            var defect_id = $("#defectid_txtbox").val()
            var manual_tc_id = $("#id_txtbox").val()
            var req_id = $("#reqid_txtbox").val();
            //status
            var status;
            if($('input[value="Production"]').attr('checked') == "checked")
                status = "Ready"
            else if($('input[value="Development"]').attr('checked') == "checked")
                status = "Dev"
            else if($('input[value="Forced-Manual"]').attr('checked') == "checked")
                status = "Forced"

            var newSectionPath = $("#sectiongroup select.section:last-child").attr("data-level").replace(/ /g,'_') + $("#sectiongroup select.section:last-child option:selected").val().replace(/ /g,'_');
            var _TC_Id = $('#TC_Id').html().substring($('#TC_Id').html().indexOf(": ")+2,$('#TC_Id').html().indexOf("</b>"))
            var title = $("#title_txtbox").val();
            var platform="";
            platform = $("input[name=platform]:checked").val();
            if(platform!="PC" && platform!="MAC"){
                alert("Test Case Platform is not selected");
                return;
            }
            var applic_client = []
            $("input[name=dependancy]:checked").each(function() {
                applic_client.push($(this).val())
            });
            if(applic_client.length==0){
                alert("Test Case Dependency is not given");
                return;
            }
            //for(var i = 0; i < $("input[name=dependancy]:checked").length; i++)
            var type = [];
            $("input[name=type]:checked").each(function() {
                type.push($(this).val())
            });
            if(type.length==0){
                alert("Test Case type is not given");
                return;
            }

            var priority = 'P' + $("#priotiy_select").val();

            var tag = new Array();
            for(var i = 0; i < $(".submitquery").length; i++){
                tag.push($(".submitquery:eq("+i+")").html().replace(/&nbsp;/g,''));
            }

            var stepName = [];
            var stepData = [];
            var stepDescription=[];
            var stepExpected=[];
            var stepVerify=[];
            for(var j = 1; j <= step_num; j++){
                stepName[j-1] = $("#searchbox" + j).val();
                stepDescription[j-1] = $("#searchbox" + j+"info").val();
                stepExpected[j-1] = $("#searchbox" + j+"expected").val();
                if($('#searchbox'+j+'verify').attr('checked')=='checked'){
                    stepVerify[j-1]="yes";
                }
                else{
                    stepVerify[j-1]="no";
                }
                for(var i = 0; i < $("#searchbox"+j+"data textarea").length; i++){
                    if(stepData[j-1] === undefined){
                        stepData[j-1] = [];
                    }
                    if($("#searchbox"+j+"data textarea:eq("+i+")").attr("data-id") == 'edit'){
                        stepData[j-1].push([$("#searchbox"+j+"data textarea:eq("+i+")").val(),$("#searchbox"+j+"data div textarea:eq("+(i+1)+")").val()]);
                        i++;
                    }else{
                        stepData[j-1].push($("#searchbox"+j+"data textarea:eq("+i+")").val());
                    }
                }
            }
            var stepDataSTR = [];
            for(var i = 0; i < stepData.length;i++){
                if(stepData[i] === undefined){
                    stepDataSTR[i] = "%";
                }else{
                    var tempSTR = [];
                    for(var j = 0; j < stepData[i].length; j++){
                        if (stepData[i][j] instanceof Array) {
                            tempSTR[j] = stepData[i][j].join("#");
                        }else{
                            tempSTR[j] = stepData[i][j];
                        }
                        console.log(tempSTR);
                    }
                    stepDataSTR[i] = tempSTR.join("%");
                }
                console.log(stepDataSTR[i]);
            }
            var query = indx != -1?"c":(indx2 != -1?"e":"o")
            if(query == "c"){
                $.get("Submit_New_TestCase/",{
                    Section_Path:newSectionPath,
                    Platform:Env,
                    Manual_TC_Id:manual_tc_id,
                    TC_Name:title,
                    TC_Creator:'Test',
                    Associated_Bugs_List:defect_id,
                    Requirement_ID_List:req_id,
                    TC_Type:type.join("|"),
                    Tag_List:tag.join("|"),
                    Dependency_List:applic_client.join("|"),
                    Priority:priority,
                    Steps_Data_List:stepDataSTR.join("|"),
                    Steps_Name_List:stepName.join("|"),
                    Steps_Description_List:stepDescription.join("|"),
                    Steps_Expected_List:stepExpected.join("|"),
                    Steps_Verify_List:stepVerify.join("|"),
                    Status:"Dev"},function(data) {
                    alert(data);
                });
            }else if(query == "e"){
                $.get("Edit_TestCase",{
                        Section_Path:newSectionPath,
                        TC_Id:_TC_Id,
                        Platform:Env,
                        Manual_TC_Id:manual_tc_id,
                        TC_Name:title,
                        TC_Creator:'Test',
                        Associated_Bugs_List:defect_id,
                        Requirement_ID_List:req_id,
                        Status:status,
                        TC_Type:type.join("|"),
                        Tag_List:tag.join("|"),
                        Dependency_List:applic_client.join("|"),
                        Priority:priority,
                        Steps_Data_List:stepDataSTR.join("|"),
                        Steps_Name_List:stepName.join("|"),
                        Steps_Description_List:stepDescription.join("|"),
                        Steps_Expected_List:stepExpected.join("|"),
                        Steps_Verify_List:stepVerify.join("|")
                    },
                    function(data) {
                        alert(data+" edited successfully");
                    });
            }

        });
    }

});
function resetNumber(){
    var row_count=$('#steps_table tr').length;
    var currentrow=$('#steps_table tr:first-child');
    for (var i=1;i<=row_count;i++){
        currentrow.attr('id','step_'+i);
        currentrow.find('td:first-child input:eq(0)').attr('id',i);
        currentrow.find('td:nth-child(2)').text(i);
        currentrow.find('td:nth-child(3) input:eq(0)').attr('id','step_'+i+'name');
        currentrow.find('td:nth-child(4) a:eq(0)').attr('id','searchbox'+i+'data');
        currentrow.find('td:nth-child(5) textarea:eq(0)').attr('id','searchbox'+i+'info');
        currentrow.find('td:nth-child(6) textarea:eq(0)').attr('id','searchbox'+i+'expected');
        currentrow.find('td:nth-child(7) input:eq(0)').attr('id','searchbox'+i+'verify');
        currentrow.find('td:nth-child(8) span:eq(0)').attr('id','searchbox'+i+'step_type');
        currentrow.find('td:nth-child(9) a:eq(0)').attr('id','searchbox'+i+'step_desc');
        currentrow=currentrow.closest('tr').next();
    }
    console.log(row_count);
    //step_num=count;
}
function recursivelyAddSection(_this){
    var fatherHeirarchy = $(_this).attr("data-level");
    var father = $(_this).children("option:selected").text();
    if(father == "")
        return;
    if(father == "Choose..."){
        for(var i = 0; i < lowest_section; i++){
            $("#sectiongroup select.section:last-child").remove();
        }
        lowest_section = 0
        return;
    }
    var current_section = (fatherHeirarchy.split(".").length - 1)
    if(current_section < lowest_section){
        for(var i = current_section + 1; i <= lowest_section; i++){
            $("#sectiongroup select.section:last-child").remove();
        }
        lowest_section = current_section
    }

    $.ajax({
        url:'GetSections/',
        dataType : "json",
        data : {
            section : (fatherHeirarchy+father).replace(/ /g,'_')
        },
        success: function( json ) {
            if(json.length != 1){
                jQuery('<select/>',{
                    'class':'section',
                    'data-level':fatherHeirarchy+father+'.',
                    change: function(){
                        isAtLowestSection = false;
                        recursivelyAddSection(this);
                    }
                }).appendTo('#sectiongroup');

                $(".section[data-level='"+fatherHeirarchy+father+".']").append("<option>Choose...</option>");

                var once = true;
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
                $.each(json, function(i, value) {
                    if(i == 0)return;
                    if(once){
                        lowest_section+=1
                        once = false
                    }
                    $(".section[data-level='"+fatherHeirarchy+father+".']").append($('<option>').text(value).attr('value', value));
                });
            }else{
                isAtLowestSection = true;
            }
        }
    });
}

function addStep(){
    step_num++;
    step_num_data_num[step_num] = 0;
    var id = AddAutoCompleteSearchBox("#stepbox", "Step " + step_num + ": ", step_num);
    //console.log("Step ID:"+id);
    RunTestAutocompleteSearch(Env, step_num);


    $('#'+step_num+'.add_test_data').live("click", function (event) {
        addDataToStep(this)
    });

    $('#'+step_num+'.remove_test_data').live("click", function (event) {
        var indx = $(this).attr("id");
        if (step_num_data_num[indx] > -1) {
            $('.searchbox'+indx +''+ step_num_data_num[indx] + 'data').remove();
            step_num_data_num[indx]--;
        }
    });
    $('#'+step_num+'step_desc').live("click",function(event){
        //alert("clicked");
        var name=$('#'+id).val();
        $.get("AutoCompleteTestStepSearch/",{term:name},function(data){
            MsgBox("Test Step Description","<b>"+data[0][3]+"</b>");
        })

    });

    /*return id;*/

    add_step_teble_row();

}
function add_new_row(){
    var message="";
    message+=('<tr id="step_'+step_num+'">' +
        '<td><input id="'+step_num+'" class="new_tc_form remove_img" type=\'image\' src=\'/site_media/minus2.png\' name=\'Remove Step\' style=\"background-color: transparent; width:18px; height:18px\"></td>' +
        '<td>'+step_num+'</td>' +
        '<td><input class="textbox" id="step_'+step_num+'name"style="width: auto"></td>' +
        '<td><a id="searchbox'+step_num+'data" class="data-popup notification-indicator tooltipped downwards" data-gotokey="n">' +
        '<span class="mail-status"></span>' +
        '</a></td>' +
        '<td><textarea id="searchbox'+step_num+'info" class="ui-corner-all  ui-autocomplete-input" style="width: 80%"></textarea></td>' +
        '<td><textarea id="searchbox'+step_num+'expected" class="ui-corner-all  ui-autocomplete-input" style="width: 80%"></textarea></td>' +
        '<td><input type="checkbox" id="searchbox'+step_num+'verify" value="yes"></td>' +
        '<td><span id="searchbox'+step_num+'step_type"></span></td>' +
        '<td><a id="searchbox'+step_num+'step_desc" class="notification-indicator tooltipped downwards" data-gotokey="n"><span class="mail-status"></span></a></td>' +
        '<td><input class="new_tc_form add_after_img" type=\'image\' src=\'/site_media/new.png\' name=\'Add Step\' style=\"background-color: transparent; width:18px; height:18px\"></td>' +
        '</tr>');
    return message;
}
function add_step_teble_row()
{
    $("#steps_table").append('' +
        '<tr id="step_'+step_num+'">' +
        '<td><input id="'+step_num+'" class="new_tc_form remove_img" type=\'image\' src=\'/site_media/minus2.png\' name=\'Remove Step\' style=\"background-color: transparent; width:18px; height:18px\"></td>' +
        '<td>'+step_num+'</td>' +
        '<td><input class="textbox" id="step_'+step_num+'name"style="width: auto"></td>' +
        '<td><a id="searchbox'+step_num+'data" class="data-popup notification-indicator tooltipped downwards" data-gotokey="n">' +
        '<span class="mail-status"></span>' +
        '</a></td>' +
        '<td><textarea id="searchbox'+step_num+'info" class="ui-corner-all  ui-autocomplete-input" style="width: 80%"></textarea></td>' +
        '<td><textarea id="searchbox'+step_num+'expected" class="ui-corner-all  ui-autocomplete-input" style="width: 80%"></textarea></td>' +
        '<td><input type="checkbox" id="searchbox'+step_num+'verify" value="yes"></td>' +
        '<td><span id="searchbox'+step_num+'step_type"></span></td>' +
'<td><a id="searchbox'+step_num+'step_desc" class="notification-indicator tooltipped downwards" data-gotokey="n"><span class="mail-status"></span></a></td>' +
        '<td><input class="new_tc_form add_after_img" type=\'image\' src=\'/site_media/new.png\' name=\'Add Step\' style=\"background-color: transparent; width:18px; height:18px\"></td>' +
        '</tr>'
    );
}
function show_data_dialog(){
    $(".one-column-emphasis tr>td:nth-child(4)").each(function(){
        $(this).css({
            'curosr':'pointer'
        });
    });
    $("#steps_table .data-popup").each(function(){
        $(this).click(function(){
            var message = ""
            message += '<table class="one-column-emphasis">' +
                '<tr>' +
                '<th>Type</th>' +
                '<th>Sub-Type</th>' +
                '<th>Title</th>' +
                '</tr>' +
                '<tr>' +
                '<td><input class="textbox" style="width: auto"></td>' +
                '<td><input class="textbox" style="width: auto"></td>' +
                '<td><input class="textbox" style="width: auto"></td>' +
                '</tr>' +
                '</table>'
            $("#inner-data").html(message);

            $("#inner-data").dialog({
                buttons : {
                    "OK" : function() {
                        $(this).dialog("close");
                    }
                },

                show : {
                    effect : 'drop',
                    direction : "up"
                },

                modal : true,
                width : 800,
                height : 500,
                title: "Data"

            });
        });
    });

    $("#steps_table .step-info").each(function(){
        $(this).click(function(){
            $("#inner-data").dialog({
                buttons : {
                    "OK" : function() {
                        $(this).dialog("close");
                    }
                },

                show : {
                    effect : 'drop',
                    direction : "up"
                },

                modal : true,
                width : 500,
                height : 500,
                title: "Info"

            });
        });
    });

}
function check_required_data()
{
    $(".section").live('change',function(){
        if($(".section").val() != "Choose...")
        {
            $("#section-flag").addClass("filled");
        }
        else
        {
            $("#section-flag").removeClass("filled");
        }
    });

   /* if($('#PC_radio').is(":checked") || $('#MAC_radio').is(":checked")){
        console.log($('#PC_radio').val());
        $("#platform-flag").addClass("filled");
    }
    else{
        $("#platform-flag").removeClass("filled");
    }*/


}
function dataArrayToString(array){
    var tempString ="";

    tempString += "["
    for(var field in array){
        tempString += "("

        if($.isArray(array[field][1])){
            tempString += array[field][0] + ","
            tempString += "["
            for(var address in array[field][1]){
                tempString += "("
                tempString += array[field][1][address].join(",")
                tempString += ")"
                if(address != array[field][1].length - 1)
                    tempString += ", "
            }
            tempString += "]"
        }else{
            tempString += array[field].join(",")
        }

        tempString += ")"
        if(field != array.length - 1)
            tempString += ", "
    }
    tempString += "]"

    return tempString
}

function addDataToStep(_this,value){
    /*Step index */
    var indx = $(_this).attr("id");

    step_num_data_num[indx]++;

    /*Get type of fields*/
    var stepName = $("#searchbox" + indx).val();
    if(stepName.indexOf("Edit") == -1){
        /* single column field */
        $(_this).parent().append("	<fieldset class='searchbox"+indx+''+step_num_data_num[indx] + "data'>"+
            "						<legend class='Text'><b>Data " + step_num_data_num[indx] + "</b></legend>"+
            "<div >" +
            "<textarea class='data' placeholder='Enter Data' style = 'position:relative; width:534px;height:100px;max-height: 150px;max-width: 534px;margin:5px;'/>" +
            "</div>" +
            "</fieldset>");
        $(".searchbox"+indx+''+step_num_data_num[indx] + "data  textarea.data").val(dataArrayToString(value));
    }else{
        /* double column field */
        $(_this).parent().append("	<fieldset class='searchbox"+indx+''+step_num_data_num[indx] + "data' >"+
            "						<legend class='Text'><b>Data " + step_num_data_num[indx] + "</b></legend>"+
            "<div style='position:relative; left:2px;'>"
            + "<textarea class='dataEdit' data-id='edit' placeholder='From...' style = 'width:300px;height:100px;max-height: 200px;max-width: 300px;margin:5px;'/>"
            + "<textarea class='dataEdit' data-id='edit' placeholder='To...' style = 'position:relative; width:300px;height:100px;max-height: 200px;max-width: 300px;margin:5px; 5px 5px 0'/>" +
            "</div>"+
            "</fieldset>");
        $(".searchbox"+indx+''+step_num_data_num[indx] + "data  textarea:eq("+0+")").val(dataArrayToString(value[0]));
        $(".searchbox"+indx+''+step_num_data_num[indx] + "data  textarea:eq("+1+")").val(dataArrayToString(value[1]));
    }
}

function validate_data(str){
    var patt1 = /\(|,|\)|\[|\]/g;

    var format_error = false;
    var error_location;
    var list = str.match(patt1);
    var temp = []

    if(list === null){
        return false;
    }

    for(var i = 0; i < list.length; i++){
        if(list[i] == '(' || list[i] == ',' || list[i] == '['){
            temp.unshift(list[i]);
            continue;
        }
        if(list[i] == ')'){
            if(temp[0] == ',' && temp[1] == '('){
                temp.shift();
                temp.shift();
            }else{
                format_error = true;
                return false;
            }
            if(temp[0] == ','){
                temp.shift();
            }
            continue;
        }

        if(list[i] == ']'){
            if(temp[0] == '['){
                temp.shift();
            }else{
                format_error = true;
                return false;
            }
            continue;
        }
    }

    return true;
}

function AddAutoCompleteSearchBox(WhereToPlaceId, Label, stepNumber) {
    var visibility="";
    if(indx!=-1 && URL.length<30){
        visibility="none";
    }
    else{
        visibility="block";
    }
    $(WhereToPlaceId).append(
        "<form id='AutoSearchResult" + stepNumber + "' class='new_tc_form'>" +

            "	<fieldset>"+
            "		<legend class='Text'><b>" + Label + "</b></legend>"+
            "		<input class='ui-corner-all stepbox ui-autocomplete-input' id='searchbox" + stepNumber + "' type='text'"+
            "		title='Please Type Keyword and Click On that to add to query' name='searchboxname" + stepNumber + "' autocomplete='off'"+
            "		aria-autocomplete='list' aria-haspopup='true'>" +

            "<div id='searchbox"+stepNumber+"infotab' style='display:"+visibility+"'>"+
            "<br><table  width='100%'>" +
            "<tr width='100%'>" +
            "<td width='20%' align='left'><img  class='Text' id='" + stepNumber + "step_desc' src='/site_media/info_button.jpg' style='background-color: transparent; width:20px; height:20px'/> </td>" +
            "<td width='40%' align='left'><span class='Text'><b>Type:</b><span id='searchbox"+stepNumber+"step_type'></span></span></td>" +
            "<td width='40%' align='right'><span style='color: darkslateblue'><b>Verification Point:</b></span><input type='checkbox' id='searchbox"+stepNumber+"verify' value='yes'/></td>" +
            "</tr>" +
            "</table><br>"+
            "       <legend class='Text'><b style='color: #ff0000'>*</b><b>Description:</b></legend>" +
            "       <textarea class='ui-corner-all  ui-autocomplete-input' id='searchbox" + stepNumber + "info' type='text'"+
            "		title='Please type the purpose of the test step' rows=\"3\" cols=\"60\"  name='searchboxname" + stepNumber + "' autocomplete='off'"+
            "		aria-autocomplete='list' aria-haspopup='true'></textarea>" +

            "       <legend class='Text'><b style='color: #ff0000'>*</b><b>Expected:</b></legend>" +
            "       <textarea class='ui-corner-all  ui-autocomplete-input' id='searchbox" + stepNumber + "expected' type='text'"+
            "		title='Please type the purpose of the test step' rows=\"3\" cols=\"60\"name='searchboxname" + stepNumber + "' autocomplete='off'"+
            "		aria-autocomplete='list' aria-haspopup='true'></textarea>" +
            "       </div>"+

            "		<div id='searchbox"+stepNumber+"data' style='display:none; text-align: right;margin:10px'>"+
            "			<a class='Text'>Test Data </a>"+
            "			<img class='add_test_data buttonCustom' id='" + stepNumber + "' src='/site_media/add_step.png' style='background-color: transparent; width:20px; height:20px'>"+
            "			<img class='remove_test_data buttonCustom' id='" + stepNumber + "' src='/site_media/remove_step.png' style='background-color: transparent; width:20px; height:20px'>"+
            "		</div>" +
            "	</fieldset>"+
            "</form>");

    return "searchbox" + stepNumber;
}

function AddAutoCompleteToTag() {
    $("#tag_txtbox").autocomplete({
        source : function(request, response) {
            $.ajax({
                url : "AutoCompleteTagSearch/",
                dataType : "json",
                data : {
                    term : request.term,
                    Env : Env
                },
                success : function(data) {
                    response(data);
                }
            });
        },

        // source : 'AutoCompleteTagSearch?Env = ' +Env,
        select : function(event, ui) {

            var value = ui.item[0].split("-");

            if (value != "") {
                AddToListTag(value);
            }
            return false;
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };;
    $("#tag_txtbox").keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();

        }
    });
}

function RunTestAutocompleteSearch(Env, step) {
    auto_complete_list = [];
    $(".stepbox").autocomplete({
        // Calling AutoCompleteTestSearch function with 'term'(default)
        // parameter and Env variable
        // So AutoCompleteTestSearch function in View.py will receive
        // two variable 'term' (this is the one when user type on search
        // box) and Env variable.

        /*
         * source : 'AutoCompleteTestStepSearch' ,
         *
         * extraParams: { Env: function() {return Env}, },
         */

        source : function(request, response) {
            $.ajax({
                url : "AutoCompleteTestStepSearch/",
                dataType : "json",
                data : {
                    term : request.term
                },
                success : function(data) {
                    //console.log(data);
                    auto_complete_list = data;
                    //console.log(auto_complete_list[3]);
                    var just_names = []

                    for(var i = 0; i < data.length; i++){
                        just_names.push(auto_complete_list[i][0]+' - '+auto_complete_list[i][2]);
                    }

                    response(just_names);
                }
            });
        },

        // source : 'AutoCompleteTestStepSearch?Env = ' +Env,
        select : function(event, ui) {

            var values = ui.item.value.split(' -')
            //console.log(values);
            //console.log(this.id);//console.log('in select'+ui.item.value);
            var value=values[0];
            var step_type=values[1].trim();
            var colour="";
            if(step_type=="automated"){
                colour="green";
            }
            if(step_type=="manual"){
                colour="red";
            }
            if(step_type=="performance"){
                colour="blue";
            }
            if (value != "") {
                this.value = value;
                for(var i = 0; i < auto_complete_list.length; i++){
                    if(auto_complete_list[i][0] == value){
                        //console.log(this.id);
                        var position=this.id.indexOf("1");
                        //console.log(position);
                        var string=this.id.substring(position);
                        //console.log(string);
                        $("#" + this.id + "step_type").html("<b style='color:"+colour+"'>"+step_type+"</b>");
                        // $("#" + this.id + "info").val(auto_complete_list[i][3]);
                        $("#" + this.id + "infotab").fadeIn(500);
                        if(auto_complete_list[i][1] === true){
                            $("#" + this.id + "data").fadeIn(500);
                        }
                        else{
                            $("#" + this.id + "data").fadeOut(500);
                        }
                    }
                }

            }
            return false;
        }
    });

    $(".stepbox").keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();

        }
    });
}

function DeleteSearchQueryText() {
    $(".delete").live("click", function() {
        $(this).parent().parent().remove();
    });
}

// Add an item to an html list
function AddToListTag(text) {
    $("#searchedtag").append(
        '<tr><td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
            + '<td class="submitquery" class = "Text" style = "size:10">' + text + "&nbsp;&nbsp;&nbsp;"
            + '</td></tr>');
}
