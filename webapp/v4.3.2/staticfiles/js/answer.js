$(document).ready(function(){
    $("input:checkbox.vuln_class").change(function(){
        var id = $(this).attr('name');
        var saved_id = $("#vuln_saved_"+id);
        var is_vuln = ($(this).is(":checked"));
        $.post("/updateVuln/"+id+"/",{
          is_vulnerable : is_vuln
        },function(data,status){
            saved_id.text("Saved");
            saved_id.show("fast").delay(1000).hide("fast");
            console.log(status);
        });

    });
    $("input:checkbox.done_class").change(function(){
        var id = $(this).attr('id').replace("is_done_","");
        var saved_id = $(`#is_done_${id}_saved`);
        var is_done = ($(this).is(":checked"));
        $.post(`/answers/${id}/done/`,{
          is_done : is_done
        },function(data,status){
            saved_id.text("Saved");
            saved_id.show("fast").delay(1000).hide("fast");
            console.log(status);
        });

    });
    // $("button").click(function(){
    //     var id = ($(this).attr('id'));
    //     id = id.replace('button_','');
    //     var saved_id = $("#desc_saved_"+id);
    //     var description = $("#description_"+id).val();
    //     $.post("/updateDes/"+id+"/",{
    //       description : description
    //     },function(data,status){
    //         saved_id.text("Saved");
    //         saved_id.show("fast").delay(1000).hide("fast");
    //         console.log(status);
    //     });
    // });

});