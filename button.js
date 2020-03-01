(function(win, doc) {
    var slider_elms = doc.querySelectorAll("#filter");

    //-------------------------------------------------------
    //Init
    //-------------------------------------------------------
    display_elms[0].innerText = slider_elms[0].value;
    display_elms[1].innerText = slider_elms[1].value;
    display_elms[2].innerText = slider_elms[2].value;

    //-------------------------------------------------------
    //Event
    //-------------------------------------------------------

    //{{{
    slider_elms[0].addEventListener("input", function() {
        display_elms[0].innerText = this.value;
    }, false);

    slider_elms[0].addEventListener("change", function() {
        display_elms[0].innerText = this.value;
    }, false);

    //-------------------------------------------------------
    slider_elms[1].addEventListener("input", function() {
        display_elms[1].innerText = this.value;
    }, false);

    slider_elms[1].addEventListener("change", function() {
        display_elms[1].innerText = this.value;
    }, false);

    //-------------------------------------------------------
    slider_elms[2].addEventListener("input", function() {
        display_elms[2].innerText = this.value;
    }, false);

    slider_elms[2].addEventListener("change", function() {
        display_elms[2].innerText = this.value;
    }, false);

    //-------------------------------------------------------

    //}}}


    //-------------------------------------------------------
    //send button
    //-------------------------------------------------------
    send_button = doc.getElementById("send");
    send_button.addEventListener("click", function() {
        for(var i=0;i<slider_elms.length;i++){
            console.log(slider_elms[i].value);
        }
    });

})(this, document);
