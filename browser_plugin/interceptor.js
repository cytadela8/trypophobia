console.log("Hello from background");
/*
function logURL(requestDetails) {
  console.log("Loading: " + requestDetails.url);
}

browser.webRequest.onBeforeRequest.addListener(
  logURL,
  {urls: ["<all_urls>"]}
);
*/

String.prototype.hexEncode = function(){
    var hex, i;

    var result = "";
    for (i=0; i<this.length; i++) {
        hex = this.charCodeAt(i).toString(16);
        result += ("000"+hex).slice(-4);
    }

    return result
}

String.prototype.hexDecode = function(){
    var j;
    var hexes = this.match(/.{1,4}/g) || [];
    var back = "";
    for(j = 0; j<hexes.length; j++) {
        back += String.fromCharCode(parseInt(hexes[j], 16));
    }

    return back;
}

var do_not_inspect_urls = [];

function redirect(requestDetails) {

   console.log("ping")

  //redirect to the dirty wrapper hack only get request - the rest will be handled by mutation observers
  if(requestDetails.method != 'GET')
  {
    return;
  }

  var url = requestDetails.url;
  var wrapUrl = browser.extension.getURL('wrapper.js')

  console.log(url)
  console.log(wrapUrl)
  console.log(do_not_inspect_urls)

  //prevent an infinite loop
  if(url == wrapUrl)
  {
  return
  }
  console.log("searching for non rederict requests")
  for( var i = do_not_inspect_urls.length-1; i>=0; i--)
  {
    if ( do_not_inspect_urls[i] === url )
    {
        console.log("ignoring url")
        do_not_inspect_urls.splice(i, 1);
        console.log(do_not_inspect_urls)
        return
    }
  }

  //prevent double wrapping
  if(url.startsWith("data:text"))
  {
  return
  }


  //internal url wrapper
  var ignore_prefix = "http://ignore__/?url="
  if(url.startsWith(ignore_prefix))
  {
      var newURL = url.substring(ignore_prefix.length);
      console.log("SADD")
      if(newURL[newURL.length-1] == '/')
      {
        newURL = newURL.slice(0,-1);
      }
      newURL = newURL.hexDecode()

      do_not_inspect_urls.push(newURL)

      return {
        redirectUrl: newURL
      };
  }

  var req = new XMLHttpRequest();
  req.open('GET', url, false); //I do not know how to do it with asynchronous io :(
  req.send();
  var htmlbody = req.responseText;

  //serve a content examiner
  var hackedUrl = 'data:text/html;charset=utf-8,' +
    encodeURIComponent( // Escape for URL formatting
        '<html><body><script src="https://code.jquery.com/jquery-3.2.1.min.js"></script><input hidden id="url" value="'+url.hexEncode()+'"></input><input hidden id="body" value="'+htmlbody.hexEncode()+'"></input><script src ="'+wrapUrl+'"></script></body></html>')

  console.log("Redirecting: " + url);
  //return
  return {
    redirectUrl: hackedUrl
  };
}

browser.webRequest.onBeforeRequest.addListener(
  redirect,
  {urls:["<all_urls>"], types:["main_frame"/*, "sub_frame"*/]},
  ["blocking"]
);
console.log("SAD123123")


/*
function rewriteXHRheaders(e) {
console.log("ASDASDHHRHRHRHRH")
   console.log(e.requestHeaders)
  e.requestHeaders.push({"name":"Pragma","value":"no-cache"})
  e.requestHeaders.push({"name":"Cache-Control","value":"no-cache"})
  console.log(e.requestHeaders)
  console.log(e.url)
  return {requestHeaders: e.requestHeaders};
}

browser.webRequest.onBeforeSendHeaders.addListener(
  rewriteXHRheaders,
  {urls:["<all_urls>"], types:["xmlhttprequest"]},
  ["blocking", "requestHeaders"]
);*/

console.log("---------------")