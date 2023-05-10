var wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'black',
    progressColor: 'red',
    cursorColor: 'navy',
    barWidth: 3,
    barGap: 1,
    responsive: true,
    height: 150,
    scrollParent: true,
});

wavesurfer.load('{{ audio_file_path }}');

var playButton = document.querySelector('#playPause');
var stopButton = document.querySelector('#stop');
var zoomInButton = document.querySelector('#zoom-in');
var zoomOutButton = document.querySelector('#zoom-out');
var annotationsButton = document.querySelector('#annotations');

playButton.addEventListener('click', function () {
    wavesurfer.playPause();
});

stopButton.addEventListener('click', function () {
    wavesurfer.stop();
});

zoomInButton.addEventListener('click', function () {
    wavesurfer.zoom(0.5);
});

zoomOutButton.addEventListener('click', function () {
    wavesurfer.zoom(-0.5);
});
