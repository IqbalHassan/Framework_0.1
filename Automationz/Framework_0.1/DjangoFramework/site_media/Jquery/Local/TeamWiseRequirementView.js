$(document).ready(function(){
    ButtonPreparation();
});
function ButtonPreparation(){
    $('.requirement').click(function(){
        $(this).closest('tr').next().slideToggle('slow');
    });
}