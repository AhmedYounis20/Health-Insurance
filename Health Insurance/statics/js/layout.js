
var elements=document.getElementsByClassName('nav-link');
for (element in elements){
    elements[element].style.color="white";
    elements[element].onmouseover=function(){this.style.backgroundColor='red'; elements[element].style.color="blue"};
    elements[element].onmouseout=function(){this.style.backgroundColor='transparent'; this.style.color="white";};
};

