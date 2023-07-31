let show_password=document.querySelector(".body .inputs span");
let password_area=document.querySelector(".body .inputs input#password");
let less_than =document.querySelector(".body .up_bar span:first-child");
let text_in_scound=document.querySelector(".body .up_bar span:last-child");

show_password.onclick=function(){
    if( password_area.type==="password"){
  this.style.backgroundColor=" #c31dd1"
    password_area.type="text";
    }else {
        show_password.style.backgroundColor="transparent"
        password_area.type="password";
    }
  
}

less_than.onclick=function(){
    if(text_in_scound.textContent=="Sign in"){
        window.open("../log_in.html","_self",true)
    }
}