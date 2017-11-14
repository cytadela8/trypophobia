var kerasWorker = new Worker(browser.extension.getURL('prediction_generator.js'))

var IMAGE_HEIGHT = 256
var IMAGE_WIDTH = 256

var queue = []
var working = false

function enqueue (fn) {
  queue.push(fn)
  if (queue.length === 1) {
    working = true
    console.log("starting to process")
    queue[0](queue_callback)
  }
  else
    console.log("already processing: " + queue.length)
}

function queue_callback () {
  queue.shift()
  if (queue.length > 0) {
    console.log("new task, left: " + queue.length)
    queue[0](queue_callback)
  }
  else
    console.log("last task finished")
}

function safe_innerhtml (node, text) {
    while( node.firstChild )
        node.removeChild( node.firstChild )
    node.appendChild( document.createTextNode("Two") )
}

document.addEventListener('DOMContentLoaded', function () {
  function whichAnimationEvent () {
    var t
    var el = document.createElement('fakeelement')
    var transitions = {
      'animation': 'animationend',
      'OAnimation': 'oAnimationEnd',
      'MozAnimation': 'animationend',
      'WebkitAnimation': 'webkitAnimationEnd'
    }

    for (t in transitions) {
      if (el.style[t] !== undefined) {
        return transitions[t]
      }
    }
  }

  function maintainSquareShape (mask, rectangle, spinner) {
    var wH = mask.clientHeight
    var wW = mask.clientWidth
    var rectangleWidth = Math.min(Number((wH * 100) / wW), 100)
    var rectangleHeight = Math.min(Number((wW * 100) / wH), 100)
    var spinnerBorderSize = Number(rectangle.clientHeight / 10)

    rectangle.style.width = rectangleWidth + '%'
    rectangle.style.height = rectangleHeight + '%'
    spinner.style.border = spinnerBorderSize + 'px solid rgba(50,50,50,1)'
    spinner.style.borderTop = spinnerBorderSize + 'px solid rgba(100,100,100,1)'
    spinner.style.borderBottom = spinnerBorderSize + 'px solid rgba(100,100,100,1)'
    spinner.style.borderLeft = spinnerBorderSize + 'px solid rgba(160,160,160,1)'
    spinner.style.borderRight = spinnerBorderSize + 'px solid rgba(160,160,160,1)'

    //mask.classList.add('tryponet_done');
    if (mask.classList.contains('tryponet_done')) {

    }
    else {
      setTimeout(function () {
        maintainSquareShape(mask, rectangle, spinner)
      }, 100)
    }
  }

  var debug = 3 //If equal 1 -> only one image is processed
  function process_image (img) {
    if (debug === 2) {
      return
    }
    debug += 1
    //image was already processed
    if (img.parentNode.classList.contains('tryponet_internal'))
      return
    //img.style.visibility = 'hidden';
    img.style.webkitFilter = 'blur(20px)'
    img.style.filter = 'blur(20px)'

    var parent = img.parentNode
    var wrapper = document.createElement('div')
    wrapper.removeAttribute('style')
    wrapper.style.position = 'relative'
    wrapper.classList.add('tryponet_internal')
    parent.replaceChild(wrapper, img)
    wrapper.appendChild(img)

    //mask the element
    var mask = document.createElement('div')
    mask.removeAttribute('style')
    mask.style.width = '100%'
    mask.style.height = '100%'
    mask.style.position = 'absolute'
    mask.style.left = '0'
    mask.style.top = '0'
    mask.style.zIndex = '1000'
    mask.style.backgroundColor = 'rgba(34,34,34,0.30)'
    wrapper.appendChild(mask)

    //add a rectangle
    var rectangle = document.createElement('div')
    rectangle.style.position = 'absolute'
    rectangle.style.right = '50%'
    rectangle.style.bottom = '50%'
    rectangle.style.transform = 'translate(50%,50%)'
    mask.appendChild(rectangle)

    //add a spinner
    var spinner = document.createElement('div')
    spinner.style.position = 'relative'
    spinner.style.borderRadius = '50%'
    spinner.style.width = '40%'
    spinner.style.paddingBottom = '40%'
    spinner.style.objectFit = 'contain'
    spinner.style.maxHeight = '100%'
    spinner.style.display = 'block'
    spinner.style.margin = 'auto'
    spinner.style.marginTop = '10%'
    spinner.style.webkitAnimation = 'trypo-spin 5s linear infinite'
    spinner.style.animation = 'trypo-spin 5s linear infinite'
    rectangle.appendChild(spinner)

    maintainSquareShape(mask, rectangle, spinner)

    //add text container
    var textCointainer = document.createElement('div')
    textCointainer.style.position = 'absolute'
    textCointainer.style.width = '100%'
    textCointainer.style.height = '30%'
    rectangle.appendChild(textCointainer)

    //add processing text
    var statusText = document.createElement('span')
    statusText.style.position = 'absolute'
    statusText.style.margin = '5% auto 5%'
    statusText.style.display = 'inline-block'
    statusText.style.textAlign = 'center'
    statusText.style.fontWeight = 'bold'
    statusText.style.color = 'white'
    statusText.style.width = '100%'
    statusText.style.paddingBottom = '10%'
    statusText.style.top = '50%'
    statusText.style.transform = 'translateY(-50%)'
    statusText.innerHTML = 'Queued...'
    textCointainer.appendChild(statusText)

    fitText(statusText, 0.8)
    statusText.style.position = 'relative'

    var process = function (callback) {
      console.log('I DO NOT KNOW WHAT IS GOING ON IN JS')
      let imgcopy = img.cloneNode(true)  //potrzebujemy zrobic kopie, bo loadimage.scale robi dziwne rzeczy
      var img2 = loadImage.scale(imgcopy, {maxWidth: IMAGE_WIDTH, maxHeight: IMAGE_HEIGHT, canvas: true})
      imgcopy=null

      console.log('asdassfdsfs')

      //var canvas = document.createElement('canvas')
      var ctx = img2.getContext('2d')
      //ctx.drawImage(img2, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
      var array_data = new Float32Array(ctx.getImageData(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT).data)
      var array_tensor = new Float32Array(IMAGE_WIDTH * IMAGE_HEIGHT * 3)
      for (var i = 0; i < IMAGE_WIDTH * IMAGE_HEIGHT; i++)
        for (var j = 0; j < 3; j++)
          array_tensor[i * 3 + j] = array_data[i * 4 + j] / 255
      var inputData = {input: array_tensor}

      console.log('Predict started')
      statusText.style.position = 'absolute'
      statusText.innerHTML = 'Processing...'
      fitText(statusText, 0.8)
      statusText.style.position = 'relative'

      console.log('--------------------------------')
      //send data to worker
      kerasWorker.postMessage(inputData)
      kerasWorker.onmessage = function (e) {
        inputData = null
        ctx=null
        array_data=null
        array_tensor=null
        canvas=null
        img2=null

        var outputData = e.data
        console.log(outputData.output)
        console.log(outputData.output[0])
        safeinnerhtml (statusText, Number(outputData.output[0] * 100).toFixed(0) + '% Trypophobic')
        rectangle.removeChild(spinner)
        rectangle.removeChild(textCointainer)
        textCointainer.removeChild(statusText)
        function reveal () {
          //console.log("ASDAS111111111");
          img.style.webkitFilter = ''
          img.style.filter = ''
          img.style.animation = 'trypo-reveal linear 1s'
          img.style.webkitAnimation = 'trypo-reveal linear 1s'

          mask.classList.add('tryponet_done')

          //mask.style.backgroundColor = "";
          mask.removeChild(rectangle)
          console.log('REE')
          wrapper.removeChild(mask)

          console.log('I\'m here')
          img.addEventListener(whichAnimationEvent(), function () {
            img.style.animation = ''
            img.style.webkitAnimation = ''
          }, false)
          //console.log("TEST");
        }

        if (outputData.output[0] < 0.005) {
          reveal()
        }
        else {
          var padding1Cointainer = document.createElement('div')
          padding1Cointainer.style.position = 'relative'
          padding1Cointainer.style.width = '100%'
          padding1Cointainer.style.height = '5%'

          var warningText1Cointainer = document.createElement('div')
          warningText1Cointainer.style.position = 'relative'
          warningText1Cointainer.style.width = '100%'
          warningText1Cointainer.style.height = '20%'

          var warningText2Cointainer = document.createElement('div')
          warningText2Cointainer.style.position = 'relative'
          warningText2Cointainer.style.width = '100%'
          warningText2Cointainer.style.height = '50%'

          var warningText3Cointainer = document.createElement('div')
          warningText3Cointainer.style.position = 'relative'
          warningText3Cointainer.style.width = '100%'
          warningText3Cointainer.style.height = '20%'

          var padding2Cointainer = document.createElement('div')
          padding1Cointainer.style.position = 'relative'
          padding1Cointainer.style.width = '100%'
          padding1Cointainer.style.height = '5%'

          /*var icon = document.createElement('span');
          icon.style.position = "absolute";
          icon.style.fontSize = "300%";
          //icon.style.margin = "5px auto 5px";
          //icon.style.textAlign = "center";
          icon.style.top = "50%";
          //icon.
          icon.style.transform = "translateY(-50%)";
          icon.classList.add('trypo-warning');*/

          statusText.style.position = 'absolute'

          var warningText1 = statusText.cloneNode(true)
          warningText1.innerHTML = 'Warning!'

          var warningText2 = statusText.cloneNode(true)
          safe_innerhtml (warningText2, Number(outputData.output[0] * 100).toFixed(0) + '%')

          var warningText3 = statusText.cloneNode(true)
          warningText3.innerHTML = 'Trypophobic'

          warningText1Cointainer.appendChild(warningText1)
          warningText2Cointainer.appendChild(warningText2)
          warningText3Cointainer.appendChild(warningText3)
          console.log("appending")
          rectangle.appendChild(padding1Cointainer)
          rectangle.appendChild(warningText1Cointainer)
          rectangle.appendChild(warningText2Cointainer)
          rectangle.appendChild(warningText3Cointainer)
          rectangle.appendChild(padding2Cointainer)
          console.log("fitting")
          fitText(warningText1, 0.8)
          fitText(warningText2, 0.4)
          fitText(warningText3, 0.8)

          warningText1.style.position = 'relative'
          warningText2.style.position = 'relative'
          warningText3.style.position = 'relative'

          mask.classList.add('tryponet-hover')

          //setup the click to reveal feature
          mask.onmouseover = function (event) {
            event.stopPropagation()
            event.preventDefault()
          }
          mask.onclick = function (event) {
            event.stopPropagation()
            event.preventDefault()
            reveal()
          }
        }
        callback()
      }
    }
    if (img.complete)
      enqueue(process)
    else {
      img.addEventListener("load", () => {enqueue(process)})
    }
  }

  Array.prototype.forEach.call(document.images, process_image)

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
  obs.observe(document.body, {childList: true, subtree: true})

})
