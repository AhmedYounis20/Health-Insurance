
var elements=document.getElementsByClassName('nav-link');
for (element in elements){
    elements[element].onmouseover=function(){this.style.backgroundColor='red';};
    elements[element].onmouseout=function(){this.style.backgroundColor='transparent';};
}
function admin(){
    var board = document.getElementById('admin-board')
    if (board.style.display=="none") board.style.display='block';
    else board.style.display='none'; 
}