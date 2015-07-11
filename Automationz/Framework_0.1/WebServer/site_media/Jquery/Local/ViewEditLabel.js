/**
 * Created by minar09 on 3/20/15.
 */
var createpath="CreateNewLabel/";
var editpath="ViewEditLabel/";
var test_case_per_page=10;
var test_case_page_current=1;
var project_id = $.session.get('project_id');
var team_id = $.session.get('default_team_identity');
var user = $.session.get('fullname');
var new_label_text = "New label";
var operation = 0;

$(document).ready(function(){

	var URL=window.location.pathname;
    var create_index=URL.indexOf(createpath);
    var edit_index=URL.indexOf(editpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    
    $("#label_search_box").select2({
		placeholder: "Label Name...",
//		minimumInputLength: 3,
		width: 460,
		quietMillis: 250,
		ajax: {
			url: "LabelSearch/",
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
			return {id: new_label_text, text: new_label_text + ": " + term};
		},
		createSearchChoicePosition: "top",
		formatResult: formatLabels
	})
	// Listens for changes so that we can prompt the user if they want to edit or
	// copy existing test cases
	.on("change", function(e) {
//		console.log(JSON.stringify({val: e.val, added: e.added, removed: e.removed}));
		if (e.val === new_label_text) {
//			console.log("New test case is being created!");
		} else {
//			console.log("Existing test case has been selected.");
			var start = $(this).select2("data")["text"].indexOf(":") + 1;
    		var length = $(this).select2("data")["text"].length;
    		
    		var label_title = $(this).select2("data")["text"].substr(start, length - 1);
        
			var label_id = $(this).val();
			$("#title_prompt").html(
				'<p style="text-align: center">You have selected ' +
				'<span style="font-weight: bold;">' + label_id +': '+ label_title + '</span>' +
				'<br/> What do you want to do?' +
				'</p> &nbsp; &nbsp; &nbsp;' +
				'<div style="padding-left: 28%">' +
				'<a class="github" href="/Home/ViewEditLabel/'+label_id+'">Edit</a>' +
				'<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
				'</div>'
			);
          $("#title_prompt").modal();
          return false;
		}
	});
	
	// Should be used for formatting results, LATER
	function formatLabels(label_details) {
		var start = label_details.text.indexOf(":") + 1;
		//var start2 = label_details.text.indexOf("#");
		var length = label_details.text.length;
		       
		var label_title = label_details.text.substr(start, length - 1);
		//var label_color = label_details.text.substr(start2, length - 1);
		
		var markup =
			'<div>' +
			'<i class="fa fa-file-text fa-fw"></i> <span>' + label_details.id + '</span>' +
			': ' +
			'<span style="font-weight: bold;">' + label_title + '</span>' +
			'  ' +
			'<a class="label" style="background-color:' + label_details.code + '"></a>' +
			'</div>';
		
		return markup;
	}

	if(create_index != -1){
		operation = 1;
	}
    if(edit_index!=-1){
        var referred_label=URL.substring((URL.lastIndexOf(editpath)+(editpath).length),(URL.length-1));
        $("#header").html(referred_label);
        $("#ms_info").show();
        $("#rename").show();
        operation = 2;
        
        $.get("getLabelinfo/",{
	        'label_id':referred_label.trim(),
	        'project_id':project_id,
	        'team_id':team_id
	    },function(data){
	    	$("#label_name").val(data['details'][0][1]);
	    	$("#label_search_box").select2("data", {"id": data['details'][0][0], "text": data['details'][0][0] + ": " + data['details'][0][1]});
			$("#label_color").val(data['details'][0][2]);
			$("#created_by").text(data['details'][0][5]);
			$("#created_date").text(data['details'][0][7]);
			$("#modified_by").text(data['details'][0][6]);
			$("#modified_date").text(data['details'][0][8]);


			get_test_cases(referred_label,project_id,team_id,test_case_per_page,test_case_page_current);

			ResultTable(reqs_div,data['reqs_heading'],data['reqs'],'Requirements','Requirements');
			$('#reqs_div tr>td:first-child').each(function(){
		        $(this).css({
		            'color':'blue',
		            'cursor':'pointer'
		        });
		        $(this).click(function(){
		         var location='/Home/'+$.session.get('project_id')+'/EditRequirement/'+$(this).text().trim()+'/';
		         window.location=location;
		         });
	    	});	        

	    	ResultTable(tasks_div,data['tasks_heading'],data['tasks'],'Tasks','Tasks');
	    	$('#tasks_div tr>td:first-child').each(function(){
		        $(this).css({
		            'color':'blue',
		            'cursor':'pointer'
		        });
		        $(this).click(function(){
		            var location='/Home/'+$.session.get('project_id')+'/EditTask/'+$(this).text().trim()+'/';
		            window.location=location;
		        });
		    });

		    ResultTable(bugs_div,data['bugs_heading'],data['bugs'],'Bugs','Bugs');
		    $('#bugs_div tr>td:first-child').each(function(){
		        $(this).css({
		            'color':'blue',
		            'cursor':'pointer'
		        });
		        $(this).click(function(){
		         var location='/Home/EditBug/'+$(this).text().trim()+'/';
		         window.location=location;
		         });
		    });
	    });
    }


    $("#edit_button").click(function(){
	        
	        var color = $("#label_color").val();

	        if(operation==1){
	        	//alertify.error("sdflkjsl");
	        	var start = $("#label_search_box").select2("data")["text"].indexOf(":") + 1;
            	var length = $("#label_search_box").select2("data")["text"].length;            		
            	var title = $("#label_search_box").select2("data")["text"].substr(start, length - 1)

	        	if($("#label_search_box").select2("val") === "" || $("#label_search_box").select2("val") === []){
	        		alertify.set({ delay: 300000 });
	            	alertify.error("Label Name is needed!");
	        	}
	            $.get("CreateLabel/",{
	                name:title.trim(),
	                color:color.trim(),
	                project:project_id,
	                team:team_id,
	                user:$.session.get('fullname')
	            },function(data){
	            	if(data=="Label name already exists!"){
	            		alertify.set({ delay: 300000 });
	                	alertify.error(data);
	            	}
	            	else{
		            	alertify.set({ delay: 300000 });
		                alertify.success("Label Created!");
		                //window.location.reload(true);
		                window.location=('/Home/ViewEditLabel/'+data);
	            	}
	            });
	        }
	        else if(operation==2){
	        	var name = $("#label_name").val();
	        	if(name == ""){
	        		alertify.set({ delay: 300000 });
	            	alertify.error("Label Name is needed!");
	        	}
	            $.get("EditLabel/",{
	            	id:referred_label.trim(),
	                name:name.trim(),
	                color:color.trim(),
	                project:project_id,
	                team:team_id,
	                user:user
	            },function(data){
	            	if(data=="Label name already exists!"){
	            		alertify.set({ delay: 300000 });
	                	alertify.error(data);
	            	}
	            	else{
		            	alertify.set({ delay: 300000 });
		                alertify.success("Label Updated!");
		                //window.location.reload(true);
		                window.location=('/Home/ViewEditLabel/'+data);
	            	}
	            });
	        }	      
	    });

});

function get_test_cases(stepname,project_id,team_id,itemPerPage,PageCurrent){
    //$('#step_name').html("Test cases for step: "+ stepname);
    $.get("TestCases_PerLabel",{
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
function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table class="two-column-emphasis">';
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
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);
}