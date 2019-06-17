(function(){
    'use strict';
    var canvas, ctx, width, height, barColors;
    var flux = [];
    var FLUXNumber = 16;
    var title = document.querySelector('#title');
    
    barColors = ['#c9c9c9', '#e0daba', '#831b87', '#afafaf'];
  
  
    function FLUX(canvas, minBarNum, maxBarNum, barWidth, barHeight, barColors) {
      this.barNum = minBarNum + Math.floor(Math.random()*(maxBarNum - minBarNum));;
      this.barWidth = barWidth;
      this.barHeight = barHeight;
      this.barColors = barColors;
      this.x = Math.floor(Math.random()*canvas.width);
      this.y = Math.floor(Math.random()*canvas.height);
      this.bars = [];
  
      //initialise bars
      var color;
      var initColorIndex = Math.floor(Math.random()*barColors.length);
      for(var i=0; i<this.barNum; i++) {
        var colorIndex = Math.floor(Math.random()*barColors.length);
        if(colorIndex==initColorIndex) colorIndex = colorIndex==(barColors.length-1)? 0 : colorIndex+1;
        this.bars[i] = {};
        //set bar colorIndex
        this.bars[i].colorIndex = colorIndex;
        //set bar color
        this.bars[i].color = this.barColors[this.bars[i].colorIndex];
        //set bar height
        this.bars[i].height = Math.floor(Math.random()*this.barHeight) + this.barHeight*0.2;
        //set bar width
        this.bars[i].width = this.barWidth;
        //set bar x
        this.bars[i].x = this.x + this.barWidth*i;
        //set bar center y
        this.bars[i].y = this.y - this.bars[i].height/2;
        //update color
        initColorIndex = colorIndex;
      }
    }
  
    FLUX.prototype.update = function() {
      for(var i=0; i<this.barNum; i++) {
        if(this.bars[i].y<0) {
          flux[i] = new FLUX(canvas, 10, 50, 2, 200, barColors);
        }
  
        if(Math.random()>0.7) {
          this.bars[i].y+=1;
        } else {
          this.bars[i].y-=2; 
        }
      }
    } 
  
    FLUX.prototype.draw = function(ctx) {
      for(var i=0; i<this.barNum; i++) {
        ctx.fillStyle = this.bars[i].color;
        ctx.fillRect(this.bars[i].x , this.bars[i].y, this.bars[i].width, this.bars[i].height );
      }
    }
  
  
  
  
    init();
    drawFrame();
  
    function init(){
      canvas = document.createElement('canvas');
      ctx = canvas.getContext('2d');
      document.body.appendChild(canvas);
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      window.addEventListener('resize', onWindowResize, false);
  
      for (var i=0; i<FLUXNumber; i++) {
        flux[i] = new FLUX(canvas, 10, 30, 2, 200, barColors);
      }
  
    }
  
    function drawFrame() {
      requestAnimationFrame(drawFrame);
      ctx.clearRect(0,0,width,height);
      for (var i=0; i<FLUXNumber; i++) {
        flux[i].draw(ctx);
        flux[i].update();
      }
  
    }
  
    function onWindowResize(event) {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
  
  
  
  
  }).call(this);