/**
 * Created by minar09 on 2/4/14.
 */


$(document).ready(function(){

    //Versions
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
        var choice = $(".version").val();
        if(choice != 0)
        {
            $.get("BundleReport_Table",{choice : choice},function(data)
            {
                ResultTable(BundleReportTable,data['Heading'],data['env'],"Bundle Report");





                $("p.flip[title =  'Bundle Report']").text("Bundle Report of (" +choice + ")" )
                $("p.flip[title =  'Bundle Report']").fadeIn(1000);
                //AnalysisTableActions();


            });

        }
    });
});


