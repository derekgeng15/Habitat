var posts = document.getElementById('posts')
function addPost(title){
    post = document.createElement('div')
    post.className += 'post row'
    ptitle = document.createElement('a')
    ptitle.href = 'http://127.0.0.1:5000/hello'
    ptitle.className += 'col-10 post-title'
    ptitle.appendChild(document.createTextNode(title))
    post.appendChild(ptitle)
    posts.appendChild(post)
    // post.appendChild(document.createTextNode(title))
    // posts.appendChild(post)
}
for(i = 1; i <= 13; i++)
    addPost('post ' + i)

button =  document.getElementById('community-btn')
button.onclick = function(){window.location='http://127.0.0.1:5000/hello'}
