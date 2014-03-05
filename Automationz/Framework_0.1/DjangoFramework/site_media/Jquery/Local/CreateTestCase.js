/**
 * Created by minar09 on 2/10/14.
 */


var indx=0;
var indx2=0;
var URL="";
var step_num = 0;
var step_num_data_num = new Array();
var tag_list = new Array();
var Env = "PC";
var lowest_section = 0;
var isAtLowestSection = false;
var popupdivrowcount=[];
$(document).ready(function() {
    addMainTableRow('#steps_table');
    check_required_data();
    show_radio_button();

    /*****************Shetu's Function************************/
    AutoCompleteTag();
    /*****************End Shetu************************/
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
        //Here the things will be added
        //AutoCompleteTagSearch

        $('#add_test_step').live('click',function(){
            addMainTableRow('#steps_table');

        });
        $('#remove_test_step').live('click',function(){
            var id=$('#steps_table tr:last').attr('id').split('_')[1].trim();
            $('#searchbox'+id+'datapop').remove();
            $('#steps_table tr:last').remove();
            step_num--;
            popupdivrowcount.pop();
        });
        /********************For Specific Index Change********************************************/
        $('.add_after_img').live('click',function(){
            var step_id=$(this).closest('tr').attr('id').split('_')[1].trim();
            //console.log('will be added after '+$('#steps_table>tr:eq('+(step_id-1)+')').attr('id'));
            //console.log('will be added after '+$('#searchbox'+step_id+'datapop').attr('id'));
            addMainTableRowFixedPlace(step_id);
            var temp=popupdivrowcount.pop();
            popupdivrowcount.splice(step_id,0,temp);
            reOrganize();
        });
        $('.remove_img').live('click',function(){
            var step_id=$(this).closest('tr');
            var index=step_id.attr('id').split('_')[1].trim();
            $('#searchbox'+index+'datapop').remove();
            $('#searchbox'+index+'descriptionpop').remove();
            step_id.remove();
            step_num--;
            resetArray(index);
            reOrganize();
        });
        /********************For Specific Index Change END********************************************/
        /********************DataPopUP Function********************************************/
        $('.add_dataset_row').live('click',function(){
            var divnum=$(this).parent().parent().attr('id').split('d')[0].split('x')[1].trim();
            var divname='#searchbox'+divnum+'data_table';
            addnewrow(divname,divnum,(popupdivrowcount[divnum-1]+1));
            popupdivrowcount[divnum-1]++;
            if(popupdivrowcount[divnum-1]>0){
                $('#searchbox'+divnum+'data span:eq(0)').removeClass('unfilled');
                $('#searchbox'+divnum+'data span:eq(0)').addClass('filled');
            }
            //reOrganize();
        });
        $('.remove_dataset_row').live('click',function(){
            var divnum=$(this).parent().parent().attr('id').split('d')[0].split('x')[1].trim();
            var divname='#searchbox'+divnum+'data_table';
            var row_name=$('#step'+divnum+'data'+popupdivrowcount[divnum-1]);
            row_name.remove();
            popupdivrowcount[divnum-1]--;
            if(popupdivrowcount[divnum-1]<=0){
                $('#searchbox'+divnum+'data span:eq(0)').removeClass('filled');
                $('#searchbox'+divnum+'data span:eq(0)').addClass('unfilled');
            }
        });
        $('.add_dataset_entry').live('click',function(){
            var tablename=$(this).parent().parent().find('table:eq(0)').attr('id');
            adddataentry(tablename);
        });
        $('.remove_dataset_entry').live('click',function(){
            var tablename=$(this).parent().parent().find('table:eq(0)').attr('id');
            if($('#'+tablename+' tr').length>1){
                $('#'+tablename+' tr:last').remove();
            }
        });
        $('.data-popup').live('click',function(){
            var id=$(this).closest('tr').find('td:nth-child(2)').text().trim();
            $('#searchbox'+id+'datapop').dialog({
                buttons : {
                    "OK" : function() {
                        $(this).dialog("destroy");
                    }
                },

                show : {
                    effect : 'drop',
                    direction : "up"
                },

                modal : true,
                width : 800,
                height : 600,
                title: "Data: Step "+id
            });
        });
        $('.descriptionpop').live('click',function(){
            var id=$(this).closest('tr').find('td:nth-child(2)').text().trim();
            $('#searchbox'+id+'descriptionpop').dialog({
                buttons : {
                    "OK" : function() {
                        $(this).dialog("destroy");
                    }
                },

                show : {
                    effect : 'drop',
                    direction : "up"
                },
                textAlign:'center',
                modal : true,
                width : 400,
                height : 400,
                title: "Data: Step "+id
            });
        });
        $('.est_time_img').live('click',function(){
            //var id=$(this).closest('tr').find('td:nth-child(9)').text().trim();
            var id = '';
            id += '<table><tr>' +
                '<td><input id="hours" class="textbox" placeholder="hours"></td>' +
                '<td><input id="minutes" class="textbox" placeholder="minutes"></td>' +
                '<td><input id="seconds" class="textbox" placeholder="seconds"></td>' +
                '</tr></table>'
            $(".est_time_img").dialog({
                buttons : {
                    "OK" : function() {
                        $(this).dialog("destroy");
                    }
                },

                show : {
                    effect : 'drop',
                    direction : "up"
                },
                textAlign:'center',
                modal : true,
                width : 400,
                height : 400,
                title: "Data: Step Estimated Time",
                data: id
            });
        });
        /********************DataPopUP Function End********************************************/
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
            $("#section-flag").removeClass("filled");
            $("#section-flag").addClass("unfilled");
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
        //AddAutoCompleteToTag();
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
                                            $("#section-flag").removeClass("filled");
                                            $("#section-flag").addClass("unfilled");
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
                                $("#section-flag").removeClass("unfilled");
                                $("#section-flag").addClass("filled");
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
                    /*if(enabledStatus == "Ready")
                     $('input[value="Production"]').attr('checked', true);
                     else if(enabledStatus == "Dev")
                     $('input[value="Development"]').attr('checked', true);
                     else if(enabledStatus == "Forced")
                     $('input[value="Forced-Manual"]').attr('checked', true);*/
                    if(enabledStatus == "Ready")
                        $("#enable_radio").addClass("selected");
                    else if(enabledStatus == "Dev")
                        $("#Disable_radio").addClass("selected");
                    else if(enabledStatus == "Forced")
                        $("#Manual_radio").addClass("selected");
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

        $('#submit').live('click',function(){
            /*********************************Properties Tab Data ********************************/
            //Select Status
            var status;
            if($('a[value="Production"]').hasClass('selected'))
                status = "Ready";
            if($('a[value="Development"]').hasClass('selected'))
                status = "Dev";
            if($('a[value="Forced-Manual"]').hasClass('selected'))
                status = "Forced";
            console.log(status);
            //Select Section Name
            var newSectionPath = $("#sectiongroup select.section:last-child").attr("data-level").replace(/ /g,'_') + $("#sectiongroup select.section:last-child option:selected").val().replace(/ /g,'_');
            console.log(newSectionPath);
            //Select Priority
            var priority='P'+$('#priotiy_select option:selected').val();
            console.log(priority);
            //Select Tag
            var tag = new Array();
            for(var i = 0; i < $(".submitquery").length; i++){
                tag.push($(".submitquery:eq("+i+")").html().replace(/&nbsp;/g,''));
            }
            console.log(tag);
            /*********************************End Properties Tab Data ********************************/
            /*********************************Parameters Tab Data ********************************/
            var platformList=[];
            $('input[name="platform"]:checked').each(function(){
               platformList.push($(this).val());
            });
            console.log(platformList);
            var browserList=[];
            $('input[name="dependancy"]:checked').each(function(){
                browserList.push($(this).val());
            });
            console.log(browserList);
            var typeList=[];
            $('input[name="type"]:checked').each(function(){
                typeList.push($(this).val());
            });
            console.log(typeList);
            /*********************************End Parameters Tab Data ********************************/
            /**************************Related Item *************************************************/
            var defectId=$('#defectid_txtbox').val().trim();
            var test_case_Id=$('#id_txtbox').val().trim();
            var required_Id=$('#reqid_txtbox').val().trim();
            var title=$('#titlebox').val().trim();
            /**************************End Related Item *************************************************/
            /***************************DataFetching From the Pop UP*********************************************/
            var stepNameList=[];
            var stepExpectedList=[];
            var stepDescriptionList=[];
            var stepVerificationList=[];
            var finalArray=[];
            for(var i=1;i<=step_num;i++){
                if($('#searchbox'+i+'name').val()==""){
                    alert('Step Name for step Number#'+i+' is not filled correctly');
                    return false;
                }
                else{
                    stepNameList.push($('#searchbox'+i+'name').val());
                    stepExpectedList.push($('#searchbox'+i+'expected').val());
                    stepDescriptionList.push($('#searchbox'+i+'info').val());
                    if($('#searchbox'+i+'verify').attr('checked')==='checked'){
                        stepVerificationList.push('yes');
                    }
                    else{
                        stepVerificationList.push('no');
                    }
                    var step_array=[];
                    if(popupdivrowcount[i-1]==0){
                        finalArray[i-1]=undefined;
                    }
                    else{
                        for(var j=1;j<=popupdivrowcount[i-1];j++){
                            var dataset=[];
                            var tableid=$('#step'+i+'data'+j+'entrytable');
                            console.log(tableid.attr('id'));
                            var tableLength=tableid.find('tr').length;
                            var row=tableid.find('tr:eq(1)');
                            for(var k=0;k<tableLength-1;k++){
                                var field=row.find('td:eq(0) input:eq(0)').val();
                                var sub_field=row.find('td:eq(1) input:eq(0)').val();
                                var value=row.find('td:eq(2) textarea:eq(0)').val();
                                var tempObject={field:field , sub_field:sub_field ,value:value};
                                dataset.push(tempObject);
                                row=row.next();
                            }
                            step_array.push(dataset);
                        }
                        finalArray[i-1]=step_array;
                    }
                };
            }
            /*************************DataFetching from the Pop up***********************************************/
            /*************************Filtering***********************************************/
            var stepDataSTR=[];
            for(var i=1;i<=step_num;i++){
                var tempSTR=[];
                var stepData=finalArray[i-1];
                if(stepData=== undefined){
                    stepDataSTR[i-1]="%";
                }
                /***********************Step Data Processing Here ********************************/
                else{
                    for(var j=1;j<=stepData.length;j++){
                        var currentDataSet=stepData[j-1];
                        var mainFields=[];
                        var subFieldskey=[];
                        var withsubFields=[];
                        for(var k=0;k<currentDataSet.length;k++){
                            //First Check whether it's a mainField or Not
                            if(currentDataSet[k].sub_field==""){
                                var temp_object={mainField:currentDataSet[k].field,fieldValue:currentDataSet[k].value};
                                mainFields.push(temp_object);
                            }
                            else{
                                var field_name=currentDataSet[k].field;
                                if($.inArray(field_name,subFieldskey)===-1){
                                    subFieldskey.push(field_name);
                                }
                                withsubFields.push(currentDataSet[k]);
                            }
                        }
                        /***************************create old format Data*********************************/
                        var temp="";
                        temp+="[";
                        for(var k=0;k<mainFields.length;k++){
                            temp+=("("+mainFields[k].mainField+","+mainFields[k].fieldValue+"),");
                        }
                        if(withsubFields.length==0 && subFieldskey==0){
                            temp=temp.substring(0,temp.length-1);
                            temp+="]";
                        }
                        else{
                            for(var k=0;k<subFieldskey.length;k++){
                                var mainField=subFieldskey[k];
                                temp+=("("+mainField+",[");
                                for(var l=0;l<withsubFields.length;l++){
                                    if(mainField==withsubFields[l].field){
                                        temp+=("("+withsubFields[l].sub_field+","+withsubFields[l].value+"),");
                                    }
                                }
                                temp=temp.substring(0,temp.length-1);
                                temp+="]),";
                            }
                            temp=temp.substring(0,temp.length-1);
                            temp+="]";
                        }
                        console.log(temp);
                        tempSTR.push(temp);
                        /*************************** end create old format Data*********************************/

                    }
                    /*********************** END Step Data Processing Here ********************************/
                    stepDataSTR[i-1]=tempSTR.join('%');
                }
                console.log(stepDataSTR);
            }
            /*************************End Filtering***********************************************/
            /************************End DataFetching From the POP Up*********************************************/
            var query = indx != -1?"c":(indx2 != -1?"e":"o");
            console.log(query);
            if(query == "c"){
                $.get("Submit_New_TestCase/",{
                    Section_Path:newSectionPath,
                    Platform:platformList.join("|"),
                    Manual_TC_Id:test_case_Id,
                    TC_Name:title,
                    TC_Creator:'Test',
                    Associated_Bugs_List:defectId,
                    Requirement_ID_List:required_Id,
                    TC_Type:typeList.join("|"),
                    Tag_List:tag.join("|"),
                    Dependency_List:browserList.join("|"),
                    Priority:priority,
                    Steps_Data_List:stepDataSTR.join("|"),
                    Steps_Name_List:stepNameList.join("|"),
                    Steps_Description_List:stepDescriptionList.join("|"),
                    Steps_Expected_List:stepExpectedList.join("|"),
                    Steps_Verify_List:stepVerificationList.join("|"),
                    Status:"Dev"},function(data) {
                    alert(data);
                });
            }
        });
        /*$('#submit').click(function(){
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
            var status;if($("#enable_radio").hasClass("selected"))
            /*if($('input[value="Production"]').attr('checked') == "checked")
             status = "Ready"
             else if($('input[value="Development"]').attr('checked') == "checked")
             status = "Dev"
             else if($('input[value="Forced-Manual"]').attr('checked') == "checked")
             status = "Forced"*/
             /*   if($("#enable_radio").hasClass("selected"))
                    status = "Ready"
                else if($("#Disable_radio").hasClass("selected"))
                    status = "Dev"
                else if($("#Manual_radio").hasClass("selected"))
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

        });*/
    }

});
/**************************************Database Works**************************************************/
/***********Autocomplete Step name*****************/
function AutoCompleteTestStep(){
    var row_count=$('#steps_table>tr').length;
    for(var i=1;i<=row_count;i++){
        $('#searchbox'+i+'name').autocomplete({
            source:function(request,response){
                $.ajax({
                    url:"AutoCompleteTestStepSearch/",
                    dataType:"json",
                    data:{term:request.term},
                    success:function(data){
                        /*var auto_list=[];
                         for(var i=0;i<data.length;i++){
                         auto_list.push(data[i][0]+'-'+data[i][2]);
                         }
                         response(auto_list);
                         */response(data);
                    }
                });
            },
            select:function(request,ui){
                console.log(ui);
                var value=ui.item[0];
                var fieldName=$('#'+$(this).attr('id'));
                if(value!=""){
                    fieldName.val(value);
                    if(ui.item[1]){
                        fieldName.closest('tr').find('td:nth-child(4) span:eq(0)').addClass('unfilled');
                    }
                    fieldName.closest('tr').find('td:nth-child(8)').html(ui.item[2]);
                    if(ui.item[3]!=""){
                        fieldName.closest('tr').find('td:nth-child(9) span:eq(0)').addClass('filled');
                        $('#searchbox'+fieldName.closest('tr').find('td:nth-child(2)').text()+'descriptionpop').html(ui.item[3]);
                    }
                    else{
                        fieldName.closest('tr').find('td:nth-child(9) span:eq(0)').addClass('unfilled');
                        $('#searchbox'+fieldName.closest('tr').find('td:nth-child(2)').text()+'descriptionpop').html("");
                    }
                }
                return false;
            }
        }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
            return $( "<li></li>" )
                .data( "ui-autocomplete-item", item )
                .append( "<a><strong>" + item[0] + "</strong>-" + item[2] + "</a>" )
                .appendTo( ul );
        };
    }
}
function AutoCompleteTag(){
    $('#tag_txtbox').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"AutoCompleteTag/",
                dataType:"json",
                data:{
                    term:request.term
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            console.log(ui);
            var value=ui.item[0].trim();
            if(value!=""){
                AddToListTag(value);
            }
            return false;
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };
    $("#tag_txtbox").keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();

        }
    });
}
/************End Autocomplete Step name****************/
/**************************************End Database Works**************************************************/
/***********************************Start New Data Pop UP**********************************************************************/
function resetArray(index){
    var temp=[];
    for(var i=0;i<popupdivrowcount.length;i++){
        if(i!=(index-1)){
            temp.push(popupdivrowcount[i]);
        }
    }
    popupdivrowcount=[];
    for(i=0;i<temp.length;i++){
        popupdivrowcount.push(temp[i]);
    }
}
function reOrganize(){
    var row_count=$('#steps_table>tr').length;
    var currentrow=$('#steps_table>tr:first-child')
    /*******************ReOrdering the Main Menu Elements*********************/
    for(var i=1;i<=row_count;i++){
        currentrow.attr('id','step_'+i);
        currentrow.find('td:first-child input:eq(0)').attr('id',i);
        currentrow.find('td:nth-child(2)').text(i);
        currentrow.find('td:nth-child(3) input:eq(0)').attr('id','searchbox'+i+'name');
        currentrow.find('td:nth-child(4) a:eq(0)').attr('id','searchbox'+i+'data');
        currentrow.find('td:nth-child(5) textarea:eq(0)').attr('id','searchbox'+i+'info');
        currentrow.find('td:nth-child(6) textarea:eq(0)').attr('id','searchbox'+i+'expected');
        currentrow.find('td:nth-child(7) input:eq(0)').attr('id','searchbox'+i+'verify');
        currentrow.find('td:nth-child(8) span:eq(0)').attr('id','searchbox'+i+'step_type');
        currentrow.find('td:nth-child(9) a:eq(0)').attr('id','searchbox'+i+'step_desc');
        currentrow=currentrow.closest('tr').next();
    }
    /*******************ReOrdering the Main Menu Elements End*********************/
    /*******************ReOrdering the Pop Up*********************/
    var currentPop=$('#outer-data>div:first');
    for(i=1;i<=row_count;i++){
        //console.log(currentPop.attr('id'));
        var temp=currentPop;
        var temptable=currentPop.find('table:eq(0)');
        var innercolumn=temptable.find('tbody>tr:eq(1)');
        var innercolumncount=popupdivrowcount[i-1];
        temp.attr('id','searchbox'+i+'datapop');
        temptable.attr('id','searchbox'+i+'data_table');
        for(var j=1;j<=innercolumncount;j++){
            var tempColumn=innercolumn;
            tempColumn.attr('id','step'+i+'data'+j);
            innercolumn=innercolumn.next();
        }
        currentPop=currentPop.next();
    }
    var currentdescpop=$('#step_description_general>div:first');
    for(i=1;i<=row_count;i++){
        var temp=currentdescpop;
        temp.attr('id','searchbox'+i+'descriptionpop');
        currentdescpop=currentdescpop.next();
    }
    /*******************ReOrdering the Pop Up End*********************/

}
function adddataentry(tablename){
    var message="";
    message+=(
        '<tr>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><textarea class="ui-corner-all  ui-autocomplete-input"></textarea></td>' +
        '</tr>');
    $('#'+tablename).append(message);
}
function addnewrow(divname,stepno,dataset_num){
    var message="";
    message+=('<tr id="step'+stepno+'data'+dataset_num+'">' +
        '<td>Data Set '+dataset_num+'</td>' +
        '<td>' +
    /******************dataset nested table(start)************/
        '<table id="step'+stepno+'data'+dataset_num+'entrytable"class="one-column-emphasis" width="100%" style="font-size:75%">' +
        '<tr>' +
        '<th width="33%">Field</th>' +
        '<th width="33%">Sub-Field</th>' +
        '<th width="33%">Value</th>' +
        '</tr>' +
        '<tr>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><textarea class="ui-corner-all  ui-autocomplete-input"></textarea></td>' +
        '</tr>' +
        '</table>' +
        '<div class="new_tc_form" style="text-align: center">' +
        '<input class="buttonCustom new_tc_form add_dataset_entry" type=\'image\' src=\'/site_media/plus1.png\' style="background-color: transparent; width:18px; height:18px">' +
        '<input class="buttonCustom new_tc_form remove_dataset_entry" type=\'image\' src=\'/site_media/minus1.png\' style="background-color: transparent; width:18px; height:18px">' +
        '</div>' +
    /******************dataset nested table(end)************/
        '</td>' +
        '</tr>');
    $(divname).append(message);
}
function GenerateMainRow()
{
    var message="";
    message+=(
        '<tr id="step_'+step_num+'">' +
            '<td><input id="'+step_num+'" class="new_tc_form remove_img" type=\'image\' src=\'/site_media/minus2.png\' name=\'Remove Step\' style=\"background-color: transparent; width:18px; height:18px\"></td>' +
            '<td>'+step_num+'</td>' +
            '<td><input class="textbox" id="searchbox'+step_num+'name"style="width: auto" value=""/></td>' +
            '<td style="cursor: pointer"><a id="searchbox'+step_num+'data" class="data-popup notification-indicator tooltipped downwards" data-gotokey="n">' +
            '<span class="mail-status"></span>' +
            '</a></td>' +
            '<td><textarea id="searchbox'+step_num+'info" class="ui-corner-all  ui-autocomplete-input" style="width: 90%"></textarea></td>' +
            '<td><textarea id="searchbox'+step_num+'expected" class="ui-corner-all  ui-autocomplete-input" style="width: 90%"></textarea></td>' +
            '<td><input type="checkbox" id="searchbox'+step_num+'verify" value="yes"></td>' +
            '<td><span id="searchbox'+step_num+'step_type"></span></td>' +
            '<td><input class="new_tc_form est_time_img" id="searchbox'+step_num+'step_est_time" type=\'image\' src=\'/site_media/clock.png\' style=\"background-color: transparent; width:16px; height:16px\"></td>' +
            //'<td><input type="time" step="1" name="time" id="searchbox'+step_num+'step_est_time" class="textbox" style="width: auto"></td>' +
            '<td><a id="searchbox'+step_num+'step_desc" class="descriptionpop notification-indicator tooltipped downwards" data-gotokey="n" style="cursor:pointer;"><span class="mail-status"></span></a></td>' +
            '<td><input class="new_tc_form add_after_img" type=\'image\' src=\'/site_media/new.png\' name=\'Add Step\' style=\"background-color: transparent; width:18px; height:18px\"></td>' +
            '</tr>'
        )
    return message;
}
function GeneratePopUpMetaData(){
    var popupmetadata="";
    popupmetadata+=('<table id="searchbox'+step_num+'data_table" class="one-column-emphasis" width="100%">' +
        '<tr>' +
        '<th width="20%">DataSet</th>' +
        '<th width="80%">Data</th>' +
        '</tr>' +
        '</table>' +
        '<div class="new_tc_form" style="text-align: center">' +
        '<input class="buttonCustom new_tc_form add_dataset_row" type=\'image\' src=\'/site_media/plus1.png\' style="background-color: transparent; width:22px; height:22px">' +
        '<input class="buttonCustom new_tc_form remove_dataset_row" type=\'image\' src=\'/site_media/minus1.png\' style="background-color: transparent; width:22px; height:22px">' +
        '</div>');
    return popupmetadata;
}
function addMainTableRowFixedPlace(fixedPlace){
    step_num++;
    popupdivrowcount[step_num-1]=0;
    $('#steps_table>tr:eq('+(fixedPlace-1)+')').after(GenerateMainRow());
    $('#searchbox'+fixedPlace+'datapop').after('<div id="searchbox'+step_num+'datapop">'+GeneratePopUpMetaData()+'</div>');
    $('#searchbox'+fixedPlace+'descriptionpop').after('<div id="searchbox'+step_num+'descriptionpop"></div>');
    AutoCompleteTestStep();
}
function addMainTableRow(divname){
    step_num++;
    popupdivrowcount[step_num-1]=0;
    $('#outer-data').append('<div id="searchbox'+step_num+'datapop">'+GeneratePopUpMetaData()+'</div>');
    $('#step_description_general').append('<div id="searchbox'+step_num+'descriptionpop"></div>');
    $(divname).append(GenerateMainRow());
    AutoCompleteTestStep();
}
/******************************************END New Data Pop Up***************************************************************/
/****************************Minar's Thing****************************************************/
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
                        $("#section-flag").removeClass("filled");
                        $("#section-flag").addClass("unfilled");
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
                $("#section-flag").removeClass("unfilled");
                $("#section-flag").addClass("filled");
            }
        }
    });
}
function check_required_data()
{
    /*$(".section").live('change',function(){
     if($(".section").val() != "Choose...")
     {
     $("#section-flag").removeClass("unfilled");
     $("#section-flag").addClass("filled");
     }
     else
     {
     $("#section-flag").removeClass("filled");
     $("#section-flag").addClass("unfilled");
     }
     });*/

    $("#PC_radio, #MAC_radio").live('click',function(){
        if(($("#PC_radio").is(':checked') == true) || ($("#MAC_radio").is(':checked') == true)){
            $("#platform-flag").removeClass("unfilled");
            $("#platform-flag").addClass("filled");
        }
        else {
            $("#platform-flag").removeClass("filled");
            $("#platform-flag").addClass("unfilled");
        }
    });

    $(".browser").live('click',function(){
        if(($('#Chrome').is(':checked') == true) || ($('#FireFox').is(':checked') == true) || ($('#IE').is(':checked') == true) || ($('#Safari').is(':checked') == true)){
            $("#browser-flag").removeClass("unfilled");
            $("#browser-flag").addClass("filled");
        }
        else {
            $("#browser-flag").removeClass("filled");
            $("#browser-flag").addClass("unfilled");
        }
    });

    $("#smoke_check, #si_check, #svv_check").live('click',function(){
        if(($('#smoke_check').is(':checked') == true) || ($('#si_check').is(':checked') == true) || ($('#svv_check').is(':checked') == true)){
            $("#type-flag").removeClass("unfilled");
            $("#type-flag").addClass("filled");
        }
        else {
            $("#type-flag").removeClass("filled");
            $("#type-flag").addClass("unfilled");
        }
    });

}
function show_radio_button(){
    $("#enable_radio").live('click',function(){
        $(this).addClass("selected");
        $("#Disable_radio").removeClass("selected");
        $("#Manual_radio").removeClass("selected");
    });
    $("#Disable_radio").live('click',function(){
        $(this).addClass("selected");
        $("#enable_radio").removeClass("selected");
        $("#Manual_radio").removeClass("selected");
    });
    $("#Manual_radio").live('click',function(){
        $(this).addClass("selected");
        $("#Disable_radio").removeClass("selected");
        $("#enable_radio").removeClass("selected");
    });
}
/****************************End Minar's Thing****************************************************/
/****************************Unused****************************************************/
/*function dataArrayToString(array){
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
    //Step index
    var indx = $(_this).attr("id");

    step_num_data_num[indx]++;

    //Get type of fields
    var stepName = $("#searchbox" + indx).val();
    if(stepName.indexOf("Edit") == -1){
        // single column field
        $(_this).parent().append("	<fieldset class='searchbox"+indx+''+step_num_data_num[indx] + "data'>"+
            "						<legend class='Text'><b>Data " + step_num_data_num[indx] + "</b></legend>"+
            "<div >" +
            "<textarea class='data' placeholder='Enter Data' style = 'position:relative; width:534px;height:100px;max-height: 150px;max-width: 534px;margin:5px;'/>" +
            "</div>" +
            "</fieldset>");
        $(".searchbox"+indx+''+step_num_data_num[indx] + "data  textarea.data").val(dataArrayToString(value));
    }else{
        // double column field
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


         * source : 'AutoCompleteTestStepSearch' ,
         *
         * extraParams: { Env: function() {return Env}, },


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
}*/
/****************************End Unused****************************************************/
function DeleteSearchQueryText() {
    $(".delete").live("click", function() {
        $(this).parent().parent().remove();
    });
}

// Add an item to an html list
function AddToListTag(text) {
    $("#searchedtag").append(
        '<tr><td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
            + '<td class="submitquery" class = "Text" style = "size:10;display: inline-block;">' + text + "&nbsp;&nbsp;&nbsp;"
            + '</td></tr>');
}
