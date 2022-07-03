function edit_profile(){
    $.get("/edit-profile/", function(data, status){
        $('.menu-profile').html(data);
    });
}
var audio = document.getElementById("volum_audio");
function playVid() {
    audio.play();
}
function pauvid() {
    audio.pause();
}
function friend_request_list(){
    $.get("/friend/list-request/", function(data, status){
        $('.menu-profile').html(data);
    });
}
function friend_list(id){
    $.get("/friend/list/53252623623632623/".replace("53252623623632623", id), function(data, status){
        $('.menu-profile').html(data);
    });
}
function friend_list_guest(id){
    $.get("/friend/list/53252623623632623/".replace("53252623623632623", id), function(data, status){
        $('.menu-guest-profile').html(data);
    });
}
function room_list(){
    $.get("/rooms/", function(data, status){
        $('#show_chat').html(data);
        $('#room_name').html("Danh sách phòng");
    });
}
function join_chat(slug){
    $.get("/chat/53252623623632623/".replace("53252623623632623", slug), function(data, status){
        $('#show_chat').html(data);
    });
}
function room_name(name){
    $('#room_name').html(name);
}
function chap_list(id){
    check = document.getElementById('headingTwo');
    if(check){
        if(check.getAttribute('aria-expanded') == 'false'){
            $.get("/b/chap/list/53252623623632623/".replace("53252623623632623", id), function(data, status){
                if( status == "success"){
                    $('#chap-list').html(data);
                }else{
                    alert('Có lỗi xảy ra!');
                }
            });
        }else{
            $('#chap-list').html('<center><div class="loader"></div>Đang tải danh sách chương</center>');
        }
    }
}