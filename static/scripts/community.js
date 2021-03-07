async function loadPosts(){
    response = await data
    for(i = 0; i < response.posts.length; i++){
        title = response.posts[0].title
        posts = document.getElementById('posts')
        post = document.createElement('div')
        post.className += 'post row'
        ptitle = document.createElement('a')
        ptitle.href = BASE + habitat + '/posts/' + i
        ptitle.className += 'col-10 post-title'
        ptitle.appendChild(document.createTextNode(title))
        post.appendChild(ptitle)
        posts.appendChild(post)
    }
}
loadPosts()
    

