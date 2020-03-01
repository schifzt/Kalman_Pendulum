fname = "./observe.csv";
// labels_arr = ["time", "x2", "y2"];
labels_arr = ["time", "x2"];
g1 = new Dygraph(
    document.getElementById("graphdiv1"), fname, {
        labels: labels_arr,
        colors: ["#FF7F7F"],
        ylabel: 'Observe',
        highlightSeriesOpts: {
            strokeWidth: 2,
            strokeBorderWidth: 3,
            highlightCircleSize: 5
        }
    }
);

fname = "./sim_pen.csv";
labels_arr = ["time", "x1", "y1", "x2", "y2"];
g2 = new Dygraph(
    document.getElementById("graphdiv2"), fname, {
        labels: labels_arr,
        // colors: ["#FFA521", "#7FF97F", "#FF7F7F", "#8884d8"],
        colors: ["#FFA521", "#00FF00", "#FF7F7F", "#8884d8"],
        ylabel: 'Sim.',
        highlightSeriesOpts: {
            strokeWidth: 2,
            strokeBorderWidth: 3,
            highlightCircleSize: 5
        }
    }
);


fname = "./kalman_pen.csv";
labels_arr = ["time", "x1", "y1", "x2", "y2"];
g3 = new Dygraph(
    document.getElementById("graphdiv3"), fname, {
        labels: labels_arr,
        // colors: ["#FFA521", "#7FF97F", "#FF7F7F", "#8884d8"],
        colors: ["#FFA521", "#00FF00", "#FF7F7F", "#8884d8"],
        ylabel: 'Kalman',
        highlightSeriesOpts: {
            strokeWidth: 2,
            strokeBorderWidth: 3,
            highlightCircleSize: 5
        }
    }
);

gs = [g1, g2, g3];
var sync = Dygraph.synchronize(gs);
sync = Dygraph.synchronize(gs, {
    zoom: true,
    selection: true,
});

// g2.setVisibility("x1", false);
// g2.setVisibility("y1", false);
