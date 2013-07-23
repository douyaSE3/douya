//do this before ajax to prove it is not a CSRF
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

//照片删除按钮
$('.photo-wrapper').mouseover(function(){
    $(this).find('.photo-del').removeClass('none');
});
$('.photo-wrapper').mouseout(function(){
    $(this).find('.photo-del').addClass('none');
});

//面包屑
$('.crumb li').mouseover(function(){
    $(this).find('.crumb-li-hover').removeClass('none');
    $(this).find('.crumb-li-subnav').removeClass('none');
}).mouseout(function(){
    $(this).find('.crumb-li-hover').addClass('none');
    $(this).find('.crumb-li-subnav').addClass('none');
});

//slide
$('.slide-main ul li').mouseover(function(){
    $(this).find('.slide-popup').removeClass('none');
}).mouseout(function(){
    $(this).find('.slide-popup').addClass('none');
});

//防止弹出窗口冒泡
$('.slide-popup').mouseover(function(){
    return false;
}).mouseout(function(){
    return false;
});

$('.slide-prev').click(function(){
    var current_prompt = $(this).closest('.slide').prev().find('.current');
    var current_num = current_prompt.data('number');
    var sliding = $(this).closest('.slide').data('sliding');
    if(current_num>0){
        if(sliding!=0){
            return false;
        }else{
            $(this).closest('.slide').data('sliding',1);
        }
        //更新右上角提示符
        current_prompt.removeClass('current');
        current_prompt.prev().addClass('current');

        //移动ul
        var move = $(this).closest('.slide').find('.slide-ul-wrapper');
        var offset = parseInt(move.css('left').replace('px',''))+509;
        
        move.animate({'left':offset+"px"},function(){
            $(this).closest('.slide').data('sliding',0);
        });
    }

    //重置按钮
    $(this).closest('.slide').find('.slide-next').removeClass('off');
    $(this).closest('.slide').find('.slide-prev').removeClass('off');
    if(current_num<=1){
        $(this).addClass('off');
    }
});
$('.slide-next').click(function(){   
    var current_prompt = $(this).closest('.slide').prev().find('.current');
    var current_num = current_prompt.data('number');
    var sliding = $(this).closest('.slide').data('sliding');
    if(current_num<3){
        if(sliding!=0){
            return false;
        }else{
            $(this).closest('.slide').data('sliding',1);
        }
        //更新右上角提示符
        current_prompt.removeClass('current');
        current_prompt.next().addClass('current');

        //移动ul
        var move = $(this).closest('.slide').find('.slide-ul-wrapper');
        var offset = parseInt(move.css('left').replace('px',''))-509;
        
        move.animate({'left':offset+"px"},function(){
            $(this).closest('.slide').data('sliding',0);
        });
    }

    //重置按钮
    $(this).closest('.slide').find('.slide-next').removeClass('off');
    $(this).closest('.slide').find('.slide-prev').removeClass('off');
    if(current_num>=2){
        $(this).addClass('off');
    }
});

$(document).ready(function(){
    $('.fancybox').fancybox();
    console.log("喜欢看豆芽的代码，还是发现了什么bug？不如和我们一起为豆芽添砖加瓦吧！")

    for(var i=0;i<$('.slide-popup').length;i++){
        var tmp = (i+1)%4;
        if(tmp == 0 || tmp == 3){
            $('.slide-popup').eq(i).addClass('slide-popup-toLeft');
        }
    }
});