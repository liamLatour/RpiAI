var fs = require('fs');
const {PythonShell} = require('python-shell');

function saveFile(content, path) {
    fs.writeFile(path, content, (err) => {
        if (err) {
            console.log(err);
        }
    });
}

function readFile(path, callback) {
    fs.readFile(path, 'utf-8', (err, data) => {
        if (err) {
            console.log("An error ocurred reading the file :" + err.message);
        }
        callback(data);
    });
}

function getMarks() {
    const myPythonScriptPath = './pythonLib/fetchHomework.py';
    const pyshell = new PythonShell(myPythonScriptPath);

    // Launch Python script
    pyshell.on('message', function (message) {
        try {
            var currentMarks = JSON.parse(message);
            readFile("note.json", function(data){
                var difference = [];
                var oldMarks = JSON.parse(data);

                if (oldMarks != undefined){
                    for(let mark in currentMarks){
                        if(oldMarks.hasOwnProperty(mark)){
                            for(let note in currentMarks[mark]){
                                if(!(oldMarks[mark].hasOwnProperty(note) && isEquivalent(oldMarks[mark][note], currentMarks[mark][note]))){
                                    difference.push({mark: currentMarks[mark][note]});
                                }
                            }
                        }
                        else{
                            difference.push({mark: currentMarks[mark]});
                        }
                    }
                }
                else{
                    console.log("new");
                    difference = currentMarks;
                }

                if (difference != []) {
                    console.log(difference);
                    saveFile(message, "note.json");
                }

                pyshell.terminate();
            });
        } catch(err) {
            console.log(err);
        }
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) {
            throw err;
        };
        alert('finished');
    });
};

function isEquivalent(a, b) {
    var aProps = Object.getOwnPropertyNames(a);
    var bProps = Object.getOwnPropertyNames(b);

    if (aProps.length != bProps.length) {
        return false;
    }

    for (var i = 0; i < aProps.length; i++) {
        var propName = aProps[i];
        if (a[propName] !== b[propName]) {
            return false;
        }
    }
    return true;
}

getMarks();