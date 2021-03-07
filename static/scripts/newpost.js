
document.getElementById('submit-btn').onclick =
    function(){
        console.log(userID)
        fetch(BASE + 'database/' + habitat + '/posts',{
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                'title': document.getElementById('title-input').value,
                'content': document.getElementById('content-input').value,
                'userID': userID
            })
        })
        .then(resp => resp.json())
        .then(function(data){
            console.log(data)
            window.location = BASE + habitat + '/posts/' + (data.posts.length - 1)
        })
        .catch((error)=>{console.error('Error', error)})
    }