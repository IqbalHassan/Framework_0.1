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
    indx = URL.indexOf("CreateNew");
    console.log("Create Index:"+indx);
    indx2 = URL.indexOf("Edit");
    console.log("Edit Index:"+indx2);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf("CreateNew") != -1;
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
            if($('#'+tablename+' tr').length>2){
                $('#'+tablename+' tr:last').remove();
            }
        });
        $('.data-popup').live('click',function(){
            var id=$(this).closest('tr').find('td:nth-child(2)').text().trim();
            $('#searchbox'+id+'datapop').dialog({
                buttons : {
                    "OK" : function() {
                        checkFunction($(this).attr('id'));
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
        /*****************estd time picker************************
        $('.est_time_img').live('click',function(){
            //var id=$(this).closest('tr').find('td:nth-child(9)').text().trim();
            var id = '';
            id += '<table><tr>' +
                '<td><input id="hours" class="textbox" placeholder="hours"></td>' +
                '<td><input id="minutes" class="textbox" placeholder="minutes"></td>' +
                '<td><input id="seconds" class="textbox" placeholder="seconds"></td>' +
                '</tr></table>';
            $("#est_time").dialog({
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
                title: "Data: Step Estimated Time"
            });
        });
        /**************************************************/

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
        DeleteSearchQueryText();
        if(indx2 != -1 || template){
            $.get("TestCase_EditData",
            {
                TC_Id : URL.substring(URL.lastIndexOf("/")+1,URL.length)
            },
            function(data){
                console.log(data);
                /******************Properties tab Data*******************************/
                //Status
                var status=data['Status'];
                console.log(status);
                if(status=="Ready"){
                    $('a[value="Production"]').addClass('selected');
                }
                if(status=="Dev"){
                    $('a[value="Development"]').addClass('selected');
                }
                if(status=="Forced"){
                    $('a[value="Forced-Manual"]').addClass('selected');
                }
                //TagList
                var tag_list=data['Tags List'];
                if(tag_list.length!=0){
                    for(var i=0;i<tag_list.length;i++){
                        console.log(tag_list);
                        if(tag_list[i]!=""){
                            AddToListTag(tag_list[i]);
                        }
                    }
                }
                //SectionPath
                var sections=data['Section_Path'];
                var sectionArray = sections.split('.');
                var dataId ="";
                var handlerString = "";
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
                //Priority
                var priority=data['Priority'];
                $("#priotiy_select").val(parseInt(priority.substring(1,2)));
                /*************** End Properties tab Data*******************************/
                /****************************Parameters Tab*****************************/
                //Select Platform
                var platform=data['Platform'];
                console.log(platform);
                for(var i=0;i<platform.length;i++){
                    $('input[name="platform"]').each(function(){
                        if($(this).val()==platform[i]){
                            $(this).attr('checked','true');
                        }
                    });
                }
                if($('input[name="platform"]:checked').length>0){
                    $("#platform-flag").removeClass("unfilled");
                    $("#platform-flag").addClass("filled");
                }
                else{
                    $("#platform-flag").removeClass("filled");
                    $("#platform-flag").addClass("unfilled");
                }
                //Select Browsers/Dependency
                var dependency=data['Dependency List'];
                for(var i=0;i<dependency.length;i++){
                    $('input[name="dependancy"]').each(function(){
                        if($(this).val()==dependency[i]){
                            $(this).attr('checked','true');
                        }
                    })
                };
                if($('input[name="dependancy"]:checked').length>0){
                    $("#browser-flag").removeClass("unfilled");
                    $("#browser-flag").addClass("filled");
                }
                else{
                    $("#browser-flag").removeClass("filled");
                    $("#browser-flag").addClass("unfilled");
                }
                //Type Select
                var tc_type=data['TC Type'];
                for(var i=0;i<tc_type.length;i++){
                    $('input[name="type"]').each(function(){
                        if($(this).val()==tc_type[i]){
                            $(this).attr('checked','true');
                        }
                    })
                };
                if($('input[name="type"]:checked').length>0){
                    $("#type-flag").removeClass("unfilled");
                    $("#type-flag").addClass("filled");
                }
                else{
                    $("#type-flag").removeClass("filled");
                    $("#type-flag").addClass("unfilled");
                }
                /****************************End Parameters Tab*****************************/
                /****************************RelatedItems Tab*******************************/
                var req_id = data['Requirement Ids'];
                var assoc_bugs = data['Associated Bugs'];
                var tc_id = data['Manual_TC_Id'];
                //AssociatedBug
                $('#defectid_txtbox').val(assoc_bugs);
                //Manual Test Case Id
                $('#id_txtbox').val(tc_id);
                //Requirement Id
                $('#reqid_txtbox').val(req_id);
                if(!template){
                    var auto_id=data['TC_Id'];
                    var title=data['TC_Name'];
                    $('#TC_Id').html("<b>Automation ID: "+auto_id +"</b>")
                    $('#TC_Id').css('display','block');
                    $('#titlebox').val(title);
                }
                /************************End RelatedItems Tab*******************************/
                /***************************Steps Tab***************************************/
                var steps_and_data = data['Steps and Data'];
                //$('#steps_table').html("");
                for(var i=0;i<(steps_and_data.length-1);i++){
                    addMainTableRow('#steps_table');
                }
                var row_count=$('#steps_table tr').length;
                var converted_data=[];
                console.log(row_count);
                popupdivrowcount=[];
                for(var i=0;i<row_count;i++){
                    $('#searchbox'+(i+1)+'name').val(steps_and_data[i][0]);
                    $('#searchbox'+(i+1)+'info').val(steps_and_data[i][3]);
                    $('#searchbox'+(i+1)+'expected').val(steps_and_data[i][4]);
                    $('#searchbox'+(i+1)+'step_type').text(steps_and_data[i][2]);
                    if(steps_and_data[i][5]=='yes'){
                        $('#searchbox'+(i+1)+'verify').attr('checked','true');
                    }
                    $('#searchbox'+(i+1)+'descriptionpop').html(steps_and_data[i][6]);
                    $('#searchbox'+(i+1)+'step_desc').find('span:eq(0)').addClass('filled');
                    $('#searchbox'+(i+1)+'time').val(convertToString(steps_and_data[i][7]));
                    var datasets=steps_and_data[i][1];
                    popupdivrowcount[i]=0;
                    if(datasets.length==0){
                        //$('#searchbox'+(i+1)+'data').html("");
                        $('#searchbox'+(i+1)+'data').parent().css({'cursor':'none'});
                    }
                    else{
                        for(var j=0;j<datasets.length;j++){
                            var temp=[];
                            addnewrow('#searchbox'+(i+1)+'data_table',(i+1),(popupdivrowcount[i]+1));
                            popupdivrowcount[i]++;
                            var currentdataset=datasets[j];
                            for(var k=0;k<currentdataset.length;k++){
                                if(currentdataset[k][1] instanceof Array){
                                    for(var l=0;l<currentdataset[k][1].length;l++){
                                        var tempObject={field:currentdataset[k][0],sub_field:currentdataset[k][1][l][0],value:currentdataset[k][1][l][0]};
                                        temp.push(tempObject);
                                    }
                                }
                                else{
                                    var tempobject={field:currentdataset[k][0],sub_field:"",value:currentdataset[k][1]};
                                    temp.push(tempobject);
                                }
                            }
                            for(var k=0;k<(temp.length-1);k++){
                                adddataentry('step'+(i+1)+'data'+(j+1)+'entrytable');
                            }
                            var currentrow=$('#step'+(i+1)+'data'+(j+1)+'entrytable tr:eq(1)');
                            for(var k=0;k<temp.length;k++){
                                currentrow.find('td:eq(0)').find('input:eq(0)').val(temp[k].field);
                                currentrow.find('td:eq(1)').find('input:eq(0)').val(temp[k].sub_field);
                                currentrow.find('td:eq(2)').find('textarea:eq(0)').val(temp[k].value);
                                currentrow=currentrow.next();
                            }
                            if(temp.length>0){
                                $('#searchbox'+(i+1)+'data').find('span:eq(0)').removeClass('unfilled');
                                $('#searchbox'+(i+1)+'data').find('span:eq(0)').addClass('filled');
                            }
                            else{
                                $('#searchbox'+(i+1)+'data').find('span:eq(0)').removeClass('filled');
                                $('#searchbox'+(i+1)+'data').find('span:eq(0)').addClass('unfilled');
                            }
                        }
                    }
                }
                /***************************End Steps Tab***************************************/
            });

        }

        $('#submit').live('click',function(){
            /*****************************Validation Check Here***********************************/
            if($('#section-flag').hasClass('unfilled')){
                alert("Section Path is not defined Correctly");
                return false;
            }
            if($('#platform-flag').hasClass('unfilled')){
                alert("Platform is not selected correctly");
                return false;
            }
            if($('#browser-flag').hasClass('unfilled')){
                alert("Browser is not selected correctly");
                return false;
            }
            if($('#type-flag').hasClass('unfilled')){
                alert("Test Type is not defined correctly");
                return false;
            }
            var row_count=$('#steps_table tr').length;
            for(var i=0;i<row_count;i++){
                if($('#searchbox'+(i+1)+'data').html()==""){
                    continue;
                }
                else{
                    if($('#searchbox'+(i+1)+'data').find('span:eq(0)').hasClass('unfilled')){
                        alert("Data in the Step #"+(i+1)+" is not complete");
                        return false;
                    }
                }
            }
            var checked_count=0;
            for(var i=0;i<row_count;i++){
                if($('#searchbox'+(i+1)+'verify').attr('checked')=='checked'){
                    checked_count++;
                }
            }
            if(checked_count<=0){
                alert("Atleast One step is to be set as Verfication point");
                return false;
            }
            /******************************END Validation Check here*******************************/
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
            //Get TC_ID for the test case
            var _TC_Id = $('#TC_Id').html().substring($('#TC_Id').html().indexOf(": ")+2,$('#TC_Id').html().indexOf("</b>"))
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
            var stepTimeList=[];
            var finalArray=[];
            for(var i=1;i<=step_num;i++){
                if($('#searchbox'+i+'name').val()==""){
                    alert('Step Name for step Number#'+i+' can not be empty');
                    return false;
                }
                else{
                    if($('#searchbox'+i+'info').val()==""){
                        alert('Step Description for step Number#'+i+' can not be empty');
                        return false;
                    }
                    if($('#searchbox'+i+'expected').val()==""){
                        alert('Expected Result for step Number#'+i+' can not be empty');
                        return false;
                    }
                    if($('#searchbox'+i+'time').val()==""){
                        alert('Estimated time for step Number#'+i+' can not be empty');
                        return false;
                    }
                    stepNameList.push($('#searchbox'+i+'name').val());
                    stepExpectedList.push($('#searchbox'+i+'expected').val());
                    stepDescriptionList.push($('#searchbox'+i+'info').val());
                    if($('#searchbox'+i+'verify').attr('checked')==='checked'){
                        stepVerificationList.push('yes');
                    }
                    else{
                        stepVerificationList.push('no');
                    }
                    /******************Convert into the seconds*******************/
                    var stringTime=$('#searchbox'+i+'time').val();
                    stepTimeList.push(convertToSeconds(stringTime));
                    /************************End Convert into seconds*****************/
                    var step_array=[];
                    if(popupdivrowcount[i-1]==0){
                        finalArray[i-1]=undefined;
                    }
                    else{
                        if($('#searchbox'+i+'data_table').attr('data-id')=='edit'){
                            var combined_array=[];
                            for(var l=0;l<2;l++){
                                var row_number=$('#searchbox'+i+'data_table table:eq('+l+') tr').length-1;
                                var temptableid=$('#searchbox'+i+'data_table table:eq('+l+')');
                                var row=temptableid.find('tr:eq(1)');
                                var tempArray=[];
                                for(var k=0;k<row_number;k++){
                                    var field=row.find('td:eq(0) input:eq(0)').val();
                                    var sub_field=row.find('td:eq(1) input:eq(0)').val();
                                    var value=row.find('td:eq(2) textarea:eq(0)').val();
                                    var tempObject={field:field , sub_field:sub_field ,value:value};
                                    tempArray.push(tempObject);
                                    row=row.next();
                                }
                                combined_array.push(tempArray);
                            }
                            step_array.push(combined_array);
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
                        if($('#searchbox'+j+'data_table').attr('data-id')=='edit'){
                            var currentDataSet=stepData[j-1];
                            var edit_data=[]
                            for(var k=0;k<currentDataSet.length;k++){
                                var mainFields=[];
                                var subFieldskey=[];
                                var withsubFields=[];
                                for(var l=0;l<currentDataSet[k].length;l++){
                                    var temp=currentDataSet[k][l];
                                    if(temp.sub_field==""){
                                        var temp_object={mainField:temp.field,fieldValue:temp.value};
                                        mainFields.push(temp_object);
                                    }
                                    else{
                                        var field_name=temp.field;
                                        if($.inArray(field_name,subFieldskey)===-1){
                                            subFieldskey.push(field_name);
                                        }
                                        withsubFields.push(temp);
                                    }
                                }
                                /***************************create old format Data*********************************/
                                var temp="";
                                temp+="[";
                                for(var m=0;m<mainFields.length;m++){
                                    temp+=("("+mainFields[m].mainField+","+mainFields[m].fieldValue+"),");
                                }
                                if(withsubFields.length==0 && subFieldskey==0){
                                    temp=temp.substring(0,temp.length-1);
                                    temp+="]";
                                }
                                else{
                                    for(var n=0;n<subFieldskey.length;n++){
                                        var mainField=subFieldskey[k];
                                        temp+=("("+mainField+",[");
                                        for(var o=0;o<withsubFields.length;o++){
                                            if(mainField==withsubFields[o].field){
                                                temp+=("("+withsubFields[o].sub_field+","+withsubFields[o].value+"),");
                                            }
                                        }
                                        temp=temp.substring(0,temp.length-1);
                                        temp+="]),";
                                    }
                                    temp=temp.substring(0,temp.length-1);
                                    temp+="]";
                                }
                                console.log(temp);
                                edit_data.push(temp);
                                /*************************** end create old format Data*********************************/
                            }
                            tempSTR.push(edit_data.join('#'));
                        }
                        else{
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
                    Steps_Time_List:stepTimeList.join("|"),
                    Status:"Dev"},function(data) {
                    //alert(data);
                    var location='/Home/ManageTestCases/Edit/'+data;
                    window.location=location;
                });
            }else if(query == "e"){
                $.get("Edit_TestCase",{
                        Section_Path:newSectionPath,
                        TC_Id:_TC_Id,
                        Platform:platformList.join("|"),
                        Manual_TC_Id:test_case_Id,
                        TC_Name:title,
                        TC_Creator:'Test',
                        Associated_Bugs_List:defectId,
                        Requirement_ID_List:required_Id,
                        Status:status,
                        TC_Type:typeList.join("|"),
                        Tag_List:tag.join("|"),
                        Dependency_List:browserList.join("|"),
                        Priority:priority,
                        Steps_Data_List:stepDataSTR.join("|"),
                        Steps_Name_List:stepNameList.join("|"),
                        Steps_Description_List:stepDescriptionList.join("|"),
                        Steps_Expected_List:stepExpectedList.join("|"),
                        Steps_Verify_List:stepVerificationList.join("|"),
                        Steps_Time_List:stepTimeList.join("|")
                    },
                    function(data) {
                        //alert(data+" edited successfully");
                        var location='/Home/ManageTestCases/Edit/'+data;
                        window.location=location;
                    });
                }
            });
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
                var index=$(this).attr('id').split('x')[1].split('n')[0].trim();
                if(value!=""){
                    fieldName.val(value);
                    if(ui.item[1]){
                        /*var index=fieldName.closest('tr').attr('id').split('_')[1].trim();
                        fieldName.closest('tr').find('td:nth-child(4)').html('<a id="searchbox'+index+'data" class="data-popup notification-indicator tooltipped downwards" data-gotokey="n">' +
                        '<span class="mail-status"></span>' +
                        '</a>');*/
                        fieldName.closest('tr').find('td:nth-child(4) span:eq(0)').addClass('unfilled');
                        fieldName.closest('tr').find('td:nth-child(4)').css({'cursor':'pointer'});
                    }else{
                        fieldName.closest('tr').find('td:nth-child(4) span:eq(0)').removeClass('unfilled');
                        fieldName.closest('tr').find('td:nth-child(4) span:eq(0)').removeClass('filled');
                        fieldName.closest('tr').find('td:nth-child(4)').css({
                            'cursor':'none'
                        });
                    }
                    fieldName.closest('tr').find('td:nth-child(8)').html(ui.item[2]);
                    if(ui.item[3]!=""){
                        fieldName.closest('tr').find('td:nth-child(10) span:eq(0)').addClass('filled');
                        $('#searchbox'+fieldName.closest('tr').find('td:nth-child(2)').text()+'descriptionpop').html(ui.item[3]);
                    }
                    else{
                        fieldName.closest('tr').find('td:nth-child(9) span:eq(10)').addClass('unfilled');
                        $('#searchbox'+fieldName.closest('tr').find('td:nth-child(2)').text()+'descriptionpop').html("");
                    }
                    if(ui.item[4]){
                        var divname='#searchbox'+index+'data_table';
                        $(divname).parent().find('div:eq(0)').remove();
                        $(divname).html("");
                        $(divname).attr('data-id','edit');
                        editTypeRow(divname,index,1,"From");
                        editTypeRow(divname,index,1,"To");
                        popupdivrowcount[index-1]=1;
                    }
                    else{
                        var divname='#searchbox'+index+'data_table';
                        $(divname).parent().find('div:eq(0)').remove();
                        $(divname).removeAttr('data-id');
                        $(divname).css({'align':'center'});
                        $(divname).html(GeneratePopUpMetaData());
                        popupdivrowcount[index-1]=0;
                    }
                    if(ui.item[5]!=""){
                        $('#searchbox'+index+'info').val(ui.item[5].trim());
                    }
                    if(ui.item[6]!=""){
                        $('#searchbox'+index+'expected').val(ui.item[6].trim());
                    }
                    if(ui.item[7]){
                        $('#searchbox'+index+'verify').attr('checked',true);
                    }
                    if(ui.item[8]){
                        $('#searchbox'+index+'time').val(convertToString(ui.item[8]));
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
function convertToString(intTime){
    var hour=Math.floor(intTime/3600);
    intTime=intTime%3600;
    var minuate=Math.floor(intTime/60);
    intTime=intTime%60;
    if(hour<10){
        hour="0"+hour;
    }
    if(minuate<10){
        minuate="0"+minuate;
    }
    if(intTime<10){
        intTime="0"+intTime;
    }
    var stringTime=hour+":"+minuate+":"+intTime;
    return stringTime.trim();
}
function convertToSeconds(stringTime){
    var hour=stringTime.split(":")[0].trim();
    var minuate=stringTime.split(":")[1].trim();
    var seconds=stringTime.split(":")[2].trim();
    var total=(hour*3600)+(minuate*60)+(seconds*1);
    return total;
}
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
        currentrow.find('td:nth-child(9) input:eq(0)').attr('id','searchbox'+i+'time');
        currentrow.find('td:nth-child(10) a:eq(0)').attr('id','searchbox'+i+'step_desc');
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
        if(temptable.attr('data-id')=='edit'){
            var stringName=['From','To'];
            count=0;
            var tempColumn=temptable.find('tbody:eq(0) tr:eq(0)');
            while(count<2){
                tempColumn.find('td:eq(1) table:eq(0)').attr('id','step'+i+stringName[count]+'entrytable');
                tempColumn.attr('id','step'+i+'data1'+stringName[count]);
                count++;
                tempColumn=tempColumn.next();
            }
        }
        else{
            for(var j=1;j<=innercolumncount;j++){
                var tempColumn=innercolumn;
                tempColumn.find('td:eq(1) table:eq(0)').attr('id','step'+i+'data'+j+'entrytable');
                tempColumn.attr('id','step'+i+'data'+j);
                innercolumn=innercolumn.next();
            }
        }
        temptable.attr('id','searchbox'+i+'data_table');
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
function editTypeRow(divname,stepno,dataset_num,stringName){
    var message="";
    message+=('<tr id="step'+stepno+'data'+dataset_num+stringName+'">' +
        '<td>'+stringName+'</td>' +
        '<td>' +
    /******************dataset nested table(start)************/
        /*id="step'+stepno+'data'+dataset_num+stringName+'entrytable"*/
        '<table id="step'+stepno+stringName+'entrytable" class="one-column-emphasis" width="100%" style="font-size:75%">' +
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
            '<td><div class="input-append bootstrap-timepicker">' +
            '<input id="searchbox'+step_num+'time" type="text" class="input-small textbox timepicker">' +
            '<span class="add-on"><i class="icon-time"></i></span></div></td>' +
            //'<td><img class="new_tc_form est_time_img" id="searchbox'+step_num+'step_est_time" type=\'image\' src=\'/site_media/clock.png\' style=\"background-color: transparent; width:16px; height:16px;cursor:pointer\"></td>' +
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
        '<div class="new_tc_form" align="center" style="text-align: center">' +
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
    TimePicker();
}
function addMainTableRow(divname){
    step_num++;
    popupdivrowcount[step_num-1]=0;
    $('#outer-data').append('<div id="searchbox'+step_num+'datapop">'+GeneratePopUpMetaData()+'</div>');
    $('#step_description_general').append('<div id="searchbox'+step_num+'descriptionpop"></div>');
    $(divname).append(GenerateMainRow());
    AutoCompleteTestStep();
    TimePicker();
}
function TimePicker(){
    $('.timepicker').timepicker({
        minuteStep: 1,
        template: 'dropdown',
        appendWidgetTo: 'body',
        showSeconds: true,
        showMeridian: false,
        defaultTime: false,
        secondStep: 1
    });
}
function checkFunction(divname){
    var status="";
    var index=divname.split('x')[1].split('d')[0].trim();
    if(popupdivrowcount[index-1]<=0){
        //alert("No dataset is included");
        $('#searchbox'+index+'data').find('span:eq(0)').addClass('unfilled');
    }
    else{
        for(var i=0;i<popupdivrowcount[index-1];i++){
            var tablename=$('#step'+index+'data'+(i+1)+'entrytable');
            var row_count=tablename.find('tr').length;
            var currentrow=tablename.find('tr:eq(1)');
            for(var j=0;j<row_count-1;j++){
                if(currentrow.find('td:eq(0) input:eq(0)').val()==""||currentrow.find('td:eq(2) textarea:eq(0)').val()==""){
                    status="false";
                    break;
                }
                currentrow=currentrow.next();
            }
            if(status!=""){
                break;
            }
        }
        if(status=="false"){
            $('#searchbox'+index+'data').find('span:eq(0)').removeClass('filled');
            $('#searchbox'+index+'data').find('span:eq(0)').addClass('unfilled');
        }
        else{
            $('#searchbox'+index+'data').find('span:eq(0)').removeClass('unfilled');
            $('#searchbox'+index+'data').find('span:eq(0)').addClass('filled');
        }
    }
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
