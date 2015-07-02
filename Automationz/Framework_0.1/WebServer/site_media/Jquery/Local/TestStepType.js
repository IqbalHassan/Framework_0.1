
$(document).ready(function(){

    //Sections

    $('.combo-box').combobox();
    $.ajax({
        url:'GetSections/',
        dataType : "json",
        data : {
            section : '',
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')
        },
        success: function( json ) {
            if(json.length > 0)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".section[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    $(".generate").click(function(event)
    {
        var choice = $(".section").val();
        if(choice != 0)
        {
            /*$("#space").append('' +
                '<br/>' +
                '<hr/>' );*/

            $.get("TestStepTypeStatus",{choice : choice, project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')},function(data)
            {
                ResultTable(TestTypeStatusTable,data['Heading'],data['TableData'],"Test Type Status Report");


                /***************pie chart***********************/

                RenderPieChart('TestTypeStatusChart', [
                    ['Automated ('+data['Summary'][1]+')', data['Summary'][1]],
                    ['Easily Automatable ('+data['Summary'][2]+')', data['Summary'][2]],
                    ['Hard to Automate ('+data['Summary'][3]+')',  data['Summary'][3]],
                    ['Not Automatable ('+data['Summary'][4]+')', data['Summary'][4]],
                    ['Undefined ('+data['Summary'][5]+')',  data['Summary'][5]],
                    ['Performance ('+data['Summary'][6]+')', data['Summary'][6]]
                ],choice);

               
                $('#TestTypeStatusTable tr>td:nth-child(n+2)').each(function(){
                    if($(this).text() != '0') {
                        $(this).css({
                        'cursor':'pointer'
                        });
                        $(this).hover(function(){$(this).css("text-decoration","underline");},function(){$(this).css("text-decoration","none");});
                        var row = $(this).closest('tr').index();
                        var col = $(this).index();
                        var pos = col + 1;
                        var section = $(this).siblings(':first-child').text();
                        var status = $(this).parent().siblings().first().children(':nth-child('+pos+')').text();
                        $(this).live('click',function(){

                            $("#inner").show();
                            $("#tc_title").html('Test Cases List : ' + section + ' - ' + status )
                            //ResultTable(tc_table,data['Short'],data['Cases'][row-1][col],"Test Cases", "Click on TC-IDs to see run history");
                            //$("#tc_table tbody").addClass("paginate");
                            tctable('#tc_table',data['Short'],data['Cases'][row-1][col],"Test Cases", "Click on TC-IDs to see steps");
                            pagination();
                            $('#tc_table tr>td:first-child').each(function () {
                                $(this).css({
                                    'color': 'blue',
                                    'cursor': 'pointer',
                                    'textAlign': 'left'
                                });
                                
                            });
                            

                        }); 
                    }
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
        else{
            alertify.set({delay:300000})
            alertify.error("You need to select an option!")
        }
        //$("#TestTypeStatusChart").selectmenu('refresh', true);
        //$("#TestTypeStatusTable").selectmenu('refresh', true);

    });
});

function tctable(divname,heading,data,ResultName,tooltip){
    if(data.length>0) {
            //make a table column
        var message = "";
        message += "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + data.length + " " + ResultName
                + "</p>"
        message += '<table class="two-column-emphasis">';
        message += '<tr>';
        for (var i = 0; i < heading.length; i++) {
            message += '<th align="left">' + heading[i] + '</th>';
        }
        message += '</tr><tbody class="paginate">';
        for (var i = 0; i < data.length; i++) {
            message += '<tr>';
            for (var j = 0; j < data[i].length; j++) {
                message += '<td align="left">' + data[i][j] + '</td>';
            }
            message += '</tr>';
        }
        message += '</tbody></table>';
        $(divname).html(message);
    }
    else{
        $(divname).empty();
    }
}

function AnalysisTableActions()
{
    $("p.flip[title =  'Test Type Status']").click(function() {

        $("#TestTypeStatusTable").slideToggle("slow");
    });
}

function RenderPieChart(elementId, dataList, title) {
    Highcharts.setOptions({
        colors: ['green', '#309959', '#124992', 'red', '#8109AF', 'orange']
    });
    new Highcharts.Chart({
        chart: {
            renderTo: elementId,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            height: 500
        }, title: {
            text: 'Summary - ' + title
        },
        tooltip: {
            /*formatter: function () {
             return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
             }*/
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    /*formatter: function () {
                        return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
                    }*/
                }
                /*dataLabels: {
                 enabled: false
                 }*/,
                showInLegend: true,
                size : '95%'
            }
        },
        series: [{
            type: 'pie',
            name: 'Bundle Report',
            data: dataList
        }]
    });
}

function make_number_clickable(divname,Cases){
    $(divname+' tr>td:nth-child(n+2)').each(function(){
        if($(this).text() != '0') {
            $(this).css({
            'cursor':'pointer'
            });
            var row = $(this).closest('tr').index();
            var col = $(this).index();
            $(this).live('click',function(){

                $("#inner").show();
                ResultTable(tc_table,'',Cases[row][col],"Test Cases List");

            }); 
        }
    });
}
