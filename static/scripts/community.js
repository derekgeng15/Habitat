async function loadPosts(){
    response = await data
    for(i =  response.posts.length - 1; i >= 0; i--){
        title = response.posts[i].title
        posts = document.getElementById('posts')
        post = document.createElement('div')
        post.className += 'post row'
        ptitle = document.createElement('a')
        ptitle.href = BASE + habitat + '/posts/' + i
        ptitle.className += 'col-10 post-title'
        ptitle.appendChild(document.createTextNode(title))
        post.appendChild(ptitle)
        posts.appendChild(post)
        document.getElementById('post-btn').onclick = function(){window.location = BASE + habitat + '/newpost'}
        document.getElementById('users').innerHTML = 'Users: ' + response.users
    }
}
loadPosts()
    

