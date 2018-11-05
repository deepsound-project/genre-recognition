CNN for Live Music Genre Recognition
====================================

Convolutional Neural Networks for Live Music Genre Recognition is a project aimed at creating a neural network recognizing music genre and providing a user-friendly visualization for the network's current belief of the genre of a song. The project was created for the 24-hour Braincode Hackathon in Warsaw by Piotr Kozakowski, Jakub Królak, Łukasz Margas and Bartosz Michalak.

The model has since been significantly improved and rewritten to TensorFlow.js, so that it doesn't require a backend - the network can be run inside of the user's browser.


Demo
----

You can see a demo at [http://deepsound.io/genres/](http://deepsound.io/genres/). You can upload a song using the big (and only) button and see the results for yourself. All mp3 files should work fine.


Usage
-----

It's easiest to run using Docker:

```shell
docker build -t genre-recognition . && docker run -d -p 8080:80 genre-recognition
```

The demo will be accessible at http://0.0.0.0:8080/.

By default, it will use a model pretrained by us, achieving 82% accuracy on the GTZAN dataset. You can also provide your own model, as long as it matches the input and output architecture of the provided model. If you wish to train a model by yourself, download the [GTZAN dataset](http://opihi.cs.uvic.ca/sound/genres.tar.gz) (or provide analogous) to the data/ directory, extract it, run `create_data_pickle.py` to preprocess the data and then run `train_model.py` to train the model. Afterwards you should run `model_to_tfjs.py` to convert the model to TensorFlow.js so it can be served.

```shell
cd data
wget http://opihi.cs.uvic.ca/sound/genres.tar.gz
tar zxvf genres.tar.gz
cd ..
pip install -r requirements.txt
python create_data_pickle.py
python train_model.py
python model_to_tfjs.py
```

You can "visualize" the filters learned by the convolutional layers using `extract_filters.py`. This script for every neuron extracts and concatenates several chunks resulting in its maximum activation from the tracks of the dataset. By default, it will put the visualizations in the filters/ directory. It requires the GTZAN dataset and its pickled version in the data/ directory. Run the commands above to obtain them. You can control the number of extracted chunks using the --count0 argument. Extracting higher numbers of chunks will be slower.


Background
----------

This model has been inspired by several works, primarily [Grzegorz Gwardys and Daniel Grzywczak, Deep Image Features in Music Information Retrieval](http://ijet.pl/index.php/ijet/article/view/10.2478-eletel-2014-0042/53) and [Recommending music on Spotify with Deep Learning](http://benanne.github.io/2014/08/05/spotify-cnns.html). The old version of the model is described in our blog post [Convolutional-Recurrent Neural Network for Live Music Genre Recognition](http://deepsound.io/music_genre_recognition.html). The new one is similar, key differences are the lack of recurrent layers, using the Adam optimizer instead of RMSprop and batch normalization. Those changes boosted accuracy from 67% to 82% while retaining the ability of the model to efficiently output predictions for every point in time.
