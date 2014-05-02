/**
 * Created by minar09 on 2/4/14.
 */


$(document).ready(function(){

    $('.combo-box').combobox();
    $.ajax({
        url:'GetVersions/',
        dataType : "json",
        data : {
            version : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 0; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                //if(i == 0)return;
                $(".version[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    /*$(".platform").click(function(event)
    {
        $(".version").selectedOptions("0");
    });*/
    $(".generate").click(function(event)
    {
        $('#BundleReportTable').empty();
        var platform = $(".platform").val();
        var version = $(".version").val();
        if(version != 0)
        {
            $.get("BundleReport_Table_Latest",{Platform : platform, Product_Version : version},function(data)
            {
                //ResultTable(BundleReportTable,data['Heading'], data['Env'],"Bundle Report");
                for(var i=0;i<data['Env'].length;i++)
                {
                    $("#BundleReportTable").append(''+
                        '<br/>' +
                        '<hr/>' +
                        '<h4 class="Text" style="text-align: center;font-weight: normal; line-height: 1.1;font-size: 25px;">'+data['Env'][i][0]+' Bit  +  '+data['Env'][i][1]+'</h4>' +
                    '<div id="env'+i+'"></div>' +
                        '<div id="chart'+i+'"></div>');
                    ResultTable("#env"+i+"", data['Heading'],data['ReportTable'][i],"");
                    /*$.get("Single_Env",{Platform : platform, Product_Version : version,OS : data['Env'][i][0], Client : data['Env'][i][1]},function(env_data)
                    {
                        ResultTable("#env"+i+"", env_data['Heading'],"");
                    });*/
                    /***************pie chart***********************/
                    RenderPieChart('chart'+i, [
                        ['Passed ('+data['ReportTable'][i][4][1]+')', data['ReportTable'][i][4][1]],
                        ['Failed ('+data['ReportTable'][i][4][2]+')', data['ReportTable'][i][4][2]],
                        ['Blocked ('+data['ReportTable'][i][4][3]+')',  data['ReportTable'][i][4][3]],
                        ['Submitted ('+data['ReportTable'][i][4][4]+')', data['ReportTable'][i][4][4]],
                        ['In-Progress ('+data['ReportTable'][i][4][5]+')',  data['ReportTable'][i][4][5]],
                        ['Skipped ('+data['ReportTable'][i][4][6]+')', data['ReportTable'][i][4][6]]
                    ],data['Env'][i][0]+' Bit  +  '+data['Env'][i][1]);

                    /***************pie chart*********************/
                }

            });
        }
        //event.stopPropagation();
    });

});

function RenderPieChart(elementId, dataList, title) {
    Highcharts.setOptions({
        colors: ['green', 'red', 'orange', 'grey', 'blue', '#D7D7D7']
    });
    new Highcharts.Chart({
        chart: {
            renderTo: elementId,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        }, title: {
            text: 'Summary - ' + title
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    formatter: function () {
                        return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Bundle Report',
            data: dataList
        }]
    });
};

