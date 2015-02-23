/**
 * Created by J on 2/2/2015.
 */

var itemPerPage=10;
var PageCurrent=1;
var project_id = $.session.get('project_id');
var team_id = $.session.get('default_team_identity');

$(document).ready(function(){
	$("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    //itemPerPage = $("#perpageitem").val();
    get_steps(project_id, team_id);
    
    /*$('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            itemPerPage=$(this).val();
            current_page=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            get_steps(itemPerPage, PageCurrent);
        }
    });*/

});


function get_steps(project_id,team_id){
    $.get("Steps_List",{'project_id':project_id ,'team_id':team_id},function(data)
    {
        if(data['steps'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr><tbody class="paginate">';
            for (var i = 0; i < data['steps'].length; i++) {
                message += '<tr>';
                for (var j = 0; j < data['steps'][i].length; j++) {
                    message += '<td align="left">' + data['steps'][i][j] + '</td>';
                }
                message += '</tr>';
            }
            message += '</tbody></table>';
            $('#allsteps').html(message);
            $('#main').simplePagination({
                items_per_page: 10,
                number_of_visible_page_numbers: 5
            });
            $("#allsteps tr>td:first-child").each(function(){
                $(this).css({
                        'color': 'blue',
                        'cursor': 'pointer',
                        'textAlign': 'left'
                    });
                $(this).click(function(){
                    step = $(this).text().trim();
                    window.location = '/Home/ManageTestCases/EditStep/' + step ;
                });
            });
            $('#allsteps tr>td:last-child').each(function () {
                if($(this).text() != '0') {
                    $(this).css({
                        'color': 'blue',
                        'cursor': 'pointer',
                        'textAlign': 'left'
                    });
                    $(this).hover(function(){$(this).css("text-decoration","underline");},function(){$(this).css("text-decoration","none");});
                    $(this).click(function(){
                        var step_name = $(this).closest('tr').find('td:first-child').text().trim();
                        itemPerPage = $("#perpageitem").val();
                        get_cases(step_name,itemPerPage, PageCurrent);
                        $('#perpageitem').on('change',function(){
                            if($(this).val()!=''){
                                itemPerPage=$(this).val();
                                current_page=1;
                                $('#pagination_tab').pagination('destroy');
                                window.location.hash = "#1";
                                get_cases(step_name,itemPerPage, PageCurrent);
                            }
                        });
                        //var location='/Home/RunHistory/'+data+'/';
                        //window.location=location;
                        /*$("#inner").show();
                        $("#tc_title").html('Test Cases List of Containing test step - ' + step_name );
                        $.get("TestCase_Results",{Query: step_name},function(data) {

                            ResultTable(tc_table,data['Heading'],data['TableData'],"Test Cases");
                            var indx = 0;
                            $('#tc_table tr>td:nth-child(3)').each(function(){
                                var ID = $("#tc_table tr>td:nth-child(1):eq("+indx+")").text().trim();

                                $(this).after('<i class="fa fa-copy fa-2x templateBtn" id="'+ID+'" style="cursor:pointer"></i>');
                                $(this).after('<i class="fa fa-pencil fa-2x editBtn" id="'+ID+'" style="cursor:pointer"></i>');

                                indx++;
                            });

                            $(".editBtn").click(function (){
                                window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                            });
                            $(".templateBtn").click(function (){
                                window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
                            });
                            //VerifyQueryProcess();
                            //$(".Buttons[title='Verify Query']").fadeIn(2000);
                            //$(".Buttons[title='Select User']").fadeOut();
                        
                        });*/
                    });
                }
                
            });
            /*$('#pagination_tab').pagination({
                items:data['count'],
                itemsOnPage:itemPerPage,
                cssStyle: 'dark-theme',
                currentPage:PageCurrent,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    //PerformSearch(project_id,team_id,user_text,itemPerPage,PageNumber);
                    get_steps(itemPerPage,PageNumber);
                }
            });*/


        }
        else{
            $("#allsteps").html('<h2>No Steps Available</h2>')
        }

        //$('#allsteps').html(message);
        
    });
}


function get_cases(UserText,itemPerPage,PageCurrent){
    $.get("TestCase_Results",{Query: UserText,itemPerPage:itemPerPage,PageCurrent:PageCurrent},function(data) {

            if (data['TableData'].length == 0)
            {
                alertify.log("Sorry There is No Test Cases For Selected Query!","",0);
                $('#search_result').children().remove();
                $('#search_result').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                //$("#DepandencyCheckboxes").children().remove();
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                $("#inner").show();
                $("#tc_title").html('Test Cases List of Containing test step - ' + UserText );
                ResultTable(tc_table,data['Heading'],data['TableData'],"Test Cases");

                $('#pagination_tab').pagination({
                    items:data['count'],
                    itemsOnPage:itemPerPage,
                    cssStyle: 'dark-theme',
                    currentPage:PageCurrent,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        //PerformSearch(project_id,team_id,user_text,itemPerPage,PageNumber);
                        get_cases(UserText,itemPerPage,PageNumber);
                    }
                });

                /*$("#tc_table tr>td:first-child").each(function(){
                    $(this).css({
                            'color': 'blue',
                            'cursor': 'pointer',
                            'textAlign': 'left'
                        });
                    $(this).click(function(){
                        tc_id = $(this).text().trim();
                        window.location = '/Home/ManageTestCases/Edit/' + tc_id ;
                    });
                });*/
                //$("#tc_table").fadeIn(1000);
                //$("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#tc_table");
                var indx = 0;
                $('#tc_table tr>td:nth-child(7)').each(function(){
                    var ID = $("#tc_table tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<i class="fa fa-copy fa-2x templateBtn" id="'+ID+'" style="cursor:pointer"></i>');
                    $(this).after('<i class="fa fa-pencil fa-2x editBtn" id="'+ID+'" style="cursor:pointer"></i>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
                });
            }

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