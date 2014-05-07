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
                    var sc = data['ReportTable'][i].length -1;
                    RenderPieChart('chart'+i, [
                        ['Passed ('+data['ReportTable'][i][sc][1]+')', data['ReportTable'][i][sc][1]],
                        ['Failed ('+data['ReportTable'][i][sc][2]+')', data['ReportTable'][i][sc][2]],
                        ['Blocked ('+data['ReportTable'][i][sc][3]+')',  data['ReportTable'][i][sc][3]],
                        ['Submitted ('+data['ReportTable'][i][sc][4]+')', data['ReportTable'][i][sc][4]],
                        ['In-Progress ('+data['ReportTable'][i][sc][5]+')',  data['ReportTable'][i][sc][5]],
                        ['Skipped ('+data['ReportTable'][i][sc][6]+')', data['ReportTable'][i][sc][6]],
                        ['Not Run ('+data['ReportTable'][i][sc][7]+')', data['ReportTable'][i][sc][7]]

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
        colors: ['green', 'red', 'orange', 'grey', 'blue', '#D7D7D7','black']
    });
    new Highcharts.Chart({
        chart: {
            renderTo: elementId,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            height: 450
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
                    formatter: function () {
                        return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
                    }
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

