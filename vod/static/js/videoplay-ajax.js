$('#like').click(function(){
    var videoid;
    videoid = $(this).attr("video-id");
    act = $(this).attr("act-type");
    var islike;
    var setAttr;
    var thumb;
    if(act.localeCompare("like") == 0) {
    	islike = 1;
    	setAttr = "unlike";
    	thumb = "<span class='glyphicon glyphicon-thumbs-down'></span>UnLike";
    } else {
    	islike = 0;
    	setAttr = "like";
    	thumb = "<span class='glyphicon glyphicon-thumbs-up'></span>Like";
    }
    $.get('/vod/like_video/', {video_id: videoid, is_like: islike}, function(data){
               $('#like_count').html(data);
               $('#like').html(thumb);
               $('#like').attr("act-type", setAttr);
    });
});

$('[id^=delete-]').click(function(){

	var id = $(this).attr("id");
	id_num = id.split("-", 2)[1]
	$.get('/vod/review/', {review_id: id_num}, function(data){
               $('#delete-'+id_num).parent().parent().remove()
    });
});

$('[id^=edit-]').click(function(){
	var id = $(this).attr("id");
	id_num = id.split("-", 2)[1]

	$('#reviewform-'+id_num).toggle();
	$('#confirm-'+id_num).toggle();
	var text = $('#edit-'+id_num).text();
	if(text == "Cancel") {
		$('#edit-'+id_num).text("Edit");
	}
	else if(text == "Edit") {
		$('#edit-'+id_num).text("Cancel");
	}

});







