/**
 * Created by 09 on 5/13/15.
 */
$(document).ready(function(){
   //alert(project_id);
   $('.team').on('click',function(){
        $('.team').css({'background-color':'#fff'});
        $(this).css({'background-color':'#ccc'});
        var team_id=$(this).attr('data-id');
        $('#mainbody').html(format_div());
       get_all_data(project_id,team_id);
       $('#submit_button').on('click',function(){
            var email=$('#from_address').val();
            var smtp_address=$('#smtp_address').val();
            var port=$('#port').val();
            var username=$('#username').val();
            var password=$('#password').val();
            if($('#ttls_check').is(":checked")){
                var ttls=true;
            }else{
                var ttls=false;
            }
            if(!validateEmail(email)){
                alertify.set({ delay: 300000 });
                alertify.error("From Email Address is not valid.");
                return false;
            }
            if(!isNumber(port)){
                alertify.set({ delay: 300000 });
                alertify.error("Port must be a number");
                return false;
            }
            if(smtp_address==''){
                alertify.set({ delay: 300000 });
                alertify.error("SMTP Address must be valid");
                return false;
            }
            if(username==''){
                alertify.set({ delay: 300000 });
                alertify.error("Username must be valid");
                return false;
            }
            if(password==''){
                alertify.set({ delay: 300000 });
                alertify.error("Password must be valid");
                return false;
            }
            $.get('updatemailingdetails',{
                from_address:email.trim(),
                smtp_address:smtp_address.trim(),
                port:port.trim(),
                username:username.trim(),
                password:password.trim(),
                ttls:ttls,
                project_id:project_id.trim(),
                team_id:team_id.trim(),
                user_id: $.session.get('fullname')
            },function(data){
                if(data['message']){
                    alertify.set({ delay: 300000 });
                    alertify.success(data['log_message']);
                }
                else{
                    alertify.set({ delay: 300000 });
                    alertify.error(data['log_message']);
                }
                window.location.reload(true);
            });
        });
   });
});
function get_all_data(project_id,team_id){
    $.get('getemaildetails',{
        'project_id':project_id,
        'team_id':team_id,
        'user_id': $.session.get('user_id')
    },function(data){
        var owner_tag=data['owner'];
        data=data['result'];
        $('#from_address').val(data['From']);
        $('#smtp_address').val(data['SMTP']);
        $('#port').val(data['PORT']);
        $('#username').val(data['USERNAME']);
        $('#password').val(data['PASSWORD']);
        if(data['TTLS']){
            $('#ttls_check').attr('checked','checked');
        }
        if (owner_tag){
            $('#submit_button').css({'display':'block'});
        }
    });
}
function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}
function format_div(){
    var message='';
    message+='<table>';
    message+='<tr><td><b>From:</b></td><td><input id="from_address" class="textbox" placeholder="Enter the From Address.."></td></tr>';
    message+='<tr><td><b>SMTP Address:</b></td><td><input class="textbox" id="smtp_address" placeholder="Enter the SMTP Address.."></td></tr>';
    message+='<tr><td><b>Port:</b></td><td><input class="textbox" id="port" placeholder="Enter the port number.."></td></tr>';
    message+='<tr><td><b>Username:</b></td><td><input class="textbox" id="username" placeholder="Enter the username.."></td></tr>';
    message+='<tr><td><b>Password:</b></td><td><input class="textbox" id="password" placeholder="Enter the password.."></td></tr>';
    message+='<tr><td><b>TTLS:</b></td><td><input class=" cmn-toggle cmn-toggle-yes-no" id="ttls_check" type="checkbox" name="type" value="yes" style="width:auto" />';
    message+='<label for="ttls_check" data-on="Yes" data-off="No"></label></td></tr>';
    message+='</table>';
    message+='<input type="button" id="submit_button" class="m-btn green" value="Save" style="display:none"/>';
    return message;
}