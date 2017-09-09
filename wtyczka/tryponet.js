document.body.style.border = "5px solid red";

function process_image(img)
{
  console.log(img.src)
  if (img.parentNode.classList.contains('tryponet_internal'))
    return;
  img.style.visibility = 'hidden';
  var parent = img.parentNode;
  var wrapper = document.createElement('div');
  wrapper.removeAttribute("style");
  wrapper.style.position = 'relative';
  wrapper.classList.add('tryponet_internal')
  // set the wrapper as child (instead of the element)
  parent.replaceChild(wrapper, img);
  // set element as child of wrapper
  wrapper.appendChild(img);
  var text = document.createElement('div');
  text.removeAttribute("style");
  text.style.backgroundColor = 'red';
  text.style.width = '100%';
  text.style.height = '100%';
  text.style.position = 'absolute';
  text.style.left = '0';
  text.style.top = '0';
  text.style.zIndex = '1000';
  text.innerHTML = "To jest jakis tekstek";
  wrapper.appendChild(text);
  //console.log("Donek")
}

//Array.prototype.forEach.call(document.images, process_image);

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
//obs.observe( document.body, { childList:true, subtree:true });
