var canvas, ctx;
var w, h;
var x = [];
var x_estm = [];
var stop_time;
var frame_rate = 0.005;
var load_count = 0;

const result = "sim_pen.csv"
const kalman = "kalman_pen.csv"
const previous = 1; //previous ? sec



var parseCSV = function(str) { //{{{
    var ret = [];
    var row = str.split("\n"); //each row

    stop_time = row.length; //down...down...
    var a = row[0].split(",")[0];
    var b = row[1].split(",")[0];
    frame_rate = parseFloat(b - a);

    for (var i = 1; i < row.length; ++i) {
        ret[i] = row[i].split(',');
    }
    return ret
}; //}}}

var getCSV = function(fname) { //{{{
    var req = new XMLHttpRequest();
    req.open("get", fname, true);
    req.send(null);
    req.onload = function() {
        if (fname === result) {
            x = parseCSV(req.responseText);
        } else if (fname === kalman) {
            x_estm = parseCSV(req.responseText);
        }
    };
}; //}}}

var drawDoublePendulum = function() {
    var t = 0;

    function render() {
        // Canvas全体をクリア
        ctx.clearRect(0, 0, w, h);

        //loop
        if (t + previous >= stop_time) {
            t = 0;
        } else {
            t++;
        }

        // console.log(frame_rate);
        // console.log(x_estm[0][0])

        for (var offset = previous; offset > 0; offset -= Math.max(parseInt(previous / 10), 1)) {
            var x1 = 70 * parseFloat(x[t + offset][1]) + w / 2;
            var y1 = 70 * parseFloat(x[t + offset][2]) * (-1) + h / 2;
            var x2 = 70 * parseFloat(x[t + offset][3]) + w / 2;
            var y2 = 70 * parseFloat(x[t + offset][4]) * (-1) + h / 2;

            var x1_estm = 70 * parseFloat(x_estm[t + offset][1]) + w / 2;
            var y1_estm = 70 * parseFloat(x_estm[t + offset][2]) * (-1) + h / 2;
            var x2_estm = 70 * parseFloat(x_estm[t + offset][3]) + w / 2;
            var y2_estm = 70 * parseFloat(x_estm[t + offset][4]) * (-1) + h / 2;



            ctx.globalAlpha = offset / previous;

            //-------------------------
            //Result
            //-------------------------
            ctx.lineWidth = 1.5; //{{{

            //l1
            ctx.strokeStyle = "#8884d8"; //pale blue
            ctx.beginPath();
            ctx.moveTo(w / 2, h / 2);
            ctx.lineTo(x1, y1);
            ctx.stroke();

            //l2
            ctx.strokeStyle = "#8884d8"; //pale blue
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();

            //Axes projections
            ctx.fillStyle = "#10FCA7"; //green
            ctx.fillRect(x1, h - 20, 5, 5);
            ctx.fillRect(20, y1, 5, 5);

            ctx.fillStyle = "#FFA521"; //orange
            ctx.fillRect(x2, h - 20, 5, 5);
            ctx.fillRect(20, y2, 5, 5);


            //line to projections
            if (offset == previous) {
                ctx.lineWidth = 1;

                ctx.strokeStyle = "#dedede"; //gray
                ctx.beginPath();
                ctx.moveTo(x1, h - 20);
                ctx.lineTo(x1, y1);
                ctx.lineTo(20, y1);
                ctx.stroke();

                ctx.strokeStyle = "#DEDEDE"; //gray
                ctx.beginPath();
                ctx.moveTo(x2, h - 20);
                ctx.lineTo(x2, y2);
                ctx.lineTo(20, y2);
                ctx.stroke();
            } //}}}

            //-------------------------
            //Kalman
            //-------------------------
            ctx.lineWidth = 1.5; //{{{

            //l1
            ctx.strokeStyle = "#FF7F7F"; //pale pink
            ctx.beginPath();
            ctx.moveTo(w / 2, h / 2);
            ctx.lineTo(x1_estm, y1_estm);
            ctx.stroke();

            //l2
            ctx.strokeStyle = "#FF7F7F"; //pale pink
            ctx.beginPath();
            ctx.moveTo(x1_estm, y1_estm);
            ctx.lineTo(x2_estm, y2_estm);
            ctx.stroke();

            //Axes projections
            ctx.fillStyle = "#10FCA7"; //green
            ctx.fillRect(x1_estm, h - 10, 5, 5);
            ctx.fillRect(10, y1_estm, 5, 5);

            ctx.fillStyle = "#FFA521"; //orange
            ctx.fillRect(x2_estm, h - 10, 5, 5);
            ctx.fillRect(10, y2_estm, 5, 5);


            //line to projections
            if (offset == previous) {
                ctx.lineWidth = 1;

                ctx.strokeStyle = "#dedede"; //gray
                ctx.beginPath();
                ctx.moveTo(x1_estm, h - 10);
                ctx.lineTo(x1_estm, y1_estm);
                ctx.lineTo(10, y1_estm);
                ctx.stroke();

                ctx.strokeStyle = "#dedede"; //gray
                ctx.beginPath();
                ctx.moveTo(x2_estm, h - 10);
                ctx.lineTo(x2_estm, y2_estm);
                ctx.lineTo(10, y2_estm);
                ctx.stroke();

            } //}}}

        }

    }

    setInterval(render, frame_rate * 1000); //to milisec
};

window.onload = new function() {
    canvas = document.getElementById('myCanvas');
    ctx = canvas.getContext('2d');
    w = canvas.width;
    h = canvas.height;

    getCSV(result);
    getCSV(kalman);
    setTimeout(drawDoublePendulum, 1000);

}
