/**Keeps track of the draggable div object */
export default class DragJS{
    constructor(dragDiv, dragHeader){
        this.dragDiv = dragDiv; //the element to be dragged.
        var pos1 = 0;
        var pos2 = 0;

        var pos3 = 0;//pos3 and pos4 are the x,y position of the mouse on click down.
        var pos4 = 0;
        dragHeader.onmousedown = dragMouseDown;
        //since we are assigning a function to an html object, we need to keep a reference of local variables
        
        /**Grab the current position and prepare the reactive functions. */
        function dragMouseDown(e){
            
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;//call this function on mouse click release
            document.onmousemove = elementDrag;//call this function when the mouse moves
        }
        /**Update the element's position as the user drags the mouse */
        function elementDrag(e){
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;//calcualte the delta position between the mouse drag event and when it was first held down
            pos2 = pos4 - e.clientY;//client is the position within the browser window
            
            
            pos3 = e.clientX;//keep track of the current position of the mouse
            pos4 = e.clientY;

            //update the current element's position
            dragDiv.style.top = (dragDiv.offsetTop - pos2) + "px" ;
            dragDiv.style.left = (dragDiv.offsetLeft - pos1) + "px";

        }
        /**Remove the reactive functions once the user lets go of the mouse click */
        function closeDragElement(){
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
    

}