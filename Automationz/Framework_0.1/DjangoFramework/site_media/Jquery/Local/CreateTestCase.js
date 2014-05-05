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
    vertical_sidebar();
    AutoCompleteSearchForPrompt();

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
        	alertify.confirm("Are you sure you want to delete the test step?", function(e) {
        		if (e) {
        			var id=$('#steps_table tr:last').attr('id').split('_')[1].trim();
                    $('#searchbox'+id+'datapop').remove();
                    $('#steps_table tr:last').remove();
                    step_num--;
                    popupdivrowcount.pop();        			
        		}
        	});
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
//        	var this_obj = $(this);
			var step_id = $(this).closest('tr');
            var index = step_id.attr('id').split('_')[1].trim();
            var step_number = $(step_id[0]).attr("id").split('_')[1];
        	alertify.confirm("Are you sure you want to delete the test step - " + step_number + "?", function(e) {
        		if (e) {
                    $('#searchbox'+index+'datapop').remove();
                    $('#searchbox'+index+'descriptionpop').remove();
                    step_id.remove();
                    step_num--;
                    resetArray(index);
                    reOrganize();
        		}
        	});
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
            if(($(this).find('span:eq(0)').hasClass('unfilled')) || ($(this).find('span:eq(0)').hasClass('filled'))){
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
            }
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
                        else if(steps_and_data[i][8]){
                            var fromdata=datasets[0][0];
                            var todata=datasets[0][1];
                            console.log(fromdata);
                            console.log(todata);
                            var divname='#searchbox'+(i+1)+'data_table';
                            $(divname).attr('data-id','edit');
                            editTypeRow(divname,i+1,1,"From");
                            editTypeRow(divname,i+1,1,"To");
                            var temp=[];
                            for(var j=0;j<fromdata.length;j++){
                                if(fromdata[j][1] instanceof  Array){
                                    for(var k=0;k<fromdata[j][1].length;k++){
                                        var tempObject={field:fromdata[j][0],sub_field:fromdata[j][1][k][0],value:fromdata[j][1][k][1]};
                                        temp.push(tempObject);
                                    }
                                }
                                else{
                                    var tempobject={field:fromdata[j][0],sub_field:"",value:fromdata[j][1]};
                                    temp.push(tempobject);
                                }
                            }
                            console.log(temp);
                            for(var j=0;j<temp.length-1;j++){
                                adddataentry('step'+(i+1)+'Fromentrytable');
                            }
                            var currentrow=$('#step'+(i+1)+'Fromentrytable tr:eq(1)');
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
                            var temp=[];
                            for(var j=0;j<todata.length;j++){
                                if(todata[j][1] instanceof  Array){
                                    for(var k=0;k<todata[j][1].length;k++){
                                        var tempObject={field:todata[j][0],sub_field:todata[j][1][k][0],value:todata[j][1][k][1]};
                                        temp.push(tempObject);
                                    }
                                }
                                else{
                                    var tempobject={field:todata[j][0],sub_field:"",value:todata[j][1]};
                                    temp.push(tempobject);
                                }
                            }
                            console.log(temp);
                            for(var j=0;j<temp.length-1;j++){
                                adddataentry('step'+(i+1)+'Toentrytable');
                            }
                            var currentrow=$('#step'+(i+1)+'Toentrytable tr:eq(1)');
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
                            popupdivrowcount[i]=1;

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
                                            var tempObject={field:currentdataset[k][0],sub_field:currentdataset[k][1][l][0],value:currentdataset[k][1][l][1]};
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
                //alert("Section Path is not defined Correctly");
                alertify.log("Section Path is not defined Correctly","",0);
                return false;
            }
            if($('#platform-flag').hasClass('unfilled')){
                //alert("Platform is not selected correctly");
                alertify.log("Platform is not selected correctly","",0);
                return false;
            }
            if($('#browser-flag').hasClass('unfilled')){
                //alert("Browser is not selected correctly");
                alertify.log("Browser is not selected correctly","",0);
                return false;
            }
            if($('#type-flag').hasClass('unfilled')){
                //alert("Test Type is not defined correctly");
                alertify.log("Test Type is not defined correctly","",0);
                return false;
            }
            if($('#tag_txtbox').val()!=""){
                //alert("Tag Field must be empty as you have to select from the suggestion provided");
                alertify.log("Tag Field must be empty as you have to select from the suggestion provided","",0);
                return false;
            }
            var row_count=$('#steps_table tr').length;
            for(var i=0;i<row_count;i++){
                if($('#searchbox'+(i+1)+'data').html()==""){
                    continue;
                }
                else{
                    if($('#searchbox'+(i+1)+'data').find('span:eq(0)').hasClass('unfilled')){
                        //alert("Data in the Step #"+(i+1)+" is not complete");
                        alertify.log("Data in the Step #"+(i+1)+" is not complete","",0);
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
                //alert("Atleast One step is to be set as Verfication point");
                alertify.log("Atleast One step is to be set as Verfication point","",0);
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
            var stepTypeList=[];
            for(var i=1;i<=step_num;i++){
                if($('#searchbox'+i+'name').val()==""){
                    //alert('Step Name for step Number#'+i+' can not be empty');
                    alertify.log('Step Name for step Number#'+i+' can not be empty',"",0);
                    return false;
                }
                else{
                    if($('#searchbox'+i+'info').val()==""){
                        //alert('Step Description for step Number#'+i+' can not be empty');
                        alertify.log('Step Description for step Number#'+i+' can not be empty',"",0);
                        return false;
                    }
                    if($('#searchbox'+i+'expected').val()==""){
                        //alert('Expected Result for step Number#'+i+' can not be empty');
                        alertify.log('Expected Result for step Number#'+i+' can not be empty',"",0);
                        return false;
                    }
                    if($('#searchbox'+i+'time').val()==""){
                        //alert('Estimated time for step Number#'+i+' can not be empty');
                        alertify.log('Estimated time for step Number#'+i+' can not be empty',"",0);
                        return false;
                    }
                    auto_step_create($('#searchbox'+i+'name').val().trim());
                    stepNameList.push($('#searchbox'+i+'name').val());
                    stepExpectedList.push($('#searchbox'+i+'expected').val());
                    stepDescriptionList.push($('#searchbox'+i+'info').val());
                    if($('#searchbox'+i+'verify').attr('checked')==='checked'){
                        stepVerificationList.push('yes');
                    }
                    else{
                        stepVerificationList.push('no');
                    }
                    stepTypeList.push($('#searchbox'+i+'name').closest('tr').find('td:nth-child(8)').text());
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
                                    field=field.trim();
                                    var sub_field=row.find('td:eq(1) input:eq(0)').val();
                                    sub_field=sub_field.trim();
                                    var value=row.find('td:eq(2) textarea:eq(0)').val();
                                    value=value.trim();
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
                                    field=field.trim();
                                    var sub_field=row.find('td:eq(1) input:eq(0)').val();
                                    sub_field=sub_field.trim();
                                    var value=row.find('td:eq(2) textarea:eq(0)').val();
                                    value=value.trim();
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
                        if($('#searchbox'+i+'data_table').attr('data-id')=='edit'){
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
                                        var mainField=subFieldskey[n];
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
            $.get("GetStepNameType/",
                {},
                function(data){
                    //Check for the Signal that it's okay
                    var alertFound=0;
                    var found=0;
                    for(var i=0;i<stepNameList.length;i++){
                        //make temp array
                        temp=[];
                        temp.push(stepNameList[i]);
                        temp.push(stepTypeList[i]);
                        for(var j=0;j<data['test_steps'].length;j++){
                            if(temp[0]==data['test_steps'][j][0] && temp[1]==data['test_steps'][j][1]){
                                found=1;
                                break;
                            }
                            else{
                                found=0;
                            }
                        }
                        if(!found){
                            //alert("StepName and Type Error in step #"+(i+1)+"Not selected from suggestion");
                            //alertify.log("StepName and Type Error in step #"+(i+1)+"Not selected from suggestion","",0);
                            //alertFound=1;
                            //return false;
                        }
                    }
                    if(tag.length>0){
                        var tag_alert=0;
                        var tag_found=0;
                        for(var i=0;i<tag.length;i++){
                            for(var j=0;j<data['tag_list'].length;j++){
                                if(tag[i].trim()==data['tag_list'][j][0].trim()){
                                    tag_found=1;
                                    break;
                                }
                                else{
                                    tag_found=0;
                                }
                            }
                            if(!tag_found){
                                //alert("Tag Name Not present in the Database");
                                alertify.log("Tag Name Not present in the Database","",0);
                                tag_alert=1;
                                return false;
                            }
                        }
                    }
                    var dataValidationCheck=true;
                    if(tag.length>0){
                        if(alertFound>0 || tag_alert>0){
                            dataValidationCheck=false;
                        }
                    }
                    else{
                        if(alertFound>0){
                            dataValidationCheck=false;
                        }
                    }
                    if(query == "c" && dataValidationCheck){
                        $("#submit").attr('disabled','disabled');
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
                            alertify.log("Test Case '"+data+"' successfully created!","",0);
                            desktop_notify("Test Case '"+data+"'-'"+title+"' successfully created!");
                            $("#submit").removeAttr('disabled');
                            var location='/Home/ManageTestCases/Edit/'+data;
                            window.location=location;
                        });
                    }
                    else if(query == "e" && dataValidationCheck){
                        $("#submit").attr('disabled','disabled');
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
                                alertify.log("Test Case '"+data+"' successfully edited!","",0);
                                desktop_notify("Test Case '"+data+"'-'"+title+"' successfully edited!");
                                $("#submit").removeAttr('disabled');
                                var location='/Home/ManageTestCases/Edit/'+data;
                                window.location=location;
                            });
                    }
                    else{
                        //alert("Wrong data in StepName,StepType");
                        alertify.log("Wrong data in StepName,StepType","",0);
                        return false;
                    }
                });
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
                        /*if(data.length==0){
                            $(".textbox:focus").css({
                                'border': '1px solid #FF3D00',
                                'box-shadow': '0px 0px 3px #FF3D00'
                            });
                            //alert("Test Step must be chosen from popup list! Either you have to create new steps first.");
                            alertify.log("Test Step must be chosen from popup list! Either you have to create new steps first.","",0);
                        }
                        else{
                            $(".textbox:focus").css({
                                'outline': 'none',
                                'border': '1px solid #7bc1f7',
                                'background-color': '#fff',
                                'box-shadow': '0px 0px 3px #7bc1f7'
                            });
                        }*/
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
            '<td style="cursor: pointer"><a id="searchbox'+step_num+'data" data-hint="Insert Data Set" class="data-popup notification-indicator hint--right hint--bounce hint--rounded" data-gotokey="n">' +
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
            '<td><a id="searchbox'+step_num+'step_desc" data-hint="Information about this step" class="descriptionpop notification-indicator hint--left hint--bounce hint--rounded" data-gotokey="n" style="cursor:pointer;"><span class="mail-status"></span></a></td>' +
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
function vertical_sidebar(){
    /*$("#add_step_tip").click(function(){
        if(confirm("Are you sure about leaving before saving?")){
            window.location = '/Home/ManageTestCases/CreateStep/'
        }
    });*/
    $('#add_step_tip').avgrund({
        height: 200,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'close',
        onBlurContainer: '.container',
        template: '<p>Are you sure about leaving before saving?</p>' +
            '<div style="margin-top: 10%">' +
            '<a href="/Home/ManageTestCases/CreateStep/" class="twitter" style="margin-left: 40%">Yes</a>' +
            '</div>'
    });
    /*$("#edit_step_tip").click(function(){
        if(confirm("Are you sure about leaving before saving?")){
            window.location = '/Home/ManageTestCases/CreateStep/'
        }
    });*/
    $('#edit_step_tip').avgrund({
        height: 200,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'close',
        onBlurContainer: '.container',
        template: '<p>Are you sure about leaving before saving?</p>' +
            '<div style="margin-top: 10%">' +
            '<a href="/Home/ManageTestCases/CreateStep/" class="twitter" style="margin-left: 40%">Yes</a>' +
            '</div>'
    });
    /*$("#set_tag_tip").click(function(){
        if(confirm("Are you sure about leaving before saving?")){
            window.location = '/Home/ManageTestCases/TestSet/'
        }
    });*/
    $('#set_tag_tip').avgrund({
        height: 200,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'close',
        onBlurContainer: '.container',
        template: '<p>Are you sure about leaving before saving?</p>' +
            '<div style="margin-top: 10%">' +
            '<a href="/Home/ManageTestCases/TestSet/" class="twitter" style="margin-left: 40%">Yes</a>' +
            '</div>'
    });
    /*$("#copy_edit_tip").click(function(){
        if(confirm("Are you sure about leaving before saving?")){
            window.location = '/Home/ManageTestCases/SearchEdit/'
        }
    });*/
    $('#copy_edit_tip').avgrund({
        height: 200,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'close',
        onBlurContainer: '.container',
        template: '<p>Are you sure about leaving before saving?</p>' +
            '<div style="margin-top: 10%">' +
            '<a href="/Home/ManageTestCases/SearchEdit/" class="twitter" style="margin-left: 40%">Yes</a>' +
            '</div>'
    });
    /*$("#history_tip").click(function(){
        if(confirm("Are you sure about leaving before saving?")){
            window.location = '/Home/Analysis/'
        }
    });*/
    $('#history_tip').avgrund({
        height: 200,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'close',
        onBlurContainer: '.container',
        template: '<p>Are you sure about leaving before saving?</p>' +
            '<div style="margin-top: 10%">' +
            '<a href="/Home/Analysis/" class="twitter" style="margin-left: 40%">Yes</a>' +
            '</div>'
    });
    /*$("#organize_tip").click(function(){
        if(confirm("Are you sure about leaving before saving?")){
            window.location = '/Home/ManageTestCases/CreateProductSections/'
        }
    });*/
    $('#organize_tip').avgrund({
        height: 200,
        holderClass: 'custom',
        showClose: true,
        showCloseText: 'close',
        onBlurContainer: '.container',
        template: '<p>Are you sure about leaving before saving?</p>' +
            '<div style="margin-top: 10%">' +
            '<a href="/Home/ManageTestCases/CreateProductSections/" class="twitter" style="margin-left: 40%">Yes</a>' +
            '</div>'
    });
}
function reset () {
    //$("#toggleCSS").attr("href", "alertify.default.css");
    alertify.set({
        labels : {
            ok     : "OK",
            cancel : "Cancel"
        },
        delay : 5000,
        buttonReverse : false,
        buttonFocus   : "ok"
    });
}
function desktop_notify(message){
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
        var n = new Notification("Test Case Created/Updated!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Test Case Created/Updated!",{body:message, icon:"/site_media/noti.ico"});
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
function desktop_notify(message){
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
        var n = new Notification("Test Case Created/Updated!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Test Case Created/Updated!",{body:message, icon:"/site_media/noti.ico"});
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
function AutoCompleteSearchForPrompt(){
        $("#titlebox").autocomplete({
                source:function(request,response){
                    $.ajax({
                            url:"TestCaseSearch/",
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
                var tc_id=ui.item[0].trim();
                var tc_name=ui.item[1].trim();
                if(tc_id!=""){
                        $(this).val(tc_name);
                        /*if(confirm("Are you sure about leaving before saving?")){
                             window.location = '/Home/ManageTestCases/Edit/'+tc_id
                         }
                         else{
                             window.location = '/Home/ManageTestCases/CreateNew/'+tc_id
                         }*/
                            $("#title_prompt").html(
                                    '<p style="text-align: center">You have selected ' +
                                        tc_id +'-'+ tc_name + '.' +
                                        '<br/> What do you want to do?' +
                                            '</p>' +
                                            '<div style="padding-left: 15%">' +
                                            '<a class="github" href="/Home/ManageTestCases/Edit/'+tc_id+'">Edit</a>' +
                                            '<a class="twitter" href="/Home/ManageTestCases/CreateNew/'+tc_id+'">Copy</a>' +
                                            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
                                            '</div>'

                                    );
                        $("#title_prompt").modal();
                        return false;
                    }
            }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
            return $( "<li></li>" )
                    .data( "ui-autocomplete-item", item )
                .append( "<a>" + item[0] + " - "+item[1]+"<strong> - " + item[2] + "</strong></a>" )
                .appendTo( ul );
        };
}
function auto_step_create(step){
    $.ajax({
        url:'Auto_Step_Create/',
        dataType : "json",
        data : {
            step : step
        },
        success: function( json ) {
            if(json[0]==0){
                alertify.log("New step created with title '"+step+"'","",0)
            }
        }
    });
}
/****************************End Minar's Thing****************************************************/
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
