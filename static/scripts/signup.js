BASE = 'http://127.0.0.1:5000/'
document.getElementById('sign-up').onclick =
function(){
    fetch(BASE + 'database/users/' + document.getElementById('username').value, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({
            'email': document.getElementById('email').value,
            'password': document.getElementById('username').value
        })
    })
    .then(resp => resp.json())
    .then(function(data){
        console.log(data)
        window.location = BASE + 'users/' + document.getElementById('username').value
    })
    .catch((error)=>{console.error('Error', error)})
}