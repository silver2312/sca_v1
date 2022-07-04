function menu_profile(){
    $.get("/menu-profile/", function(data, status){
        $('.menu-profile').html(data);
    });
}
function check_all_book(id) {
    $.get("/b/check/all/53252623623632623/".replace("53252623623632623", id), function(data, status){});
}
function check_profile() {
    $.get("/check-user/", function(data, status){});
}
document.addEventListener("DOMContentLoaded", function(event) {
    $(window).on('load',function(){
        check_profile();
    });    
});
function scrolltop(){
    $([document.documentElement, document.body]).animate({
        scrollTop: 0
    }, 200);
}

function check_content_book(id) {
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const btn = document.getElementById('check_content_book')
    btn.value="Đang cập nhật...";
    data = {
        'id' :id,
        'csrfmiddlewaretoken': csrf[0].value,
    }
    $.ajax({
        type: 'POST',
        url: "/b/check-content/",
        data: data,
        success: function (data) {
            alert(data)
            btn.value="Cập nhật nội dung chương";
        }
    });
}