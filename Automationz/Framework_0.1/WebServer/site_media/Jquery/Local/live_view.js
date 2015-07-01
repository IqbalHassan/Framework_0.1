/**
 * Created by Raju on 7/1/2015.
 */
var log_id=0;
$(document).ready(function(){
    $('#live_console').html("Run ID: "+run_id+'<br>');
    var count=0;
    //test(run_id,count);
    var inter=setInterval(function(){
        test(run_id,log_id);
    },2000);
});
function test(run_id,numitem){
    $.get('get_execution_log',{
        'run_id':run_id,
        'offset':numitem,
    },function(data){
        if(data['log'].length==0){
            clearInterval(inter);
        }
        for(var i=0;i<data['log'].length;i++){
            //$("#live_console").append(data['log_id']);
            //log_id=data['log_id'];
            $('#live_console').append(data['log'][i][0]+" : " +data['log'][i][1]+'<br>');
        }
        console.log(data['last_id']);
        log_id=data['last_id'];
    });
}
