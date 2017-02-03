!function(a,b){"use strict";function c(a){a=a||{};for(var b=1;b<arguments.length;b++){var c=arguments[b];if(c)for(var d in c)c.hasOwnProperty(d)&&("object"==typeof c[d]?deepExtend(a[d],c[d]):a[d]=c[d])}return a}function d(d,g){function h(){if(y){r=b.createElement("canvas"),r.className="pg-canvas",r.style.display="block",d.insertBefore(r,d.firstChild),s=r.getContext("2d"),i();for(var c=Math.round(r.width*r.height/g.density),e=0;c>e;e++){var f=new n;f.setStackPos(e),z.push(f)}a.addEventListener("resize",function(){k()},!1),b.addEventListener("mousemove",function(a){A=a.pageX,B=a.pageY},!1),D&&!C&&a.addEventListener("deviceorientation",function(){F=Math.min(Math.max(-event.beta,-30),30),E=Math.min(Math.max(-event.gamma,-30),30)},!0),j(),q("onInit")}}function i(){r.width=d.offsetWidth,r.height=d.offsetHeight,s.fillStyle=g.dotColor,s.strokeStyle=g.lineColor,s.lineWidth=g.lineWidth}function j(){if(y){u=a.innerWidth,v=a.innerHeight,s.clearRect(0,0,r.width,r.height);for(var b=0;b<z.length;b++)z[b].updatePosition();for(var b=0;b<z.length;b++)z[b].draw();G||(t=requestAnimationFrame(j))}}function k(){i();for(var a=d.offsetWidth,b=d.offsetHeight,c=z.length-1;c>=0;c--)(z[c].position.x>a||z[c].position.y>b)&&z.splice(c,1);var e=Math.round(r.width*r.height/g.density);if(e>z.length)for(;e>z.length;){var f=new n;z.push(f)}else e<z.length&&z.splice(e);for(c=z.length-1;c>=0;c--)z[c].setStackPos(c)}function l(){G=!0}function m(){G=!1,j()}function n(){switch(this.stackPos,this.active=!0,this.layer=Math.ceil(3*Math.random()),this.parallaxOffsetX=0,this.parallaxOffsetY=0,this.position={x:Math.ceil(Math.random()*r.width),y:Math.ceil(Math.random()*r.height)},this.speed={},g.directionX){case"left":this.speed.x=+(-g.maxSpeedX+Math.random()*g.maxSpeedX-g.minSpeedX).toFixed(2);break;case"right":this.speed.x=+(Math.random()*g.maxSpeedX+g.minSpeedX).toFixed(2);break;default:this.speed.x=+(-g.maxSpeedX/2+Math.random()*g.maxSpeedX).toFixed(2),this.speed.x+=this.speed.x>0?g.minSpeedX:-g.minSpeedX}switch(g.directionY){case"up":this.speed.y=+(-g.maxSpeedY+Math.random()*g.maxSpeedY-g.minSpeedY).toFixed(2);break;case"down":this.speed.y=+(Math.random()*g.maxSpeedY+g.minSpeedY).toFixed(2);break;default:this.speed.y=+(-g.maxSpeedY/2+Math.random()*g.maxSpeedY).toFixed(2),this.speed.x+=this.speed.y>0?g.minSpeedY:-g.minSpeedY}}function o(a,b){return b?void(g[a]=b):g[a]}function p(){console.log("destroy"),r.parentNode.removeChild(r),q("onDestroy"),f&&f(d).removeData("plugin_"+e)}function q(a){void 0!==g[a]&&g[a].call(d)}var r,s,t,u,v,w,x,y=!!b.createElement("canvas").getContext,z=[],A=0,B=0,C=!navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry|BB10|mobi|tablet|opera mini|nexus 7)/i),D=!!a.DeviceOrientationEvent,E=0,F=0,G=!1;return g=c({},a[e].defaults,g),n.prototype.draw=function(){s.beginPath(),s.arc(this.position.x+this.parallaxOffsetX,this.position.y+this.parallaxOffsetY,g.particleRadius/2,0,2*Math.PI,!0),s.closePath(),s.fill(),s.beginPath();for(var a=z.length-1;a>this.stackPos;a--){var b=z[a],c=this.position.x-b.position.x,d=this.position.y-b.position.y,e=Math.sqrt(c*c+d*d).toFixed(2);e<g.proximity&&(s.moveTo(this.position.x+this.parallaxOffsetX,this.position.y+this.parallaxOffsetY),g.curvedLines?s.quadraticCurveTo(Math.max(b.position.x,b.position.x),Math.min(b.position.y,b.position.y),b.position.x+b.parallaxOffsetX,b.position.y+b.parallaxOffsetY):s.lineTo(b.position.x+b.parallaxOffsetX,b.position.y+b.parallaxOffsetY))}s.stroke(),s.closePath()},n.prototype.updatePosition=function(){if(g.parallax){if(D&&!C){var a=(u-0)/60;w=(E- -30)*a+0;var b=(v-0)/60;x=(F- -30)*b+0}else w=A,x=B;this.parallaxTargX=(w-u/2)/(g.parallaxMultiplier*this.layer),this.parallaxOffsetX+=(this.parallaxTargX-this.parallaxOffsetX)/10,this.parallaxTargY=(x-v/2)/(g.parallaxMultiplier*this.layer),this.parallaxOffsetY+=(this.parallaxTargY-this.parallaxOffsetY)/10}var c=d.offsetWidth,e=d.offsetHeight;switch(g.directionX){case"left":this.position.x+this.speed.x+this.parallaxOffsetX<0&&(this.position.x=c-this.parallaxOffsetX);break;case"right":this.position.x+this.speed.x+this.parallaxOffsetX>c&&(this.position.x=0-this.parallaxOffsetX);break;default:(this.position.x+this.speed.x+this.parallaxOffsetX>c||this.position.x+this.speed.x+this.parallaxOffsetX<0)&&(this.speed.x=-this.speed.x)}switch(g.directionY){case"up":this.position.y+this.speed.y+this.parallaxOffsetY<0&&(this.position.y=e-this.parallaxOffsetY);break;case"down":this.position.y+this.speed.y+this.parallaxOffsetY>e&&(this.position.y=0-this.parallaxOffsetY);break;default:(this.position.y+this.speed.y+this.parallaxOffsetY>e||this.position.y+this.speed.y+this.parallaxOffsetY<0)&&(this.speed.y=-this.speed.y)}this.position.x+=this.speed.x,this.position.y+=this.speed.y},n.prototype.setStackPos=function(a){this.stackPos=a},h(),{option:o,destroy:p,start:m,pause:l}}var e="particleground",f=a.jQuery;a[e]=function(a,b){return new d(a,b)},a[e].defaults={minSpeedX:.1,maxSpeedX:.7,minSpeedY:.1,maxSpeedY:.7,directionX:"center",directionY:"center",density:1e4,dotColor:"#666666",lineColor:"#666666",particleRadius:7,lineWidth:1,curvedLines:!1,proximity:100,parallax:!0,parallaxMultiplier:5,onInit:function(){},onDestroy:function(){}},f&&(f.fn[e]=function(a){if("string"==typeof arguments[0]){var b,c=arguments[0],g=Array.prototype.slice.call(arguments,1);return this.each(function(){f.data(this,"plugin_"+e)&&"function"==typeof f.data(this,"plugin_"+e)[c]&&(b=f.data(this,"plugin_"+e)[c].apply(this,g))}),void 0!==b?b:this}return"object"!=typeof a&&a?void 0:this.each(function(){f.data(this,"plugin_"+e)||f.data(this,"plugin_"+e,new d(this,a))})})}(window,document),/**
 * requestAnimationFrame polyfill by Erik Möller. fixes from Paul Irish and Tino Zijdel
 * @see: http://paulirish.com/2011/requestanimationframe-for-smart-animating/
 * @see: http://my.opera.com/emoller/blog/2011/12/20/requestanimationframe-for-smart-er-animating
 * @license: MIT license
 */
function(){for(var a=0,b=["ms","moz","webkit","o"],c=0;c<b.length&&!window.requestAnimationFrame;++c)window.requestAnimationFrame=window[b[c]+"RequestAnimationFrame"],window.cancelAnimationFrame=window[b[c]+"CancelAnimationFrame"]||window[b[c]+"CancelRequestAnimationFrame"];window.requestAnimationFrame||(window.requestAnimationFrame=function(b){var c=(new Date).getTime(),d=Math.max(0,16-(c-a)),e=window.setTimeout(function(){b(c+d)},d);return a=c+d,e}),window.cancelAnimationFrame||(window.cancelAnimationFrame=function(a){clearTimeout(a)})}();


particleground(document.getElementById('particles-foreground'), {
  dotColor: 'rgba(255, 255, 255, 1)',
  lineColor: 'rgba(255, 255, 255, 0.05)',
  minSpeedX: 0.3,
  maxSpeedX: 0.6,
  minSpeedY: 0.3,
  maxSpeedY: 0.6,
  density: 50000, // One particle every n pixels
  curvedLines: false,
  proximity: 250, // How close two dots need to be before they join
  parallaxMultiplier: 10, // Lower the number is more extreme parallax
  particleRadius: 4, // Dot size
});

particleground(document.getElementById('particles-background'), {
  dotColor: 'rgba(255, 255, 255, 0.5)',
  lineColor: 'rgba(255, 255, 255, 0.05)',
  minSpeedX: 0.075,
  maxSpeedX: 0.15,
  minSpeedY: 0.075,
  maxSpeedY: 0.15,
  density: 30000, // One particle every n pixels
  curvedLines: false,
  proximity: 20, // How close two dots need to be before they join
  parallaxMultiplier: 20, // Lower the number is more extreme parallax
  particleRadius: 2, // Dot size
});
var pickout=function(){"use strict";function e(e){t(e),a()}function t(e){var t="object"==typeof e?e:{};"string"==typeof e&&(t.el=e),t.DOM=C.$$(t.el),h(t)}function a(){v.DOM.map(function(e,t){r(e,t)}),u()}function r(e,t){var a=v,r=!1;e.style.display="none",e.hasAttribute("multiple")&&(r=!0,e.name=-1!==e.name.indexOf("[]")?e.name:e.name+"[]");var l=e.parentElement;C.attr(l,"style","position:relative;float:left;");var i=C.attr(e,"placeholder"),d=C.create("div");
if(C.addClass(d,"icon-text beneath pk-field -"+a.theme+(r?" -multiple":"")),i&&(d.innerHTML=i),l.hasAttribute("for")&&C.attr(d,"id",C.attr(l,"for")),l.appendChild(d),!r){var o=C.create("span");C.addClass(o,"pk-arrow -"+a.theme),l.appendChild(o)}C.events(l,"click",function(e){e.preventDefault(),e.stopPropagation(),a.currentIndex=t,a.multiple=!!r,n(a)})}function n(e){var t,a=C.$(".pk-modal"),r=e.DOM[e.currentIndex],n=C.$(".main",a);if(C.addClass(a,"-"+e.theme),!n.children.length){var l=C.$(".pk-overlay"),d=C.toArray(r),o=d.map(function(r,n){return t={index:n,item:r},"optgroup"===r.parentElement.localName&&(t.optGroup=r.parentElement),i(t,a,e)});C.addClass(a,"-show"),C.addClass(l,"-show");var s=r.hasAttribute("placeholder")?C.attr(r,"placeholder"):"Select to option";if(C.$(".head",a).innerHTML=s,C.rmClass(a,"-multiple"),e.multiple){var p=C.$(".pk-multiple",a);C.addClass(p,"-show"),C.addClass(p,"-"+e.theme),C.addClass(a,"-multiple ")}if(e.search){var c=C.$(".pk-search",a),u=C.$("input",c);u.value="",setTimeout(function(){u.focus()},300),C.addClass(c,"-show");var f=[];C.events(u,"keyup",function(t){function a(){var e=C.$(".pk-no_result_search",n);e&&n.removeChild(e)}function r(e){e.map(function(e){e.parentNode&&n.removeChild(e)})}if(t.preventDefault(),t.stopPropagation(),f=C.$$("li",n),r(f),!t.target.value)return a(),void o.map(function(e){Array.isArray(e)&&(n.appendChild(e[0]),e=e[1]),n.appendChild(e)});if(o.map(function(e){Array.isArray(e)&&(e=e[1]);var r=e.lastChild;r&&-1!==r.innerHTML.toLowerCase().indexOf(t.target.value.toLowerCase())&&(a(),n.appendChild(e))}),!n.children.length){var l=C.create("li");return C.addClass(l,"pk-no_result_search"),C.addClass(l,"-"+e.theme),l.innerHTML=e.noResults,void n.appendChild(l)}})}}}function l(e,t,a){var r=C.create("li");return C.addClass(r,"pk-option-group -"+a.theme),C.attr(r,"data-opt-group",e.label),C.attr(r,"data-type",e.localName),r.innerHTML=e.label.toUpperCase(),t.appendChild(r),r}function i(e,t,a){var r=a.DOM[a.currentIndex],n=t.querySelector(".main"),i=[];if(e.optGroup){var s=C.$("li[data-opt-group="+e.optGroup.label+"]",n);s||i.push(l(e.optGroup,n,a))}var p=C.create("li"),c=e.item.hasAttribute("selected")?"-selected":"";if(C.addClass(p,"pk-option "+c+" -"+a.theme),a.multiple){var u=C.create("span");C.addClass(u,"pk-circle -"+a.theme),p.appendChild(u)}e.item.value||C.attr(p,"style","display:none;");var f=C.create("span");C.addClass(f,"icon"),f.innerHTML=C.attr(e.item,"data-icon")||"";var h=C.create("span");return C.addClass(h,"txt"),h.innerHTML=e.item.innerHTML,n.appendChild(p),p.appendChild(f),p.appendChild(h),e.txt=h.innerHTML,C.events(p,"click",function(t){if(t.preventDefault(),t.stopPropagation(),a.multiple){if(e.field=r.parentElement.querySelector(".pk-field"),r[e.index].hasAttribute("selected")){r[e.index].removeAttribute("selected"),C.rmClass(p,"-selected");var n=C.$('.pk-tag[data-select="'+r.name.replace("[]","")+e.index+'"]');return e.field.removeChild(n),void(e.field.children.length||(e.field.innerHTML=C.attr(r,"placeholder")))}return C.attr(r[e.index],"selected","selected"),C.addClass(p,"-selected"),void d(r,e,a)}o(r,e)}),i.length?(i.push(p),i):p}function d(e,t,a){t.field.children.length||(t.field.innerHTML="");var r=C.create("div"),n=C.create("span"),l=C.create("span");C.addClass(r,"pk-tag -"+a.theme),C.attr(r,"data-select",e.name.replace("[]","")+t.index),C.addClass(n,"txt"),C.addClass(l,"close"),n.innerHTML=t.txt,l.innerHTML="&times;",r.appendChild(n),r.appendChild(l),t.field.appendChild(r);var i=t.index;C.events(l,"click",function(a){a.preventDefault(),a.stopPropagation(),e[i].removeAttribute("selected"),t.field.removeChild(a.target.parentElement),t.field.children.length||(t.field.innerHTML=C.attr(e,"placeholder"))})}function o(e,t,a){C.toArray(e).map(function(e,a){return a===t.index?void C.attr(e,"selected","selected"):void e.removeAttribute("selected")}),s(e,t.txt),f()}function s(e,t){e.parentElement.querySelector(".pk-field").innerHTML=t}function p(e){t(e),v.DOM.forEach(function(e){s(e,e[e.selectedIndex].innerHTML)})}function c(e){var a={};t(e),v.DOM.forEach(function(e){a.field=e.parentElement.querySelector(".pk-field"),C.toArray(e).forEach(function(t,r){t.hasAttribute("selected")&&(a.index=r,a.txt=t.innerHTML,d(e,a,v))})})}function u(){if(!C.$(".pk-overlay")){var e=C.create("div");C.addClass(e,"pk-overlay");var t=C.create("div");C.addClass(t,"pk-modal");var a=C.create("ul");C.addClass(a,"main");var r=C.create("div");C.addClass(r,"head");var n=C.create("div");C.addClass(n,"pk-search");var l=C.create("input");C.attr(l,"type","text");var i=C.create("div");C.addClass(i,"pk-multiple");var d=C.create("button");C.addClass(d,"pk-btnMultiply"),d.innerHTML=v.txtBtnMultiple;var o=C.create("span");C.addClass(o,"close"),o.innerHTML="&times;",document.body.appendChild(e),document.body.appendChild(t),t.appendChild(r),t.appendChild(n),n.appendChild(l),t.appendChild(o),t.appendChild(a),t.appendChild(i),i.appendChild(d),[e,o,d].forEach(function(e){C.events(e,"click",function(e){e.preventDefault(),e.stopPropagation(),f()})})}}function f(){var e=C.$(".pk-overlay"),t=C.$(".pk-modal"),a=C.$(".pk-search",t),r=C.$(".pk-multiple",t);C.attr(t,"class","pk-modal"),C.attr(r,"class","pk-multiple"),C.attr(a,"class","pk-search"),C.attr(e,"class","pk-overlay"),setTimeout(function(){C.$(".main",t).innerHTML=""},500)}function h(e){v=JSON.parse(JSON.stringify(m));for(var t in e)e.hasOwnProperty(t)&&(v[t]=e[t])}var v={},m={theme:"clean",search:!1,noResults:"No Results",multiple:!1,txtBtnMultiple:"CONFIRM SELECTED"},C={create:function(e){return document.createElement(e)},attr:function(e,t,a){return a?Array.isArray(e)?void e.forEach(function(e){e.setAttribute(t,a)}):void e.setAttribute(t,a):e.getAttribute(t)},events:function(e,t,a){e.addEventListener(t,a,!1)},toArray:function(e){return[].slice.call(e)},addClass:function(e,t){var a=this,r=a.attr(e,"class")?a.attr(e,"class"):"";a.attr(e,"class",r+" "+t)},rmClass:function(e,t){var a=this;return Array.isArray(e)?void e.forEach(function(e){a.attr(e,"class",a.attr(e,"class").replace(" "+t,""))}):void a.attr(e,"class",a.attr(e,"class").replace(" "+t,""))},$:function(e,t){return(t||document).querySelector(e)},$$:function(e,t){return this.toArray((t||document).querySelectorAll(e))}};return{to:e,updated:p,updatedMultiple:c}}();"undefined"!=typeof module&&module.exports&&(module.exports=pickout);
pickout.to({
    'el': '.skills',
    'theme': 'cricket'
});

$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

// ===== Scroll to Top ====
$(window).scroll(function() {
    if ($(this).scrollTop() >= .6*$(window).height()) {        // If page is scrolled more than 50px
        $('#return-to-top').fadeIn(300);    // Fade in the arrow
    } else {
        $('#return-to-top').fadeOut(700);   // Else fade out the arrow
    }
  });
  $('#return-to-top').click(function() {      // When arrow is clicked
    $('body,html').animate({
        scrollTop : 0                       // Scroll to top of body
    }, 1000);
});

// for fading on scroll
$(document).ready(function() {

    /* Every time the window is scrolled ... */
    $(window).scroll( function(){

        /* Check the location of each desired element */
        $('.hideme').each( function(i){

            var bottom_of_object = $(this).offset().top + $(this).outerHeight();
            var bottom_of_window = $(window).scrollTop() + $(window).height();

            /* If the object is completely visible in the window, fade it it */
            if( bottom_of_window > bottom_of_object ){

                $(this).animate({'opacity':'1'},100);

            }
        });

    });

});

$('#analyze').click(function(e){
    $('#welcome').fadeOut('slow', function(){
        $('#uploading').fadeIn('slow');
    });
    $('body,html').animate({
        scrollTop : 0                       // Scroll to top of body
    }, 1000);
});

document.getElementById('analyze').addEventListener('click', function() {
  var files = document.getElementById('file').files;
  if (files.length > 0) {
    getBase64('../../../data/SEP-GluA1-KI_tp1.tif');
  }
});

function getBase64(file) {
   var data = File.ReadAllBytes(file);
   var result = Convert.ToBase64String(data);
}


/*socket.on('fileUpload', function() {
  $('#uploading').fadeOut('slow', function(){
      $('#analyzing').fadeIn('slow');
  });
});*/

var id = 0;
$(document).ready(function(){
    namespace = '/';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    //socket.on('response', function(id) {
    $('form#submit').submit(function(event) {
      socket.emit('analyze', {myID : '1123'});
      id = "1123";
    });


    socket.on('complete', function() {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET",location.protocol + '//' + document.domain + ':' + location.port + '/results', true); // true for asynchronous
      xmlHttp.setRequestHeader(str(id), id);
      xmlHttp.send();
    })
});
