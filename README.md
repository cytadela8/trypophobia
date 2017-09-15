# Browser Plugin With Deep Learning

```
Ever wanted to censor inappropriate images on the web using deep learning?
```

<div style="width: 100%;">
<div>
<img src="./resources/poc.gif" height="214px" width="50%" />
</div>
</div>

A deep learning project by [Artur Puzio](https://github.com/cytadela8) and [Grzegorz Uriasz](https://github.com/grzegorz225) made as part of an internship at [Deepsense](http://deepsense.ai/) sponsored by [The Polish Children's Fund](http://fundusz.org/english/) and supervised by [Piotr Migdał](https://github.com/stared).

## Goals
- Create a deep learning model for detecting [trypophobia triggers](https://en.wikipedia.org/wiki/Trypophobia) suitable for running on an CPU
- Create a plug and play browser plugin for censoring trypophobic images on the fly while browsing the internet running entirely client-side.
- Prepare a high quality data set for training trypophobia classifiers combining different data sources together

## To do list
- ~~Create an utility for scrapping images from Google Images~~
- ~~Create utilities for quick image sorting and image normalization~~
- ~~Create a browser plugin using the WebExtension API capable of censoring images on the fly~~
- ~~Create neural networks suitable for running on a CPU in Javascript~~
- One global browser-wide keras.js instance in the browser plugin, cache predictions based on image fingerprints, create a settings page 
- Polish the browser plugin and publish it in the plugin store

## The utilities
The utilities contained in the `utils` folder are small programs and scripts necessary to generate the data set and easing the usage of the deep learning lab neptune.   

## The data set
The data set used for training the classifier is available [here](https://s3.eu-central-1.amazonaws.com/trypophobia/tryponet_set2.tar.gz). It contains almost `17k` images(16884 to be exact) `6.5k` of which(6316) are trypophobic. Disturbing images were obtained from the [trypophobia subreddit](https://www.reddit.com/r/trypophobia/) on Reddit and Google Images. Ordinary pictures were obtained from Google Images by querying more than 5k randomly chosen words from [this](https://github.com/dwyl/english-words) english dictionary for which we downloaded up to 2 images per search result - additionally to improve the quality of the data set we introduced 98 pictures of forests, 181 pictures of grass and 192 pictures of bushes. Duplicate images were removed by first comparing md5 hashes and then using photo duplicate detection available in [digiKam](https://www.digikam.org/). Each image was then rescaled and cropped to a 256x256 picture. The data was split into two pieces - 1000 images went to the validation set with the rest being the training set.

> Anyone interested in the "raw" unprocessed data please send us an [email](mailto:gorbak25@gmail.com,cytadela8@interia.pl).

## The models
The models which we created were made in the machine learning framework [keras](https://keras.io/) and are compatible with the javascript library [keras.js](https://github.com/transcranial/keras-js). The models were trained on the Google Computing Platform and were deployed using [neptune](https://neptune.ml/). This repository contains some of the considered models(`models` folder) together with the training results for them. We aimed for the models to have less than 20k parameters although the performance of bigger models was examined. Currently some of our models using less than 10k parameters exhibit high accuracy(90% on the validation set).

## Browser plugin
The browser plugin censors images encountered while browsing the web. It then employs one of our models to determine which images are safe to reveal and for which a warning must be issued. Currently the extension is working on Mozilla Firefox with other browsers untested. Currently the extension works on most sites.
