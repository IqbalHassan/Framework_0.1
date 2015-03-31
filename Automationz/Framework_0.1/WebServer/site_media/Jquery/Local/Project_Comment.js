$(document).ready(function(){
    StylePreparation();
});
function StylePreparation(){
    $('#id_comment').closest('tr').find('th:first').css({'vertical-align':'0%'});
    $('#id_commented_by').val($.session.get('fullname').trim());
    $('#id_commenter_id').val($.session.get('user_id').trim());
}