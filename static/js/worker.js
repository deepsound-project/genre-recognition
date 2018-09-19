var window = self;

importScripts(
    'https://cdnjs.cloudflare.com/ajax/libs/aurora.js/0.4.2/aurora.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/aurora.js-mp3/0.1.0/mp3.min.js',
    'audio-utils.js'
);

const N_FFT = 2048;
const FFT_HOP = 1024;
const N_MELS = 128;

function decodeMp3(file) {
    return new Promise(function(resolve, reject) {
        var asset = AV.Asset.fromFile(file);
        var length = 0;
        var chunks = [];
        asset.on('data', function(chunk) {
            chunks.push(chunk);
            length += chunk.length;
        });
        var buffer;
        function end() {
            if(buffer) {
                return;
            }
            buffer = new Float32Array(length);
            var index = 0;
            for(var i = 0; i < chunks.length; ++i) {
                buffer.set(chunks[i], index);
                index += chunks[i].length;
            }
            resolve(buffer);
        }
        asset.on('end', end);
        // Bind end() to the error event to workaround a bug.
        asset.on('error', end);
        asset.start();
    });
}

function logMelSpectrogram(wav) {
    const stft = AudioUtils.default.stft(wav, N_FFT, FFT_HOP);
    const stftEnergies = stft.map(wnd => AudioUtils.default.fftEnergies(wnd));
    const mel = AudioUtils.default.melSpectrogram(stftEnergies, N_MELS);
    return mel.map(wnd => wnd.map(energy => Math.log(Math.max(energy, 1e-6))));
}

async function preprocess(file) {
    const wav = await decodeMp3(file);
    return logMelSpectrogram(wav);
}

onmessage = async function(event) {
    const prediction = await preprocess(event.data);
    postMessage(prediction);
}
