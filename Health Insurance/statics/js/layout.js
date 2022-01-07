
var elements=document.getElementsByClassName('nav-link');
for (i = 0, len = elements.length; i < len; i++) {
  elements[i].style.color = 'white';
}
for (element in elements){
    elements[element].onmouseover=function(){this.style.backgroundColor='red'; this.style.color="blue"};
    elements[element].onmouseout=function(){this.style.backgroundColor='transparent'; this.style.color="white";};
};

$('#Remove').on('click', function() {
    
  $(this).val('');
});
$('#Remove').on('mouseleave', function() {
  if ($(this).val() == '') {
    $(this).attr('placeholder');
  }
});

$('.add_phone').on('click',function(){
$('.contacts').append("<div id='plus-contact'><input class='form-item input ' type='tel' name='Phone' > <a class='btn btn-info' id='remove_phone'style='margin-top : -10px;' placeholder='+321432123' onclick='  this.parentElement.remove();return false;' ><i class='fas fa-minus-square'></i></a></div>")

return false;
});

function remove_me(){
  this.parentElement.remove();
  return false;
  };

var element=document.getElementById('profile');
element.onclick=function(){
    var email=prompt('please enter you Email:');
    if(email) window.location.replace(`/customer/Profile?Email=${email}`);
    return false;
};