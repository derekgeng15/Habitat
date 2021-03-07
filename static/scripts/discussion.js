messageNode = document.getElementById('msg-input')


messageNode.addEventListener('keydown',
function(event){
    if (event.key === 'Enter'){
        msg = document.createElement('div')
        msg.className += 'sent-msg'
        msgInbox = document.createElement('div')
        msgInbox.className += 'sent-msg-inbox'
        p = document.createElement('p')
        p.appendChild(document.createTextNode(messageNode.value))
        msgInbox.appendChild(p)
        time = document.createElement('span')
        time.className += 'time'
        time.innerHTML = '&nbsp You &nbsp &nbsp' + (new Date()).getHours() + ':' + (new Date()).getMinutes() + ' Today'
        msgInbox.appendChild(time)
        msg.appendChild(msgInbox)
        console.log(msg)
        chat = document.createElement('div')
        chat.className += 'sent-chats'
        chat.appendChild(msg)
        console.log(chat)
        con = document.createElement('div')
        con.className += 'sent-chats-img'
        img = document.createElement('img')
        img.src = imgurl
        con.appendChild(img)
        chat.appendChild(con)
        document.getElementById('msg-page').appendChild(chat)
        messageNode.value = ""

    }
})

async function set(){
    response = await data
    document.getElementById('chat-title').innerHTML = '&nbsp' + username

}
set()

{/*  <div class="sent-chats"> 
            <div class="sent-msg">
                <div class="sent-msg-inbox">
                    <p>Sounds good. Are we still having our video call later today? </p>
                    <span class="time">&nbsp You &nbsp &nbsp 11:42 AM, Today</span>
                </div>
            </div>
            <div class="sent-chats-img">
                <img src="{{url_for('static', filename = 'images/pfp.jpg')}}">
            </div>
    </div>*/}