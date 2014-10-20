var stepCount=20;
$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    AutoComplete(project_id,team_id);
    PerformSearch(project_id,team_id);
    PaginationButton(project_id,team_id);
    DeleteFilterData(project_id,team_id);
    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val());
        window.location.reload(true);
    });
    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val());
        window.location.reload(true);
    });
});
function DeleteFilterData(project_id,team_id){
    $('#searchedFilter td .delete').live('click',function(){
        $(this).parent().remove();
        $(this).remove();
        PerformSearch(project_id,team_id);
    });
}
function AutoComplete(project_id,team_id){
    $('#inputText').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"GetResultAuto",
                dataType:"json",
                data:{
                    term:request.term,
                    project_id:project_id,
                    team_id:team_id
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if(value!=""){
                $('#searchedFilter').append('<td align="left"><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /><b>'+value+':<span style="display: none;">'+ui.item[1].trim()+'</span>&nbsp;</b></td>');
                //    '<td class="Text"></td>');
                $('#pagination_no').text(1);
                PerformSearch(project_id,team_id);
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
}
function PaginationButton(project_id,team_id){
    $('.previous_page').click(function(){
        var index=$("#pagination_no").text().trim();
        index=parseInt(index);
        if(index>=2){
            index--;
        }
        $('#pagination_no').text(index);
        PerformSearch(project_id,team_id);
    });
    $('.next_page').click(function(){
        var index=$('#pagination_no').text().trim();
        index=parseInt(index);
        var end=$('#end').text().trim();
        var total_entry=$('#total').text().trim();
        if (parseInt(end)<parseInt(total_entry)){
            index++;
        }
        $('#pagination_no').text(index);
        PerformSearch(project_id,team_id);
    });
}
function PerformSearch(project_id,team_id){
    var message=[];
    $('#searchedFilter td').each(function(){
        message.push($(this).find('b').text().trim());
    });
    var currentPagination=$('#pagination_no').text().trim();
    var UserText=message.join("|");
    $.get("GetFilteredDataResult",
        {
            UserText:UserText,
            pagination:currentPagination,
            project_id: project_id,
            team_id: team_id
        },
        function(data){
            if(data['total'].length>0){
                //make a table column
                var message="";
                message+='<table class="one-column-emphasis">';
                message+='<tr>';
                for(var i=0;i<data['column'].length;i++){
                    message+='<th align="left">'+data['column'][i]+'</th>';
                }
                message+='</tr>'
                for(var i=0;i<data['total'].length;i++){
                    message+='<tr>';
                    for(var j=0;j<data['total'][i].length;j++){
                        if(data['total'][i][j]=='status'){
                            message+=(drawStatusTable(data['status'][i]));
                        }
                        else{
                            message+='<td align="left">'+data['total'][i][j]+'</td>';
                        }

                    }
                    message+='</tr>';
                }
                message+='</table>';
                $('#allRun').html(message);
                make_clickable('#allRun');
                make_bar_clickable('#allRun');
                $('#total').html(data['totalGet']);
                $('#start').html((currentPagination-1)*stepCount+1);
                if(parseInt((currentPagination)*stepCount)>parseInt(data['totalGet'])){
                    $('#end').html(data['totalGet']);
                }
                else{
                    $('#end').html((currentPagination)*stepCount);
                }
                $('#pagination_div').css({'display':'block'});
                $('#UpperDiv').css({'display':'block'});
            }
            else{
                $('#allRun').html('<p>No Result is found for these filters</p>');
                $('#total').html(data['totalGet']);
                $('#start').html((currentPagination-1)*stepCount+1);
                if(parseInt((currentPagination)*stepCount)>parseInt(data['totalGet'])){
                    $('#end').html(data['totalGet']);
                }
                else{
                    $('#end').html((currentPagination)*stepCount);
                }
                $('#pagination_div').css({'display':'none'});
                $('#UpperDiv').css({'display':'none'});
            }
        });
}
function make_clickable(divname){
    $(divname+' tr>td:first-child').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer',
            'textAlign':'left'
        }) ;
        $(this).click(function(){
            var location='/Home/RunID/'+$(this).text().trim()+'/';
            window.location=location;
        });
    });
    $(divname+' tr>td:nth-child(2)').each(function(){
        $(this).css({
            'textAlign':'left'
        }) ;
    });
    $(divname+' tr>td:nth-child(3)').each(function(){
        $(this).css({
            'textAlign':'left'
        }) ;
    });
    $(divname+' tr>td:nth-child(6)').each(function(){
        $(this).css({
            'textAlign':'left'
        });
    });
    $(divname+' tr>td:nth-child(9)').each(function(){
        $(this).css({
            'textAlign':'left'
        }) ;
    });
}
function make_bar_clickable(divname){
    $(divname+' tr>td:nth-child(5)').each(function(){
        $(this).css({
            'cursor':'pointer'
        });
        $(this).live('click',function(){

            //$("#inner").append('<a id="show_chart" class="button primary">Show Graph</a>');

            var RunID=$(this).closest('tr').find('td:first-child').text().trim();
            $.get("chartDraw",
                {
                    runid:RunID
                },
                function(data){
                    console.log(data);
                    /***************pie chart***********************/
                    google.load("visualization", "1", {packages:["corechart"], callback:drawChart});

                    function drawChart() {
                        var piedata = google.visualization.arrayToDataTable([
                            ['Run Status', 'Total Case Number'],
                            ['Passed ('+data[1]+')',     data[1]],
                            ['Failed ('+data[2]+')',      data[2]],
                            ['Blocked ('+data[3]+')',  data[3]],
                            ['In-Progress ('+data[4]+')', data[4]],
                            ['Submitted ('+data[5]+')',  data[5]],
                            ['Skipped ('+data[6]+')', data[6]]
                        ]);
                        var options = {
                            title:'Run-ID: '+RunID,
                            // width: 500,
                            height: 500,
                            fontSize: 13,
                            titleTextStyle:{fontSize:19, color: '#4183c4', fontName:'Helvetica Neue, Helvetica, Arial, sans-serif'},
                            legend:{ textStyle: {fontSize: 17}},
                            colors:['#65bd10','#FD0006','#FF9e00','blue','grey','#88a388']
                        };
                        var chart = new google.visualization.PieChart(document.getElementById('chart'));
                        chart.draw(piedata, options);
                        $("#inner").dialog({
                            buttons : {
                                "OK" : function() {
                                    $(this).dialog("close");
                                }
                            },

                            show : {
                                effect : 'drop',
                                direction : "up"
                            },

                            modal : true,
                            width : 700,
                            height : 650,
                            align:'center',
                            title:"Summary"

                        });
                    }
                });
        });


    });
}

function drawStatusTable(status){
    var message="";
    message+='<td style="text-align: left;">';
    message+='<div>';
    message+='<div class="repository-lang-stats-graph js-toggle-lang-stats" aria-label="Show language statistics" style="background-color:#ccc" original-title="">';
    message+='<span class="language-color" style="width:'+status[0]+';';
    message+='background-color: #65bd10;';
    message+='background-image: -moz-linear-gradient(#8dcf16, #65bd10);';
    message+='background-image: -webkit-linear-gradient(#8dcf16, #65bd10);';
    message+='background-image: linear-gradient(#8dcf16, #65bd10);';
    message+='float:left" itemprop="keywords">PASS</span>';
    message+='  <span class="language-color" style="width:'+status[1]+'; background-color:#FD0006;';
    message+=' background-image: -moz-linear-gradient(#FE4044, #FD0006);';
    message+='background-image: -webkit-linear-gradient(#FE4044, #FD0006);';
    message+='background-image: linear-gradient(#FE4044, #FD0006);';
    message+='float:left" itemprop="keywords">JavaScript</span>';
    message+='   <span class="language-color" style="width:'+status[2]+'; background-color:#FF9e00;';
    message+='background-image: -moz-linear-gradient(#ffb640, #FF9e00);';
    message+='background-image: -webkit-linear-gradient(#ffb640, #FF9e00);';
    message+='background-image: linear-gradient(#ffb640, #FF9e00);';
    message+='float:left" itemprop="keywords">CSS</span>';
    message+='  <span class="language-color" style="width:'+status[3]+'; background-color:blue;';
    message+='background-image: -moz-linear-gradient(#7373ff, #0000ff);';
    message+='background-image: -webkit-linear-gradient(#7373ff, #0000ff);';
    message+='background-image: linear-gradient(#7373ff, #0000ff);';
    message+='float:left" itemprop="keywords">Other</span>';
    message+='   <span class="language-color" style="width:'+status[4]+'; background-color:grey;';
    message+='background-image: -moz-linear-gradient(#B0B0B0, #606060);';
    message+='background-image: -webkit-linear-gradient(#B0B0B0, #606060);';
    message+='background-image: linear-gradient(#B0B0B0, #606060);';
    message+='float:left" itemprop="keywords">defgd</span>';
    message+='  <span class="language-color" style="width:'+status[5]+'; background-color:#88a388;';
    message+='background-image: -moz-linear-gradient(#b7d1b7, #88a388);';
    message+='background-image: -webkit-linear-gradient(#b7d1b7, #88a388);';
    message+='background-image: linear-gradient(#b7d1b7, #88a388);';
    message+='float:left" itemprop="keywords">defgd</span>';
    message+='</div>';
    message+='</div>';
    message+='</td>';
    return message;
}