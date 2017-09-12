//web worker for classification of trypophobic images using keras.js

//load keras.js
console.log("Hello World");
self.importScripts(self.location.origin + '/lib/keras.js');
console.log("Keras included");

//create the model
var model = new KerasJS.Model({
    filepaths: {
        model: self.location.origin + '/model/model.json',
        weights: self.location.origin + '/model/model_weights.buf',
        metadata: self.location.origin + '/model/model_metadata.json'
    },
    gpu: false
});

console.log("Keras model loaded");

self.addEventListener('message', function(e) {
    var inputData = e.data;

    model.ready().then( function () {
        model.predict(inputData).then(function (outputData) {
            console.log(outputData.output);

            self.postMessage(outputData);

        }).catch(function (exception) {
            console.log(exception);
        });
    });

}, false);
