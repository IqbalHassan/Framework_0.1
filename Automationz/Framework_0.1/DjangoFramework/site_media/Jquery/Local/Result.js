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
    PaginationButton();
    //Testers
    $.ajax({
        url:'GetTesters/',
        dataType : "json",
        data : {
            tester : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".tester[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    //Status
    $.ajax({
        url:'GetStatus/',
        dataType : "json",
        data : {
            status : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                //if(i == 0)return;
                $(".status[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    //versions
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

    //run-types
    $.ajax({
        url:'GetRunTypes/',
        dataType : "json",
        data : {
            run_type : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 0; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".run-type[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    /*$("#simple-menu").click(function(){
        if($(this).text() == "Advanced Filter >>"){
            $(this).val("<< Advanced Filter");
        }
        else if($(this).text("<< Advanced Filter")) {
            $(this).val("Advanced Filter >>");
        }
    });*/

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
        })
    .autocomplete({
        source: function(request,response){
            $.ajax({
                url:"ResultFilter",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value = ui.item[0];
            if(value!=""){
                $("#searchInput").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };

    $(".tester").live('change',function () {
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
                //"color": "black"
            });
            $(this).unbind('focus');
        }).css({
            "color": "#C0C0C0"
        });

    $(".status").live('change' ,function () {
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
            //"color": "black"
        });
        $(this).unbind('focus');
    }).css({
        "color": "#C0C0C0"
    });

    $(".version").live('change' ,function () {
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
                //"color": "black"
            });
            $(this).unbind('focus');
        }).css({
            "color": "#C0C0C0"
        });


});
function PaginationButton(){
    $('.previous_page').click(function(){
        var url=window.location.pathname;
        index=url.split('/')[3].split('-')[1];
        if(index>1){
            index--;
        }
        else{
            index=1;
        }
        var location='/Home/Results/Page-'+index+'/';

        window.location=location;
    });
    $('.next_page').click(function(){
        var url=window.location.pathname;
        $.get("GetPageCount",{},function(data){
            console.log(data);
            index=url.split('/')[3].split('-')[1];
            if(index<data){
                index++;
            }
            else{
                index=data;
            }
            var location='/Home/Results/Page-'+index+'/';
            window.location=location;
        });

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
                            ['Passed',     data[1]],
                            ['Failed',      data[2]],
                            ['Blocked',  data[3]],
                            ['In-Progress', data[4]],
                            ['Submitted',  data[5]],
                            ['Skipped', data[6]]
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
