/**
 * Created by 09 on 3/29/15.
 */

$(document).ready(function(){
    $('#create_user').on('click',function(){
        var user_name=$('#user_name').val().trim();
        var full_name=$('#full_name').val().trim();
        var email=$('#email').val().trim();
        var password=$('#password').val().trim();
        var confirm_password=$('#confirm_password').val().trim();
        var user_level=$('#user_level option:selected').val().trim();
        if(user_name=='' || full_name==''||email==''||user_level==''||password==''||confirm_password==''){
            alertify.error('Check Input Fields',1500)
        }
        if(password!=confirm_password){
            alertify.error('Password don\'t match',1500);
        }
        $.get('Create_New_User',{
            user_name:user_name.trim(),
            email:email.trim(),
            password:password.trim(),
            full_name:full_name.trim(),
            user_level:user_level
        },function(data){
            if(data==true){
                window.location='/Home/superAdminFunction/AssignMembers/';
            }
        });
    });
});
