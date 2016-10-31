CRNN for Live Music Genre Recognition
=====================================

Convolutional-Recurrent Neural Networks for Live Music Genre Recognition is a project aimed at creating a neural network recognizing music genre and providing a user-friendly visualization for the network's current belief of the genre of a song. The project was created for the 24-hour Braincode Hackathon in Warsaw by Piotr Kozakowski, Jakub Królak, Łukasz Margas and Bartosz Michalak.

This project uses Keras for the neural network and Tornado for serving requests.


Demo
----

You can see a demo for a few selected songs here: [Demo](http://deepsound.io/genres/).


Usage
-----

In a fresh virtualenv type:  

```shell
pip install -r requirements.txt
```

to install all the prerequisites. Run: 

```shell
THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python server.py  
```

to run the server at http://0.0.0.0:8080/  

Then you can upload a song using the big (and only) button and see the results for yourself. All mp3 files should work fine.  

Running server.py without additional parameters launches the server using a default model provided in the package. You can provide your own model, as long as it matches the input and output architecture of the provided model. You can train your own model by modifying and running train\_model.py. If you wish to train a model by yourself, download the [GTZAN dataset](http://opihi.cs.uvic.ca/sound/genres.tar.gz) (or provide analogous) to the data/ directory, extract it, run create\_data\_pickle.py to preprocess the data and then run train\_model.py to train the model:

```shell
cd data
wget http://opihi.cs.uvic.ca/sound/genres.tar.gz
tar zxvf genres.tar.gz
cd ..
python create_data_pickle.py
THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python train_model.py
```

You can "visualize" the filters learned by the convolutional layers using extract\_filters.py. This script for each convolutional neuron extracts and concatenates a few chunks resulting in maximum activation of this neuron from the tracks from the dataset. By default, it will put the visualizations in the filters/ directory. It requires the GTZAN dataset and its pickled version in the data/ directory. Run the commands above to obtain them. You can control the number of extracted chunks using the --count0 argument. Extracting higher number of chunks will be slower.


Background
----------

The rationale for this particular model is based on several works, primarily [Grzegorz Gwardys and Daniel Grzywczak, Deep Image Features in Music Information Retrieval](http://ijet.pl/index.php/ijet/article/view/10.2478-eletel-2014-0042/53) and [Recommending music on Spotify with Deep Learning](http://benanne.github.io/2014/08/05/spotify-cnns.html). The whole idea is extensively described in our blog post [Convolutional-Recurrent Neural Network for Live Music Genre Recognition](http://deepsound.io/music_genre_recognition.html).  
