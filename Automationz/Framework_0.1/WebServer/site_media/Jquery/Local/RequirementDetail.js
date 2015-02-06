$(document).ready(function(){
    StylePreparation();
});
function StylePreparation(){
    $('#id_comment').closest('tr').find('th:first').css({'vertical-align':'0%'});
    $('#id_commented_by').val($('#user_name').text().trim());
}