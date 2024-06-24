let buttonSelectUser = document.getElementById("select_User");
let buttonGetInfo = document.getElementById("infoButton")
function chooseUser() {
    BX24.selectUser(function (res) {
        buttonSelectUser.innerHTML = res['name'];
        buttonGetInfo.disabled = false;
        buttonGetInfo.value = res['id'];
    })
}
