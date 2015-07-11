/**
 * Created by J on 9/11/14.
 */
var label_per_page=5;
var label_page_current=1;
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');
$(document).ready(function(){

    $("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    /*$.get("GetMileStones",{project_id : project_id, team_id:team_id},function(data)
    {
        if(data['TableData'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr>';
            for (var i = 0; i < data['TableData'].length; i++) {
                //msid.push(data['TableData'][i][0]);
                message += '<tr>';
                for (var j = 0; j < data['TableData'][i].length; j++) {
                    message += '<td align="left">' + data['TableData'][i][j] + '</td>';
                }
                message += '</tr>';
            }
            message += '</table>';
            $('#allMilestones').html(message);
            make_clickable('#allMilestones');

        }
        else{
            $("#allMilestones").html('<h2>No Data Available</h2>')
        }

    });*/


    get_labels(project_id,team_id,label_per_page,label_page_current);

    label_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            label_per_page=$(this).val();
            label_page_current=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            get_labels(project_id,team_id,label_per_page,label_page_current);
        }
    });


});


function make_clickable(divname) {
    $(divname + ' tr>td:first-child').each(function () {
        $(this).css({
            'color': 'blue',
            'cursor': 'pointer',
            'textAlign': 'left'
        });
        $(this).click(function(){
            $.get("GetMileStoneID",{term : $(this).text().trim(),project_id:project_id, team_id:team_id},function(data)
            {
                var location='/Home/EditMilestone/'+data+'/';
                window.location=location;
            });
        });
    });
}

function get_labels(project_id,team_id,label_per_page,label_page_current){
    $.get("Show_Milestones",{'project_id':project_id ,'team_id':team_id,'label_per_page':label_per_page,'label_page_current':label_page_current},function(data){
        form_table("AllMSTable",data['Heading'],data['TableData'],data['Count'],"Milestones");
        
        $('#pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:label_per_page,
            cssStyle: 'dark-theme',
            currentPage:label_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_labels(project_id,team_id,label_per_page,PageNumber);
            }
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
    make_clickable('#'+divname);
}