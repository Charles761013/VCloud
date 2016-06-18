$('[id^=delete-video-]').click(function(){

	var id = $(this).attr("id");
	id_num = id.split("-")[2];
	if(confirm("確定刪除這個影片?")) {
				$.get('/vod/delete_video/', {'video_id': id_num}, function(data){
  		$('#delete-video-'+id_num).parent().parent().remove();
    });
	}
	else {

	}

});