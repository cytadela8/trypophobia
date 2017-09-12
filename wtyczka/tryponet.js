document.addEventListener("DOMContentLoaded", function() {
/*
var model = new KerasJS.Model({
    filepaths: {
        model: browser.extension.getURL('model/model.json'),
        weights: browser.extension.getURL('model/model_weights.buf'),
        metadata: browser.extension.getURL('model/model_metadata.json')
    },
    gpu: true
});
*/
var IMAGE_HEIGHT = 250;
var IMAGE_WIDTH = 250;

function waitfor(test, expectedValue, msec, count, source, callback) {
    // Check if condition met. If not, re-check later (msec).
    while (test() !== expectedValue) {
        count++;
        setTimeout(function() {
            waitfor(test, expectedValue, msec, count, source, callback);
        }, msec);
        return;
    }
    // Condition finally met. callback() can be executed.
    console.log(source + ': ' + test() + ', expected: ' + expectedValue + ', ' + count + ' loops.');
    callback();
}

function whichAnimationEvent(){
    var t;
    var el = document.createElement('fakeelement');
    var transitions = {
        'animation':'animationend',
        'OAnimation':'oAnimationEnd',
        'MozAnimation':'animationend',
        'WebkitAnimation':'webkitAnimationEnd'
    }

    for(t in transitions){
        if( el.style[t] !== undefined ){
            return transitions[t];
        }
    }
}

var debug = 3;

function process_image(img) {
    if (debug === 2){
        return;
    }
    debug+=1;
  //console.log(img.src)
  if (img.parentNode.classList.contains('tryponet_internal'))
    return;

  var originalImg = img.cloneNode(true);
  //img.style.visibility = 'hidden';
  img.style.webkitFilter = "blur(20px)";
  img.style.filter = "blur(20px)";
  var unmutatedImg = img.cloneNode(true);

  var parent = img.parentNode;
  var wrapper = document.createElement('div');
  wrapper.removeAttribute("style");
  wrapper.style.position = 'relative';
  wrapper.classList.add('tryponet_internal');
  // set the wrapper as child (instead of the element)
  parent.replaceChild(wrapper, img);
  // set element as child of wrapper
  wrapper.appendChild(img);

  //mask the element
  var mask = document.createElement('div');
    mask.removeAttribute("style");
    mask.style.width = '100%';
    mask.style.height = '100%';
    mask.style.position = 'absolute';
    mask.style.left = '0';
    mask.style.top = '0';
    mask.style.zIndex = '1000';
    mask.style.backgroundColor = "rgba(34,34,34,0.30)";
    wrapper.appendChild(mask);

    var wH = mask.clientHeight;
    var wW = mask.clientWidth;
    var rectangleWidth = Math.min(Number((wH*100)/wW), 100);
    var rectangleHeight = Math.min(Number((wW*100)/wH), 100);

  //add a rectangle
    var rectangle = document.createElement('div');
    rectangle.style.position = "absolute";
    rectangle.style.width = rectangleWidth+"%";
    rectangle.style.height = rectangleHeight+"%";
    rectangle.style.right = "50%";
    rectangle.style.bottom = "50%";
    rectangle.style.transform = "translate(50%,50%)";
    //rectangle.style.backgroundColor = 'rgba(34,34,34,0.30)';

    mask.appendChild(rectangle);

  //add a spinner
    var spinner = document.createElement('div');
    var spinnerBorderSize = Number(rectangle.clientHeight/10);
    spinner.style.border = +"px solid rgba(50,50,50,1)";
    spinner.style.borderTop = spinnerBorderSize+"px solid rgba(100,100,100,1)";
    spinner.style.borderBottom = spinnerBorderSize+"px solid rgba(100,100,100,1)";
    spinner.style.borderLeft = spinnerBorderSize+"px solid rgba(160,160,160,1)";
    spinner.style.borderRight = spinnerBorderSize+"px solid rgba(160,160,160,1)";
    spinner.style.position = "relative";
    spinner.style.borderRadius = "50%";
    spinner.style.width = "40%";
    spinner.style.paddingBottom = "40%";
    spinner.style.objectFit = "contain";
    spinner.style.maxHeight = "100%";
    spinner.style.display = "block";
    spinner.style.margin = "auto";
    spinner.style.marginTop = "10%";
    spinner.style.webkitAnimation = "trypo-spin 5s linear infinite";
    spinner.style.animation = "trypo-spin 5s linear infinite";
    rectangle.appendChild(spinner);

    //add text container
    var textCointainer = document.createElement('div');
    textCointainer.style.position = "absolute";
    textCointainer.style.width = "100%";
    textCointainer.style.height = "30%";

    //add processing text
    var statusText = document.createElement('span');
    statusText.style.position = "absolute";
    //statusText.style.fontSize = "calc(0.75em + 1vmin)";
    statusText.style.margin = "5% auto 5%";
    //statusText.style.display = "inline-block";
    statusText.style.textAlign = "center";
    statusText.style.fontWeight = "bold";
    statusText.style.color = "white";
    //statusText.style.marginTop = "5%";
    statusText.style.width = "100%";
    //statusText.style.height = "30%";
    statusText.style.paddingBottom = "10%";
    //statusText.style.paddingTop = "10%";
    statusText.style.top = "50%";
    statusText.style.transform = "translateY(-50%)";
    statusText.innerHTML = "Processing...";

    rectangle.appendChild(textCointainer);
    textCointainer.appendChild(statusText);
    fitText(statusText, 0.8);

    /*model.ready().then( () => {
        waitfor(function(){return model.isRunning}, false, 50, 0, "model waiter",
            function () {*/

                var img2 = loadImage.scale(img, {maxWidth: IMAGE_WIDTH, maxHeight: IMAGE_HEIGHT});

                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img2, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT);
                var data = ctx.getImageData(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT).data;
                //console.log(data);

                var array_data = new Float32Array(data)
                //console.log(array2);
                var array_tensor = new Float32Array(IMAGE_WIDTH * IMAGE_HEIGHT * 3);
                for (var i=0;i<IMAGE_WIDTH * IMAGE_HEIGHT; i++)
                    for (var j=0;j<3;j++)
                        array_tensor[i*3+j] = array_data[i*4+j] / 255;
                const inputData = { input: array_tensor };

            console.log("Predict started");
            statusText.innerHTML = "Predicting...";
            fitText(statusText, 0.8);

            //in case the js code of the website modified the node we restore it
            wrapper.removeChild(img);
            var img = unmutatedImg.cloneNode(true);
            wrapper.appendChild(img);

            //model.predict(inputData).then( outputData => {
            setTimeout(function(){
                //console.log("I WAS INVOKED")
                var outputData = {"output":[0.6,0.4]};
                console.log(outputData.output);
                console.log(outputData.output[0]);

                statusText.innerHTML = Number(outputData.output[0]*100).toFixed(0)+'% Trypophobic';
                rectangle.removeChild(spinner);
                rectangle.removeChild(textCointainer);
                textCointainer.removeChild(statusText);

                //console.log("REMOVAL")
                if(outputData.output[0] < 0.005) {
                    //console.log("ASDAS111111111");
                    img.style.webkitFilter = "";
                    img.style.filter = "";
                    img.style.animation = "trypo-reveal linear 1s";
                    img.style.webkitAnimation = "trypo-reveal linear 1s";

                    //mask.style.backgroundColor = "";
                    mask.removeChild(rectangle);
                    console.log("REE")
                    wrapper.removeChild(mask);

                    console.log("I'm here");
                    img.addEventListener(whichAnimationEvent(), function(){
                        //console.log("Restoring original img - in case it was changed")
                        //restore original image in case some js changed it during runtime
                        wrapper.removeChild(img);
                        wrapper.appendChild(originalImg);
                    }, false);
                    //console.log("TEST");
                }
                else
                {
                    var padding1Cointainer = document.createElement('div');
                    padding1Cointainer.style.position = "relative";
                    padding1Cointainer.style.width = "100%";
                    padding1Cointainer.style.height = "5%";

                    var warningText1Cointainer = document.createElement('div');
                    warningText1Cointainer.style.position = "relative";
                    warningText1Cointainer.style.width = "100%";
                    warningText1Cointainer.style.height = "20%";

                    var warningText2Cointainer = document.createElement('div');
                    warningText2Cointainer.style.position = "relative";
                    warningText2Cointainer.style.width = "100%";
                    warningText2Cointainer.style.height = "50%";

                    var warningText3Cointainer = document.createElement('div');
                    warningText3Cointainer.style.position = "relative";
                    warningText3Cointainer.style.width = "100%";
                    warningText3Cointainer.style.height = "20%";

                    var padding2Cointainer = document.createElement('div');
                    padding1Cointainer.style.position = "relative";
                    padding1Cointainer.style.width = "100%";
                    padding1Cointainer.style.height = "5%";

                    /*var icon = document.createElement('span');
                    icon.style.position = "absolute";
                    icon.style.fontSize = "300%";
                    //icon.style.margin = "5px auto 5px";
                    //icon.style.textAlign = "center";
                    icon.style.top = "50%";
                    //icon.
                    icon.style.transform = "translateY(-50%)";
                    icon.classList.add('trypo-warning');*/

                    var warningText1 = statusText.cloneNode(true);
                    warningText1.innerHTML = "Warning!";

                    var warningText2 = statusText.cloneNode(true);
                    warningText2.innerHTML = Number(outputData.output[0]*100).toFixed(0)+'%';

                    var warningText3 = statusText.cloneNode(true);
                    warningText3.innerHTML = "Trypophobic";

                    warningText1Cointainer.appendChild(warningText1);
                    warningText2Cointainer.appendChild(warningText2);
                    warningText3Cointainer.appendChild(warningText3);

                    rectangle.appendChild(padding1Cointainer);
                    rectangle.appendChild(warningText1Cointainer);
                    rectangle.appendChild(warningText2Cointainer);
                    rectangle.appendChild(warningText3Cointainer);
                    rectangle.appendChild(padding2Cointainer);

                    fitText(warningText1, 0.8);
                    fitText(warningText2, 0.4);
                    fitText(warningText3, 0.8);

                    mask.classList.add("tryponet-hover");

                    //setup the click to reveal feature
                    mask.onclick = function(event)
                    {
                        event.stopPropagation();
                        event.preventDefault();

                      rectangle.removeChild(padding1Cointainer);
                      rectangle.removeChild(warningText1Cointainer);
                      rectangle.removeChild(warningText2Cointainer);
                      rectangle.removeChild(warningText3Cointainer);
                      rectangle.removeChild(padding2Cointainer);
                      mask.removeChild(rectangle);
                      wrapper.removeChild(mask);

                      img.style.webkitFilter = "";
                      img.style.filter = "";
                      img.style.animation = "trypo-reveal linear 1s";
                      img.style.webkitAnimation = "trypo-reveal linear 1s";
                      img.addEventListener(whichAnimationEvent(), function(){
                          //console.log("Restoring original img - in case it was changed")
                          // restore original image in case some js changed it during runtime
                          wrapper.removeChild(img);
                          wrapper.appendChild(originalImg);
                        }, false);
                    }
                }

            }, 1000);/*.catch(exception => {
                console.log(exception);
            })} );*/

    }//);

  //console.log("Donek")
//}

Array.prototype.forEach.call(document.images, process_image);

obs = new window.MutationObserver(function (mutations, observer) {
  for (var mutation of mutations) {
    if (mutation.addedNodes.length) {
      //console.log(mutation.addedNodes.length)
      for (var i = 0; i < mutation.addedNodes.length; i++) {
        var nodek = mutation.addedNodes[i]
        //console.log(nodek.tagName)
        if (nodek.getElementsByTagName) {
          console.log(nodek.getElementsByTagName('img').length)
          for (var img of nodek.getElementsByTagName('img'))
            process_image(img);
        }//console.log('asddas')
      }
      //console.log(mutation.addedNodes.length)
      //console.log('qweqweqwe')
    }
  }
})
// have the observer observe foo for changes in children
obs.observe( document.body, { childList:true, subtree:true });

});
