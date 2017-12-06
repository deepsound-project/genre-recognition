from common import load_track, GENRES, NUMTRACKS, GENRE_IDS, GENRE_IDS_STRS
import sys
import numpy as np
from math import pi
#import _pickle as cPickle
from cPickle import dump
import os
import pandas as pd
from optparse import OptionParser
import librosa

from progress.bar import Bar

TRACK_COUNT = 1000

MEL_KWARGS = {
    'n_fft': 2048,
    'hop_length': 2048//2,
    #'n_mels': 128
}


def get_default_shape(dataset_path):
    tmp_features, _ = load_track(os.path.join(dataset_path,
        '000002.mp3'))
    return tmp_features.shape

def collect_data(dataset_path, genre_num):
    '''
    Collects data from the GTZAN dataset into a pickle. Computes a Mel-scaled
    power spectrogram for each track.

    :param dataset_path: path to the GTZAN dataset directory
    :returns: triple (x, y, track_paths) where x is a matrix containing
        extracted features, y is a one-hot matrix of genre labels and
        track_paths is a dict of absolute track paths indexed by row indices in
        the x and y matrices
    '''
    print genre_num
    
    print [GENRE_IDS_STRS[genre_num]]

    tracks = pd.read_csv('data/track_to_genre.csv');
    tracks = tracks[np.isfinite(tracks['genre_id'])]

    print len(tracks)

    reduced_tracks = tracks.loc[tracks['genre_id'] == GENRE_IDS[genre_num]]
    print len(reduced_tracks)
    num_tracks = len(reduced_tracks)
    default_shape = get_default_shape(dataset_path)
    print "default:",default_shape
    x = np.zeros((num_tracks,) + default_shape, dtype=np.float32)
    y = np.zeros((num_tracks, len(GENRE_IDS)), dtype=np.float32)
    track_paths = {}

    #print(tracks)
    #print(NUMTRACKS[0])

    reduced_tracks = reduced_tracks.sort_values(by=['genre_id'])
    
    print reduced_tracks
    curr_genre = None
    song_ID = ""
    i = 0

    bar = Bar('Progress:', max=len(reduced_tracks))

    for row in reduced_tracks.iterrows():
        #print "Processing Row : " , row
        genre =  int(row[1]['genre_id'])
        song_ID = str(int(row[1][1]))
        if genre != curr_genre:
            curr_genre = genre
        
        z = str(song_ID).zfill(6) 
        
        file_name = z+".mp3"
        #file_name = "132567.mp3"

        path = os.path.join(dataset_path, file_name)

        if os.path.isfile(path):
            track_index = i#curr_genre  * (num_tracks // len(GENRES)) + i
            genre_index = GENRE_IDS.index(curr_genre)
            #print curr_genre, "genre_index:", genre_index
            try:
                d, sample_rate = librosa.load(path, sr=None, mono=True)#load_track(path, default_shape)
                

                #stft = np.abs(librosa.stft(x, n_fft=2048,  hop_length=512))
                #mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft**2).T
                #log_mel = librosa.logamplitude(mel)

                features = librosa.feature.melspectrogram(d, **MEL_KWARGS).T
                

                if features.shape[0] < default_shape[0]:
                    delta_shape = (default_shape[0] - features.shape[0],
                            default_shape[1])
                    features = np.append(features, np.zeros(delta_shape), axis=0)
                elif features.shape[0] > default_shape[0]:
                    features = features[: default_shape[0], :]

                features[features == 0] = 1e-6
                features = np.log(features)

                x[track_index] = features
                y[track_index, genre_index] = 1
                
                #print y[track_index]
                track_paths[track_index] = os.path.abspath(path)
                i += 1
            except Exception, e:
                print "Corrupted File at" + path
                print e
        bar.next()
        

    bar.finish()

    return (x, y, track_paths)
    '''
        file_name = z+".mp3"
        print('Processing', file_name)
        path = os.path.join(dataset_path, file_name)
        track_index = genre_index  * (num_tracks // len(GENRES)) + i
        #x[track_index], _ = librosa.load(path, sr=None, mono=False)#load_track(path, default_shape)
        x, sample_rate = librosa.load(path, sr=None, mono=True)#load_track(path, default_shape)
        #print(x[track_index])
        #print(x[1000:20000])


        stft = np.abs(librosa.stft(x, n_fft=2048,  hop_length=512))
        mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft**2)
        log_mel = librosa.logamplitude(mel)

        #librosa.display.specshow(log_mel, sr=sample_rate, hop_length=512, x_axis='time', y_axis='mel')

        print(log_mel)

        y[track_index, genre_index] = 1
        track_paths[track_index] = os.path.abspath(path)
        #Process

    for (genre_index, genre_name) in enumerate(GENRES):
        #temp_
        for i in xrange(NUMTRACKS[genre_index]): 
            z = str(i).zfill(6)
            file_name = z+'.mp3'  #need to fix filename to our format.
            print('Processing', file_name)
            path = os.path.join(dataset_path, file_name)
            track_index = genre_index  * (num_tracks // len(GENRES)) + i
            #x[track_index], _ = librosa.load(path, sr=None, mono=False)#load_track(path, default_shape)
            x, sample_rate = librosa.load(path, sr=None, mono=True)#load_track(path, default_shape)
            #print(x[track_index])
            #print(x[1000:20000])


            stft = np.abs(librosa.stft(x, n_fft=2048,  hop_length=512))
            mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft**2)
            log_mel = librosa.logamplitude(mel)

            #librosa.display.specshow(log_mel, sr=sample_rate, hop_length=512, x_axis='time', y_axis='mel')

            print(log_mel)

            y[track_index, genre_index] = 1
            track_paths[track_index] = os.path.abspath(path)
    '''


if __name__ == '__main__':
    parser = OptionParser()
    #Change default = ps.path.join(os.path.dirname(__file___, 'data/genres')
    parser.add_option('-d', '--dataset_path', dest='dataset_path',
            default=os.path.join(os.path.dirname(__file__), '/Users/Andrew/Downloads/fma'),
            help='path to the GTZAN dataset directory', metavar='DATASET_PATH')
    parser.add_option('-o', '--output_pkl_path', dest='output_pkl_path',
            default=os.path.join(os.path.dirname(__file__), 'data/data.pkl'), #/Volumes/G-DRIVE mob/pickled_spect/data.pkl
            help='path to the output pickle', metavar='OUTPUT_PKL_PATH')
    options, args = parser.parse_args()


    (x, y, track_paths) = collect_data(options.dataset_path, int(sys.argv[1]))

    data = {'x': x, 'y': y, 'track_paths': track_paths}
    #print(data)
    print(data['x'])
    with open(options.output_pkl_path, 'w') as f:
        dump(data, f)
        f.close()
