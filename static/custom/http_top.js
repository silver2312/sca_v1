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
