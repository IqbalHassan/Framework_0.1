/**
 * Created by lent400 on 1/22/14.
 *//*
$(document).ready(function(){
    show_Results("all");
});
function drawTable(column,row){
    var message="";
    message+='<table id="data_table" class="one-column-emphasis" style="font-size:small; border-collapse:collapse;" width="100%">';
    message+='<tr class="paginated" width="100%" style="display: none">';
    for(var i=0;i<column.length;i++){
        message+='<td style="text-align: center">'+column[i]+'</td> ';
    }
    message+='</tr>';
    for(var i=0;i<row.length;i++){
        message+='<tr class="paginated" width="100%" style="display: none">';
        for(var j=0;j<row[i].length;j++){
            if(row[i][j]=="status"){
                message+='<td  id="status'+i+'"></td>'
            }
            else{
                message+='<td style="text-align: center">'+row[i][j]+'</td> ';
            }
        }
    }
    message+='</tr>';
    message+='</table>';
    return message;
}
function Clickable_RunID(){
    $('#ResultPane tr>td:first-child').each(function(){
       if($(this).text().trim()!="Run ID"){
           $(this).css({
               'color':'blue',
               'cursor':'pointer'
           });
           $(this).live('click',function(){
              var run_id=$(this).text().trim();
              if(run_id!=""){
                  window.location='/Home/RunID/'+run_id+'/';
              }

           });
       }
    });
}
function make_table(array){
    console.log(array);
    var message="";
    var column=["Legend","Status","No of Cases","Percentage"];
    var tag=["Passed","Failed","Blocked","In-Progress","Submitted"];
    var color=["green","red","orange","blue","silver"];
    message+='<table class="one-column-emphasis" style="font-size: small;border-collapse: collapse">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<td style="text-align: center">'+column[i]+'</td>';
    }
    message+='</tr>';
    for(var i=0;i<color.length;i++){
        var percentage=(array[i+1]/array[0])*100;
        if(percentage!=0){
            percentage=percentage-0.01;
        }
        percentage=percentage+"%";
        console.log(percentage);
        message+='<tr>';
        message+='<td width="40%"><table width="100%" height="100%"><tr><td style="background-color: '+color[i]+'">&nbsp;&nbsp;</td></tr></table></td>';
        message+='<td width="30%" style="text-align:center;color:'+color[i]+'"><b>'+tag[i]+'</b></td>';
        message+='<td style="text-align: center;font-weight:bolder;color:'+color[i]+'" width="100%">'+array[i+1]+'</td>';
        message+='<td style="text-align: center;font-weight:bolder;color:'+color[i]+'" width="100%">'+percentage+'</td>';
        message+='</tr>'
    }
    message+='<tr>';
    message+='<td style="text-align: center"><b>Total</b></td> ';
    message+='<td style="text-align: center" colspan="3"><b>'+array[0]+'</b></td> ';
    message+='</tr>'
    message+='</table> ';
    return message;
}
function Make_Detail_Status(){
    $('#ResultPane tr td:nth-child(5)').each(function(){
        $(this).closest("tr").find("td:nth-child(2)").css({'textAlign':'left'});
        if($(this).text().trim()!="Report Status"){
            $(this).css({
                'cursor':'pointer'
            }) ;
            $(this).live('click',function(){
                var run_id=$(this).closest("tr").find("td:first-child").text().trim();
                var data_got=0;
                var message="";
                $.get("RunIDStatus",{
                    'run_id':run_id
                },function(data){
                    data_got=data['message'];
                    console.log(data_got);
                    message=make_table(data_got);
                    $('#inner').html(message);
                    $("#inner").dialog({
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
                        width : 500,
                        height : 620,
                        title:"Result Summary"
                    });
                });

            });
        }
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
            console.log('page :'+pageNumber+' from: ' + from + ' to :' + to);
            $(divname+' '+classname).css({ 'display': 'none' });
            for (var i = from; i <= to ; i++) {
                console.log('loop :'+i);
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
function show_Results(searchText){
    $.get("ResultTableFetch",{
        'searchText':searchText
    },function(data){
        var message=drawTable(data['column'],data['data']);
        //console.log(message);
        $('#ResultPane').html(message);
        for(var i=0;i<data['status_list'].length;i++){
            var array=data['status_list'][i];
            var message="";
            pass=(array[1]/array[0])*100;
            fail=(array[2]/array[0])*100;
            blocked=(array[3]/array[0])*100;
            progress=(array[4]/array[0])*100;
            submitted=(array[5]/array[0])*100;
            message+='<table style="border-collapse:collapse" width="100%" height="100%"><tr width="100%" height="100%">';
            if(pass!=0){
                message+='<td style="background-color: green;" width="'+pass+'%">&nbsp;</td>';
            }
            if(fail!=0){
                message+='<td style="background-color: red;" width="'+fail+'%">&nbsp;</td>';
            }
            if(blocked!=0){
                message+='<td style="background-color: orange;" width="'+blocked+'%">&nbsp;</td>';
            }
            if(progress!=0){
                message+='<td style="background-color: blue;" width="'+progress+'%">&nbsp;</td>';
            }
            if(submitted!=0){
                message+='<td style="background-color: #c0c0c0;" width="'+submitted+'%">&nbsp;</td>';
            }
            message+='</tr></table>';
            $('#status'+i).html(message+'Total:'+array[0]);
        }
        Make_Detail_Status();
        Clickable_RunID();
        make_pagination('#allPage','#ResultPane','.paginated');

    });
}

*/
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
});
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
            console.log('page :'+pageNumber+' from: ' + from + ' to :' + to);
            $(divname+' '+classname).css({ 'display': 'none' });
            for (var i = from; i <= to ; i++) {
                console.log('loop :'+i);
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