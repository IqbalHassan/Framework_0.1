/**
 * Created by Raju on 7/1/2015.
 */
var log_id=0;
var current_test_case='';
var current_step_id='';
var color={
    'Passed':'#00ff00',
    'Error':'#ff0000',
    'Warning':'#ffa500'
}
$(document).ready(function(){
    $('#live_console').html("Run ID: "+run_id+'<br>');
    var count=0;
    var inter=setInterval(function(){
        test(run_id,log_id);
    },2000);
});
function test(run_id,numitem){
    $.get('get_execution_log',{
        'run_id':run_id,
        'offset':numitem,
    },function(data){
        for(var i=0;i<data['log'].length;i++){
            var test_case=data['log'][i][0];
            var test_case_name=data['log'][i][1];
            var step_name=data['log'][i][2];
            var module_name=data['log'][i][3];
            var log=data['log'][i][4];
            var step_id=data['log'][i][5];
            var tstamp=data['log'][i][6];
            var status=data['log'][i][7];
            if (test_case!=current_test_case){
                $('#live_console').append('<br>---------------------------------------------<br>');
                $('#live_console').append('ID: '+test_case+' Name: '+test_case_name+'<br>');
                $('#live_console').append('---------------------------------------------<br>');
                current_test_case=test_case;
            }
            if(step_id!=current_step_id){
                $('#live_console').append('<br>---------------------------------------------<br>');
                $('#live_console').append('Step Name: '+step_name+'<br>');
                $('#live_console').append('---------------------------------------------<br>');
                current_step_id=step_id;
            }
            $('#live_console').append('<span style="color:'+color[status]+'">'+tstamp+" -- "+module_name+" - " +log+'</span><br>');
        }
        log_id=data['last_id'];
    });
}
