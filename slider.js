(function(win, doc) {
    var slider_elms = doc.querySelectorAll(".slider");
    var display_elms = doc.querySelectorAll(".display");

    //closure shoretens code!

    //-------------------------------------------------------
    //Init
    //-------------------------------------------------------
    for (var i = 0; i < slider_elms.length; i++) {
        display_elms[i].innerText = function(index) {
            return slider_elms[index].value;
        }(i);
    }

    //-------------------------------------------------------
    //Event
    //-------------------------------------------------------
    for (var i = 0; i < slider_elms.length; i++) {
        slider_elms[i].addEventListener("input", function(index) {
            return function() {
                display_elms[index].innerText = this.value;
            };
        }(i), false);

        slider_elms[i].addEventListener("change", function(index) {
            return function() {
                display_elms[index].innerText = this.value;
            };
        }(i), false);

    }

    //-------------------------------------------------------
    //send button
    //-------------------------------------------------------
    send_button = doc.getElementById("generate");
    send_button.addEventListener("click", function() {
        for (var i = 0; i < slider_elms.length; i++) {
            console.log(slider_elms[i].value);
        }
    });

})(this, document);
