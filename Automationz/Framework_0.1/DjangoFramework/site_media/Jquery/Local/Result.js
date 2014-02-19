$(document).ready(function(){
    make_clickable('#allRun');
    make_clickable('#completeRun');
    make_clickable('#cancelledRun');
    make_clickable('#progressRun');
    make_clickable('#submittedRun');
    make_bar_clickable('#allRun');
    make_bar_clickable('#completeRun');
    make_bar_clickable('#cancelledRun');
    make_bar_clickable('#progressRun');
    make_bar_clickable('#submittedRun');
});
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
                            ['Passed',     data[1]],
                            ['Failed',      data[2]],
                            ['Blocked',  data[3]],
                            ['In-Progress', data[4]],
                            ['Submitted',  data[5]],
                            ['Skipped', data[6]]
                        ]);
                        var options = {
                            title:'Run-ID: '+RunID,
                            width: 500,
                            height: 500,
                            fontSize: 13,
                            titleTextStyle:{fontSize:16},
                            legend:{ textStyle: {fontSize: 17}},
                            colors:['#65bd10','#FD0006','#FF9e00','blue','#FFFC00','#88a388']
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
                            width : 620,
                            height : 620,
                            align:'center',
                            title:"Summary"

                        });
                    }
                });

        });

    });
}