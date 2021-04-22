const electron = require('electron');
const path = require('path');
const {remote} = require('electron')
let {PythonShell} = require('python-shell');

var timeText = document.getElementById("newClock"); //This is the clock
var speakButton = document.getElementById("announceButton");//This button is to start the speech recognition
var correctButton = document.getElementById("correctButton");//send the announcement text to similarity match
var announcementIcon = document.getElementById("btnIcon");//this is also for
var engMessage = document.getElementById("engMessage");//this is announcement text
var norMessage = document.getElementById("norMessage");//this is announcement text
var speaking = false;//boolean to check either speaking or not

//var info = new PythonShell('../new_thread_file.py', mainElectronlocation);

var messageFromBack = '';
var englishFlag = document.getElementById("engBtn")
var norFlag = document.getElementById("norBtn")
// header utilities
document.getElementById('minimize').addEventListener('click', minimizeWindow);
document.getElementById('maximize').addEventListener('click', maximizeWindow);
document.getElementById('close').addEventListener('click', closeWindow);

engMessage.innerHTML = "This metro and the station are now being evacuated. Please leave the metro now and get the staff's help to exit the station.";
norMessage.innerHTML = "Denne metroen og stasjonen evakueres nå. Gå fra metroen nå og få personalets hjelp til å gå ut av stasjonen.";

function minimizeWindow(){
    var window = remote.getCurrentWindow();
    window.minimize();
}

function maximizeWindow(){
    var window = remote.getCurrentWindow();
    window.isMaximized()?window.unmaximize() : window.maximize();
}

function closeWindow(){
    var window = remote.getCurrentWindow()
    window.close();
}
//defining language code
var lanCode = "en-US"
var translator_target_code = "no"

englishFlag.addEventListener('click', function(){
    lanCode = "en-US"
    translator_target_code = "no"
    document.getElementById("englishBtn").src='images/en-gb-tick.png';
    document.getElementById("norwegianBtn").src='images/nb-no.png';
});

norFlag.addEventListener('click', function(){
    lanCode = "nb-NO"
    translator_target_code = "en"
    document.getElementById("norwegianBtn").src='images/nb-no-tick.png';
    document.getElementById("englishBtn").src='images/en-gb.png';
    console.log(lanCode)
});

//var mainElectronlocation = { scriptPath: path.join(__dirname, ''),args:[lanCode], pythonPath: 'C:/Program Files/Python36/python'}
//Event listener for speak button



speakButton.addEventListener('click', function(){

    if (!speaking){
        speaking = true;
        announcementIcon.className="fa fa-microphone";
        document.getElementById('logo').src='images/warning_icon.jpg';
        info = new PythonShell('../new_thread_file.py',
            { scriptPath: path.join(__dirname, ''),args:[lanCode, translator_target_code], pythonPath: 'C:/Program Files/Python37/python'}
        );
        info.on("message", function(messageFromBackend){
            console.time("Speech-To-Text runtime >>");
            //console.log(messageFromBackend);
            split_Message(messageFromBackend)
            engMessage.innerHTML = split_Message(messageFromBackend)[0];
            norMessage.innerHTML = split_Message(messageFromBackend)[1];
            messageFromBack = split_Message(messageFromBackend)[0];
            console.timeEnd("Speech-To-Text runtime >>");

        });
    }else{
        speaking = false;
        /*buttonImage.src=("images/mic_on_small.png");*/
        announcementIcon.className="fa fa-microphone-slash";
        document.getElementById('logo').src='images/omu.png';
        console.log("No");
        engMessage.innerHTML = "";
        norMessage.innerHTML = "";
        info.childProcess.kill('SIGINT');//terminating python background
    }
});


correctButton.addEventListener('click', function(){

    info.childProcess.kill('SIGINT');
    announcementIcon.className="fa fa-microphone-slash";
    //console.log("This is to script:",messageFromBack);
    correct = new PythonShell('../announcement_similarity.py',
        { scriptPath: path.join(__dirname, ''),args:[messageFromBack, translator_target_code], pythonPath: 'C:/Program Files/Python37/python'}
    );
    correct.on("message", function(correctedMessage){
        console.time("Announcement correction runtime >>");
        engMessage.innerHTML = split_Message(correctedMessage)[0];
        norMessage.innerHTML = split_Message(correctedMessage)[1];
        console.log("Matching:", split_Message(correctedMessage)[0], split_Message(correctedMessage)[2]);
        console.timeEnd("Announcement correction runtime >>");
//        messageFromBack = split_Message(correctedMessage)[0];
    });

});

function split_Message(message){
    splitted_message = message.split("++ ")
    return splitted_message
    }


//All the code for the clock
var clock = new Vue({
    el: '#top_left_div',
    data: {
        time: '',
        date: ''
    }
});

var week = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
var timerID = setInterval(updateTime, 0);
updateTime();
function updateTime() {
    var cd = new Date();
    clock.time = zeroPadding(cd.getHours(), 2) + ':' + zeroPadding(cd.getMinutes(), 2) + ':' + zeroPadding(cd.getSeconds(), 2);
    clock.date = zeroPadding(cd.getFullYear(), 4) + '-' + zeroPadding(cd.getMonth()-1, 2) + '-' + zeroPadding(cd.getDate()+5, 2) + ' ' + week[cd.getDay()];
};

function zeroPadding(num, digit) {
    var zero = '';
    for(var i = 0; i < digit; i++) {
        zero += '0';
    }
    return (zero + num).slice(-digit);
}

//
//var text = document.getElementById("stot")
//
//var speech = ""
//var timer = setTimeout(getText(), 1000)
////setInterval
//function getText(){
//    // get data from the python script
//
//    eel.generateSpeechToText()(function(ret){
//        console.log("This is not speech: ", ret);
//        if (ret==null){
//            clearTimeout(timer)
//            console.log("This is if condition with ret", ret)
//        }
//        speech = speech + " "+ret;
//        text.innerHTML = speech;
//    });
//
//    setTimeout(getText(), 1000)
//}
//
