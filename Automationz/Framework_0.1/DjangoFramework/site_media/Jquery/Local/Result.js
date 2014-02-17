$(document).ready(function(){
    make_pagination('#allPage','#allRun','.paginated');
    make_pagination('#completePage','#completeRun','.paginated');
    make_pagination('#cancelledPage','#cancelledRun','.paginated');
    make_pagination('#progressPage','#cancelledRun','.paginated');
    make_pagination('#submittedPage','#submittedRun','.paginated');
    make_clickable('#allRun');
    make_clickable('#completeRun');
    make_clickable('#cancelledRun');
    make_clickable('#progressRun');
    make_clickable('#submittedRun');
    drawGraph('#allRun');
});
function drawGraph(divname){
    $(divname+' tr>td:nth-child(5)').each(function(){
        var text=$(this).text().trim();
        text=text.split(')');
        text=text[0].split("(")[1].split(",");
        var status_array=[];
        for(var i=0;i<text.length;i++){
            var each=text[i].trim().split('L')[0].trim();
            status_array.push(each);
        }
        drawTable(status_array);
    });
}
function drawTable(status_array){
    var pass=(status_array[1]/status_array[0])*100;
    var fail=(status_array[2]/status_array[0])*100;
    var block=(status_array[3]/status_array[0])*100;
    var progress=(status_array[4]/status_array[0])*100;
    var submitted=(status_array[5]/status_array[0])*100;
    pass+='%';
    fail+='%';
    block+='%';
    progress+='%';
    submitted+='%';
    var message="";
}
function make_clickable(divname){
    $(divname+' tr>td:first-child').each(function(){
       $(this).css({
           'color':'blue',
           'cursor':'pointer'
       }) ;
       $(this).click(function(){
           var location='/Home/RunID/'+$(this).text().trim()+'/';
            window.location=location;
       });
    });
}
function make_pagination(pagediv,divname,classname){
    var itemsOnPage = 5;
    $(pagediv).pagination({
        items: $(divname+' '+classname).length,
        itemsOnPage: itemsOnPage,
        cssStyle: 'light-theme',
        onPageClick: function (pageNumber, event) {
            var pageN = pageNumber != 0 ? (pageNumber - 1) : pageNumber;
            var from = (pageN * itemsOnPage) + 1;
            var to = (pageNumber * itemsOnPage);
            //console.log('page :'+pageNumber+' from: ' + from + ' to :' + to);
            $(divname+' '+classname).css({ 'display': 'none' });
            for (var i = from; i <= to ; i++) {
              //  console.log('loop :'+i);
                $(divname+' '+classname+':eq(' + (i-1) + ')').css({ 'display': 'block' });
            }
        },
        onInit: function () {
            $(divname+' '+classname).css({ 'display': 'none' });
            for (var i = 0; i <itemsOnPage; ++i) {
                $(divname+' '+classname+':eq('+i+')').css({ 'display': 'block' });
            }
        }
    });
}