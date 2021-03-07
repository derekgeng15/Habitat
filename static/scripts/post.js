
function loadPost(){
    console.log(BASE + 'database/' + habitat)
    fetch(BASE + 'database/' + habitat)
    .then((resp) => resp.json())
    .then(function(data){
        document.getElementById('post-title').innerHTML = data.posts[parseInt(postID)].title
        document.getElementById('post-body').innerHTML = data.posts[parseInt(postID)].content

    }) 
    .catch(function(error){
        console.log(error)
    })
}

loadPost()