//foction created for optimize the navbar at mobile screen
const nav_header=document.querySelector(".desktop-navbar");
const mob_nav=document.querySelector('.mobile-view-icon');
const toggleNavbar=() =>{
    nav_header.classList.toggle('active')
};
mob_nav.addEventListener('click', ()=>toggleNavbar());

//Login/Signup popup code here

//function scrollToTop is created for scroll bottom to top -----start here....
const scroll_top=document.querySelector(".move-top");
function scrollToTop(){
    const scrollStep=-window.scrollY/20;
    const scrollInterval=setInterval(function(){
        if(window.scrollY !==0){
            window.scrollBy(0,scrollStep);
        }else{
            clearInterval(scrollInterval);
        }
    }, 15)
}

scroll_top.addEventListener("click",scrollToTop)