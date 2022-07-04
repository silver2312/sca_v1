//dark mode
    var element = $(document.body);
    var card_body = $('.card-body');
    var card_header = $('.card-header');
    var card = $('.card');
    var footer = $('.card-footer');
    var model_header = $('.modal-header');
    var model_body = $('.modal-body');
    var modal_footer = $('.modal-footer');
    var nav_top = $('#nav_top');
    $(document).ready(function(){
        if(localStorage.getItem('switch_color')!==null){
            const data = localStorage.getItem('switch_color');
            const data_obj = JSON.parse(data);
            element.addClass(data_obj.class_1);
            card.addClass(data_obj.class_1);
            card_body.addClass(data_obj.class_1);
            card_header.addClass(data_obj.class_1);
            model_header.addClass(data_obj.class_1);
            model_body.addClass(data_obj.class_1);
            modal_footer.addClass(data_obj.class_1);
            footer.addClass(data_obj.class_1);
            nav_top.addClass(data_obj.class_2);
        }
    });
    function dark_mode(){
        element.toggleClass("switch_color");
        card_body.toggleClass("switch_color");
        card_header.toggleClass("switch_color");
        card.toggleClass("switch_color");
        footer.toggleClass("switch_color");
        model_header.toggleClass("switch_color");
        model_body.toggleClass("switch_color");
        modal_footer.toggleClass("switch_color");
        nav_top.toggleClass("bg-black");
        if(document.body.classList.contains("switch_color")){
            var item = {
                'class_1':'switch_color',
                'class_2':'bg-black',
                }
            localStorage.setItem('switch_color', JSON.stringify(item));
        }
        else{
            localStorage.removeItem('switch_color');
        }
    }
//end dark mode
//đếm giờ
    function Dong_ho() {
        var ngay = document.getElementById("ngay");
        var thang = document.getElementById("thang");
        var nam = document.getElementById("nam");
        var gio = document.getElementById("gio");
        var phut = document.getElementById("phut");
        var giay = document.getElementById("giay");
        var Ngay_hien_tai = new Date().getDate();
        var Thang_hien_tai = new Date().getMonth();
        var Nam_hien_tai = new Date().getFullYear();
        var Gio_hien_tai = new Date().getHours();
        var Phut_hien_tai = new Date().getMinutes();
        var Giay_hien_tai = new Date().getSeconds();
        ngay.innerHTML = Ngay_hien_tai;
        thang.innerHTML = Thang_hien_tai+1;
        nam.innerHTML = Nam_hien_tai;
        gio.innerHTML = Gio_hien_tai;
        phut.innerHTML = Phut_hien_tai;
        giay.innerHTML = Giay_hien_tai;
    }
    var Dem_gio = setInterval(Dong_ho, 1000);
//end đếm giờ



function acceptFriendRequest(friend_request_id, uiUpdateFunction){
    var url = "/friend/accept/53252623623632623/".replace("53252623623632623", friend_request_id)
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: url,
        timeout: 5000,
        success: function(data) {
            if(data['response'] == "Done."){
                alert("Đã chấp nhận lời mời kết bạn.")
            }
            else if(data['response'] != null){
                alert(data['response'])
            }
        },
        error: function(data) {
            alert("Có lỗi xảy ra.")
        },
        complete: function(data){
            uiUpdateFunction()
        }
    });
}
function removeFriend(id, uiUpdateFunction){
    var url = "/friend/remove/53252623623632623/".replace("53252623623632623", id)
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: url,
        timeout: 5000,
        success: function(data) {
            if(data['response'] == "Done."){
                alert("Đã xóa bạn bè.")
            }
            else if(data['response'] != null){
                alert(data['response'])
            }
        },
        error: function(data) {
            alert("Có lỗi xảy ra.")
        },
        complete: function(data){
            uiUpdateFunction()
        }
    });
}
function declineFriendRequest(friend_request_id, uiUpdateFunction){
    var url = "/friend/decline/53252623623632623/".replace("53252623623632623", friend_request_id)
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: url,
        timeout: 5000,
        success: function(data) {
            console.log("SUCCESS", data)
            if(data['response'] == "Done."){
                alert("Đã huỷ lời mời kết bạn.")
            }
            else if(data['response'] != null){
                alert(data['response'])
            }
        },
        error: function(data) {
            alert(data['response'])
        },
        complete: function(data){
            uiUpdateFunction()
        }
    });
}
function rep_mess(add){
    var text = $('#chat-message-input');
    text.val( text.val() + add );  
}
$(document).ready(function(){
    $('[rel="tooltip"]').tooltip();
});
function scroltoView(){
    var a = $('#my_chapter');
    if(a){
        try {
        $([document.documentElement, document.body]).animate({
                scrollTop: $(a).offset().top - 300            
            }, 200);
        }
        catch(err) {
            console.log("Lỗi di chuyển đến trang đang đọc")
        }
    }

}