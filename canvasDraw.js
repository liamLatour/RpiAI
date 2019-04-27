var SimplexNoise = require('simplex-noise');

winWidth = window.innerWidth;
winHeight = window.innerHeight;

// Auto scale canvas
var can = document.getElementById("myCanvas");
can.style.width = winWidth + "px";
can.style.height = winHeight + "px";

// Draw on it
var ctx = can.getContext("2d");
ctx.canvas.width  = winWidth
ctx.canvas.height = winHeight;

let phase = 0;
let zoff = 0;
let madness = 1;

var simplex = new SimplexNoise();
ctx.translate(can.width/2, can.height/2);
ctx.lineWidth = 10;
ctx.strokeStyle = "#1031ed";

function draw(){
    ctx.clearRect(-can.width/2, -can.height/2, can.width, can.height);

    ctx.beginPath();
    for (let a = 0; a < 2*Math.PI; a += 0.1) {
        let xoff = (Math.cos(a + phase)+1)*madness;
        let yoff = (Math.sin(a + phase)+1)*madness;
        let r = (simplex.noise3D(xoff, yoff, zoff)+10)*winHeight/40;
        let x = r * Math.cos(a);
        let y = r * Math.sin(a);

        if(a == 0){
            ctx.moveTo(x, y);
        }
        else{
            ctx.lineTo(x, y);
        }
    }
    ctx.closePath();
    ctx.stroke();
    phase += 0.003;
    zoff += madness/100;//0.005;
}
setInterval(draw, 10);