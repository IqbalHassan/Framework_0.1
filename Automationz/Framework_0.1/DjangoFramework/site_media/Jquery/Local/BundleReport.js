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

    ManageMilestone(project_id,team_id);

    
});

function ManageMilestone(project_id,team_id){
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
    message+='<td width="19%"><select id="branch_name"><option value="">Branch</option>';
    for(var i=0;i<global_version_list.length;i++){
        message+='<option value="'+global_version_list[i][0]+'">'+global_version_list[i][0]+'</option> ';
    }
    message+='</select></td><td><select id="branch_version" style="display: none;"></select></td>'
    message+='</tr></table></td>'
    message+='</tr>';
    //message+='<tr><td align="right">&nbsp;</td><td align="left"><input value="create" type="button" class="button primary" id="create_manual_machine"/></td></tr>';
    $('#choice_div').html(message);
    for(var i=0;i<dependency_list.length;i++){
        $('#'+dependency_list[i][0]+'_name').on('change',function(){
            if($(this).val()!=""){
                generate_name(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
        });
        $('#'+dependency_list[i][0]+'_bit').on('change',function(){
            if($(this).val()!=""){
                generate_version(dependency_list,$(this).val(),$(this).attr('id').substring(0,$(this).attr('id').indexOf('_')));
            }
        });
    }
    $('#branch_name').on('change',function(){
        if($(this).val()!=""){
            for(var i=0;i<global_version_list.length;i++){
                if(global_version_list[i][0]==$(this).val()){
                    var version=global_version_list[i][1];
                    var message="";
                    message+='<option value="">Version</option>';
                    for(var j=0;j<version.length;j++){
                        message+='<option value="'+version[j]+'">'+version[j]+'</option>';
                    }
                    $('#branch_version').html(message);
                    $('#branch_version').css({'display':'block'});
                }
            }
        }
    });

    $(".generate").click(function(event)
    {
        $('#BundleReportTable').empty();
        //var platform = $(".platform").val();
        //var version = $(".version").val();
        /*for(var i=0;i<dependency_list.length;i++){
            var temp=[];
            var name=dependency_list[i][0];
            temp.push(name);
            if($('#'+name+'_name option:selected').val().trim()==""){
                alertify.error(name+' name is empty',1500);
                return false;
            }
            else{
                temp.push($('#'+name+'_name option:selected').val().trim());
            }
            if($('#'+name+'_bit option:selected').val()==null){
                temp.push('Nil');
            }
            else if($('#'+name+'_bit option:selected').val().trim()==""){
                alertify.error(name+' bit is empty',1500);
                return false;
            }
            else{
                temp.push($('#'+name+'_bit option:selected').val().trim());
            }
            if($('#'+name+'_bit option:selected').val()==null){
                temp.push('Nil');
            }
            else if($('#'+name+'_version option:selected').val().trim()==""){
                alertify.error(name+' version is empty',1500);
                return false;
            }
            else{
                temp.push($('#'+name+'_version option:selected').val().trim());
            }
            dependency.push(temp.join('|'));
        }
        if($('#branch_name').val().trim()==""){
            alertify.error('Branch name is empty',1500);
        }
        if($('#branch_version').val().trim()==""){
            alertify.error('Branch Version is empty',1500);
        }
        var branch_name=$('#branch_name').val().trim();
        var branch_version=$('#branch_version').val().trim();*/

        $.get("New_Execution_Report",
        {
            'project_id':project_id,
            'team_id':team_id
         },function(data)
            {
                ResultTable(BundleReportTable,data['Heading'], data['Table'],"Execution Report");
                $("#BundleReportTable .one-column-emphasis").addClass('two-column-emphasis');
                $("#BundleReportTable .one-column-emphasis").removeClass('one-column-emphasis');
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
                /*for(var i=0;i<data['Env'].length;i++)
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
                    /*var sc = data['ReportTable'][i].length -1;
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
                //}

            });

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
            height: 450
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
                        message+='<option value="">Bit</option>';
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
                            message+='<option value="">Version</option>';
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