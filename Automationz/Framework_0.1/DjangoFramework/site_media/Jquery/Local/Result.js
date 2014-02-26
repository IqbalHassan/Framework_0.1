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

    $("#searchInput").keyup(function () {
        //split the current value of searchInput
        var data = this.value.split(" ");
        //create a jquery object of the rows
        var jo = $("#fbody").find("tr");
        if (this.value == "") {
            jo.show();
            return;
        }
        //hide all the rows
        jo.hide();

        //Recusively filter the jquery object to get results.
        jo.filter(function (i, v) {
            var $t = $(this);
            for (var d = 0; d < data.length; ++d) {
                if ($t.is(":contains('" + data[d] + "')")) {
                    return true;
                }
            }
            return false;
        })
            //show the rows that match.
            .show();
    }).focus(function () {
            this.value = "";
            $(this).css({
                "color": "black"
            });
            $(this).unbind('focus');
        }).css({
            "color": "#C0C0C0"
        });

    $(".textbox").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"GetSections",
                dataType:"json",
                data:{
                    section : ''
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value = ui.item[0];
            if(value!=""){
                $(".textbox").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "</a>" )
            .appendTo( ul );
    };


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