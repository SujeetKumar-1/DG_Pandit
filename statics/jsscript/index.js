//foction created for optimize the navbar at mobile screen
const nav_header=document.querySelector(".desktop-navbar");
const mob_nav=document.querySelector('.mobile-view-icon');
const toggleNavbar=() =>{
    nav_header.classList.toggle('active');
};
    
mob_nav.addEventListener('click', ()=>toggleNavbar());

/* **********************************************
function scrollToTop is created for scroll bottom to top -----start here....
*************************************************/
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

/* **********************************************
Site carousel imgase code for slide the image at header of website
*************************************************/
let carousel_images=[
    {
        name:"Ganesh Lakshmi Puja",
        desc:"This Puja can be performed on any occasion like starting of a new Business, Job, Shifting to a New House or any other Festival related to Lord Ganesha or Goddess Maha Lakshmi",
        image:"/statics/Image/slide1.jpeg",
    },
    {
        name:"Durga Puja",
        desc:"This puja of the goddess Maa Durga is performed to obtain spiritual knowledge, peace, and prosperity",
        image:"/statics/Image/slide2.jpg",
    },
    {
        name:"Ganesh Lakshmi Puja",
        desc:"This Puja can be performed on any occasion like starting of a new Business, Job, Shifting to a New House or any other Festival related to Lord Ganesha or Goddess Maha Lakshmi",
        image:"/statics/Image/slide3.jpeg",
    },
];

const carousel = document.querySelector('.carousel');
let sliders=[];
let slideIndex=0; //track current slide

 const createSlide=()=>{
    if(slideIndex>=carousel_images.length){
        slideIndex=0;
    }

    //create DOM Elements
    let slide=document.createElement('div');
    let imgElement =document.createElement('img');
    let content =document.createElement('div');
    let h1=document.createElement('h1');
    let p=document.createElement('p');

    //now attaching all elements
    imgElement.appendChild(document.createTextNode(''));
    h1.appendChild(document.createTextNode(carousel_images[slideIndex].name));
    p.appendChild(document.createTextNode(carousel_images[slideIndex].desc));
    content.appendChild(h1);
    content.appendChild(p);
    slide.appendChild(content);
    slide.appendChild(imgElement);
    carousel.append(slide);

    //setting images
    imgElement.src=carousel_images[slideIndex].image;
    slideIndex++;

    //setting elements class name
    slide.className="slider";
    content.className="slide-content";
    h1.className="slide-title";
    p.className="slide-desc";

    sliders.push(slide);
    if(sliders.length>1){
        sliders[0].style.marginLeft=`calc(-${100*(sliders.length-2)}% - ${30*(sliders.length-2)}px)`;
    }
 }

 for(let i=0; i<3; i++){
    createSlide();
 }

 setInterval(()=>{
    createSlide();
 }, 8000);


 /* **********************************************
    card slider container properties
*************************************************/

let cardContainers= [...document.querySelectorAll('.card-container')];
let preBtn= [...document.querySelectorAll('.pre-btn')];
let nxtBtn= [...document.querySelectorAll('.next-btn')];

cardContainers.forEach((item, i)=>{
    let containerDimensions= item.getBoundingClientRect();
    let containerWidth= containerDimensions.width;

    nxtBtn[i].addEventListener('click',()=>{
        item.scrollLeft += containerWidth - 90;
    });

    preBtn[i].addEventListener('click', ()=>{
        item.scrollLeft-=containerWidth + 90;
    });;
});
