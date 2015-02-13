$(document).ready(function(){
	
	var Env = "";
	var URL = window.location.pathname;
	indx = URL.indexOf("Run");
    machine_div();
    //Codes for the MileStone Tab
    MileStoneTab();
    $.get("GetOS",
        {
            os:''
        },
        function(data){
            console.log(data['os']);
            console.log(data['browser']);
            console.log(data['productVersion']);
            populate_manual_test_div(data['os'],data['browser'],data['productVersion']);
        });
	if (indx != -1)
	{
		//when use will click on PC flip bar
		$(".buttonPic[title='PC_Platform']").click(function(){
			
			//$(".flip[title='Availeable Test Machine']").fadeIn(1000);
			//$(".flip[title='Add Manual Test Machine']").fadeIn(1000);
			$("#Place_AutoComplete_Here").fadeIn(1000);
			$('#PlatformChose').css({'display':'none'});
			$(".buttonPic[title='Mac_Platform']").css({'display':'none'})
			$(".text[title='Choose']").text('Welcome to PC Environment Test Lab');
			//$(".flip[title='PC_Platform']").text('Welcome to PC Environment Test Lab');
			//$(".flip[title='PC_Platform']").css({ 'cursor':'default','margin-left': '40%', 'height': '15%' , 'width': '200%'})
			$(".buttonPic[title='PC_Platform']").css({'display':'none'})
			
			Env = "PC"
			RunTestAutocompleteSearch(Env);
			
		});
		
		
		//when user will click on Mac flip bar
		$(".buttonPic[title='Mac_Platform']").click(function(){
			
			//$(".flip[title='Availeable Test Machine']").fadeIn(1000)
			$("#Place_AutoComplete_Here").fadeIn(1000);
            $('#PlatformChose').css({'display':'none'});
			
			$(".buttonPic[title='PC_Platform']").css({'display':'none'})
			$(".text[title='Choose']").text('Welcome to Mac Environment Test Lab');
			//$(".flip[title='Mac_Platform']").text('Welcome to Mac Environment Test Lab');
			//$(".flip[title='Mac_Platform']").css({ 'cursor':'default','margin-left': '-100%','height': '15%' , 'width': '200%'})
			$(".buttonPic[title='Mac_Platform']").css({'display':'none'})
			
			Env = "Mac"
			RunTestAutocompleteSearch(Env);
		});
		
		
		/*$(".flip[title='Add Manual Test Machine']").click(function(){
            //console.log($(this).attr('title')+" has been clicked");

            $("#error").html("");
            $("#error").insertBefore("#AvailableTestMachine");
            $("#AvailableTestMachine").css({'display':'none'});
            $("#AddManualTestMachine").children().remove();
            populate_manual_test_div();
            $("#AddManualTestMachine").slideToggle("slow");
        });*/
			
			AddAutoCompleteSearchBox("#Place_AutoComplete_Here","Search Test Cases Data By Keywords:");
			
			//AvailebableTestMachineflipButton(Env);
			
			
			
			//======================Calling flip Code =================
				FlipFunction();
			
			
			// Calling DeleteSearchQueryText for Deleting query text after clicking on delete button
				DeleteSearchQueryText();
			
			
			// On Clicking Auto Complete Search Button, Send Query Text to View.py > AjaxData function
			$(".Buttons[title='Search Test Cases']").click(function(){ 
				
				if ($("#AutoSearchTextBoxLabel").text() != "Search User:")
				{
					PerformSearch();
				}
				
			});
			
			
			
			// On Clicking Auto Complete Verify Query Button, Send Query Text to View.py > Verify_Query function
			$(".Buttons[title='Verify Query']").click(function(){ 
				
				VerifyQueryProcess();
			 });
			
			
			
			// On Clicking Select User Button, Send Query Text to View.py > SelectUser function
			$(".Buttons[title='Select User']").click(function(){ 
				
				
				$("P:contains('Test Data Type')").fadeOut(1000);
				SelecteUserProcess();
				SelectEmail();
			 });
			
			
			
			// On Clicking Run Test Button, Send Query Text to View.py > RunTest function
			$(".Buttons[title='Run Test']").click(function(){ 
			
				RunTestProcess();
				
			});
	
	  }


    /*$("#operation_milestone").click(function(event){
        populate_milestone();
    });*/

	
});
function MileStoneTab(){
    $('#msinput').autocomplete({
        source:function(request,response){
            if($('#operation_milestone option:selected').val()!="0"){
                $.ajax({
                    url:"AutoMileStone",
                    dataType:"json",
                    data:{term:request.term},
                    success:function(data){
                        response(data);
                    }
                });
            }
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                $(this).val(value.trim());
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $('#operation_milestone').live('change',function(){
        // autoCompleteMilestone();
        var selection=$('#operation_milestone option:selected').val();
        if(selection==2){
            $('#renamebox').css({'display':'inline-block'});
            $('#msinput2').autocomplete({
                source:function(request,response){
                    if($('#operation_milestone option:selected').val()!="0"){
                        $.ajax({
                            url:"AutoMileStone",
                            dataType:"json",
                            data:{term:request.term},
                            success:function(data){
                                response(data);
                            }
                        });
                    }
                },
                select:function(request,ui){
                    var value=ui.item[0].trim();
                    if (value!=""){
                        $(this).val(value.trim());
                        return false;
                    }
                }
            }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li></li>" )
                    .data( "ui-autocomplete-item", item )
                    .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
                    .appendTo( ul );
            };
        }
        else{
            $('#renamebox').css({'display':'none'});
        }
    });
    $('#ms_button').live('click',function(){
        var operation=$('#operation_milestone option:selected').val();
        if(operation==2){
            var new_name=$('#msinput2').val();
            var old_name=$('#msinput').val();
        }
        else{
            var new_name=$('#msinput').val();
            var old_name="";
        }
        if(operation=="0"){
            var title_msg = "Fields are Empty!"
        }
        else if(operation=="1"){
            title_msg = "Milestone Created"
        }
        else if(operation=="2"){
            title_msg = "Milestone Renamed"
        }
        else if(operation=="3"){
            title_msg = "Milestone Deleted"
        }
        if(operation=="0"||new_name==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_milestone').html(error_message);
            $('#error_milestone').css({'display':'block'});
        }
        else {
            $.get('MileStoneOperation',{old_name:old_name,new_name:new_name,operation:operation},function(data){
                if(data['confirm_message']==""){
                    var color='red';
                }
                else{
                    var color='green';
                }
                if(data['confirm_message']==""){
                    alertify.log(""+data['error_message']+"","",0);
                    milestone_notify(""+data['error_message']+"",""+data['error_message']+"","/site_media/noti2.ico");
                    $('#error_milestone').html('<b style="color:red;">'+data['error_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/RunTest/';
                }
                else{
                    alertify.log(""+data['confirm_message']+"","",0);
                    milestone_notify(title_msg,""+data['confirm_message']+"","/site_media/noti.ico");
                    $('#error_milestone').html('<b style="color:green;">'+data['confirm_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                    $('#error_milestone').slideDown('slow');
                    //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    window.location = '/Home/RunTest/';
                }

            })
        }
    });
}
function machine_div(){
    Env = Get_Selected_Env_Name();
    //$("#AvailableTestMachine").slideToggle("slow");
    var SearchUser = "True"
    $.get("Table_Data_UserList",{UserListRequest : SearchUser, Env: Env},function(data) {
        ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User(s)", "Number of users available");
    });
}
function populate_manual_test_div(environment,browserdata,productVersion){
    //populate the os names
    var message="";
    console.log(environment);
    for(var i=0;i<environment.length;i++){
        //console.log(message);
        message+='<option value="'+environment[i][0].trim()+'">'+environment[i][0]+'</option>';
    }
    $('#os_name').append(message);
    message="";
    for(var i=0;i<browserdata.length;i++){
        message+='<option value="'+browserdata[i][0].trim()+'">'+browserdata[i][0]+'</option>'
    }
    $('#browser').append(message);
    message="";
    for(var i=0;i<productVersion.length;i++){
        message+='<option value="'+productVersion[i].trim()+'">'+productVersion[i].trim()+'</option>'
    }
    $('#product_version').append(message);
    $('#os_name').live('change',function(){
        if($('#os_name').val()!=''){
            console.log($(this).val());
            var message="";
            for(var i=0;i<environment.length;i++){
                if($(this).val()==environment[i][0].trim()){
                    console.log(environment[i][1]);
                    var os_version=environment[i][1];
                    for(var j=0;j<os_version.length;j++){
                        message+='<option value="'+os_version[j]+'">'+os_version[j]+'</option>'
                    }
                }
            }
            $('#os_version').html(message);
            $('#version_bit').css({'display':'inline-block'});
        }
        else{
            $('#os_version').html("");
            $('#version_bit').css({'display':'none'});
        }
    });
    $('#browser').live('change',function(){
        if($('#browser').val()!=''){
            var message="";
            for(var i=0;i<browserdata.length;i++){
                if($(this).val()==browserdata[i][0].trim()){
                    browser_version=browserdata[i][1];
                    for(var j=0;j<browser_version.length;j++){
                        message+='<option value="'+browser_version[j].trim()+'">'+browser_version[j].trim()+'</option> '
                    }
                }
            }
            $('#browser_version').html(message);
            $('#b_version').css({'display':'inline-block'});
        }
        else{
            $('#browser_version').html("");
            $('#b_version').css({'display':'none'});
        }
    });
    AutoCompletionButton(environment,browserdata);
}
function AutoCompletionButton(environment,browserdata){
    //console.log('into the AutoCompleteing');
    $("#machine_name").autocomplete({
        source:function(request,response){
            $.ajax({
                url:"Auto_MachineName",
                dataType:"json",
                data:{term:request.term},
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
                    console.log(data[0]);
                    var list=data[0];
                    $('#os_name').val(list[0]);
                    for(var i=0;i<environment.length;i++){
                        var message="";
                        if($('#os_name').val()==environment[i][0]){
                            for(var j=0;j<environment[i][1].length;j++){
                                message+='<option value="'+environment[i][1][j].trim()+'">'+environment[i][1][j]+'</option> '
                            }
                            $('#os_version').html(message);
                            break;
                        }
                    }
                    $('#os_version').val(list[1]);
                    $('#os_bit').val(list[2]);
                    $('#version_bit').css({'display':'inline-block'});
                    $('#machine_ip').val(list[3]);
                    var browsers=list[4].split(";")[0].split("(");
                    for(var i=0;i<browserdata.length;i++){
                        var message="";
                        if(browsers[0].trim()==browserdata[i][0]){
                            var browser_version=browserdata[i][1];
                            for(var j=0;j<browser_version.length;j++){
                                message+='<option value="'+browser_version[j].trim()+'">'+browser_version[j]+'</option> ';
                            }
                            $('#browser_version').html(message);
                            $('#browser_version').val(browsers[1]);
                            break;
                        }
                    }
                    $('#b_version').css({'display':'inline-block'});
                    $('#browser').val(browsers[0].trim());
                    $('#product_version').val(list[5]);
                    console.log(browsers);
                })
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };
    $('#machine_name').live('click',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#os_name').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#os_version').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#os_bit').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#machine_ip').live('click',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#browser').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");

    });
    $('#browser_version').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#product_version').live('change',function(){
        $('#error_message').slideUp("slow");
        $('#error_message').html("");
    });
    $('#submit_button').live('click',function(){
        var machine_name=$('#machine_name').val();
        var os_name=$('#os_name option:selected').val();
        var os_version=$('#os_version option:selected').val();
        var os_bit=$('#os_bit option:selected').val();
        var browser=$('#browser option:selected').val();
        var browser_version=$('#browser_version option:selected').val();
        var machine_ip=$('#machine_ip').val();
        var product_version=$('#product_version option:selected').val();
        if(machine_name==''||os_name==''||browser==''||machine_ip==''||product_version==''){
            var error_message="<b style='color: #ff0000'>Fields are empty</b>";
            alertify.log("Fields are empty","",0);
            $('#error_message').html(error_message);
            $('#error_message').css({'display':'block'});
        }
        else{
            $.get("AddManualTestMachine",{
                machine_name:machine_name,
                os_name:os_name,
                os_version:os_version,
                os_bit:os_bit,
                browser:browser,
                browser_version:browser_version,
                machine_ip:machine_ip,
                product_version:product_version
            },function(data){
                //console.log(data);
                alertify.log(""+data+"","",0);
                machine_notify(""+data+"");
                $('#error_message').html('<b style="color: #109F40">'+data+'<br>Page will be refreshed to change effect</b>');
                $('#error_message').slideDown('slow');
                //setTimeout(function(){window.location='/Home/RunTest/';},4000);
                window.location = '/Home/RunTest/';
            });
        }
    });
}
var DepandencyNameList = [];

function SendingQueryAndDepandency()
{
	DepandencyNameList = []
	$("#AutoSearchResult #searchedtext").each(function() 
	{
		var UserText = $(this).find("td").text();
		UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		Env = Get_Selected_Env_Name()
	
		$.get("Verify_Query", {Query : UserText, Env: Env}, function(data) 
		{
			if (data["DepandencyList"].length != 0 )
			{	
				var DepandencyName = "";
				//var DepandencyNameList = [];
				for (Depand in data["DepandencyList"]) 
				{
					var DepandencyName = "";
					DepandencyName = data["DepandencyList"][Depand][0]
                    console.log(DepandencyName);
					DepandencyNameList.push(DepandencyName)
				}
			}
			
			else
			{
				$(".Buttons[title='Select User']").fadeIn(2000)
			}
		
			
			//$("#DepandencyCheckboxes form#device_memory input").is(":checked")
            var client="";
			$("input [type='radio'], #DepandencyCheckboxes").each(function()
			{
				$(this).live('click',function()
				{	
					var Text = "";
					var DNL = DepandencyNameList
                    client=$(this).val();
					for (i in DNL)
					{	
						temp = $("#DepandencyCheckboxes form#" +DNL[i]+ " input:checked").val();
                        console.log(temp);
						if(temp !== undefined)
						{
							Text += temp + ":";
						}
					}
					DNL = ""
					if ( (Text.split(":").length)-1 === (DepandencyNameList.length) )
					{
						$(".Buttons[title='Select User']").fadeIn(2000)
						$("#DepandencyCheckboxes").slideUp("slow");
                       // var place=$("#AutoSearchResult #DependencyText td").text();
                        //console.log("before:"+place);
						$("#AutoSearchResult #DependencyText td").remove();
                        //place=$("#AutoSearchResult #DependencyText td").text();
                        //console.log("after:"+place);

                        var DNL = DepandencyNameList
                       // console.log(DNL);
						for (t in DNL)
						{	
							Depend = $("#DepandencyCheckboxes form#" +DNL[t]+ " input:checked").val();
							if(Depend !== undefined)
							{
								//Text += Depend + ":";
								$("#AutoSearchResult #DependencyText").css('display','block')
								$("#AutoSearchResult #DependencyText").append(
										
										'<td><img class="delete" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
										+ '<td name = "Dependencyquery" class = "Text" style = "size:10">'
										+ Depend
										+ ":&nbsp"
										+ '</td>'
										 );
								
							}
						}
						DNL = ""
						
					}
                    });
            });
            $("#AutoSearchResult #searchedtext").each(function() {
                var UserText = $(this).find("td").text();
                UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
                UserText+=(' '+client+":");
                Env = Get_Selected_Env_Name()
                $.get("Table_Data_TestCases",{Query: UserText, Env: Env},function(data) {

                    if (data['TableData'].length == 0)
                    {
                        $('#RunTestResultTable').children().remove();
                        //$('#RunTestResultTable').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                        $("#DepandencyCheckboxes").children().remove();
                        //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
                        $('#timeRequired').fadeOut(500);
                        $('#timeRequired').html("");
                    }
                    else
                    {
                        ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

                        $("#RunTestResultTable").fadeIn(1000);
                        $("p:contains('Show/Hide Test Cases')").fadeIn(2000);
                        var message=('<p align="center" style="font-size:150%;font-weight: bold;color:#003bb3;">TimeRequired:&nbsp;&nbsp;<b style="font-size: 150%;font-weight:bolder; color: #000000;">'+data['TimeEstimated']+'</b></p>');
                        $('#timeRequired').html(message);
                        $('#timeRequired').fadeIn(1000);
                        implementDropDown('#RunTestResultTable');
                        VerifyQueryProcess();
                        //$(".Buttons[title='Verify Query']").fadeIn(2000);
                        $(".Buttons[title='Select User']").fadeOut();
                    }

                });

            });

        });
	});
}


function AddAutoCompleteSearchBox(WhereToPlaceId, Label)
{	
	
	$(WhereToPlaceId).append(
						
			
		"<form method = 'get' >"

				+"<table id='AutoSearchResult' style='display: block;' >"
					+ "<tbody>"
						+ "<tr>"
							//Dependency CheckBoxes
							+"<td>"
								+"<p class='flip' title='DepandencyCheckBox' style='color: black; width: 43%  ;display:None; margin-top: 10px;'>Please Select Dependency</p>"
								+"<div id = 'DepandencyCheckboxes' class = 'Text'  style= 'margin-right: 50%; display:block; color: black;'>"
								+" </div>"
						    +"</td>"
							
							
							//Test Data Type CheckBoxes
							/*+"<td style='position:relative;left:700px;'>"
								+"<p  class='flip' id = 'TestDataTypeCheckboxes' title='TestDataTypeCheckBox' style='color: black; width: 160%  ;display:none; margin-top: -94px;'>Test Data Type</p>"
								+"<div id = 'TestDataTypeCheckboxes' class = 'Text'  style= 'display:none; color: black;'>"
								+"<form  action =''>"
									+"<input   class=' ui-corner-all'  type='radio' name = 'TestDataType' value = 'Default' checked='checked' >Default <br>"
									+"<input   class=' ui-corner-all'  type='radio' name = 'TestDataType' value = 'Performance'>Performance <br>"
									+"<input   class=' ui-corner-all'  type='radio' name = 'TestDataType' value = 'Localization'>Localization <br>"
								+"</form>"
								+" </div>"
							+"</td>"
						+ "</tr>"*/
						
						
						+"<tr>"
							//Search Email Input Box
							+"<td>"
								+"<label  class = 'Text SearchEmail' style = 'display:none' > <b> Select Name for Email: </b></label>"
							+ "</td>"
							+ "<td>"
								+"<input  id = 'EmailSearchBox' class='SearchEmail ui-corner-all textbox' style = 'display:none;' size='42' type='text' title = 'Please Select Email by Keyword' />"
							+ "</td>"
						+ "</tr>"
                        + "<tr>"
                            + "<td>"
                                + "<label class='Text SearchEmail' style='display:none'><b>*Select a Tester:</b></label>"
                            + "</td>"
                            + "<td>"
                                + "<input id='TesterSearchBox' class='SearchEmail ui-corner-all textbox' style=' display: none;' size='42' type='text' title='Please Select a tester'>"
                            + "</td>"
                        + "</tr>"
						
						+"<tr>"
							+"<td >"
								+"<label  style = 'display:none'   class = 'Text' id = 'TestObjective' > <b> *Test Objective: </b></label>"
							+"</td>"
						
							+"<td>"
								+"<input class = 'ui-corner-all textbox' id = 'TestObjective' style = 'display:none;' size = '42' maxlength = '50' type='text' title = 'Type Test Obejct' />"
							+"</td>"
						+"</tr>"

                        +"<tr>"
                            +"<td >"
                                +"<label  style = 'display:none'   class = 'Text' id = 'TestMileStoneText' > <b> *Test MileStone: </b></label>"
                            +"</td>"

                            +"<td>"
                                +"<input class = 'ui-corner-all textbox' id = 'TestMileStone' style = 'display:none;'  size = '42' maxlength = '50' type='text' title = 'Type Test Obejct' />"
                            +"</td>"
                        +"</tr>"
					
					
						+ "<tr>"
							+ "<td>"
								+ "<label > <b id = 'AutoSearchTextBoxLabel' class = 'Text'>"
								+ Label
								+ " </b></label>"
							+ "</td>"
							+ "<td>"
								+ "<input class = 'ui-corner-all textbox' id='searchbox' type='text' title = 'Please Type Keyword and Click On that to add to query' name='searchboxname' />"
							+ "</td>"
						+ "</tr>"
						
						
				
				+ "<tr>"
				+"<table id = 'AutoSearchResult' >"
					+ "<tbody>"
						
						+ "<tr id = 'searchedtext'>"
							+"<p> </p>"
							+ "<th class = 'Text' style= 'text-align: left'>Test Data Set:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </th>"
						+ "</tr>"
						
					+ "</tbody>"	
				+ "</table>"
				+ "</tr>"
				
				+ "<tr>"
				+"<table id = 'AutoSearchResult' >"
					+ "<tbody>"
						+ "<tr id = 'DependencyText' style = 'display:None' >"
							+ "<th class = 'Text' style= 'text-align: left'>Parameters:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </th>"
						+ "</tr>"
					 + "</tbody>"	
				+ "</table>"
				+ "</tr>"
				
				+ "<tr>"
				+"<table id = 'AutoSearchResult' >"
					+ "<tbody>"
						+ "<tr id = 'SelectedEmail' class='SearchEmail' style='display:None'>"
					    	
							+ "<th class = 'Text' style= 'display:None ; text-align: left'>Email Name:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </th>"
					    + "</tr>"
				    + "</tbody>"	
				+ "</table>"
				+ "</tr>"
				
				+ "<tr>"
                +"<table id = 'AutoSearchResult' >"
                    + "<tbody>"
                        + "<tr id = 'AssignedTester' class='SearchEmail' style='display:None'>"

                        + "<th class = 'Text' style= 'display:None ; text-align: left'>Selected Tester:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </th>"
                        + "</tr>"
                    + "</tbody>"
                + "</table>"
                + "</tr>"
                + "<tr>"
                +"<table id = 'AutoSearchResult' >"
                    + "<tbody>" +
                            "<tr id='MileStoneHeader'>" +
                                "<td><th class = 'Text' style= 'display:None ; text-align: left'>MileStone Added:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </th>" +
                            "</td>" +
                            "<td>" +
                                "<table>"
                                + "<tr id = 'AddedMileStone' class='SearchEmail' style='display:None;margin-top: -10%;'>"

                                + "</tr>"
                                + "</table>" +
                            "</td>" +
                            "</tr>"
                    + "</tbody>"
                + "</table>"
                + "</tr>"
                + "</div>"
			+ "</tbody>"
		+ "</table>"
	  + "</form>"
			
			
	
	);
}


function AvailebableTestMachineflipButton()
{
	$(".flip[title='Availeable Test Machine']").click(function(){

        $("#error").html("");
        $("#error").insertBefore("#AvailableTestMachine");
		$("#AddManualTestMachine").css({'display':'none'});
		Env = Get_Selected_Env_Name();
		$("#AvailableTestMachine").slideToggle("slow");
		var SearchUser = "True"
		$.get("Table_Data_UserList",{UserListRequest : SearchUser, Env: Env},function(data) {
		ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User/s");
		
		//Removing Unnecessary columns
		//$("#AvailableTestMachine .ui-widget th:nth-child(1), .ui-widget td:nth-child(1)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(2), .ui-widget td:nth-child(2)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(3), .ui-widget td:nth-child(3)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(6), .ui-widget td:nth-child(6)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(9), .ui-widget td:nth-child(9)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(12), .ui-widget td:nth-child(12)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(15), .ui-widget td:nth-child(15)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(16), .ui-widget td:nth-child(16)").remove()
		
		
		
		});
	}); 
	
}
function RunTestAutocompleteSearch(Env)

{

    $("#searchbox").autocomplete(
        {
            //Calling AutoCompleteTestSearch function with 'term'(default) parameter and Env variable
            //So AutoCompleteTestSearch function in View.py will receive two variable 'term' (this is the one when user type on search box) and Env variable.


            /*source :  'AutoCompleteTestCasesSearch' ,

             extraParams: {
             Env: function() {return Env},

             },*/

            source : function(request, response) {
                $.ajax({
                    url:"AutoCompleteTestCasesSearch",
                    dataType: "json",
                    data:{ term: request.term, Env: Env },
                    success: function( data ) {
                        response( data );
                    }
                });
            },

            //source : 'AutoCompleteTestCasesSearch?Env = ' +Env,
            select : function(event, ui) {

                var tc_id_name = ui.item[0].split(" - ");
                console.log(tc_id_name);
                var value = "";
                if (tc_id_name != null)
                    value = tc_id_name[0]
                console.log(value);
                var str=$("#AutoSearchTextBoxLabel").text()
                console.log(str);

                // Checking if Search Text box is for User Search
                if ($("#AutoSearchTextBoxLabel").text().trim() === "*Select Test Machine:")

                {
                    $(".Buttons[title='Select User']").css('display', 'none');
                    $(".Buttons[title='Run Test']").fadeIn(2000);
                    $("P:contains('Dependency')").fadeOut(1000);
                    $("P:contains('Test Data Type')").fadeOut(1000);
                }

                else
                    (value != "")
                {
                    $(".Buttons[title='Search']").fadeIn(2000);

                    //$("#Main_Heading_And_Menu").slideUp("slow");
                    $("p:contains('Menu')").fadeIn(2000);

                    $("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                        + '<td name = "submitquery" class = "Text" style = "size:10">'
                        + value
                        + ":&nbsp"
                        + '</td>');

                    if ($("#AutoSearchTextBoxLabel").text() != "Search User:") {
                        PerformSearch();
                    }
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

    $("#searchbox").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }

        if ($("#AutoSearchTextBoxLabel").text().trim() === "*Select Test Machine:") {
            PerformSearch();
        }
    });
}






function PerformSearch() {
	$("#AutoSearchResult #searchedtext").each(function() {
						var UserText = $(this).find("td").text();
						UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
						Env = Get_Selected_Env_Name()
						$.get("Table_Data_TestCases",{Query: UserText, Env: Env},function(data) {

											if (data['TableData'].length == 0)
											{
												$('#RunTestResultTable').children().remove();
												//$('#RunTestResultTable').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
												$("#DepandencyCheckboxes").children().remove();
												//$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
                                                $('#timeRequired').fadeOut(500);
                                                $('#timeRequired').html("");
                                            }
											else 
											{
												ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

												$("#RunTestResultTable").fadeIn(1000);
												$("p:contains('Show/Hide Test Cases')").fadeIn(2000);

												// ===============To Make First
												// td or each tr (i.e Test Case
												// ID) Click able
												//Making MKS link to MKS ID
												/*$("#RunTestResultTable tr>td:nth-child(1)").each(function(){
													
													MKS_ID = $(this).text();
													if (MKS_ID != "")
														{
															$(this).html("<a target='_blank' href ='http://mksintegrity:7001/im/issues?selection=" + MKS_ID + "' > "+ MKS_ID + " </a>");
																	
														}
												
												});		
												*/
											//	TestCase_TestStep_Details_Table('#RunTestResultTable tr>td:nth-child(2)');

												/*$(".ui-widget tr td:nth-child(2)").css({'color' : 'skyblue','cursor' : 'pointer'});
												$(".ui-widget tr td:nth-child(2)").each(function() {
													$(this).live('click',function() {
														
														var childrenCount = $(this).children().length
														console.log(childrenCount);
                                                        if (childrenCount == 0)
														{
															$(this).children().slideDown();
														}
														else
														{
															$(this).children().slideUp();
                                                            $(this).children().remove();
                                                            return;
                                                            console.log($(this).children());
															//return;
														}
														var ClickedTC = $(this).text();
														var RunID = $(this).closest('tr').find('td:nth-child(1)').text();
														RunID = RunID.trim();
														
														var $TC = $(this).text();
														var TestSteps;
														$.get("TestCase_TestSteps_SearchPage",{ClickedTC : ClickedTC,RunID: RunID},function(data) {
															TestSteps = data['Result'];
															
															$(".ui-widget tr td:nth-child(2)").each(function() {
																if (($(this).text()) == ClickedTC) 
																{
																	
																	$(this).children().remove();
																  for (eachitem in data['Result'])
																  {
																	  
																	$($(this)).append("<p id = 'TestCase_Steps'>"+ data['Result'][eachitem]																																				+ "</p>");
																  }
																  
																}

															  $("p#TestCase_Steps").css({'color' : 'silver','cursor' : 'text'});
															});

														});
																											
													});
												});*/
                                                var message=('<p align="center" style="font-size:150%;font-weight: bold;color:#003bb3;">TimeRequired:&nbsp;&nbsp;<b style="font-size: 150%;font-weight:bolder; color: #000000;">'+data['TimeEstimated']+'</b></p>');
                                                $('#timeRequired').html(message);
                                                $('#timeRequired').fadeIn(1000);
                                                implementDropDown('#RunTestResultTable');
												VerifyQueryProcess();
												//$(".Buttons[title='Verify Query']").fadeIn(2000);
												$(".Buttons[title='Select User']").fadeOut();
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

function SelecteUserProcess() {
	
	$("#PlatformChose").remove();
    Env = Get_Selected_Env_Name();
	$("#searchbox").autocomplete({

		//source : 'AutoCompleteUsersSearch',

        source : function(request, response) {
            $.ajax({
                url:"AutoCompleteUsersSearch",
                dataType: "json",
                data:{ term: request.term, Env: Env },
                success: function( data ) {
                    response( data );
                }
            });
        }
	});
	var SearchUser = "True"
	$(".flip[title='DepandencyCheckBox'], #DepandencyCheckboxes").css('display','None');
	$("div#TestDataTypeCheckboxes, p#TestDataTypeCheckboxes").css('display','None');
	$(".flip[title = 'Availeable Test Machine']").css('display','None');
	
	Env = Get_Selected_Env_Name()
	$.get("Table_Data_UserList",{UserListRequest : SearchUser, Env: Env},function(data) {

		//When User Clicks on Availebable Test Machine flip image
		$(".flip[title='Availeable Test Machine']").click(function(){
			
			//$("#AvailableTestMachine").slideToggle("slow");
			ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User/s");
			
		}); //End Of Code
		
		
		
		if (data['TableData'].length == 0) 
		{
			$("#AutoSearchTextBoxLabel").html("<b>*Select Test Machine:&nbsp;&nbsp;</b>");
			$('#RunTestResultTable').children().remove();
			$('#RunTestResultTable').append('<p class = "Text"><b>Sorry There is No Availaable User To Run The Test!!!</b></p>');
		}
		
		else 
		{
			ResultTable('#RunTestResultTable', data['Heading'],data['TableData'], "Available User/s");

			$("#AutoSearchTextBoxLabel").html("<b>*Select Test Machine:&nbsp;&nbsp;  </b>");

			$(".Buttons[title='Search Test Cases']").fadeOut(1000);
			
			$(".delete").css('cursor','default');

			$(".SearchEmail").fadeIn(1000);
			$("P:contains('Dependency')").fadeOut(100);
			$("P:contains('Test Data Type')").fadeOut(100);
			
			$("label#TestObjective, input#TestObjective").css("display","block");
			$("label#TestMileStoneText, input#TestMileStone").css("display","block");

		 }

	});
}


function VerifyQueryProcess()

{	
	
	
	$("#DepandencyCheckboxes").children().remove();
	$("#AutoSearchResult #searchedtext").each(function() {
		var UserText = $(this).find("td").text();
		UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		Env = Get_Selected_Env_Name()
		
		$.get("Verify_Query", {Query : UserText, Env: Env}, function(data) {
			
			if (data["DepandencyList"].length != 0 )
			{
					
				$(".flip[title='DepandencyCheckBox']").css('display','block');
				$("p#TestDataTypeCheckboxes").css('display','block');
				
					for (Depand in data["DepandencyList"]) 
					{
                        console.log(Depand);
						var content = ""
						
						DepandencyName = data["DepandencyList"][Depand][0]
                        console.log(data["DepandencyList"][Depand]);
                        console.log(DepandencyName);
						content += "<form id = '" + DepandencyName + "'action=''>"
						content += "<p style = 'margin:0'>" +DepandencyName+ "</p>"
						lis = data["DepandencyList"][Depand]

                        lis.shift();
						console.log(lis);
						for (items in lis) 
						{
								content += "<input class = 'ui-corner-all' type='radio' name =  '" +DepandencyName+ "'value = '"  + lis[items]  + "' />" + lis[items] + "<br>"
								
						}
						
						content += "</form>"
						content += "<p> </p>"
						$("#DepandencyCheckboxes").append(content )
						
					}
					
			}
			
		});
		
	});
	
	
	SendingQueryAndDepandency();
		
			
			
			
			/*
			if (data['Result'] == 'Error') {
				$(".Dependency").fadeIn(2000);
				
				$(".Dependency").text("Don't Forget To Add Dependency: " + data['Response'])
				//MsgBox("Test Case Selection Error", data['Response']);
				
			}

			else {
				$(".Dependency").fadeOut(2000)
				$(".Buttons[title='Select User']").fadeIn(2000)
				
				
				// css("display","block");

			}
			
			*/

		
		
		

	
}


function DeleteSearchQueryText()

{

	$("#AutoSearchResult td .delete").live('click', function() {
		
		if ($("#AutoSearchTextBoxLabel").text().trim() != "*Select Test Machine:") //If user is on select user page, do not allow him to delete the Test Data Set
		{
            console.log("clicked");
            console.log($(this).text());
			$(this).parent().next().remove();
			$(this).remove();
            PerformSearch();
            if($('#AutoSearchResult #searchedtext td').text()==""){
                $('#DepandencyCheckboxes').css('display','none');
                $('.flip[title="DepandencyCheckBox"]').css('display','none');
                $('#RunTestResultTable').css('display','none');
                $('#timeRequired').fadeOut(500);
                $('#timeRequired').html("");
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

	});
}


function SelectEmail()
{
	$("#EmailSearchBox").autocomplete({

		source : 'AutoCompleteEmailSearch',
		select : function(event, ui) {

			var value = ui.item.value
			$("#AutoSearchResult #SelectedEmail").append('<td><img class="delete" id = "DeleteEmail" title = "EmailDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
					+ '<td class="Text">'
					+ value
					+ ":&nbsp"
					+ '</td>');
			
			$("#SelectedEmail th").css('display', 'block');
			
			$("#EmailSearchBox").val("");
			return false
			
		}
	});
	
	$("#EmailSearchBox").keypress(function(event) {
		if (event.which == 13) {

			event.preventDefault();

		}
	});
	
	
	//Delete Seleted Email Ids
	$("#DeleteEmail").live('click', function() {
		
		$(this).parent().next().remove();
		$(this).remove();
		
	});
    $("#TesterSearchBox").autocomplete({

        source : 'AutoCompleteTesterSearch',
        select : function(event, ui) {

            var value = ui.item.value
            $("#AutoSearchResult #AssignedTester").append('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text">'
                + value
                + ":&nbsp"
                + '</td>');

            $("#AssignedTester th").css('display', 'block');

            $("#TesterSearchBox").val("");
            return false;

        }
    });
    $("#TesterSearchBox").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteTester").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
    $('#TestMileStone').autocomplete({
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
                $("#AutoSearchResult #AddedMileStone").html('<td><img class="delete" id = "DeleteMileStone" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text">'
                    + value
                    + ":&nbsp"
                    + '</td>');

                $("#MileStoneHeader th").css('display', 'block');

                $("#TestMileStone").val("");
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $("#TestMileStone").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteMileStone").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });

}


var EmailIds = '';
var DependencyText = '';
var TestObjective = '';
var TestMileStone='';
//var TestDataType = '';
var TesterIds='';
function RunTestProcess() {

	$("#AutoSearchResult #searchedtext").each( function()
	{
		
		//Getting Test Data Set text
		var RunTestQuery = $(this).find("td").text();
		RunTestQuery = RunTestQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        console.log(RunTestQuery);
		
		//Getting Selected Email ids
		$("#AutoSearchResult #SelectedEmail").each( function() 
		{
			var Email= $(this).find("td").text();
			EmailIds = Email.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
            console.log(EmailIds);
		});
		if(EmailIds.length==0){
            //alert("EmailIds is to be selected from suggestion");
            alertify.log("EmailIds is to be selected from suggestion","",0);
            return false;
        }
		//Getting Selected Dependency Text
		$("#AutoSearchResult #DependencyText").each( function() 
		{
			DependencyText= $(this).find("td").text();
			DependencyText = DependencyText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
            console.log(DependencyText);
		});
        //Getting the selected Tester
        $("#AutoSearchResult #AssignedTester").each( function()
        {
            var Tester= $(this).find("td").text();
            TesterIds = Tester.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
            console.log(TesterIds);
        });
        if(TesterIds.length==0){
            //alert("Testers is to be selected from suggestion");
            alertify.log("Testers is to be selected from suggestion","",0);
            return false;
        }
		//Getting Test Data Type Checkbox value
		TestDataType = $("#TestDataTypeCheckboxes input:checked").val()
		console.log(TestDataType);

        //Getting Test Objective text
        TestObjective =  $("input#TestObjective").val();
        TestObjective=TestObjective.trim();
        if(TestObjective==""){
            //alert("Test Objective is empty");
            alertify.log("Test Objective is empty","",0);
            return false;
        }
		//Getting the addedMileStone
        $("#AutoSearchResult #AddedMileStone").each( function()
        {
            var Tester= $(this).find("td").text();
            TestMileStone = Tester.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "");
            TestMileStone=TestMileStone.split(":")[0].trim();
            console.log(TestMileStone);
        });
        if(TestMileStone==""){
            //alert("MileStone is to be selected from suggestion");
            alertify.log("MileStone is to be selected from suggestion","",0);
            return false;
        }
        //TestMileStone=$('#TestMileStone').val();
        //TestMileStone=TestMileStone.trim();
		Env = Get_Selected_Env_Name()
		$.get("Run_Test", {RunTestQuery : RunTestQuery,TesterIds:TesterIds,EmailIds:EmailIds, DependencyText:DependencyText, TestObjective:TestObjective,TestMileStone:TestMileStone, Env: Env}, function(data)
		{
			
			//MsgBox("Test Run Response",	"Your Test Run Request Has Been Submitted, Here is the result :"+ data['Result']);
			// alert(data['Result']);
            if(data['Result']){
                run_notify("RunID-'"+data['runid']+"' got executed!");
                var location='/Home/RunID/'+data['runid'];
                window.location=location;
            }
            else{
                MsgBox("Test Run Response",	"Your Test Run Request Has Been Submitted, Here is the result :"+ data['Result']);
            }

		});
		
	});
						
		//});
}



function Get_Selected_Env_Name()

{
	
	var St = $(".text[title='Choose']").text()
	if ( St.indexOf("Mac") !== -1 )
		{ Env = "Mac"}
	else
	   { Env = "PC" }
	return Env
		
}

function machine_notify(message){
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
        var n = new Notification("Manual Test Machine Added!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Manual Test Machine Added!",{body:message, icon:"/site_media/noti.ico"});
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
function milestone_notify(title_msg,message,icon){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('ms_button');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification(title_msg,{body:message, icon:icon});
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
                var n = new Notification(title_msg,{body:message, icon:icon});
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
function run_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('run_test');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Run Executed!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Run Executed!",{body:message, icon:"/site_media/noti.ico"});
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