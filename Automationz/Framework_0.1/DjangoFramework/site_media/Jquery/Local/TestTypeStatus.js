
$(document).ready(function(){

    //Sections
    $.ajax({
        url:'GetSections/',
        dataType : "json",
        data : {
            section : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".section[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    $(".section").click(function(event)
    {
        var choice = $(".section").val();
        if(choice != 0)
        {
            $.get("TestTypeStatus_Report",{choice : choice},function(data)
            {
                ResultTable(TestTypeStatusTable,data['Heading'],data['TableData'],"Test Type Status Report");

                /***************pie chart***********************/
                 google.load("visualization", "1", {packages:["corechart"], callback:drawChart});

                 function drawChart() {
                    /*var jsonData = $.ajax({
                        url: "TestTypeStatus_Report",
                        dataType:"json",
                        async: false
                    }).responseText;*/

                var piedata = google.visualization.arrayToDataTable([
                    ['Test Type', 'Total Case Number'],
                    ['Manual',     data['Summary'][2]],
                    ['Manual in-progress',      data['Summary'][3]],
                    ['Automated',  data['Summary'][4]],
                    ['Automated in-progress', data['Summary'][5]]
                ]);

                var options = {
                    title: 'Summary - ' + choice,
                    //width: 500,
                    height: 400,
                    fontSize: 13,
                    titleTextStyle:{fontSize:17}
                };

                //var data = google.visualization.arrayToDataTable(jsonData);

                var chart = new google.visualization.PieChart(document.getElementById('TestTypeStatusChart'));
                chart.draw(piedata, options);
            }

                /***************pie chart*********************/


                $("p.flip[title =  'Test Type Status']").text("Test type status report of (" +choice + ")" )
                $("p.flip[title =  'Test Type Status']").fadeIn(1000);
                AnalysisTableActions();


                $("#TestTypeStatusTable").css({
                    'text-align':'center',
                    'cursor' : 'pointer',
                    'border' : '1px solid grey'
                });

                $("#TestTypeStatusTable .ui-widget th").css({
                    'cursor':'pointer',
                    'background' : 'black',
                    'color' : 'white'
                });

                $("#TestTypeStatusTable .ui-widget tr td:first-child").each(function(){

                   /* $(this).live('click',function(){

                        $("#TestTypeStatusTable").slideToggle("slow");

                    });*/
                    $(this).css({
                        'color':'black',
                        'font-weight' : 'bold',
                        'font-size':'120%',
                        'cursor':'pointer',
                        'border' : '0px',
                        'border-collapse' : 'collapse',
                        'border-spacing': '0'
                    });
                });
                $("#TestTypeStatusTable .ui-widget tr td:nth-child(2)").css({
                    'font-weight' : 'bold'
                });
                $("#TestTypeStatusTable .ui-widget tr:nth-child(5n+1) td").css({
                    'color':'black',
                    'cursor':'pointer',
                    'font-weight' : 'bold',
                    'border' : '1px solid grey',
                    'background' : '#CCFFCC',
                    'font-size':'110%'
                });

                $("#TestTypeStatusTable tr:nth-child(5n-2) td:first-child").each(function(){
                    var t = $(this);
                    //var n = t.next();
                    t.html(t.html()+ " ");
                });
                $("#TestTypeStatusTable tr:nth-child(5n-2) td:nth-child(1)").each(function(){
                    $(this).html("");
                    $(this).css({
                        bgColor : 'black'
                    });
                });

                $("#TestTypeStatusTable tr:nth-child(5n-3) td:nth-child(1)").each(function(){
                    $(this).html("");
                });

                $("#TestTypeStatusTable tr:nth-child(5n+1) td:first-child").each(function(){
                    var t = $(this);
                    var n = t.next();
                    t.html(" "+ n.html() + "       ");
                    $(this).css({
                        'text-indent' : '5cm'
                    });
                });
                $("#TestTypeStatusTable tr:nth-child(5n+1) td:nth-child(2)").each(function(){
                    $(this).html("");
                });

                $("#TestTypeStatusTable tr:last-child td:first-child").each(function(){
                    $(this).html("Grand Total   ");
                    $(this).css({
                        'color' : 'red',
                        'font-weight' : 'bold'
                    });
                });

                $("#TestTypeStatusTable tr:last-child td").css({
                    'color' : 'red',
                    'font-size':'140%'
                });
                $("#TestTypeStatusTable tr:nth-child(5n-3) td").css({
                    'background' : '#CCFFFF'
                });

                $("#TestTypeStatusTable tr:nth-child(5n-1) td").css({
                    'background' : '#CCFFFF'
                });
                $("#TestTypeStatusTable tr:nth-child(5n-3) td:first-child").css({
                    'background' : 'white'
                });
                $("#TestTypeStatusTable tr:nth-child(5n-1) td:first-child").css({
                    'background' : 'white'
                });
                $("#TestTypeStatusTable tr td:last-child").css({
                    'font-weight':'bold',
                    'font-size':'120%'
                });
                $("#TestTypeStatusTable tr:nth-child(5n+1) td:last-child").css({
                    'color' : 'red',
                    'font-size':'140%'
                });
                $("#TestTypeStatusTable tr:last-child td:last-child").css({
                    'font-size':'160%'
                });
                $('#TestTypeStatusTable table').each(function () {

                    var dimension_cells = new Array();
                    var dimension_col = null;

                    var i = 1;
                    // First, scan first row of headers for the "Dimensions" column.
                    $(this).find('th').each(function () {
                        if ($(this).text() == 'Section') {
                            dimension_col = i;
                        }
                        i++;
                    });

                    // first_instance holds the first instance of identical td
                    var first_instance = null;
                    // iterate through rows
                    $(this).find('tr').each(function () {

                        // find the td of the correct column (determined by the dimension_col set above)
                        var dimension_td = $(this).find('td:nth-child('+ dimension_col + ')');

                        if (first_instance == null) {
                            // must be the first row
                            first_instance = dimension_td;
                        } else if (dimension_td.text() == first_instance.text()) {
                            // the current td is identical to the previous
                            // remove the current td
                            dimension_td.html("");
                            // increment the rowspan attribute of the first instance
                            first_instance.attr('rowspan', first_instance.attr('rowspan') + 1);
                        } else {
                            // this cell is different from the last
                            first_instance = dimension_td;
                        }

                    });
                });
            });
        }

    });
});


function AnalysisTableActions()
{

    $("p.flip[title =  'Test Type Status']").click(function() {

        $("#TestTypeStatusTable").slideToggle("slow");
    });

}

