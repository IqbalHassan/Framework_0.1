$(document).ready(function(){


		
	MKSReportAutomCompleteEmailSearch();
	MKSReportFolderSearchBox();
	MKSReport_Query_Submit();

});


function MKSReportAutomCompleteEmailSearch()

{
	
	$("#Email_Search_Box").autocomplete(
			{
				source : 'AutoCompleteEmailSearch',
				select : function(event, ui) 
				{

					var value = ui.item.value
					
					$("#MKSReportTable2 #MKSReportQuery").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
							+ '<td >'
							+ value
							+ ":&nbsp"
							+ '</td>');
					
					$("#MKSReportTable2 td .delete").live('click', function() {
						
						
							$(this).c
							$(this).remove();
							
					});
						
						
					
					$("#Email_Search_Box").val("");
							return false
				},

		});

	$("#Email_Search_Box").keypress(function(event) {
		if (event.which == 13) 
		{

			event.preventDefault();
			
		}

	});

}

function MKSReportFolderSearchBox()

{
	
	/*	
	$("#FolderName").keypress(function(event){
		
		var keycode = (event.keyCode ? event.keyCode : event.which);
		if ( (keycode == '13') &&  $("#FolderName").val()!="" )   
			
			{
			
			//$("#MKSReportTable2 #MKSReportQuery").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
				//	+ '<td >'
				//	+ $("#FolderName").val()
				//	+ ":&nbsp"
				//	+ '</td>');
			
		//	$("#FolderName").val("");
			
			}
		
		$("#MKSReportTable2 td .delete").live('click', function() {
			
			
			$(this).parent().next().remove();
			$(this).remove();
			
		});
			
		
	});
	
		
 */
}


function MKSReport_Query_Submit()

{
	$(".Buttons[title='Submit MKS Query']").on('click',function(){
		
		
		if ( $("#FolderName").val() == "" )
			{
				alert("Please Type Folder");
			}
		else
			{
				$("#MKSReportTable2 #MKSReportQuery").each(function() {
					var UserText = $(this).find("td").text();
					UserEmails = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
					Folder = $("#FolderName").val();
					
					$("#TotalTimeRow").css('display', 'none');
					$("#TotalTimeTaken").children('p').remove();
					$("#Wait").css('display', 'block');
					$("#MKSReportTable").css('display', 'none');
					
					$.get("MKS_Report_Table", {UserEmails : UserEmails, Folder: Folder}, function(data) {
						
						$("#MKSReportTable").css('display', 'block');
						
						
						ResultTable('#MKSReportTable',data['Headings'],data['Result'],"Test Result");
						
						$("#Wait").css('display', 'none');
						
						$("#TotalTimeRow").css('display', 'block');
						$("#TotalTimeTaken").append("<p>" + data['TotalTime'] + "</p>");
						
					});
					
				});
			}
		
	});
	
	
		
}