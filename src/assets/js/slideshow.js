/*Slideshow code */

var slideIndex = [1,1];
var slideId = ["mySlides1", "mySlides2"]


export function plusSlides(n, no) {
  showSlides(slideIndex[no] += n, no);
  console.log("plusSlides")
}

export function showSlides(n, no) {
  var i;
  var x = document.getElementsByClassName(slideId[no]);
  if (n > x.length) {slideIndex[no] = 1}    
  if (n < 1) {slideIndex[no] = x.length}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";  
  }
  x[slideIndex[no]-1].style.display = "block";  
}