/**
 * Created by J on 9/11/14.
 */
var label_per_page=10;
var label_page_current=1;
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');

$(document).ready(function(){
    $("#new_label").click(function(){
        //$("#label_creation").show();
        if($("#label_creation").is(":visible")){
            $("#label_creation").slideUp('slow');
            //$("#label_creation").hide();
        }
        else{
            $("#label_creation").slideDown('slow');
            //$("#label_creation").show();
        }
    });
    $("#cancel_label").click(function(){
        $("#label_creation").slideUp('slow');
    });
    $("#color_picker").spectrum({
        color: "#f00",
        preferredFormat: "hex",
        showInput: true
    });

    $("#create_label").click(function(){
        var name = $("#label_name").val();
        var color = $(".sp-input").val();

        if(name!= ""){
            $.get("CreateLabel/",{
                name:name.trim(),
                color:color.trim(),
                project:project_id,
                team:team_id,
                user:$.session.get('fullname')
            },function(data){
                if(data=="Label name already exists!"){
                    alertify.set({ delay: 300000 });
                    alertify.error(data);
                }
                else{
                    alertify.set({ delay: 300000 });
                    alertify.success("Label Created!");
                    $("#label_creation").slideUp('slow');
                    //window.location.reload(true);
                    get_labels(project_id,team_id,label_per_page,label_page_current);
                }
            });
        }
        else{
            alertify.set({ delay: 300000 });
            alertify.error("Label Name is needed!");
        }
    });

    get_labels(project_id,team_id,label_per_page,label_page_current);

    label_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            label_per_page=$(this).val();
            label_page_current=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            get_labels(project_id,team_id,label_per_page,label_page_current);
        }
    });
})


function get_labels(project_id,team_id,label_per_page,label_page_current){
    $.get("Show_Labels",{'project_id':project_id ,'team_id':team_id,'label_per_page':label_per_page,'label_page_current':label_page_current},function(data){
        form_table("AllLabelsTable",data['Heading'],data['TableData'],data['Count'],"Labels");
        
        $('#pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:label_per_page,
            cssStyle: 'dark-theme',
            currentPage:label_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_labels(project_id,team_id,label_per_page,PageNumber);
            }
        });
    });
}


function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table class="two-column-emphasis" id="table_vai_table">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        message += '<td><a href="/Home/ViewEditLabel/'+data[i][0]+'" class="label" style="background-color: '+data[i][2]+';">'+data[i][1]+'</a></td>'
        message += '<td>'+data[i][0]+'</td>'
        message += '<td>'+data[i][3]+'</td>'
        message += '<td>'+data[i][4]+'</td>'
        message += '<td><span style="cursor:pointer;" class="hint--right hint--bounce hint--rounded" data-hint="Delete this label"><i class="fa fa-trash fa-fw fa-lg"></span></td>'
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);

    $("#table_vai_table tr td:nth-child(5)").each(function(){
        $(this).on('click',function(){
            var label = $(this).parent().find('td:first-child').text().trim();
            var label_id = $(this).parent().find('td:nth-child(2)').text().trim();
            //reset();
            var message='';
            message+='<div>';
            message+='<p style="font-size:140%">Are you sure to delete label <b>' + label + '</b>?</p>';
            message+='<br/>';
            message+='</div>';
            alertify.confirm(message, function (e) {
                if (e) {
                    $.get("DeleteLabel/",{
                        label_id:label_id
                    },function(data){
                        alertify.set({ delay: 300000 });
                        alertify.success("Label Deleted!");
                        window.location.reload(true);
                    });
                    
                } else {
                    alertify.set({ delay: 300000 });
                    alertify.error("You've clicked Cancel");
                }
            });
            return false;
       });
    });
}
