/**
 * Created by minar09 on 2/4/14.
 */


$(document).ready(function(){

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
    $(".version").click(function(event)
    {
        $('#BundleReportTable').empty();
        var platform = $(".platform").val();
        var version = $(".version").val();
        if(version != 0)
        {
            $.get("BundleReport_Table",{Platform : platform, Product_Version : version},function(data)
            {
                //ResultTable(BundleReportTable,data['Heading'], data['Env'],"Bundle Report");
                for(var i=0;i<data['Env'].length;i++)
                {
                    $("#BundleReportTable").append(
                        '<a>'+data['Env'][i][0]+'</a>' +
                        '<hr/>');
                    $("#BundleReportTable").append(''+
                    '<div id="env'+i+'"></div>');
                    ResultTable("#env"+i+"",data['Heading'], data['Env'],"");
                }
            });
        }
        //event.stopPropagation();
    });

});


