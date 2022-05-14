/*****************************
TODO:

1. 按鈕fun 模組化 V
2. clean code


*****************************/
//目前跳轉是回login，再回各自首頁。

//切割網址，找上個頁面傳來的參數
var myUrl = decodeURI(window.location.href);
const url = new URL(
    myUrl
);

userID = url.searchParams.get('userID'); 
boardsID = url.searchParams.get('boardsID'); 

//讀取token
token = localStorage.token ;

//Url全域變數
const apiKeeepLoginUrl = 'http://120.113.173.182:8000/api/KeepLogin'; //ok
const apiUserMe = 'http://120.113.173.182:8000/api/user/me' ; //ok
const apiViewBoardBoard_id = 'http://120.113.173.182:8000/api/ViewBoard/' + boardsID ;//ok

const apiLog = 'http://120.113.173.182:8000/api/logs/ViewBoard/' + boardsID;
const apiLogEnterBoard =  apiLog + '/EnterBoard';
const apiLogPlayBox = apiLog + '/PlayBox?subcontent=';
const apiLogDeleteSingleButton = apiLog  + '/DeleteSingleButton?subcontent=';
const apiLogDeleteAllButton = apiLog + '/DeleteAllButton?subcontent=';
const apiLogAddButton = apiLog  + '/AddButton?button_id=';
const apiLogLeaveBoard =  apiLog  + '/LeaveBoard';

//全域變數
const userRole = 'teacher' ;
const userRole2 = 'student' ;



//使用Deferred，參考「https://reurl.cc/EZQEMa」
function checkUserToken() {
    var $dfd = $.Deferred();

    //用這個API可以確認使用者是否為登入狀態以及身分以及這個頁面的身分權限
    //API(KeeepLogin)
    $.ajax({
        url:apiKeeepLoginUrl,
        type:'get',
        headers:{
            'Authorization':'Bearer '+ token
        },
        success:function(data){
            
            if(data.user.role == userRole || data.user.role == userRole2){
                //更新舊的token
                localStorage.clear();
                
                localStorage.role = data.user.role;
                localStorage.token = data.access_token;
                
                //回傳UserId
                $dfd.resolve({
                    id: data.user.id,
                });
            }else{
                $dfd.reject({
                    msg: '您無權限使用本網頁，將為您自動跳轉頁面',
                });
            }
            
        },
        error:function (xhr, thrownError,errorMessage) {
            console.log("failure:" + errorMessage);
            $dfd.reject({
                msg: '驗證失敗，請重新登入',
            });
        }
    });
    return $dfd.promise();
}

//離開頁面
$(window).bind('beforeunload', function(){
    ajaxForLogs(apiLogLeaveBoard,"");
    return "You're leaving?";
});

//Deferred的when
$.when(checkUserToken())
//驗證成功後
.done(function(user) {
    //console.log('Hi, ' + user.name); // Hi, Peter Wang

    
    $("#homepage").attr("href",localStorage.role + 'HomePage.html');
    //API(UserMe)
    $.ajax({
        url:apiUserMe,
        type:'get',
        headers:{
            'Authorization':'Bearer '+ token
        },
        success:function(data){
            //更新舊的token
            //console.log(localStorage.token);
            localStorage.clear();
            localStorage.token = data.access_token;

            //在header上顯示userName
            userName.innerHTML += data.user.name;

        },
        error:function (xhr, thrownError,errorMessage) {
            console.log("failure:" + errorMessage);
        }
    });

    getBoard(boardsID);
    //寫入進入面板log
    ajaxForLogs(apiLogEnterBoard,"");
})

//驗證失敗後
.fail(function(user) {
    alert(user.msg);
    //console.log(user.msg); // Get User Profile Error :(
    window.location.href="login.html"; 
})

//不管驗證成功或失敗
.always(function(user) {
    //console.log('Always execute this line!');
});



//------------------------------------------------------------------全域變數
//API(ViewBoardBoard_id), 有關面板相關變數
var stringList = [];     // 點過哪些button    list
var stringNum = [];      // 點過的button的pos list
var boxList = []; // 結構 = [按鈕字串, imageID(如果沒圖片=null), 字串顏色]

var boarddata;
var tempstring = ""
var tempStringForKeyBoard = "";
var isLinkedBoard = false;

//------------------------------------------------------------------全域變數


window.onresize=function(){                  

    showBoard();
}

// print the board

function showBoard(){
    
    stringList = [];
    stringNum = [];

    console.log(boarddata);
    if(isLinkedBoard)
    {
        $("#stringBoxDiv").removeClass('col-md-9').addClass('col-md-8');
        $("#goBackDiv").show();
    }
    else
    {
        $("#stringBoxDiv").removeClass('col-md-8').addClass('col-md-9');
        $("#goBackDiv").hide();
    }

    let windowHeight = $(window).height();
    let windowWidth  = $(window).width();

    //高度有幾格
    var heightNum = boarddata.board.row_size;
    //寬度有幾格
    var widthNum = boarddata.board.column_size;

    var rowHeight ="7rem";

    var editBoard_content = "";
    var arrayNum = -1;
    var editBoardOfButtons = document.getElementById("editBoardOfButtons");
    //蒐集面板按鈕資訊
    for(i=0;i<heightNum;i++){
        editBoard_content += '<div id = "heightNum_' + i + '"class="row" style="height:'+ rowHeight + '; gap:'+windowWidth*0.05/(widthNum) +'px;" >';
        for(j=0;j<widthNum;j++){
            
            arrayNum += 1;
            var pos = i + "_" + j
            var ele_array_ = "array_" + pos;
            var ele_button_ = "button_"+ pos;
            var ele_button_Name = ele_button_ + "_Name";
            var ele_button_Pic = ele_button_ + "_Pic";
            var ele_button_showPic = ele_button_ + "_showPic";
            var url = 'setButton.html?userID='+ userID + '&buttonID=' + boarddata.board.buttons[arrayNum].id;   
            url = "'" + url + "'";
            var color = '#FFFF00';
            var ele_button_voice = ele_button_+"_voice";
            var fun_button_click = "buttonPlay(" +i+ "," +j+ "," +widthNum+ "," + 1 +")";
            //var fun_button_click = ele_button_voice +"_play()";

            editBoard_content += 
            '<div class = "notsetdiv" id = "' + ele_array_ + '"  style="cursor: pointer; padding:0px 0px; height:95%;width:'+ windowWidth*0.94/(widthNum) + 'px;display:none;" onclick="'+fun_button_click+'">\
                <audio id= "'+ele_button_voice+'" preload="none" src = ""  ></audio>\
                <div id="'+ele_button_Name+'" class = "align-self-center" style="height:25%;text-align:center;">\
                </div>\
                <div id="'+ele_button_Pic+'" class = "align-self-center" style="text-align:center;height:75%;overflow:hidden;color:#000000;font-size:vmin;">\
                    <img id= "'+ele_button_showPic+'" src = "" style = "vertical-align:middle; max-height:100%; max-width:100%; width:auto; height:auto;"></img>\
                </div>\
            </div>';
        }
        editBoard_content += '</div>';
    }
    if(editBoard_content != "")
        editBoardOfButtons.innerHTML = editBoard_content;
    else
        editBoardOfButtons.innerHTML = '<h1>目前面板沒有按鈕可以顯示!</h1>'

    arrayNum = -1
    //把按鈕排列在面板上
    for(i=0;i<heightNum;i++){
        document.getElementById("heightNum_"+i).style.height = rowHeight;
        for(j=0;j<widthNum;j++){
            arrayNum += 1;
            var pos = i + "_" + j
            var ele_array_ = "array_" + pos;
            var ele_button_ = "button_"+ pos;
            var ele_button_Name = ele_button_ + "_Name";
            var ele_button_Pic = ele_button_ + "_Pic";
            var ele_button_showPic = ele_button_ + "_showPic";
            var ele_button_voice = ele_button_+"_voice";
            document.getElementById(ele_array_).style.display = "block";

            //判斷按鈕是否為初始狀態，是的話則顯示「尚未設定」
            if (boarddata.board.buttons[arrayNum].label == ""){
                document.getElementById(ele_button_Name).innerHTML += "尚未設定"; 
                document.getElementById(ele_button_Pic).innerHTML += "尚未設定";   
                document.getElementById(ele_array_).style.visibility = "hidden";
                continue;
            }

            //放入label名稱
            document.getElementById(ele_button_Name).innerHTML += boarddata.board.buttons[arrayNum].label; 
            //設定label名稱文字的顏色
            document.getElementById(ele_button_Name).style.color = boarddata.board.buttons[arrayNum].name_color;
            
            //有圖片就顯示圖片，沒圖片就顯示文字
            if(boarddata.board.buttons[arrayNum].is_image_enable == "1"){
                document.getElementById(ele_button_showPic).src = "http://120.113.173.182:8000/EditBoard/images/" + boarddata.board.buttons[arrayNum].image + '?' + Math.random();;
            }else{
                var elePic = document.getElementById(ele_button_Pic);
                document.getElementById(ele_button_Name).innerHTML = ""; 
                document.getElementById(ele_button_Name).style.height = "0%";
                document.getElementById(ele_button_Pic).style.height = "100%";

                elePic.style.background = boarddata.board.buttons[arrayNum].background_color;
                elePic.innerHTML = boarddata.board.buttons[arrayNum].label;
                elePic.style.color = boarddata.board.buttons[arrayNum].label_color;
                elePic.style.fontSize = "3rem";
                
            }

            //按鈕隱藏為虛框，顯示為實框
            if(boarddata.board.buttons[arrayNum].status == "0"){
                //document.getElementById(ele_array_).style.border = "dashed" ;
                document.getElementById(ele_array_).style.visibility = "hidden";
            }else{
                document.getElementById(ele_array_).className = "divhover" ;
            }
            //用於字串處理
            voiceURL = "http://120.113.173.182:8000/ViewBoard/voices/" + boarddata.board.buttons[arrayNum].voice + '?' + Math.random();
            //console.log(voiceURL);
            document.getElementById(ele_button_voice).src = voiceURL;
            stringList.push(boarddata.board.buttons[arrayNum].label);
            stringNum.push(i*widthNum+j);
        }
    }
    if(globalcheck == true){//當輔助輸入功能是開啟的狀態，載入新面板維持掃描
        clearInterval(interval);
        status1 = true;
        scanningrow();
    }
}
var status1 = false;//鍵盤控制row亮燈開關
var status2 = false;//鍵盤控制button亮燈開關
var status3 = true;//確保輔助輸入不被異常使用
var globalcheck=false;//確保隨模式轉換按紐開啟或結束
var check3=false;//確保使用者跟著框框操作
var blocktime;//計時器，計算距離可以重啟的時間還要多少秒
var timing = 1000;
function scanning(element){
    if(element.innerText == "普通模式"&&status3 == true){
        element.innerText = "掃描模式";
        element.style.color = "blue";
        status1 = true;
        globalcheck = true;
        scanningrow();
    }
    else if(element.innerText == "普通模式"&&status3 == false){
        alert('請等待'+blocktime+'秒後再重啟掃描模式');
    }
    else if(element.innerText == "掃描模式"){
        element.innerText = "普通模式";
        element.style.color = "black";
        status1 = false;
        globalcheck = false;
        status3 = false;
        clearInterval(interval);
        blockguard();
    }
}
$(document).keydown(function(event){
    if(event.keyCode == 32){
        event.preventDefault();
        if(status1 == true){
            status1 = false;
            status2 = true;
            check3=false;
        }
        else if(check3 ==true){
            status2 = false;
        }
    }
    if(event.keyCode == 66)//鍵盤上的"B"
        goBackBoard(1)
    if(event.keyCode == 67)//鍵盤上的"C"
        stringboxClear()
    if(event.keyCode == 68)//鍵盤上的"D"
        stringboxDelete()
    if(event.keyCode == 80)//鍵盤上的"P"
        stringboxVoice()
    if(event.keyCode == 83)//鍵盤上的"S"
        document.getElementById("Switchmode").onclick();
})
function blockguard(){
    blocktime=15;
    setTimeout(function() {
        status3 = true;
    }, 15000)
    var t = setInterval(function () {
        if(blocktime <= 0) {
            clearinterval(t);
        } else {
            blocktime= blocktime -1;
        }
   }, 1000)
}
function scanningrow(){  
    var rownum = 0;
    Array(boarddata.board.row_size).fill(false);
    for(let i = 0; i < boarddata.board.row_size;i++){
        for(let j = 0; j < boarddata.board.column_size; j++){
            ele_array_ = "array_" + i +"_"+ j;
            if(document.getElementById(ele_array_).style.visibility != "hidden"){
                Array[i] = true;
            }
        }
    }
    for(let i = 0; i < boarddata.board.row_size;i++){
        if(Array[i] == true){
            rownum = rownum + 1;
        }
    }
    var localcheck=true;//確保只執行一次就停用
    if(rownum == 0){
        status1 = false;
        status2 = true;
        check3 = false;
        scanningmenubutton();
        localcheck=false;
        return;
    }
    if(isLinkedBoard)
        document.getElementById("goBack").style.border = "5px green solid" ;
    document.getElementById("stringBox1").style.border = "5px green solid" ;
    document.getElementById("Delete").style.border = "5px green solid" ;
    document.getElementById("Clear").style.border = "5px green solid" ;
    document.getElementById("Switchmode").style.border = "5px green solid" ;
    setTimeout(function(){
        if(isLinkedBoard)
            document.getElementById("goBack").style.border = "1px solid transparent" ;
        document.getElementById("stringBox1").style.border = "2px solid black " ;
        document.getElementById("Delete").style.border = "1px solid transparent" ;
        document.getElementById("Clear").style.border = "1px solid transparent" ;
        document.getElementById("Switchmode").style.border = "1px solid transparent" ;
        if(status1 == false){
            clearInterval(interval);
            scanningmenubutton();
            localcheck=false;
            return;
        }
    }, timing)
    var k = 0;
    var s = 0;
    var t = 0;
    for(let i = 0; i < boarddata.board.row_size;i++){
        if(Array[i]==true){
            s= s + 1;
            for(let j = 0; j < boarddata.board.column_size; j++){
                setTimeout(function(){
                    if(j==0)
                    t = t + 1;
                    ele_array_ = "array_" + k +"_"+ j;
                    document.getElementById(ele_array_).style.border = "3px black solid" ;
                    if(globalcheck == true&&localcheck == true){
                        if(status1 == true){
                            ele_array_ = "array_" + i +"_"+ j;
                            document.getElementById(ele_array_).style.border = "5px green solid" ;
                            if(j==boarddata.board.column_size-1)
                            k=i;
                        }
                        else if(status1 == false){
                            clearInterval(interval);
                            scanningbutton(k);
                            localcheck=false;
                            return;
                        }
                    }
                    if(t== rownum){
                        setTimeout(function() {
                            ele_array_ = "array_" + i +"_"+ j;
                            document.getElementById(ele_array_).style.border = "3px black solid" ;
                        }, timing)
                    }
                }, timing * (s))
            }
        }
    }
    interval = setInterval(function(){
        if(status1 == false){
            clearInterval(interval);
            scanningbutton(k);
            localcheck=false;
            return;
        }
        if(globalcheck ==true&&localcheck==true){
            if(isLinkedBoard)
                document.getElementById("goBack").style.border = "5px green solid" ;
            document.getElementById("stringBox1").style.border = "5px green solid" ;
            document.getElementById("Delete").style.border = "5px green solid" ;
            document.getElementById("Clear").style.border = "5px green solid" ;
            document.getElementById("Switchmode").style.border = "5px green solid" ;
            setTimeout(function() {
                if(isLinkedBoard)
                    document.getElementById("goBack").style.border = "1px solid transparent" ;
                document.getElementById("stringBox1").style.border = "2px solid black " ;
                document.getElementById("Delete").style.border = "1px solid transparent" ;
                document.getElementById("Clear").style.border = "1px solid transparent" ;
                document.getElementById("Switchmode").style.border = "1px solid transparent" ;
                if(status1 == false){
                    clearInterval(interval);
                    scanningmenubutton();
                    localcheck=false;
                    return;
                }
            }, timing)
        }
        var s = 0;
        var t = 0;
        for(let i = 0; i < boarddata.board.row_size;i++) {
            if(Array[i]==true){
                s= s + 1;
                for(let j = 0; j < boarddata.board.column_size; j++) {
                    setTimeout(function(){
                        if(j==0)
                        t = t + 1;
                        ele_array_ = "array_" + k +"_"+ j;
                        document.getElementById(ele_array_).style.border = "3px black solid" ;
                        if(globalcheck == true&&localcheck == true){
                            if(status1 == true){
                                ele_array_ = "array_" + i +"_"+ j;
                                document.getElementById(ele_array_).style.border = "5px green solid" ;
                                if(j==boarddata.board.column_size-1)
                                k=i;
                            }
                            else if(status1 == false){
                                clearInterval(interval);
                                scanningbutton(k);
                                localcheck=false;
                                return;
                            }
                        }
                        if(t== rownum){
                            setTimeout(function() {
                                ele_array_ = "array_" + i +"_"+ j;
                                document.getElementById(ele_array_).style.border = "3px black solid" ;
                            }, timing)
                        }
                    }, timing * (s))
                }
            }
        }
    }, timing*(rownum+1))
}
function scanningmenubutton(){
    var localcheck=true;
    var menubutton = ["goBack", "stringBox1","Delete","Clear","Switchmode"];
    if(isLinkedBoard){
        for(let i=0;i<5;i++){
            setTimeout(function() {
                var j=i-1;
                if(j!=1&&j!=-1)
                    document.getElementById(menubutton[j]).style.border = "1px solid transparent" ;
                else if(j==1)
                    document.getElementById(menubutton[j]).style.border = "2px solid black" ;
                if(j==3){
                    setTimeout(function() {
                        document.getElementById(menubutton[4]).style.border = "2px solid black" ;
                    }, timing)
                }
                if(globalcheck == true&&localcheck==true){
                    if(status2 == true){
                        document.getElementById(menubutton[i]).style.border = "5px green solid" ;
                        check3=true;
                    }
                    else if(status2 == false){
                        clearInterval(interval);
                        localcheck=false;
                        status1 = true;
                        if(j==0)
                            goBackBoard();
                        else if(j==1)
                            stringboxVoice();
                        else if(j==2&&boxList.length!=0)
                            stringboxDelete();
                        else if(j==3)
                            stringboxClear();
                        else if(j==-1)
                            document.getElementById("Switchmode").click();
                        if(j!=0)
                            scanningrow();
                        return;
                    }
                }
            }, timing * (i+1))
        }
        interval = setInterval(function(){
            for(let i=0;i<5;i++){
                setTimeout(function() {
                    var j=i-1;
                    if(j!=1&&j!=-1)
                        document.getElementById(menubutton[j]).style.border = "1px solid transparent" ;
                    else if(j==1)
                        document.getElementById(menubutton[j]).style.border = "2px solid black" ;
                    if(j==3){
                        setTimeout(function() {
                            document.getElementById(menubutton[4]).style.border = "2px solid black" ;
                        }, timing)
                    }
                    if(globalcheck == true&&localcheck==true){
                        if(status2 == true){
                            document.getElementById(menubutton[i]).style.border = "5px green solid" ;
                            check3=true;
                        }
                        else if(status2 == false){
                            clearInterval(interval);
                            localcheck=false;
                            status1 = true;
                            if(j==0)
                                goBackBoard();
                            else if(j==1)
                                stringboxVoice();
                            else if(j==2&&boxList.length!=0)
                                stringboxDelete();
                            else if(j==3)
                                stringboxClear();
                            else if(j==-1)
                                document.getElementById("Switchmode").click();
                            if(j!=0)
                                scanningrow();
                            return;
                        }
                    }
                }, timing * (i+1))
            }
        }, timing*5)
    }
    else if(!isLinkedBoard){
        for(let i=1;i<5;i++){
            setTimeout(function() {
                var j=i-1;
                if(j!=1)
                    document.getElementById(menubutton[j]).style.border = "1px solid transparent" ;
                else if(j==1)
                    document.getElementById(menubutton[j]).style.border = "2px solid black" ;
                if(j== 3){
                    setTimeout(function() {
                        document.getElementById(menubutton[4]).style.border = "2px solid black" ;
                    }, timing)
                }
                if(globalcheck == true&&localcheck==true){
                    if(status2 == true){
                        document.getElementById(menubutton[i]).style.border = "5px green solid" ;
                        check3=true;
                    }
                    else if(status2 == false){
                        clearInterval(interval);
                        localcheck=false;
                        status1 = true;
                        if(j==0)
                            document.getElementById("Switchmode").click();
                        else if(j==1)
                            stringboxVoice();
                        else if(j==2&&boxList.length!=0)
                            stringboxDelete();
                        else if(j==3)
                            stringboxClear();
                        if(j!=0)
                            scanningrow();
                        return;
                    }
                }
            }, timing * (i))
        }
        interval = setInterval(function(){
            for(let i=1;i<5;i++){
                setTimeout(function(){
                    var j=i-1;
                    if(j!=1)
                        document.getElementById(menubutton[j]).style.border = "1px solid transparent" ;
                    else if(j==1)
                        document.getElementById(menubutton[j]).style.border = "2px solid black" ;
                    if(j==3){
                        setTimeout(function() {
                            document.getElementById(menubutton[4]).style.border = "2px solid black" ;
                        }, timing)
                    }
                    if(globalcheck == true&&localcheck==true){
                        if(status2 == true){
                            document.getElementById(menubutton[i]).style.border = "5px green solid" ;
                            check3=true;
                        }
                        else if(status2 == false){
                            clearInterval(interval);
                            localcheck=false;
                            status1 = true;
                            if(j==0)
                                document.getElementById("Switchmode").onclick();
                            else if(j==1)
                                stringboxVoice();
                            else if(j==2&&boxList.length!=0)
                                stringboxDelete();
                            else if(j==3)
                                stringboxClear();
                            if(j!=0)
                                scanningrow();   
                            return;
                        }
                    }
                }, timing * (i))
             }
        }, timing*4)
    }
}
function scanningbutton(rownumber){
    var localcheck=true;
    var i = rownumber
    var buttonnum = 0
    var s = 0
    var t = 0
    var g = 0
    for(let k = 0; k < boarddata.board.column_size; k++) {
        ele_array_ = "array_" + i +"_"+ k;
        if(document.getElementById(ele_array_).style.visibility != "hidden")
        buttonnum = buttonnum +1
    }
    for(let j = 0; j < boarddata.board.column_size; j++) {
        ele_array_ = "array_" + i +"_"+ j;
        if(document.getElementById(ele_array_).style.visibility != "hidden"){
            s = s+1
            setTimeout(function() {
                t = t+1
                ele_array_ = "array_" + i +"_"+ g;
                document.getElementById(ele_array_).style.border = "3px black solid" ;
                if(globalcheck == true&&localcheck==true){
                    if(status2 == true){
                        ele_array_ = "array_" + i +"_"+ j;
                        document.getElementById(ele_array_).style.border = "5px green solid" ;
                        check3=true;
                        g=j;
                    }
                    else if(status2 == false){
                        ele_array_ ="array_" +i +"_"+g;
                        clearInterval(interval);
                        localcheck=false;
                        status1 = true;
                        buttonPlay(i,g,boarddata.board.column_size);
                        scanningrow();
                        return;
                    }
                }
                if(t == buttonnum&&buttonnum!=1){
                    setTimeout(function() {
                        ele_array_ = "array_" + i +"_"+ j;
                        document.getElementById(ele_array_).style.border = "3px black solid" ;
                    }, timing)
                }
            }, timing * (s))
        }
    }
    interval = setInterval(function() {
        s = 0
        t = 0
        for(let j = 0; j < boarddata.board.column_size; j++){
            ele_array_ = "array_" + i +"_"+ j;
            if(document.getElementById(ele_array_).style.visibility != "hidden"){
                s = s+1
                setTimeout(function() {
                    t = t+1
                    ele_array_ = "array_" + i +"_"+ g;
                    document.getElementById(ele_array_).style.border = "3px black solid" ;
                    if(globalcheck == true&&localcheck==true){
                        if(status2 == true){
                            ele_array_ = "array_" + i +"_"+ j;
                            document.getElementById(ele_array_).style.border = "5px green solid" ;
                            check3=true;
                            g=j;
                        }
                        else if(status2 == false){
                            ele_array_ ="array_" +i +"_"+g;
                            clearInterval(interval);
                            localcheck=false;
                            status1 = true;
                            buttonPlay(i,g,boarddata.board.column_size);
                            scanningrow();
                            return;
                        }
                    }
                    if(t == buttonnum&&buttonnum!=1){
                        setTimeout(function() {
                            ele_array_ = "array_" + i +"_"+ j;
                            document.getElementById(ele_array_).style.border = "3px black solid" ;
                        }, timing)
                    }
                }, timing *(s))
            }
        }
    }, timing*buttonnum)
}
function goBackBoard(x)//回原面板
{
    if(x==1&&globalcheck == true)
    return;
    if(boxList.length > 0 && tempStringForKeyBoard != "") boxList.pop();
    if(tempStringForKeyBoard != "")
    {
        boxList.push([
            tempStringForKeyBoard,
            null,
            "black"
        ]);
        tempStringForKeyBoard = "";
    }

    isLinkedBoard = false;
    getBoard(boardsID);
}

function buttonPlay(x,y,w,z)//點擊的反應 上方輸入欄
{   
    let eleButtonVoiceId = "button_" + x + '_' + y + "_voice";
    let voiceEle = document.getElementById(eleButtonVoiceId);
    let posValue = x * w + y;
    let valueOfStringNum = stringNum.indexOf(posValue);
    let buttonID = boarddata.board.buttons[posValue].id;
    let buttonString = stringList[valueOfStringNum]
    let buttonImage = boarddata.board.buttons[posValue].image;
    let buttonColor = "Black";
    let buttonType = boarddata.board.buttons[posValue].category;

    if(boarddata.board.buttons[posValue].is_hyperlink_inside)//有連結則連到子面板
    {
        if(z==1&&globalcheck == true)
        return;
        isLinkedBoard = true;
        getBoard(boarddata.board.buttons[posValue].hyperlink);
    }
    else
    {
        if(buttonType == 0)//普通按鈕
        {
            if(!boarddata.board.buttons[posValue].is_image_enable)
            {
                buttonColor = boarddata.board.buttons[posValue].label_color;
                buttonImage = null;
            }
            else
            {
                buttonColor = boarddata.board.buttons[posValue].name_color;
            }
            
            //--
            boxList.push([
                buttonString,
                buttonImage,
                buttonColor
            ]);
            //--
            ajaxForLogs(apiLogAddButton,buttonID);
            stringBoxValue();
            //console.log(voiceEle)
            voiceEle.play();
        }
        else if(buttonType == 1)//字母鍵盤的回饋
        {
            buttonImage = null;
            buttonColor = "red";
            if(boxList.length > 0 && tempStringForKeyBoard != "") boxList.pop();
            if(buttonString != "Space")
            {
                tempStringForKeyBoard += buttonString;
                boxList.push([
                    tempStringForKeyBoard,
                    buttonImage,
                    buttonColor
                ]);

                voiceEle.play();
            }
            else if (buttonString == "Space" && tempStringForKeyBoard!= "")//字母鍵盤裡的空白鍵
            {
                buttonColor = "black";
                boxList.push([
                    tempStringForKeyBoard,
                    buttonImage,
                    buttonColor
                ]);
                
                var VoiceURL = "http://120.113.173.182:8000/ViewBoard/voices/new?" + "text=" + encodeURIComponent(tempStringForKeyBoard) ;
                voiceEle.src = VoiceURL;

                voiceEle.play();
                
                tempStringForKeyBoard = "";
            }
            stringBoxValue();
        }
    }
}


function getBoard(ID)
{
    boarddata = "";
    $.ajax({
        url: VIEWBOARD_API+ID,
        type: "GET",
        headers:{
            'Authorization':'Bearer '+ token
        },
        dataType: "json",
        success: function(data, status, xhr) {
            boarddata = "";
            boarddata = data;
            showBoard();
        },
        error: function(jqXhr, textStatus, errorMessage) {
            console.log("failure:" + errorMessage);
            alert("登入過期，回首頁");
            window.href("Login.html");
        }
    });
}


//字串的文字輸出
function stringBoxValue(){
    let style1 = 'height:100%;text-align:center;color:black';
    let style2 = 'text-align:center;height:0%;overflow:hidden;color:#000000;font-size:vmin;';
    let photosrc = ""
    
    tempstring = "";
    document.getElementById("stringBox").innerHTML = "";
    for(i=0;i<boxList.length;i++){

        let strlen = boxList[i][0].length;
        let gridSize = strlen/5;
        if(gridSize<1) gridSize = 1;
        gridSize = Math.round(gridSize);
        tempstring += (boxList[i][0]+ ',');
        if ( boxList[i][1] != null)
        {
            style1 = 'height:30%;font-size:0.85rem; align-items: center;text-align:center;overflow:hidden;color:' + boxList[i][2];
            style2 = 'text-align:center;height:70%;overflow:hidden;color:#000000;font-size:vmin;';
            photosrc = "http://120.113.173.182:8000/EditBoard/images/" + boxList[i][1];
            //console.log(photosrc)
        }
        else
        {
            style1 = 'height:100%;font-size:'+ 3.5/strlen +'rem;text-align:center;overflow:hidden;color:' + boxList[i][2];
            style2 = 'text-align:center;height:0%;overflow:hidden;color:#000000;font-size:vmin;';
            photosrc = ""
        }
            
        
        document.getElementById("stringBox").innerHTML += 
        '<div class="col-' +gridSize+ ' noPadding"><div class = "align-self-center" style="'+style1+'">'+ boxList[i][0] +'</div>\
         <div class = "align-self-center" style="'+ style2 +'">\
            <img src = "'+ photosrc +'" style = "vertical-align:middle; max-height:100%; max-width:100%; width:auto; height:auto;"></img>\
        </div></div>'
    }

}



//字串的聲音輸出
function stringboxVoice(){
    stringOfBox = tempstring;
    //console.log(stringOfBox);
    stringVoiceURL = "http://120.113.173.182:8000/ViewBoard/voices/new?" + "text=" + encodeURIComponent(stringOfBox) ;
    //console.log(stringVoiceURL);
    document.getElementById("string_box_Voices").src = stringVoiceURL;


    ajaxForLogs(apiLogPlayBox,stringOfBox);
}

//之後加入字和詞的分別後，要重新改寫
//刪除陣列最後一個
function stringboxDelete(){

    tempStringForKeyBoard = "";
    //--
    t = boxList.pop()[0];
    console.log(t)
    //--
    stringBoxValue();

    ajaxForLogs(apiLogDeleteSingleButton,t);

}

//之後加入字和詞的分別後，要重新改寫
//清空陣列
function stringboxClear(){
    tempStringForKeyBoard = "";
    stringOfBox = tempstring;
    ajaxForLogs(apiLogDeleteAllButton,stringOfBox);
    //--
    boxList = [];
    //--
    stringBoxValue();
}



function ajaxForLogs(api,content)
{   
    apiUrl = api+content;
    $.ajax({
        url:apiUrl,
        type:'Post',
        headers:{
            'Authorization':'Bearer '+ token
        },
        success:function(data){
            
            //console.log("success to do" + apiUrl);
        },
        error:function (xhr, thrownError,errorMessage) {
            console.log("failure:" + errorMessage);
        }
    });
}



