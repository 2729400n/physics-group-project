const fieldCanvas = new OffscreenCanvas(400,400);

function drawInitialState(state,...params){

    let ctx=fieldCanvas.getContext('2d',{alpha:false,'willReadFrequently':true});

    ctx.clearRect(0,0,fieldCanvas.width,fieldCanvas.height);
    ctx.lineWidth=1;
    ctx.fillStyle = '#ff0000';
    ctx.strokeStyle = '#ff0000';
    switch (state[0]) {
        case 'A':

            ctx.beginPath();
            ctx.moveTo(fieldCanvas.width,fieldCanvas.height/2);
            ctx.arc(fieldCanvas.width/2,fieldCanvas.height/2,fieldCanvas.width/2,0,2*Math.PI,false);
            ctx.closePath()
            break;
        case 'B':
            ctx.save()
            ctx.moveTo(0,0);
            ctx.beginPath()
            ctx.lineTo(0,fieldCanvas.height);
            ctx.transform(1,0,0,1,fieldCanvas.width,0);
            ctx.moveTo(0,0);
            ctx.lineTo(0,fieldCanvas.height);
            ctx.restore();
    
        default:
            break;
    }
    
    let fieldArray = ctx.getImageData()
    
}


function preformDiffusion() {
    
}