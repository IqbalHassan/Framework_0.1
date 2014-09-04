/**
 * Created by J on 9/1/14.
 */
$(document).ready(function(){

    ActivateNecessaryButton();
    ButtonSet();

    $("#submit").click(function(){

        var project = $("#project_name").val();
        var bug_desc=$("#bug_desc").val();
        var start_date=$('#start_date').val();
        var end_date=$('#end_date').val();
        var team=$("#team_name").val();
        var priority= 'P' + $('#priority').val();
        var milestone=$('#milestone').text();
        var title=$('#title').val();
        var creator = $("#created_by").val();
        var testers=[];
        $('.selected').each(function(){
            testers.push($(this).text().trim());
        });
        var status = $('#status').val();


        if(title!=""){
            $.get("LogNewBug/",{
                'title':title.trim(),
                'description':bug_desc.trim(),
                'status':status.trim(),
                'start_date':start_date.trim(),
                'end_date':end_date.trim(),
                'team':team.trim(),
                'tester':testers.join("|").trim(),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': project.trim(),
                'user_name':$('#user_name').text().trim(),
                'created_by':creator.trim()
            },function(data){
                window.location='/Home/CreateBug/';
            });
        }
        else{
            alertify.error("Fields are empty!", 5500);
        }
    });
});


function ButtonSet(){

    $("#assigned_tester").autocomplete({

        source : 'AutoCompleteTesterSearch',
        select : function(event, ui) {

            var value = ui.item.value
            $("#tester").append('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text selected">'
                + value
                + "&nbsp"
                + '</td>');

            //$("#tester th").css('display', 'block');

            $("#assigned_tester").val("");
            return false;

        }
    });
    $("#assigned_tester").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteTester").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
    $('#milestone_list').autocomplete({
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
                $("#milestone").html('<td><img class="delete" id = "DeleteMileStone" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text">'
                    + value
                    + "&nbsp"
                    + '</td>');

                //$("#MileStoneHeader th").css('display', 'block');

                $("#milestone_list").val("");
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $("#milestone_list").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteMileStone").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
}
function ActivateNecessaryButton(){
    $('#start_date').datepicker({ dateFormat: "dd-mm-yy" });
    $('#start_date').datepicker("option", "showAnim", "slide" );
    $('#end_date').datepicker({ dateFormat: "dd-mm-yy" });
    $('#end_date').datepicker("option", "showAnim", "slide" );
    $(".selectdrop").selectBoxIt();
}
