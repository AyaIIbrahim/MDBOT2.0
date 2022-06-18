const canvas = document.getElementById("particles-js");
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray;

// get mouse position
let mouse = {
    x: null,
    y: null,
    radius: (canvas.height/80) * (canvas.width/80)
}

window.addEventListener('mousemove',
    function(event) {
        mouse.x = event.x;
        mouse.y = event.y;
    }
);

// create particle
class Particle {
    constructor(x, y, directionX, directionY, size, color) {
        this.x = x;
        this.y = y;
        this.directionX = directionX;
        this.directionY = directionY;
        this.size = size;
        this.color = color;
    }
    // method to draw individual particle
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
        ctx.fillStyle = '#FFFFFF';
        ctx.fill();
    }
    // check particle position, check mouse position, move the particle, draw the particle
    update() {
        //check if particle is still within canvas and adjust how far they should go outside.
        if (this.x > canvas.width + 20 || this.x < -20 ) {
            this.directionX = -this.directionX;
        }
        if (this.y > canvas.height + 20 || this.y < -20) {
            this.directionY = -this.directionY;
        }

        //check collision detection - mouse position / particle position
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        let distance = Math.sqrt(dx*dx + dy*dy);

        let mouseDistance = Math.sqrt(dx*dx+dy*dy);


        if (distance*2 < mouse.radius + this.size){                                             //here you can tweak the radios of the circle
            if (mouse.x < this.x && this.x < canvas.width - this.size * 10) {                   //here you can change the speed
                this.x += 10;
            }
            if (mouse.x > this.x && this.x > this.size * 10) {
                this.x -= 10;
            }
            if (mouse.y < this.y && this.y < canvas.height - this.size * 10) {
                this.y += 10;
            }
            if (mouse.y > this.y && this.y > this.size * 10) {
                this.y -= 10;
            }

//            console.log("X",this.directionX)
//            console.log("Y",this.directionY)
            if (mouseDistance < 180) {
                
                this.directionX = -this.directionX
    
                this.directionY = -this.directionY
            }
            
        }
        // move particle
        this.x += this.directionX;
        this.y += this.directionY;
        // draw particle
        this.draw();

    }
}

// create particle array
function particel() {
    particlesArray = [];
    let numberOfParticles = (canvas.height * canvas.width) / 9000;
    for (let i = 0; i < numberOfParticles/2; i++) {                                       // can tweak number of particles here
        let size = (Math.random() * 5) + 1;
        let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
        let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
        let directionX = (Math.random() * 5) - 3;                                        //change min speed here
        let directionY = (Math.random() * 5) - 3;
        let color = '#FFFFFF';

        particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
    }
}

// check if particles are close enough to draw line between them
function connect(){
    let opacityValue = 1;
    for (let a = 0; a < particlesArray.length; a++) {
        for (let b = a; b < particlesArray.length; b++) {
            let distance = (( particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x))
            + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
            if (distance < (canvas.width/7) * (canvas.height/7)) {
                opacityValue = 1 - (distance/20000);
                let dx = mouse.x - particlesArray[a].x;
                let dy = mouse.y - particlesArray[a].y;
                let mouseDistance = Math.sqrt(dx*dx+dy*dy);
                if (mouseDistance < 180) {
                  ctx.strokeStyle='rgba(63, 136, 143,' + opacityValue + ')';                // once mouse gets too close
                } else {
                ctx.strokeStyle='rgba(159, 226, 191,' + opacityValue + ')';                 // nomral colour
                }
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                ctx.stroke();

// If you want to connect lines with Mouse.
                // ctx.lineWidth = 1;
                // ctx.strokeStyle = 'rgba(255,255,0,0.03)';
                // ctx.beginPath();
                // ctx.moveTo(mouse.x, mouse.y);
                // ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                // ctx.stroke();
            }
        }
    
    }
}
// animation loop
function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0,0,innerWidth, innerHeight);

    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
    }
    connect();
}
// resize event
window.addEventListener('resize', 
    function(){
        canvas.width = innerWidth;
        canvas.height = innerHeight;
        mouse.radius = ((canvas.height/80) * (canvas.height/80));
        particel();
        if (canvas.width <= 1520) {
            mouse.radius = 0
        };
    }
);

// mouse out event
window.addEventListener('mouseout',
    function(){
        mouse.x = undefined;
        mouse.x = undefined;
    }
)

particel();
animate();


// // check if particles are close enough to draw line between them
// function connect(){
//     let opacityValue = 1
//     for (let a = 0; a < particlesArray.length; a++) {
//         for(let b = a; b < particlesArray.length; b++) {
//             let distance = (( particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x))
//             + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y) - particlesArray[b]);
//             if (distance < (canvas.width/7) * (canvas.height/7)) {
//                 opacityValue = 1 - (distance/20000);
//                 ctx.strokeStyle = 'rgba(140,85,31,' + opacityValue + ')';
//                 ctx.beginPath();
//                 ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
//                 ctx.lineTo(particlesArray[b].x, particlesArray[a].y);
//                 ctx.stroke();
//             }
//         }
//     }
// }  


