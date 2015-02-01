/*
 * Created by minar09 on 2/4/14.
 */


$(document).ready(function(){

    /*$('.combo-box').combobox();
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

    $(".platform").click(function(event)
     {
     $(".version").selectedOptions("0");
     });*/

    
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');

    ManageDependency(project_id,team_id);

    
});

function ManageDependency(project_id,team_id){
    $.get('GetOS',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        dependency_list=data['dependency_list'];
        global_version_list=data['version_list'];
        populate_manual_div(dependency_list,global_version_list,project_id,team_id);
    });
}


function populate_manual_div(dependency_list,global_version_list,project_id,team_id){
    var message="";
    /*message+='<tr>';
    message+='<td align="right"><b class="Text">Machine Name:</b></td>';
    message+='<td align="left"><input class="textbox" id="machine_name"  placeholder="Machine Name Here.."></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Machine IP:</b></td>';
    message+='<td align="left"><input class="textbox" id="machine_ip"  placeholder="Machine IP Here.."></td>';
    message+='</tr>';*/
    for(var i=0;i<dependency_list.length;i++){
        message+='<tr>';
        message+='<td align="right"><b class="Text">'+dependency_list[i][0]+':</b></td>';
        message+='<td align="left"><table width="100%"><tr><td width="10%">';
        message+='<select id="'+dependency_list[i][0]+'_name">';
        message+='<option value="">All</option>';
        var option_list=dependency_list[i][1];
        for(var j=0;j<option_list.length;j++){
            message+=('<option value="'+option_list[j][0]+'" >'+option_list[j][0]+'</option>');
        }
        message+='</select></td>';
        message+='<td width="10%"><select id="'+dependency_list[i][0]+'_bit" style="display:none;"></select></td><td width="33%"><select id="'+dependency_list[i][0]+'_version" style="display:none;"></select></td></tr></table></td>';
        message+='</tr>';
    }
    message+='<tr>';
    message+='<td align="right"><b class="Text">Version:</b></td>';
    message+='<td align="left"><table width="100%"><tr>';
    message+='<td width="19%"><select id="branch_name"><option value="">All</option>';
    for(var i=0;i<global_version_list.length;i++){
        message+='<option value="'+global_version_list[i][0]+'">'+global_version_list[i][0]+'</option> ';
    }
    message+='</select></td><td><select id="branch_version" style="display: none;"></select></td>'
    message+='</tr></table></td>'
    message+='<tr><td align="right"><b class="Text">Test Run Type:</b></td>';
    message+='<td align="left"><select id="run_type"><option value="">All</option><option value="Automation">Automation</option><option value="Manual">Manual</option></select></td>'
    message+='</tr>';
    message+='<tr><td align="right"><b class="Text">Milestone:</b></td>';
    message+='<td align="left"><select class="milestone"><option value="">All</option></select></td>'
    message+='</tr>';
    //message+='<tr><td align="right">&nbsp;</td><td align="left"><input value="create" type="button" class="button primary" id="create_manual_machine"/></td></tr>';
    $.ajax({
        url:'Get_MileStone_Names/',
        dataType : "json",
        data : {
            term : '',
            //project_id: $.session.get('project_id'),
            //eam_id: $.session.get('default_team_identity')
        },
        success: function( json ) {
            /*if(json.length > 0)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')*/
            $.each(json, function(i, value) {
                //if(i == 0)return;
                $(".milestone").append($('<option>').text(value).attr('value', value));
            });
        }
    });
    $('#choice_div').html(message);
    for(var i=0;i<dependency_list.length;i++){
        $('#'+dependency_list[i][0]+'_name').on('change',function(){
            if($(this).val()!=""){
                generate_name(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
            else{
                $(this).closest('td').siblings().find('select').hide();
            }
        });
        $('#'+dependency_list[i][0]+'_bit').on('change',function(){
            if($(this).val()!=""){
                generate_version(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
            else{
                $(this).closest('td').next().find('select').hide();
            }
        });
    }
    $('#branch_name').on('change',function(){
        if($(this).val()!=""){
            for(var i=0;i<global_version_list.length;i++){
                if(global_version_list[i][0]==$(this).val()){
                    var version=global_version_list[i][1];
                    var message="";
                    message+='<option value="">All Versions</option>';
                    for(var j=0;j<version.length;j++){
                        message+='<option value="'+version[j]+'">'+version[j]+'</option>';
                    }
                    $('#branch_version').html(message);
                    $('#branch_version').css({'display':'block'});
                }
            }
        }
        else{
            $('#branch_version').hide();
        }
    });

    $(".generate").click(function(event)
    {
        $('#inner').hide();
        $('#BundleReportTable').empty();
        var dependency=[];
        for(var i=0;i<dependency_list.length;i++){
            var temp=[];
            var name=dependency_list[i][0];
            temp.push(name);
        
            temp.push($('#'+name+'_name option:selected').val());
            
            temp.push($('#'+name+'_bit option:selected').val());
            
            temp.push($('#'+name+'_version option:selected').val());
            
            dependency.push(temp.join('|'));
        }
        
        var branch_name=$('#branch_name').val();
        var branch_version=$('#branch_version').val();
        var run_type=$("#run_type").val();
        var milestone=$('.milestone').val();

        $.get("New_Execution_Report",
        {
            'project_id':project_id,
            'team_id':team_id,
            'dependency':dependency.join('#'),
            'branch_name':branch_name,
            'branch_version':branch_version,
            'run_type':run_type,
            'milestone':milestone
         },function(data)
            {
                ResultTable(BundleReportTable,data['Heading'], data['Table'],"Execution Report", "Click on numbers to see the test cases");
                //$("#BundleReportTable .one-column-emphasis").addClass('two-column-emphasis');
                //$("#BundleReportTable .one-column-emphasis").removeClass('one-column-emphasis');
                var sc = data['Table'].length -1
                RenderPieChart('BundleReportGraph', [
                    ['Passed ('+data['Table'][sc][1]+')', data['Table'][sc][1]],
                    ['Failed ('+data['Table'][sc][2]+')', data['Table'][sc][2]],
                    ['Blocked ('+data['Table'][sc][3]+')',  data['Table'][sc][3]],
                    ['Submitted ('+data['Table'][sc][4]+')', data['Table'][sc][4]],
                    ['In-Progress ('+data['Table'][sc][5]+')',  data['Table'][sc][5]],
                    ['Skipped ('+data['Table'][sc][6]+')', data['Table'][sc][6]],
                    ['Not Run ('+data['Table'][sc][7]+')', data['Table'][sc][7]]

                ]);

                $("#BundleReportTable tr:last-child").css({'font-weight':'bold'})

                $('#BundleReportTable tr>td:nth-child(n+2)').each(function(){
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
                            ResultTable(tc_table,data['Short'],data['Cases'][row-1][col],"Test Cases", "Click on TC-IDs to see run history");
                            $('#tc_table tr>td:first-child').each(function () {
                                $(this).css({
                                    'color': 'blue',
                                    'cursor': 'pointer',
                                    'textAlign': 'left'
                                });
                                $(this).click(function(){
                                    var tc_id = $(this).text().trim();
                                    //var location='/Home/RunHistory/'+data+'/';
                                    //window.location=location;
                                    $.get("Selected_TestCaseID_Analaysis",{Selected_TC_Analysis : tc_id},function(data){
                                        ResultTable(tc_table,data['Heading'],data['TestCase_Analysis_Result'],"Test Analysis Result of "+tc_id);
                                        makeRunClickable();
                                    });
                                });
                            });
                            $('#tc_table tr>td:nth-child(2)').each(function(){
                               if($(this).text() != 'N/A'){
                                    $(this).css({
                                      'color':'blue',
                                       'cursor':'pointer'
                                   });
                                   $(this).click(function(){
                                      var run_id=$(this).text().trim();
                                      var location='/Home/RunID/'+run_id;
                                      window.location=location;
                                   });
                               }
                            });

                        }); 
                    }
                });
                
                //make_number_clickable('#BundleReportTable',data['Cases']);
            });

    });
}


function makeRunClickable(){
    $('#tc_table tr>td:first-child').each(function(){
       $(this).css({
          'color':'blue',
           'cursor':'pointer'
       });
       $(this).click(function(){
          var run_id=$(this).text().trim();
          var location='/Home/RunID/'+run_id;
          window.location=location;
       });
    });

    $('#tc_table tr>td:last-child').each(function(){
        var log=$(this).text().trim();
        if(log != "null"){
            $(this).html('<a href="file:///'+log+'">Log File</a>');
        }
    });
}

    

function RenderPieChart(elementId, dataList, title) {
    Highcharts.setOptions({
        colors: ['#65bd10','#FD0006','#FF8C00','grey','blue','#88a388','black']
    });
    new Highcharts.Chart({
        chart: {
            renderTo: elementId,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            height: 500
        }, title: {
            text: 'Summary'
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

function generate_name(dependency_list,name,type){
    for (var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            for(var j=0;j<dependency_list[i][1].length;j++){
                if(dependency_list[i][1][j][0]==name){
                    var version_list=dependency_list[i][1][j][1];
                    if (version_list.length>0){
                        var message="";
                        message+='<option value="">All Bits</option>';
                        for(var k=0;k<version_list.length;k++){
                            message+='<option value="'+version_list[k][0]+'">'+version_list[k][0]+' Bit</option>';
                        }
                        $('#'+type+'_bit').html(message);
                        $('#'+type+'_bit').css({'display':'block'});
                        break;
                    }
                }
            }
        }
    }
}

function generate_version(dependency_list,name,type){
    for(var i=0;i<dependency_list.length;i++){
        if(dependency_list[i][0]==type){
            var names=dependency_list[i][1];
            for(var j=0;j<names.length;j++){
                if(names[j][0]==$('#'+type+'_name option:selected').val()){
                    var bit_list=names[j][1];
                    for(var k=0;k<bit_list.length;k++){
                        if(bit_list[k][0]==name){
                            var version_list=bit_list[k][1];
                            console.log(version_list);
                            var message="";
                            message+='<option value="">All Versions</option>';
                            for(var l=0;l<version_list.length;l++){
                                message+='<option value="'+version_list[l]+'">'+version_list[l]+'</option>';
                            }
                            $('#'+type+'_version').html(message);
                            $('#'+type+'_version').css({'display':'block'});
                            break;
                        }
                    }
                }
            }
        }
    }
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

                /*$("#inner").dialog({
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
                    title:"Test Cases"
                });*/

            }); 
        }
    });
}
