const BASE = 'http://127.0.0.1:5000/'
const data = fetch(BASE + 'database/' + habitat)
.then((resp) => resp.json())
.then((jreps)=>{
    return jreps
})
const setHabitat = async() =>{
    const response = await data
    document.getElementById('habitat-name').innerHTML = response.name
    document.getElementById('habitat-name').href = BASE + habitat
    document.getElementById('community-btn').onclick = function(){window.location = BASE + habitat}
    document.getElementById('dis-btn').onclick = function(){window.location = BASE + habitat + '/discussion'}
}
setHabitat()