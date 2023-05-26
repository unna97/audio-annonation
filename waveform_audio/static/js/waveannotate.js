function createButtonforRow(button, onclickEvent){
    current_button = document.createElement("button");
    current_button.innerHTML = button;
    current_button.onclick = onclickEvent;
    return current_button;
}

function addRegiontoWaveformer(start_time, end_time, label){
    var region = {
        start: start_time,
        end: end_time,
        data: {
            label: label
        },
        color: 'hsla(40, 70%, 50%, 0.5)'
    }
    wavesurfer.addRegion(region);
}


//called when save button is clicked:
function addtoTable(){
    // get the table:
    var table = document.getElementById("annotation_table");
    // get the start and end times:
    var start_time = document.getElementById('start_time').innerHTML;
    var end_time = document.getElementById('end_time').innerHTML;
    // get the label selected:
    var label = document.getElementById('label').value;
    // create a new row:
    var row = table.insertRow(-1);
    // add the delete button to the row:
    var delete_button = createButtonforRow("Delete", function(){
        // delete the row:
        table.deleteRow(row.rowIndex);
    });
    // insert the delete button into the row:
    row.insertCell(0).appendChild(delete_button);
    var show_region_button = createButtonforRow("Show Region", function(){
        // get the start and end times from same row as the button:
        var start_time = row.cells[0].innerHTML;
        var end_time = row.cells[1].innerHTML;
        var label = row.label;
        // show the region on the waveform:
        addRegiontoWaveformer(start_time, end_time, label);

    });
    // insert the show region button into the row:
    row.insertCell(1).appendChild(show_region_button);


    // insert cells into the row:
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    // add the start and end times to the cells:
    cell1.innerHTML = start_time;
    cell2.innerHTML = end_time;
    cell3.innerHTML = label;
    // add the label to the row:
    row.label = label;
    // add the row to the table:
    table.appendChild(row);
    
    // show the table:
    table.style.display = "block";


}

function createWaveformer(audio_file_path, regions, waveform){

    var wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'black',
        progressColor: 'red',
        cursorColor: 'navy',
        barWidth: 3,
        barGap: 1,
        responsive: true,
        height: 150,

        mediaControls: true,
        backend: 'MediaElement',

        scrollParent: true,

        plugins: [
            WaveSurfer.regions.create(
                {
                    regions: regions,
                    dragSelection: {
                        slop: 5
                    }
                }
            )
        ],
        // enable drag selection:
        dragSelection: true,

        onended: function () {
            console.log('Finished playing');
            wavesurfer.seek(0)
        },
        buffer: 1024 * 1024 * 10 // 10 MB buffer
    });
    //get the waveform which is given as {"waveform": [0.1, 0.2, 0.3]}:\
    console.log("loading new code")
    waveform = JSON.parse(waveform)['waveform'];
    console.log("waveform is: " + waveform);
    var waveform = waveform["waveform"];
    wavesurfer.load(audio_file_path, waveform);
    // return the wavesurfer object:
    return wavesurfer;
}


function showRegionsTable(){
    // button to show all regions on the waveform:
    console.log("showing regions table");
    // delete all current regions:
    wavesurfer.clearRegions();
    // get all rows in the table:
    var table = document.getElementById("annotation_table");
    var rows = table.rows;
    // for each row, get the start and end times and label:
    for (var i = 1; i < rows.length; i++) {
        var start_time = rows[i].cells[0].innerHTML;
        var end_time = rows[i].cells[1].innerHTML;
        var label = rows[i].cells[2].innerHTML;
        // show the region on the waveform:
        addRegiontoWaveformer(start_time, end_time, label);
    }

}



function audiotoWave(
    audio_file_path, waveform
    ) {


    var regions = [
        {
            start: 0,
            end: 1,
            color: 'hsla(400, 100%, 30%, 0.5)'
        },
        {
            start: 2,
            end: 3,
            color: 'hsla(200, 50%, 70%, 0.4)'
        },
        {
            start: 4,
            end: 5,
            color: 'hsla(100, 50%, 70%, 0.4)'
        },
        {
            start: 6,
            end: 7,
            color: 'hsla(100, 70%, 50%, 0.5)'
        }
    ];

    wavesurfer = createWaveformer(audio_file_path, regions, waveform);

    var playButton = document.querySelector('#playPause');
    var stopButton = document.querySelector('#stop');
    

    playButton.addEventListener('click', function () {
        wavesurfer.playPause();
    });

    stopButton.addEventListener('click', function () {
        wavesurfer.stop();
    });

    regions = wavesurfer.regions.list;

    // annotationsButton.addEventListener('click', function () {
    //     // console.log(regions);
    // });

    wavesurfer.on('region-created', function (region) {
        // console.log(region);
    });

    wavesurfer.on('region-updated', function (region) {
        // console.log(region);
    });
    // on double clicking a region, it is deleted:
    wavesurfer.on('region-dblclick', function (region) {
        region.remove();
    });
    // on click a region, it is selected:
    wavesurfer.on('region-click', function (region, e) {
        e.stopPropagation();
        // Play on click, loop on shift click
        e.shiftKey ? region.playLoop() : region.play();
        //update the label start and end times:
        var start_time = document.getElementById('start_time');
        var end_time = document.getElementById('end_time');
        start_time.innerHTML = region.start;
        end_time.innerHTML = region.end;
        // create a region labeller on the html id="label":
        var label = document.getElementById('label').value;

        region.update({
            data: {
                label: label
            }
        });
    });
}
function saveAnnotations() {
    var annotationTable = [];
    var table = document.getElementById("annotation_table");
    var rows = table.rows;
    // for each row, get the start and end times and label:
    for (var i = 1; i < rows.length; i++) {
        var start_time = rows[i].cells[0].innerHTML;
        var end_time = rows[i].cells[1].innerHTML;
        var label = rows[i].cells[2].innerHTML;
        // add the row to the annotation table:
        annotationTable.push({
            "start_time": start_time,
            "end_time": end_time,
            "label": label
        });
    }

    console.log(annotationTable);
    // Send the annotation table data to Django
    // var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrfToken);

    var requestData = {
        "annotation_table": JSON.stringify(annotationTable),
        "csrfmiddlewaretoken": csrfToken
    };

    // $.ajax({
    //     url: "/save_annotations/",
    //     type: "POST",
    //     data: {
    //         "annotation_table": JSON.stringify(annotationTable),
    //         "csrfmiddlewaretoken": csrfToken
    //     },
    //     success: function (response) {
    //         console.log(response);
    //     }
    // });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/save_annotations/");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(requestData));

}
