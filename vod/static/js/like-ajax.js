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