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
var lowest_feature = 0;
var isAtLowestSection = false;
var isAtLowestFeature = false;
var popupdivrowcount=[];
var referred_test_case="";
var dependency_classes=[];
var new_test_case_text = "New test case";
var test_case_format= new RegExp(/(\S+)-(\d+)/i);
var image_list=['jpg','jpeg','gif','tiff','png','bitmap'];
$(document).ready(function() {
	$("#test_case_search_box").select2({
		placeholder: "Test Case title...",
//		minimumInputLength: 3,
		width: 460,
		quietMillis: 250,
		ajax: {
			url: "TestCaseSearch/",
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
		createSearchChoice: function(term) {
			return {id: new_test_case_text, text: new_test_case_text + ": " + term};
		},
		createSearchChoicePosition: "top",
		formatResult: formatTestCases
	})
	// Listens for changes so that we can prompt the user if they want to edit or
	// copy existing test cases
	.on("change", function(e) {
//		console.log(JSON.stringify({val: e.val, added: e.added, removed: e.removed}));
		if (e.val === new_test_case_text) {
//			console.log("New test case is being created!");
		} else {
//			console.log("Existing test case has been selected.");
			var start = $(this).select2("data")["text"].indexOf(":") + 1;
    		var length = $(this).select2("data")["text"].length;
    		
    		var tc_title = $(this).select2("data")["text"].substr(start, length - 1);
        
			var tc_id = $(this).val();
			$("#title_prompt").html(
				'<p style="text-align: center">You have selected ' +
				'<span style="font-weight: bold;">' + tc_id +': '+ tc_title + '</span>' +
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
	});
	
	// Should be used for formatting results, LATER
	function formatTestCases(tc_details) {
		var start = tc_details.text.indexOf(":") + 1;
		var length = tc_details.text.length;
		
		var tc_title = tc_details.text.substr(start, length - 1);
		
		var markup =
			'<div>' +
			'<i class="fa fa-file-text fa-fw"></i> <span style="font-weight: bold;">' + tc_details.id + '</span>' +
			': ' +
			'<span>' + tc_title + '</span>'
			'</div>';
		
		return markup;
	}
//	
//	function formatTestCasesSelection(tc_details) {
//		return tc_id + ": " + tc_name + " - " + tc_type
//	}
	
    //show_labels();
    addMainTableRow('#steps_table');
    //check_required_data();
    //show_radio_button();
    vertical_sidebar();
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_default_settings(project_id,team_id);
    AutoCompleteSearchForPrompt();
    /*****************Shetu's Function************************/
    AutoCompleteLabel();
    //$(".combo-box").combobox();
    /*****************End Shetu************************/

    URL = window.location.pathname
//    console.log("url:"+URL);
    indx = URL.indexOf("CreateNew");
//    console.log("Create Index:"+indx);
    indx2 = URL.indexOf("Edit");
//    console.log("Edit Index:"+indx2);
    var template = URL.length > (URL.lastIndexOf("CreateNew/")+("CreateNew/").length) && URL.indexOf("CreateNew") != -1;
    if(indx!=-1 && template){
        referred_test_case=URL.substring((URL.lastIndexOf("CreateNew/")+("CreateNew/").length),(URL.length-1));
        $("#header").html($.session.get('project_id')+' / Create Test Case');
    }
    if(indx2!=-1){
        referred_test_case=URL.substring((URL.lastIndexOf("Edit/")+("Edit/").length),(URL.length-1));
        $("#header").html($.session.get('project_id')+' / Edit Test Case / '+referred_test_case);
    }
//    console.log("Url Length:"+URL.length);
//    console.log("Template:"+template);
    if (indx != -1 || indx2 != -1) {
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
        GetBrowserSections();
        DeleteSearchQueryText();
        if(indx2 != -1 || template){
            $.get("TestCase_EditData",
                {
                    //TC_Id : URL.substring(URL.lastIndexOf("/")+1,URL.length)
                    TC_Id:referred_test_case
                },
                function(data){
//                    console.log(data);
                    /******************Properties tab Data*******************************/
                    //Status
                    if (typeof(data)!='string'){
                        $("#status").val(data['Status']);
                        /*console.log(status);
                        if(status=="Ready"){
                            $('a[value="Production"]').addClass('selected');
                        }
                        if(status=="Dev"){
                            $('a[value="Development"]').addClass('selected');
                        }
                        if(status=="Forced"){
                            $('a[value="Forced-Manual"]').addClass('selected');
                        }*/
                        //LabelsList
                        var label_list=data['Labels'];
                        if(label_list.length!=0){
                            for(var i=0;i<label_list.length;i++){
                                if(label_list[i]!=""){
                                    AddToListLabel(label_list[i][0],label_list[i][1],label_list[i][2]);
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
                                    section : dataId.replace(/^\.+|\.+$/g, "").replace(/ /g,'_'),
                                    project_id: $.session.get('project_id'),
                                    team_id: $.session.get('default_team_identity')
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
                        
                        //FeaturePath
                        
                        /*var feature_id=data['Feature_Id'];
                        var features = '';
                        var feature_id = data['Feature_Id'];
                        
                        $.get("Get_Feature_Path/",{Feature_Id : feature_id},function(data)
                        {
                            var features = data['Path'];
                        });*/

                        var features = data['Feature_Path'];
                        var featureArray = features.split('.');
                        var dataId ="";
                        var handlerString = "";
                        for(var index in featureArray){
                            if(featureArray[index] == "")
                                continue;
                            $.ajax({
                                url:'GetFeatures/',
                                dataType : "json",
                                data : {
                                    feature : dataId.replace(/^\.+|\.+$/g, "").replace(/ /g,'_'),
                                    project_id: $.session.get('project_id'),
                                    team_id: $.session.get('default_team_identity')
                                },
                                success: function( json ) {
                                    if(json.length != 1){
                                        var realItemIndex = parseInt(json[0][0])
                                        var handlerString = ""
                                        for(var i = 0; i < realItemIndex; i++)
                                            handlerString+=featureArray[i]+'.'

                                        if(realItemIndex == 0){
                                            $(".feature[data-level='']").find('option').each(function(){$(this).remove();});
                                            $(".feature[data-level='']").append("<option>Choose...</option>");

                                            for(var i = 0; i < json.length; i++)
                                                json[i] = json[i][0].replace(/_/g,' ')
                                            $.each(json, function(i, value) {
                                                if(i == 0)return;
                                                $(".feature[data-level='']").append($('<option>').text(value).attr('value', value));
                                            });
                                            $(".feature[data-level='']").val(featureArray[realItemIndex].replace(/_/g,' '))
                                        }else{
                                            var tag = jQuery('<select/>',{
                                                'class':'feature',
                                                'data-level':handlerString,
                                                'id':realItemIndex+1,
                                                change: function(){
                                                    isAtLowestFeature = false;
                                                    recursivelyAddFeature(this);
                                                    $("#feature-flag").removeClass("filled");
                                                    $("#feature-flag").addClass("unfilled");
                                                }
                                            })
                                            if($('#featuregroup select[id='+realItemIndex+']').length != 0)
                                                $('#featuregroup select[id='+realItemIndex+']').after(tag)
                                            else
                                                $('#featuregroup select[id=1]').after(tag);

                                            $(".feature[data-level='"+handlerString+"']").append("<option>Choose...</option>");

                                            var once = true;
                                            for(var i = 0; i < json.length; i++)
                                                json[i] = json[i][0].replace(/_/g,' ')
                                            $.each(json, function(i, value) {
                                                if(i == 0)return;
                                                if(once){
                                                    lowest_feature+=1
                                                    once = false
                                                }
                                                $(".feature[data-level='"+handlerString+"']").append($('<option>').text(value).attr('value', value));
                                            });
                                            $(".feature[data-level='"+handlerString+"']").val(featureArray[realItemIndex].replace(/_/g,' '))
                                        }
                                        isAtLowestFeature = true;
                                        $("#feature-flag").removeClass("unfilled");
                                        $("#feature-flag").addClass("filled");


                                        /*var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

                                        $.get("Check_Feature_Path",{Feature_Path : newFeaturePath},function(data)
                                            {
                                                if (data.length > 1) {
                                                    $("#feature-flag").removeClass("filled");
                                                    $("#feature-flag").addClass("unfilled");
                                                    isAtLowestFeature = false;
                                                };
                    
                                            });*/
                                    }
                                }
                            });

                            dataId += featureArray[index] + '.'
                        }
                        //Priority
                        var priority=data['Priority'];
                        $("#priotiy_select").val(parseInt(priority.substring(1,2)));
                        /*************** End Properties tab Data*******************************/
                        /****************************Parameters Tab*****************************/
                        var dependency=data['Dependency List'];
                        for(var i=0;i<dependency.length;i++){
                            var name=dependency[i][0];
                            //console.log($('.'+name+" :checked").length);
                            $('.'+name).attr('checked',false);
                            //console.log($('.'+name+" :checked").length);
                            var listings=dependency[i][1];
                            for(var j=0;j<listings.length;j++){
                                $('.'+name+':checkbox[value="'+listings[j]+'"]').attr('checked',true);
                            }
                            //console.log($('.'+name+" :checked").length);
                            if($('.'+name).is(':checked')==false){
                                $('#'+name+"-flag").removeClass('filled');
                                $('#'+name+"-flag").addClass('unfilled');
                            }
                            else{
                                $('#'+name+"-flag").removeClass('unfilled');
                                $('#'+name+"-flag").addClass('filled');
                            }

                        }
                        /****************************End Parameters Tab*****************************/
                        /****************************RelatedItems Tab*******************************/
                        var req_id = data['Requirement Ids'];
                        var assoc_bugs = data['Associated Bugs'];
                        var tc_id = data['Manual_TC_Id'];
                        var get_project_id=data['project_id'];
                        var get_team_id=data['team_id'];
                        //AssociatedBug
                        $('#defectid_txtbox').val(assoc_bugs);
                        //Manual Test Case Id
                        $('#id_txtbox').val(tc_id);
                        $('#file_upload_tc').val(data['TC_Id']);
                        //Requirement Id
                        $('#reqid_txtbox').val(req_id);
                        $('#project_identity').val(get_project_id);
                        $('#default_team_identity').val(get_team_id);
                        if(data['attachement'].length>0){
                            var message='';
                            message+='<table class="two-column-emphasis">';
                            for(var i=0;i<data['attachement'].length;i++){
                                if(image_list.indexOf(data['attachement'][i][2])!=-1){
                                    message+='<tr><td>'+data['attachement'][i][0]+'.'+data['attachement'][i][2]+'<img src="'+data['attachement'][i][1]+'"/></td></tr>';
                                }
                                else{
                                    message+='<tr><td><a target="_blank" href="'+data['attachement'][i][1]+'">'+data['attachement'][i][0]+'.'+data['attachement'][i][2]+'</a> </td></tr>';
                                }
                                //message+='<tr><td><iframe src="'+data['attachement'][i][1]+'">'+data['attachement'][i][0]+'.'+data['attachement'][i][2]+'</iframe></td></tr>'
                            }
                            message+='</table>';
                            $('#attachement_div').empty();
                            $('#attachement_div').html(message);
                        }
                        if(!template){
                            var auto_id=data['TC_Id'];
                            var title=data['TC_Name'];
                            //$('#TC_Id').html("<b>Automation ID: "+auto_id +"</b>")
                            $('#TC_Id').css('display','block');
//                            console.log("Title: " + title);
//                            $('#titlebox').val(title);
                            $("#test_case_search_box").select2("data", {"id": auto_id, "text": auto_id + ": " + title});
                        }
                        /************************End RelatedItems Tab*******************************
                        $('input[name="labels"]').each(function(){
                            $(this).prop('checked',false);
                        });
                        $('input[name="labels"]').each(function(){
                            if(data['Labels'].indexOf($(this).val())>-1){
                                $(this).prop('checked',true);
                            }
                        });

                        /***************************Steps Tab***************************************/
                        var steps_and_data = data['Steps and Data'];
                        //$('#steps_table').html("");
                        for(var i=0;i<(steps_and_data.length-1);i++){
                            addMainTableRow('#steps_table');
                        }
                        var row_count=$('#steps_table tr').length;
                        var converted_data=[];
//                        console.log(row_count);
                        popupdivrowcount=[];
                        for(var i=0;i<row_count;i++){
                            $('#searchbox'+(i+1)+'name').val(steps_and_data[i][0]);
                            $('#searchbox'+(i+1)+'info').val(steps_and_data[i][3]);
                            $('#searchbox'+(i+1)+'expected').val(steps_and_data[i][4]);
                            $('#searchbox'+(i+1)+'step_type').text(steps_and_data[i][2]);
                            if(steps_and_data[i][5]=='yes'){
                                $('#searchbox'+(i+1)+'verify').toggles({on:true});
                                //$('#searchbox'+(i+1)+'verify .toggle-on').addClass('active');
                                //$('#searchbox'+(i+1)+'verify .toggle-off').removeClass('active');
                            }
                            if(steps_and_data[i][10]=='yes'){
                                $('#searchbox'+(i+1)+'continue').toggles({on:true});
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
//                                console.log(fromdata);
//                                console.log(todata);
                                var divname='#searchbox'+(i+1)+'data_table';
                                $(divname).attr('data-id','edit');
                                editTypeRow(divname,i+1,1,"From");
                                editTypeRow(divname,i+1,1,"To");
                                var temp=[];
                                for(var j=0;j<fromdata.length;j++){
                                    if(fromdata[j][1] instanceof  Array){
                                        for(var k=0;k<fromdata[j][1].length;k++){
                                            var tempObject={field:fromdata[j][0],sub_field:fromdata[j][1][k][0],value:fromdata[j][1][k][1],keyfield:fromdata[j][1][k][2],ignorefield:fromdata[j][1][k][3]};
                                            temp.push(tempObject);
                                        }
                                    }
                                    else{
                                        var tempobject={field:fromdata[j][0],sub_field:"",value:fromdata[j][1],keyfield:fromdata[j][2],ignorefield:fromdata[j][3]};
                                        temp.push(tempobject);
                                    }
                                }
//                                console.log(temp);
                                for(var j=0;j<temp.length-1;j++){
                                    adddataentry('step'+(i+1)+'Fromentrytable');
                                }
                                var currentrow=$('#step'+(i+1)+'Fromentrytable tr:eq(1)');
                                for(var k=0;k<temp.length;k++){
                                    if(temp[k].keyfield){
                                        currentrow.find('td:eq(0)').find('input:eq(0)').attr('checked','checked');
                                    }
                                    currentrow.find('td:eq(1)').find('input:eq(0)').val(temp[k].field);
                                    currentrow.find('td:eq(2)').find('input:eq(0)').val(temp[k].sub_field);
                                    currentrow.find('td:eq(3)').find('textarea:eq(0)').val(temp[k].value);
                                    if(temp[k].ignorefield){
                                        currentrow.find('td:eq(4)').find('input:eq(0)').attr('checked','checked');
                                    }
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
                                            var tempObject={field:todata[j][0],sub_field:todata[j][1][k][0],value:todata[j][1][k][1],keyfield:todata[j][1][k][2],ignorefield:todata[j][1][k][3]};
                                            temp.push(tempObject);
                                        }
                                    }
                                    else{
                                        var tempobject={field:todata[j][0],sub_field:"",value:todata[j][1],keyfield:todata[j][2],ignorefield:todata[j][3]};
                                        temp.push(tempobject);
                                    }
                                }
//                                console.log(temp);
                                for(var j=0;j<temp.length-1;j++){
                                    adddataentry('step'+(i+1)+'Toentrytable');
                                }
                                var currentrow=$('#step'+(i+1)+'Toentrytable tr:eq(1)');
                                for(var k=0;k<temp.length;k++){
                                    if(temp[k].keyfield){
                                        currentrow.find('td:eq(0)').find('input:eq(0)').attr('checked','checked');
                                    }
                                    currentrow.find('td:eq(1)').find('input:eq(0)').val(temp[k].field);
                                    currentrow.find('td:eq(2)').find('input:eq(0)').val(temp[k].sub_field);
                                    currentrow.find('td:eq(3)').find('textarea:eq(0)').val(temp[k].value);
                                    if(temp[k].ignorefield){
                                        currentrow.find('td:eq(4)').find('input:eq(0)').attr('checked','checked');
                                    }
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
                                                var tempObject={field:currentdataset[k][0],sub_field:currentdataset[k][1][l][0],value:currentdataset[k][1][l][1],keyfield:currentdataset[k][1][l][2],ignorefield:currentdataset[k][1][l][3]};
                                                temp.push(tempObject);
                                            }
                                        }
                                        else{
                                            var tempobject={field:currentdataset[k][0],sub_field:"",value:currentdataset[k][1], keyfield:currentdataset[k][2],ignorefield:currentdataset[k][3]};
                                            temp.push(tempobject);
                                        }
                                    }
                                    for(var k=0;k<(temp.length-1);k++){
                                        adddataentry('step'+(i+1)+'data'+(j+1)+'entrytable');
                                    }
                                    var currentrow=$('#step'+(i+1)+'data'+(j+1)+'entrytable tr:eq(1)');
                                    for(var k=0;k<temp.length;k++){
                                        if(temp[k].keyfield){
                                            currentrow.find('td:eq(0)').find('input:eq(0)').attr('checked','checked');
                                        }
                                        currentrow.find('td:eq(1)').find('input:eq(0)').val(temp[k].field);
                                        currentrow.find('td:eq(2)').find('input:eq(0)').val(temp[k].sub_field);
                                        currentrow.find('td:eq(3)').find('textarea:eq(0)').val(temp[k].value);
                                        if(temp[k].ignorefield){
                                            currentrow.find('td:eq(4)').find('input:eq(0)').attr('checked','checked');
                                        }
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

                    }
                    /***************************End Steps Tab***************************************/
                });
            $('#show_format').on('click',function(){
                if(test_case_format.test(referred_test_case)){
                    $.get('TestCaseDataFromMainDriver/',{
                        'test_case_id':referred_test_case
                    },function(data){
                        //alert(data);
                        var message=form_table(data);
                        $('#data_table_show').html(message);
                    });
                }
                else{
                    alert('Test Case Format Error');
                    return false;
                }
            });
        }

        $('#submit').live('click',function(e){
            /*****************************Validation Check Here***********************************/

            if ($("#test_case_search_box").select2("val") === "" || $("#test_case_search_box").select2("val") === []) {
                e.preventDefault();

                alertify.error("Please provide the <span style='font-weight: bold;'>Test Case title</span>", 2500);

                $("#test_case_search_box").select2("open");

//                setTimeout(function() {
//                    $("#titlebox").css({
//                        "border-color": "",
//                        "box-shadow": ""
//                    });
//                }, 1500);

                return false;
            }

            if($('#section-flag').hasClass('unfilled')){
                //alert("Section Path is not defined Correctly");
                alertify.error("Section Path is not defined Correctly","",0);
                return false;
            }
            if($('#feature-flag').hasClass('unfilled')){
                //alert("Feature Path is not defined Correctly");
                alertify.error("Feature Path is not defined Correctly","",0);
                return false;
            }
            for(var i=0;i<dependency_classes.length;i++){
                if($('#'+dependency_classes[i].name+'-flag').hasClass('unfilled')){
                    //alert("Platform is not selected correctly");
                    alertify.error(dependency_classes[i].name.trim()+" is not selected correctly","",0);
                    return false;
                }
            }
            if($('#project_identity option:selected').val()==""){
                alertify.error("Please select a project topbar",1500);
                return false;
            }
            if($('#default_team_identity option:selected').val()==""){
                alertify.error("Please select a team from topbar",1500);
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
                        alertify.error("Data in the Step #"+(i+1)+" is incomplete","",0);
                        return false;
                    }
                }
            }
            var checked_count=0;
            for(var i=0;i<row_count;i++){
                if($('#searchbox'+(i+1)+'verify').data('toggles').active===true){
                    checked_count++;
                }
            }
            if(checked_count<=0){
                alertify.error("Atleast One step is to be set as Verfication point","",0);
                return false;
            }
            /******************************END Validation Check here*******************************/
            /*********************************Properties Tab Data ********************************/
            //Select Status
            var status = $("#status").val();
            /*if($('a[value="Production"]').hasClass('selected'))
                status = "Ready";
            if($('a[value="Development"]').hasClass('selected'))
                status = "Dev";
            if($('a[value="Forced-Manual"]').hasClass('selected'))
                status = "Forced";
            console.log(status);*/
            //Select Section Name
            var newSectionPath = $("#sectiongroup select.section:last-child").attr("data-level").replace(/ /g,'_') + $("#sectiongroup select.section:last-child option:selected").val().replace(/ /g,'_');
            var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

            /*$.get("Check_Feature_Path",{Feature_Path : newFeaturePath},function(data)
                {
                    if (data.length != 1) {
                        $("#feature-flag").removeClass("filled");
                        $("#feature-flag").addClass("unfilled");
                    };
                });*/

//            console.log(newSectionPath);
//            console.log(newFeaturePath);
            //Get TC_ID for the test case
            //Select Priority
            var priority='P'+$('#priotiy_select option:selected').val();
//            console.log(priority);
            //Select Tag
            var tag = new Array();
            for(var i = 0; i < $(".submitquery").length; i++){
                tag.push($(".submitquery:eq("+i+")").html().replace(/&nbsp;/g,''));
            }
//            console.log(tag);
            /*********************************End Properties Tab Data ********************************/
            /*********************************Parameters Tab Data ********************************/
            /*var platformList=[];
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
            console.log(typeList);*/
            var dependency_list=[];
            for(var i=0;i<dependency_classes.length;i++){
                var temp_list=[];
                $('.'+dependency_classes[i].name+':checked').each(function(){
                   temp_list.push($(this).val());
                });
                var temp=(dependency_classes[i].name+':'+temp_list.join(",")).toString();
                dependency_list.push(temp);
            }
//            console.log(dependency_list);
            /*********************************End Parameters Tab Data ********************************/
            /**************************Related Item *************************************************/
            var defectId=$('#defectid_txtbox').val().trim();
            var test_case_Id=$('#id_txtbox').val().trim();
            var required_Id=$('#reqid_txtbox').val().trim();
    		
            var start = $("#test_case_search_box").select2("data")["text"].indexOf(":") + 1;
    		var length = $("#test_case_search_box").select2("data")["text"].length;
    		
    		var title = $("#test_case_search_box").select2("data")["text"].substr(start, length - 1);
            
            //var project_id=$('#project_identity option:selected').val().trim();
            //var team_id=$('#default_team_identity option:selected').val().trim();
            var project_id = $.session.get('project_id');
            var team_id = $.session.get('default_team_identity');
            /**************************End Related Item *************************************************/
            /***************************DataFetching From the Pop UP*********************************************/
            var stepNameList=[];
            var stepExpectedList=[];
            var stepDescriptionList=[];
            var stepVerificationList=[];
            var stepContinueList=[]
            var stepTimeList=[];
            var finalArray=[];
            var stepTypeList=[];
            for(var i=1;i<=step_num;i++){
                if($('#searchbox'+i+'name').val()==""){
                    //alert('Step Name for step Number#'+i+' can not be empty');
                    alertify.error('Step Name for step Number#'+i+' can not be empty',"",0);
                    return false;
                }
                else{
                    if($('#searchbox'+i+'info').val()==""){
                        //alert('Step Description for step Number#'+i+' can not be empty');
                        alertify.error('Step Description for step Number#'+i+' can not be empty',"",0);
                        return false;
                    }
                    if($('#searchbox'+i+'expected').val()==""){
                        //alert('Expected Result for step Number#'+i+' can not be empty');
                        alertify.error('Expected Result for step Number#'+i+' can not be empty',"",0);
                        return false;
                    }
                    if($('#searchbox'+i+'time').val()==""){
                        //alert('Estimated time for step Number#'+i+' can not be empty');
                        alertify.error('Estimated time for step Number#'+i+' can not be empty',"",0);
                        return false;
                    }
                    auto_step_create($('#searchbox'+i+'name').val().trim());
                    stepNameList.push($('#searchbox'+i+'name').val());
                    stepExpectedList.push($('#searchbox'+i+'expected').val());
                    stepDescriptionList.push($('#searchbox'+i+'info').val());
                    if($('#searchbox'+i+'verify').data('toggles').active){
                        stepVerificationList.push('yes');
                    }
                    else{
                        stepVerificationList.push('no');
                    }
                    if($('#searchbox'+i+'continue').data('toggles').active){
                        stepContinueList.push('yes');
                    }
                    else{
                        stepContinueList.push('no');
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
                                    if(row.find('td:eq(0) input:eq(0)').is(':checked')){
                                        var keyfield=true;
                                    }
                                    else{
                                        var keyfield=false;
                                    }
                                    var field=row.find('td:eq(1) input:eq(0)').val();
                                    field=field.trim();
                                    var sub_field=row.find('td:eq(2) input:eq(0)').val();
                                    sub_field=sub_field.trim();
                                    var value=row.find('td:eq(3) textarea:eq(0)').val();
                                    value=value.trim();
                                    if(row.find('td:eq(4) input:eq(0)').is(':checked')){
                                        var ignorefield=true;
                                    }
                                    else{
                                        var ignorefield=false;
                                    }
                                    var tempObject={field:field , sub_field:sub_field ,value:value,keyfield:keyfield,ignorefield:ignorefield};
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
//                                console.log(tableid.attr('id'));
                                var tableLength=tableid.find('tr').length;
                                var row=tableid.find('tr:eq(1)');
                                for(var k=0;k<tableLength-1;k++){
                                    if(row.find('td:eq(0) input:eq(0)').is(':checked')){
                                        var keyfield=true;
                                    }
                                    else{
                                        var keyfield=false;
                                    }
                                    var field=row.find('td:eq(1) input:eq(0)').val();
                                    field=field.trim();
                                    var sub_field=row.find('td:eq(2) input:eq(0)').val();
                                    sub_field=sub_field.trim();
                                    var value=row.find('td:eq(3) textarea:eq(0)').val();
                                    value=value.trim();
                                    if(row.find('td:eq(4) input:eq(0)').is(':checked')){
                                        var ignorefield=true;
                                    }
                                    else{
                                        var ignorefield=false;
                                    }
                                    var tempObject={field:field , sub_field:sub_field ,value:value,keyfield:keyfield,ignorefield:ignorefield};
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
            /*****************************************verifying the keyfield and ignore***************************/
            return_type=keyfield_ignorefield(finalArray);
            if(!return_type.status){
                alertify.error("Please give correct key field in all datasets in  Step #"+(return_type.index+1),"",0);
                return false;
            }
            /*****************************************verifying the keyfield and ignore***************************/
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
                                        var temp_object={mainField:temp.field,fieldValue:temp.value,keyfield:temp.keyfield,ignorefield:temp.ignorefield};
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
                                    temp+=("("+mainFields[m].mainField+","+mainFields[m].fieldValue+","+mainFields[m].keyfield+","+mainFields[m].ignorefield+"),");
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
                                                temp+=("("+withsubFields[o].sub_field+","+withsubFields[o].value+","+withsubFields[o].keyfield+","+withsubFields[o].ignorefield+"),");
                                            }
                                        }
                                        temp=temp.substring(0,temp.length-1);
                                        temp+="]),";
                                    }
                                    temp=temp.substring(0,temp.length-1);
                                    temp+="]";
                                }
//                                console.log(temp);
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
                                    var temp_object={mainField:currentDataSet[k].field,fieldValue:currentDataSet[k].value,keyfield:currentDataSet[k].keyfield,ignorefield:currentDataSet[k].ignorefield};
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
                                temp+=("("+mainFields[k].mainField+","+mainFields[k].fieldValue+","+mainFields[k].keyfield+","+mainFields[k].ignorefield+"),");
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
                                            temp+=("("+withsubFields[l].sub_field+","+withsubFields[l].value+","+withsubFields[l].keyfield+","+withsubFields[l].ignorefield+"),");
                                        }
                                    }
                                    temp=temp.substring(0,temp.length-1);
                                    temp+="]),";
                                }
                                temp=temp.substring(0,temp.length-1);
                                temp+="]";
                            }
//                            console.log(temp);
                            tempSTR.push(temp);
                            /*************************** end create old format Data*********************************/

                        }
                        /*********************** END Step Data Processing Here ********************************/
                        stepDataSTR[i-1]=tempSTR.join('%');
                    }
//                    console.log(stepDataSTR);
                }
            }
            /*************************End Filtering***********************************************/
            /************************End DataFetching From the POP Up*********************************************/
            var labels=[];
            $('input[name="labels"]:checked').each(function(){
                labels.push($(this).val());
            });
            /***********************Other Linking***************************************/
            var query = indx != -1?"c":(indx2 != -1?"e":"o");
//            console.log(query);
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
                                alertify.error("Tag Name Not present in the Database","",0);
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
                    
                    var start = $("#test_case_search_box").select2("data")["text"].indexOf(":") + 1;
            		var length = $("#test_case_search_box").select2("data")["text"].length;
            		
            		var tc_title = $("#test_case_search_box").select2("data")["text"].substr(start, length - 1);
                    
                    var tc_id = $("#test_case_search_box").val();
                    
                    if(query == "c" && dataValidationCheck){
                        $("#submit").attr('disabled','disabled');
                        $.get("Submit_New_TestCase/",{
                            Section_Path:newSectionPath,
                            Feature_Path:newFeaturePath,
                            //Platform:platformList.join("|"),
                            //Manual_TC_Id:test_case_Id,
                            TC_Name:tc_title,
                            TC_Creator:$.session.get('fullname').trim(),
                            Associated_Bugs_List:defectId,
                            Requirement_ID_List:required_Id,
                            //TC_Type:typeList.join("|"),
                            Tag_List:tag.join("|"),
                            //Dependency_List:browserList.join("|"),
                            Dependency_List:dependency_list.join("|"),
                            Priority:priority,
                            Steps_Data_List:stepDataSTR.join("|"),
                            Steps_Name_List:stepNameList.join("|"),
                            Steps_Description_List:stepDescriptionList.join("|"),
                            Steps_Expected_List:stepExpectedList.join("|"),
                            Steps_Verify_List:stepVerificationList.join("|"),
                            Steps_continue_List:stepContinueList.join("|"),
                            Steps_Time_List:stepTimeList.join("|"),
                            Status:"Dev",
                            Project_Id:project_id,
                            Team_Id: team_id,
                            labels:labels.join("|")
                        },function(data) {
                            //alert(data);
                            alertify.success("Test Case '"+data+"' successfully created!","",0);
                            desktop_notify("Test Case '"+data+"'-'"+title+"' successfully created!");
                            $("#submit").removeAttr('disabled');
                            var location='/Home/ManageTestCases/Edit/'+data;
                            window.location=location;
                        });
                    }
                    else if(query == "e" && dataValidationCheck){
//                        var _TC_Id = $('#header').text().split('/')[2].trim();

                        $("#submit").attr('disabled','disabled');
                        $.get("Edit_TestCase",{
                                Section_Path:newSectionPath,
                                Feature_Path:newFeaturePath,
                                TC_Id:tc_id,
                                //Platform:platformList.join("|"),
                                //Manual_TC_Id:test_case_Id,
                                TC_Name:tc_title,
                                TC_Creator:$.session.get('fullname').trim(),
                                Associated_Bugs_List:defectId,
                                Requirement_ID_List:required_Id,
                                Status:status,
                                //TC_Type:typeList.join("|"),
                                Tag_List:tag.join("|"),
                                //Dependency_List:browserList.join("|"),
                                Dependency_List:dependency_list.join("|"),
                                Priority:priority,
                                Steps_Data_List:stepDataSTR.join("|"),
                                Steps_Name_List:stepNameList.join("|"),
                                Steps_Description_List:stepDescriptionList.join("|"),
                                Steps_Expected_List:stepExpectedList.join("|"),
                                Steps_Verify_List:stepVerificationList.join("|"),
                                Steps_continue_List:stepContinueList.join("|"),
                                Steps_Time_List:stepTimeList.join("|"),
                                Project_Id:project_id,
                                Team_Id: team_id,
                                labels:labels.join("|")
                            },
                            function(data) {
                                //alert(data+" edited successfully");
                                alertify.success("Test Case '"+data+"' successfully updated!","",0);
                                desktop_notify("Test Case '"+data+"' successfully updated!");
                                $("#submit").removeAttr('disabled');
                                var location='/Home/ManageTestCases/Edit/'+data;
                                window.location=location;
                            });
                    }
                    else{
                        //alert("Wrong data in StepName,StepType");
                        alertify.error("Wrong data in StepName,StepType","",0);
                        return false;
                    }
                });
        });
    }
});
function form_table(data_list){
    var dependency=data_list['dependency'];
    data_list=data_list['data'];
    var message="";
    message+='<table width="100%" class="two-column-emphasis"><caption><b style="font-size: 125%">Data List</b></caption>';
    message+='<tr><td><b>Step Name</b></td><td><b>Step Type</b></td><td><b>Step Data</b></td></tr>'
    for(var i=0;i<data_list.length;i++){
        message+='<tr>';
        message+='<td>'+data_list[i][0]+'</td>';
        message+='<td>'+data_list[i][1]+'</td>';
        message+='<td>';
        var step_data=data_list[i][2];
        if(step_data.length==0){
            message+='[ ]';
        }
        if(step_data.length>0){
            message+='[ ';
            for(var j=0;j<step_data.length;j++){
                message+='[ ';
                for(var k=0;k<step_data[j].length;k++){
                    message+='( ';
                    for(var l=0;l<step_data[j][k].length;l++){
                        if(step_data[j][k][l]!='' && typeof(step_data[j][k][l])==='string'){
                            message+="'"+step_data[j][k][l]+"'";
                        }
                        else if(!step_data[j][k][l] && step_data[j][k][l].toString()==='false'){
                            message+=capitalize(step_data[j][k][l].toString());
                        }
                        else if(step_data[j][k][l] && step_data[j][k][l].toString()==='true'){
                            message+=capitalize(step_data[j][k][l].toString());
                        }
                        else{
                            message+="''";
                        }
                        if(l<(step_data[j][k].length-1)){
                            message+=' , ';
                        }
                    }
                    message+=' )';
                    if(k<(step_data[j].length-1)){
                        message+=' , ';
                    }
                }
                message+=' ] ';
                if(j<(step_data.length-1)){
                    message+=' , ';
                }
            }
            message+=']';
        }
        message+='</td>';
        message+='</tr>';
    }
    message+='</table>';
    message+='<table width="100%" class="two-column-emphasis"><caption><b style="font-size: 125%">Dependency List</b></caption>';
    message+='<tr><td><b>Type</b></td><td><b>Name</b></td></tr>';
    for(var i=0;i<dependency.length;i++){
        message+='<tr>';
        message+='<td>'+dependency[i][0]+'</td>';
        message+='<td>';
        for(var j=0;j<dependency[i][1].length;j++){
            message+=dependency[i][1][j];
            if(j<(dependency[i][1].length-1)){
                message+=' , ';
            }
        }
        message+='</td>';
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function capitalize(stringarray){
    return stringarray.charAt(0).toUpperCase()+stringarray.slice(1);
}
function keyfield_ignorefield(finalArray){
    var status=true;
    for(var i=0;i<finalArray.length;i++){
        var current_data=finalArray[i];
        if(current_data===undefined){
            //this means data not required in this step
            continue;
        }
        else{
            if(current_data.length>1){

                //means keyfield and ignorefield will be checked
                //take out the first dataset key field
                if(current_data)
                var reference_data=current_data[0];
                var key_field=[];
                for(var j=0;j<reference_data.length;j++){
                    if(reference_data[j].keyfield && !reference_data[j].ignorefield){
                        if(key_field.indexOf(reference_data[j].field)==-1){
                            key_field.push(reference_data[j].field);
                        }
                    }
                }
                for(var j=1;j<current_data.length;j++){
                    var temp=[];
                    for( var k=0;k<current_data[j].length;k++){
                        if(current_data[j][k].keyfield && !current_data[j][k].ignorefield){
                            if(temp.indexOf(current_data[j][k].field)==-1){
                                temp.push(current_data[j][k].field);
                            }
                        }
                    }
                    if(key_field.length!=temp.length){
                        status=false;
                    }
                    else{
                        for(var k=0;k<temp.length;k++){
                            if(key_field.indexOf(temp[k])==-1){
                                status=false;
                                break;
                            }
                        }
                        if(!status){
                            break;
                        }
                        for(var k=0;k<key_field.length;k++){
                            if(temp.indexOf(key_field[k])==-1){
                                status=false;
                                break;
                            }
                        }
                        if(!status){
                            break;
                        }
                    }
                }
                if (!status){
                    break;
                }
            }
            else{
                //means only one dataset in this set. so no worry
                if(current_data[0] instanceof  Array && current_data[0].length==2){
                    var from=current_data[0][0];
                    var to=current_data[0][1];
                    //find the keyfield
                    var key_field=[];
                    for(var j=0;j<from.length;j++){
                        if(from[j].keyfield && !from[j].ignorefield){
                            if(key_field.indexOf(from[j].field)==-1){
                                key_field.push(from[j].field);
                            }
                        }
                    }
                    var to_key_field=[];
                    for(var j=0;j<to.length;j++){
                        if(to[j].keyfield && !to[j].ignorefield){
                            if(to_key_field.indexOf(to[j].field)==-1){
                                to_key_field.push(to[j].field);
                            }
                        }
                    }
                    if(key_field.length!=to_key_field.length){
                        status=false;
                    }
                    else{
                        for(var k=0;k<to_key_field.length;k++){
                            if(key_field.indexOf(to_key_field[k])==-1){
                                status=false;
                                break;
                            }
                        }
                        for(var k=0;k<key_field.length;k++){
                            if(to_key_field.indexOf(key_field[k])==-1){
                                status=false;
                                break;
                            }
                        }
                    }
                }
                else{
                    continue;
                }

            }
        }
        if (!status){
            break;
        }
    }
    var temp={'status':status,'index':i}
    return temp;
}
function get_default_settings(project_id,team_id){
    $.get('get_default_settings/',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        populate_parameter_div(data['result'],"parameter_div");
    });
}
function populate_parameter_div(array_list,div_name){
    var message="";
    for(var i=0;i<array_list.length;i++){
        var dependency=array_list[i][0];
        var name_list=array_list[i][1].split(",");
        message+='<form id="tc_'+dependency+'" class="new_tc_form">';
        message+='<table>';
        message+='<tr>';
        message+='<td class="tc_form_label_col">'
        message+='<b class="Text">'+dependency+':</b>';
        message+='</td>';
        message+='<td class="tc_form_input_col">';
        message+='<table width="100%">';
        var equal_size=(100/name_list.length);
        var dep_name=[];
        message+='<tr>';
        for(var j=0;j<name_list.length;j++){
            message+='<td width="'+equal_size+'%">';
            message+='<input class="'+dependency+'" id="'+dependency+'_'+name_list[j]+'" type="checkbox" name="type" value="'+name_list[j]+'" style="width:auto" />';
            message+='<label for="'+dependency+'_'+name_list[j]+'">'+name_list[j]+'</label>';
            message+='</td>';
            dep_name.push(dependency+'_'+name_list[j]);
        }
        message+='</tr>';
        message+='</table>';
        message+='</td>';
        message+='<td><a class="notification-indicator tooltipped downwards" data-gotokey="n"><span id="'+dependency.trim()+'-flag" class="mail-status unfilled"></span></a></td>';
        message+='<tr>';
        message+='</table>';
        message+='</form>';
        var temp={'name':dependency,'list':dep_name};
        dependency_classes.push(temp);
    }
    $('#'+div_name).html(message);
    for(var i=0;i<array_list.length;i++){
        var dependency=array_list[i][0];
        var name_list=array_list[i][1].split(",");
        for(var j=0;j<name_list.length;j++){
            if(array_list[i][2].indexOf(name_list[j])>-1){
                $('#'+dependency+'_'+name_list[j]).attr('checked','checked');
            }
        }
        if($('.'+dependency).is(':checked')==false){
            $('#'+dependency+"-flag").removeClass('filled');
            $('#'+dependency+"-flag").addClass('unfilled');
        }
        else{
            $('#'+dependency+"-flag").removeClass('unfilled');
            $('#'+dependency+"-flag").addClass('filled');
        }
    }
    check_required_data(dependency_classes);
}
function GetBrowserSections(){
    $.ajax({
        url:'GetSections/',
        dataType : "json",
        data : {
            section : '',
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".section[data-level='']").append($('<option>').text(value).attr('value', value));
            });
            $(".section[data-level='']").attr('id',1);
        }
    });
    $(".section[data-level='']").change(function(){
        isAtLowestSection = false;
        recursivelyAddSection(this);
        $("#section-flag").removeClass("filled");
        $("#section-flag").addClass("unfilled");
    });


    $.ajax({
        url:'GetFeatures/',
        dataType : "json",
        data : {
            feature : '',
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')
        },
        success: function( json ) {
            if(json.length > 0)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".feature[data-level='']").append($('<option>').text(value).attr('value', value));
            });
            $(".feature[data-level='']").attr('id',1);
        }
    });
    $(".feature[data-level='']").change(function(){
        isAtLowestFeature = false;
        recursivelyAddFeature(this);
        $("#feature-flag").removeClass("filled");
        $("#feature-flag").addClass("unfilled");
    });


    //Browsers
    $.ajax({
        url:'GetBrowsers/',
        dataType : "json",
        data : {
            browser : '',
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')
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
}
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
                    data:{term:request.term,project_id: $.session.get('project_id'),
                    team_id: $.session.get('default_team_identity')},
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
//                console.log(ui);
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
                    fieldName.closest('tr').find('td:nth-child(9)').html(ui.item[2]);
                    if(ui.item[3]!=""){
                        fieldName.closest('tr').find('td:nth-child(11) span:eq(0)').addClass('filled');
                        $('#searchbox'+fieldName.closest('tr').find('td:nth-child(2)').text()+'descriptionpop').html(ui.item[3]);
                    }
                    else{
                        fieldName.closest('tr').find('td:nth-child(11) span:eq(0)').addClass('unfilled');
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
                        //$('#searchbox'+index+'verify').attr('checked',true);
                        $('#searchbox'+index+'verify').toggles({on:true});
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
function AutoCompleteLabel(){
    $('#label_txtbox').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"AutoCompleteLabel/",
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
//            console.log(ui);
            var id=ui.item[0].trim();
            var name=ui.item[1].trim();
            var color=ui.item[2].trim();
            if(id!=""){
                AddToListLabel(id,name,color);
            }
            return false;
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };
    $("#label_txtbox").keypress(function(event) {
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
        currentrow.find('td:nth-child(7) div:eq(0)').attr('id','searchbox'+i+'verify');
        currentrow.find('td:nth-child(8) div:eq(0)').attr('id','searchbox'+i+'continue');
        currentrow.find('td:nth-child(9) span:eq(0)').attr('id','searchbox'+i+'step_type');
        currentrow.find('td:nth-child(10) input:eq(0)').attr('id','searchbox'+i+'time');
        currentrow.find('td:nth-child(11) a:eq(0)').attr('id','searchbox'+i+'step_desc');
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
        '<tr>'
            +'<td><input type="checkbox" style="width: auto"></td>' +
            '<td><input class="textbox" style="width: auto"></td>' +
            '<td><input class="textbox" style="width: auto"></td>' +
            '<td><textarea class="ui-corner-all  ui-autocomplete-input"></textarea></td>' +
            '<td><input type="checkbox" style="width: auto"></td>' +

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
        '<table id="step'+stepno+stringName+'entrytable" class="two-column-emphasis" width="100%" style="font-size:75%">' +
        '<tr>' +
        '<th width="33%">Keyfield</th>' +
        '<th width="33%">Field</th>' +
        '<th width="33%">Sub-Field</th>' +
        '<th width="33%">Value</th>' +
        '<th width="33%">IgnoreField</th>' +
        '</tr>' +
        '<tr>' +
        '<td><input type="checkbox" style="width: auto"></td>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><textarea class="ui-corner-all  ui-autocomplete-input"></textarea></td>' +
        '<td><input type="checkbox" style="width: auto"></td>' +
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
        '<table id="step'+stepno+'data'+dataset_num+'entrytable"class="two-column-emphasis" width="100%" style="font-size:75%">' +
        '<tr>' +
        '<th width="33%">KeyField</th>' +
        '<th width="33%">Field</th>' +
        '<th width="33%">Sub-Field</th>' +
        '<th width="33%">Value</th>' +
        '<th width="33%">IgnoreField</th>' +
        '</tr>' +
        '<tr>' +
        '<td><input type="checkbox" style="width: auto"></td>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><input class="textbox" style="width: auto"></td>' +
        '<td><textarea class="ui-corner-all  ui-autocomplete-input"></textarea></td>' +
        '<td><input type="checkbox" style="width: auto"></td>' +
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
            '<td><div class="toggles toggle-light"  id="searchbox'+ step_num +'verify"  style="width:40%;"></div></td>'+
            '<td><div class="toggles toggle-light"  id="searchbox'+ step_num +'continue" style="width:40%;"></div></td>'+
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
    popupmetadata+=('<table id="searchbox'+step_num+'data_table" class="two-column-emphasis" width="100%">' +
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
    $('.toggles').each(function(){
        if($(this).attr('id')=="searchbox"+step_num+"verify" && $(this).find('div.toggle-slide').length==0){
            $(this).toggles({});
        }
        if($(this).attr('id')=="searchbox"+step_num+"continue" && $(this).find('div.toggle-slide').length==0){
            $(this).toggles({});
        }
    });
    AutoCompleteTestStep();
    TimePicker();
}
function addMainTableRow(divname){
    step_num++;
    popupdivrowcount[step_num-1]=0;
    $('#outer-data').append('<div id="searchbox'+step_num+'datapop">'+GeneratePopUpMetaData()+'</div>');
    $('#step_description_general').append('<div id="searchbox'+step_num+'descriptionpop"></div>');
    $(divname).append(GenerateMainRow());
    $('.toggles').each(function(){
       if($(this).attr('id')=="searchbox"+step_num+"verify" && $(this).find('div.toggle-slide').length==0){
           $(this).toggles({});
       }
        if($(this).attr('id')=="searchbox"+step_num+"continue" && $(this).find('div.toggle-slide').length==0){
            $(this).toggles({});
        }
    });
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
            section : (fatherHeirarchy+father).replace(/ /g,'_'),
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')

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


function recursivelyAddFeature(_this){
    var fatherHeirarchy = $(_this).attr("data-level");
    var father = $(_this).children("option:selected").text();
    if(father == "")
        return;
    if(father == "Choose..."){
        for(var i = 0; i < lowest_feature; i++){
            $("#featuregroup select.feature:last-child").remove();
        }
        lowest_feature = 0
        return;
    }
    var current_feature = (fatherHeirarchy.split(".").length - 1)
    if(current_feature < lowest_feature){
        for(var i = current_feature + 1; i <= lowest_feature; i++){
            $("#featuregroup select.feature:last-child").remove();
        }
        lowest_feature = current_feature
    }

    $.ajax({
        url:'GetFeatures/',
        dataType : "json",
        data : {
            feature : (fatherHeirarchy+father).replace(/ /g,'_'),
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')

        },
        success: function( json ) {
            if(json.length != 1){
                jQuery('<select/>',{
                    'class':'feature',
                    'data-level':fatherHeirarchy+father+'.',
                    change: function(){
                        isAtLowestFeature = false;
                        recursivelyAddFeature(this);
                        $("#feature-flag").removeClass("filled");
                        $("#feature-flag").addClass("unfilled");
                    }
                }).appendTo('#featuregroup');

                $(".feature[data-level='"+fatherHeirarchy+father+".']").append("<option>Choose...</option>");

                var once = true;
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
                $.each(json, function(i, value) {
                    if(i == 0)return;
                    if(once){
                        lowest_feature+=1
                        once = false
                    }
                    $(".feature[data-level='"+fatherHeirarchy+father+".']").append($('<option>').text(value).attr('value', value));
                });
            }else{
                isAtLowestFeature = true;
                $("#feature-flag").removeClass("unfilled");
                $("#feature-flag").addClass("filled");
            }
        }
    });
}

function check_required_data(array_list)
{
    for(var i=0;i<array_list.length;i++){
        var message="";
        for(var j=0;j<array_list[i].list.length;j++){
            if(j==0 || j==(array_list[i].list.length-1)){
                if(j==0){
                    message+='#'+array_list[i].list[j];
                }
                else{
                    message+=', #'+array_list[i].list[j];
                }
            }
            else{
                message+=', #'+array_list[i].list[j];
            }
        }
//        console.log(message);
        $(message).live('click',function(){
           for(var i=0;i<array_list.length;i++){
               for(var j=0;j<array_list[i].list.length;j++){
//                   console.log($(array_list[i].list[j]));
                   if($('#'+array_list[i].list[j]).is(':checked')==true){
                       $('#'+array_list[i].name+"-flag").removeClass('unfilled');
                       $('#'+array_list[i].name+"-flag").addClass('filled');
                   }
               }
               if($('.'+array_list[i].name).is(':checked')==false){
                   $('#'+array_list[i].name+"-flag").removeClass('filled');
                   $('#'+array_list[i].name+"-flag").addClass('unfilled');
               }
           }
        });

    }
}
/*function show_radio_button(){
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
}*/
function vertical_sidebar(){
    /*$("#add_step_tip").click(function(){
     if(confirm("Are you sure about leaving before saving?")){
     window.location = '/Home/ManageTestCases/CreateStep/'
     }
     });
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
     });*/
    $("#add_step_tip").click(function(){
        /*alertify.confirm("Are you sure about leaving before saving?", function(e) {
            if (e) {
                window.location = '/Home/ManageTestCases/CreateStep/'
            }
        });*/
        $("#title_prompt").html(
            //'<p style="text-align: center">You have selected ' +
            //tc_id +'-'+ tc_name + '.' +
            '<br/><p style="text-align: center; font-size: large; font: Helvetica, arial, freesans, clean, sans-serif;">Are you sure about leaving withoout saving?</p>' +
            '</p>' +
            '<div align="center" style="margin-left: 5%">' +
            '<a class="github" href="/Home/ManageTestCases/CreateStep/">Yes</a>' +
            '<a class="twitter" href="/Home/ManageTestCases/CreateStep/" target="_blank">Open in new tab</a>' +
            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
            '</div>'

        );
        $("#title_prompt").modal();
        return false;
    });

    /*$("#edit_step_tip").click(function(){
     if(confirm("Are you sure about leaving before saving?")){
     window.location = '/Home/ManageTestCases/CreateStep/'
     }
     });
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
     });*/
    $("#edit_step_tip").click(function(){
        /*alertify.confirm("Are you sure about leaving before saving?", function(e) {
            if (e) {
                //window.location = '/Home/ManageTestCases/CreateStep/'
                window.open('/Home/ManageTestCases/CreateStep/','_blank');
            }
        });*/
        $("#title_prompt").html(
            //'<p style="text-align: center">You have selected ' +
            //tc_id +'-'+ tc_name + '.' +
            '<br/><p style="text-align: center; font-size: large; font: Helvetica, arial, freesans, clean, sans-serif;">Are you sure about leaving before saving?</p>' +
            '</p>' +
            '<div align="center" style="margin-left: 5%">' +
            '<a class="github" href="/Home/ManageTestCases/CreateStep/">Yes</a>' +
            '<a class="twitter" href="/Home/ManageTestCases/CreateStep/" target="_blank">Open in new tab</a>' +
            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
            '</div>'

        );
        $("#title_prompt").modal();
        return false;
    });

    /*$("#set_tag_tip").click(function(){
     if(confirm("Are you sure about leaving before saving?")){
     window.location = '/Home/ManageTestCases/TestSet/'
     }
     });
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
     });*/
    $("#set_tag_tip").click(function(){
        /*alertify.confirm("Are you sure about leaving before saving?", function(e) {
            if (e) {
                window.location = '/Home/ManageTestCases/TestSet/'
            }
        });*/
        $("#title_prompt").html(
            //'<p style="text-align: center">You have selected ' +
            //tc_id +'-'+ tc_name + '.' +
            '<br/><p style="text-align: center; font-size: large; font: Helvetica, arial, freesans, clean, sans-serif;">Are you sure about leaving before saving?</p>' +
            '</p>' +
            '<div align="center" style="margin-left: 5%">' +
            '<a class="github" href="/Home/ManageLabel/">Yes</a>' +
            '<a class="twitter" href="/Home/ManageLabel/" target="_blank">Open in new tab</a>' +
            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
            '</div>'

        );
        $("#title_prompt").modal();
        return false;
    });
    /*$("#copy_edit_tip").click(function(){
     if(confirm("Are you sure about leaving before saving?")){
     window.location = '/Home/ManageTestCases/SearchEdit/'
     }
     });
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
     });*/
    $("#copy_edit_tip").click(function(){
        /*alertify.confirm("Are you sure about leaving before saving?", function(e) {
            if (e) {
                window.location = '/Home/ManageTestCases/SearchEdit/'
            }
        });*/
        $("#title_prompt").html(
            //'<p style="text-align: center">You have selected ' +
            //tc_id +'-'+ tc_name + '.' +
            '<br/><p style="text-align: center; font-size: large; font: Helvetica, arial, freesans, clean, sans-serif;">Are you sure about leaving before saving?</p>' +
            '</p>' +
            '<div align="center" style="margin-left: 5%">' +
            '<a class="github" href="/Home/ManageTestCases/SearchEdit/">Yes</a>' +
            '<a class="twitter" href="/Home/ManageTestCases/SearchEdit/" target="_blank">Open in new tab</a>' +
            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
            '</div>'

        );
        $("#title_prompt").modal();
        return false;
    });
    /*$("#history_tip").click(function(){
     if(confirm("Are you sure about leaving before saving?")){
     window.location = '/Home/Analysis/'
     }
     });
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
     });*/
    $("#history_tip").click(function(){
        /*alertify.confirm("Are you sure about leaving before saving?", function(e) {
            if (e) {
                window.location = '/Home/Analysis/'
            }
        });*/
        $("#title_prompt").html(
            //'<p style="text-align: center">You have selected ' +
            //tc_id +'-'+ tc_name + '.' +
            '<br/><p style="text-align: center; font-size: large; font: Helvetica, arial, freesans, clean, sans-serif;">Are you sure about leaving before saving?</p>' +
            '</p>' +
            '<div align="center" style="margin-left: 5%">' +
            '<a class="github" href="/Home/Analysis/">Yes</a>' +
            '<a class="twitter" href="/Home/Analysis/" target="_blank">Open in new tab</a>' +
            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
            '</div>'

        );
        $("#title_prompt").modal();
        return false;
    });
    /*$("#organize_tip").click(function(){
     if(confirm("Are you sure about leaving before saving?")){
     window.location = '/Home/ManageTestCases/CreateProductSections/'
     }
     });
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
     });*/
    $("#organize_tip").click(function(){
        /*alertify.confirm("Are you sure about leaving before saving?", function(e) {
            if (e) {
                window.location = '/Home/ManageTestCases/'
            }
        });*/
        $("#title_prompt").html(
            //'<p style="text-align: center">You have selected ' +
            //tc_id +'-'+ tc_name + '.' +
            '<br/><p style="text-align: center; font-size: large; font: Helvetica, arial, freesans, clean, sans-serif;">Are you sure about leaving before saving?</p>' +
            '</p>' +
            '<div align="center" style="margin-left: 5%">' +
            '<a class="github" href="/Home/ManageTestCases/">Yes</a>' +
            '<a class="twitter" href="/Home/ManageTestCases/" target="_blank">Open in new tab</a>' +
            '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
            '</div>'

        );
        $("#title_prompt").modal();
        return false;
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
/*function desktop_notify(message){
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


}*/
function AutoCompleteSearchForPrompt(){
//    $("#titlebox").autocomplete({
//        source:function(request,response){
//            $.ajax({
//                url:"TestCaseSearch/",
//                dataType:"json",
//                data:{
//                    term:request.term
//                },
//                success:function(data){
//                    response(data);
//                }
//            });
//        },
//        select:function(event,ui){
//            var tc_id=ui.item[0].trim();
//            var tc_name=ui.item[1].trim();
//            if(tc_id!=""){
//                $(this).val(tc_name);
//                /*if(confirm("Are you sure about leaving before saving?")){
//                 window.location = '/Home/ManageTestCases/Edit/'+tc_id
//                 }
//                 else{
//                 window.location = '/Home/ManageTestCases/CreateNew/'+tc_id
//                 }*/
//                $("#title_prompt").html(
//                    '<p style="text-align: center">You have selected ' +
//                        tc_id +'-'+ tc_name + '.' +
//                        '<br/> What do you want to do?' +
//                        '</p>' +
//                        '<div style="padding-left: 15%">' +
//                        '<a class="github" href="/Home/ManageTestCases/Edit/'+tc_id+'">Edit</a>' +
//                        '<a class="twitter" href="/Home/ManageTestCases/CreateNew/'+tc_id+'">Copy</a>' +
//                        '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
//                        '</div>'
//
//                );
//                $("#title_prompt").modal();
//                return false;
//            }
//        }
//    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
//        return $( "<li></li>" )
//            .data( "ui-autocomplete-item", item )
//            .append( "<a>" + item[0] + " - "+item[1]+"<strong> - " + item[2] + "</strong></a>" )
//            .appendTo( ul );
//    };
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
                alertify.success("New step created with title '"+step+"'","",0)
            }
        }
    });
}

/*function show_labels(){
    $.ajax({
        url:'GetLabels',
        dataType : "json",
        data : {
            term : ''
        },
        success: function( json ) {
            $.each(json, function(index, value){
                $("#labels").append('<tr><td><input type="checkbox" value="' +
                value[0] +
                '" name="labels"><a class="label" style="background-color: ' +
                value[2] +
                ';">' +
                value[1] +
                '</a></td></tr>')
            });
        }
    });
}*/
/****************************End Minar's Thing****************************************************/
function DeleteSearchQueryText() {
    $(".delete").live("click", function() {
        $(this).parent().parent().remove();
    });
}

// Add an item to an html list
function AddToListLabel(id,name,color) {
    $("#searchedlabel").append(
        '<td><input type="checkbox" checked="true" value="' +
        id +
        '" name="labels">' +
        '<a class="label" style="background-color: ' +
        color +
        ';">' +
        name +
        '</a></td>'
            + '</td>&nbsp;&nbsp;&nbsp;');
}
