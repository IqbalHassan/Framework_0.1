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

    $(".version").click(function(event)
    {
        var platform = $(".platform").val();
        var version = $(".version").val();
        if(version != 0)
        {
            $.get("BundleReport_Table",{platform : platform, version : version},function(data)
            {
                ResultTable(BundleReportTable,data['Heading'],data['browsers'],"Bundle Report");
            });

        }
    });

});


