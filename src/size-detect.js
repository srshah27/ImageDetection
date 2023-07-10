
let options_exe = {
  mode: "text",
  pythonPath: "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
};

let options_py = {
  mode: "text",
  pythonOptions: ["-u"], // get print results in real-time
  pythonPath: "C:\\Users\\dusng\\Documents\\GitHub\\image-dimension-electron-app\\src\\engine\\size-detect-env\\Scripts\\python.exe",
};
// possible type of messages passed by python code to javascript
// tn = total number of images sent to python
// sd = started on image number
// cd = current number of images currently processed
// er = error message to see if manual stitching is required
// er_msg = shows files with errors
// fd = file directory of the stitched image
// finished = save file location of the stitched image

let { PythonShell } = require("python-shell");
// let pyshell = new PythonShell("./src/engine/trial.py", options_py); // for when py is converted to exe
// let pyshell = new PythonShell("./src/trial.exe", options_exe); // for when py is converted to exe
let pyshell = new PythonShell("./resources/app/src/trial.exe", options_exe);  // for when py is converted to exe

fileNames = [];
hasPythonCodeRun = false;
hasPythonCodeStarted = false;
var imageUpload = document.getElementById("image-upload");
// const imageContainer = document.getElementById('image-container');
imageUpload.addEventListener("change", function (event) {

  // // Create a FileReader object
  // const reader = new FileReader();
  
  // // Set up the reader to load the image
  // reader.onload = function(e) {
  //   // Create a new image element
  //   const img = document.createElement('img');
    
  //   // Set the source of the image to the loaded file
  //   img.src = e.target.result;
    
  //   // Wait for the image to load
  //   img.onload = function() {
  //     // Create a canvas element
  //     const canvas = document.createElement('canvas');
  //     const ctx = canvas.getContext('2d');
      
  //     // Calculate the desired width and height for the resized image
  //     const maxWidth = 300; // Change this value to your desired maximum width
  //     const maxHeight = 300; // Change this value to your desired maximum height
  //     let width = img.width;
  //     let height = img.height;
      
  //     // Adjust the width and height if necessary to fit within the maximum dimensions
  //     if (width > maxWidth || height > maxHeight) {
  //       const aspectRatio = width / height;
        
  //       if (aspectRatio > 1) {
  //         width = maxWidth;
  //         height = width / aspectRatio;
  //       } else {
  //         height = maxHeight;
  //         width = height * aspectRatio;
  //       }
  //     }
      
  //     // Set the canvas dimensions to the rotated image dimensions
  //     canvas.width = height;
  //     canvas.height = width;
      
  //     // Rotate the canvas to make the image vertical
  //     ctx.translate(height, 0);
  //     ctx.rotate(90 * Math.PI / 180);
      
  //     // Draw the rotated image onto the canvas
  //     ctx.drawImage(img, 0, 0, width, height);
      
  //     // Convert the canvas content to a data URL
  //     const rotatedImageSrc = canvas.toDataURL();
      
  //     // Create a new image element for the rotated image
  //     const rotatedImg = document.createElement('img');
      
  //     // Set the source of the rotated image to the data URL
  //     rotatedImg.src = rotatedImageSrc;
      
  //     // Append the rotated image to the image container
  //     imageContainer.appendChild(rotatedImg);
  //   };
  // };
  

  // Reset state to before python code was run
  const path = require("path");
  hasPythonCodeRun = false;
  var files = event.target.files;
  for (var i = 0; i < files.length; i++) {
    fileNames.push(files[i].path);
  }
  console.log(event.target.files);
  pyshell.send(fileNames);
  console.log(fileNames);
  

  hasPythonCodeStarted = true;
  pythonRunner(files);
  var imageUploadLabel = document.getElementById("uploadtour");
  imageUploadLabel.classList.add("d-none");
});

function pythonRunner(files) {
  // // Create a FileReader object
  // const reader = new FileReader();
  
  // // Set up the reader to load the image
  // reader.onload = function(e) {
  //   // Create a new image element
  //   const img = document.createElement('img');
    
  //   // Set the source of the image to the loaded file
  //   img.src = e.target.result;
    
  //   // Wait for the image to load
  //   img.onload = function() {
  //     // Clear the previous images
  //     imageContainer.innerHTML = '';

  //     // Create a canvas element
  //     const canvas = document.createElement('canvas');
  //     const ctx = canvas.getContext('2d');
      
  //     // Calculate the desired width and height for the resized image
  //     const maxWidth = 300; // Change this value to your desired maximum width
  //     const maxHeight = 300; // Change this value to your desired maximum height
  //     let width = img.width;
  //     let height = img.height;
      
  //     // Adjust the width and height if necessary to fit within the maximum dimensions
  //     if (width > maxWidth || height > maxHeight) {
  //       const aspectRatio = width / height;
        
  //       if (aspectRatio > 1) {
  //         width = maxWidth;
  //         height = width / aspectRatio;
  //       } else {
  //         height = maxHeight;
  //         width = height * aspectRatio;
  //       }
  //     }
      
  //     // Set the canvas dimensions to the rotated image dimensions
  //     canvas.width = height;
  //     canvas.height = width;
      
  //     // Rotate the canvas to make the image vertical
  //     ctx.translate(height, 0);
  //     ctx.rotate(90 * Math.PI / 180);
      
  //     // Draw the rotated image onto the canvas
  //     ctx.drawImage(img, 0, 0, width, height);
      
  //     // Convert the canvas content to a data URL
  //     const rotatedImageSrc = canvas.toDataURL();
      
  //     // Create a new image element for the rotated image
  //     const rotatedImg = document.createElement('img');
      
  //     // Set the source of the rotated image to the data URL
  //     rotatedImg.src = rotatedImageSrc;

  //     // Append the rotated image to the image container
  //     imageContainer.appendChild(rotatedImg);
  //   };
  // };

  var progressBarParent = document.getElementById("progress-bar-parent");
  progressBarParent.classList.remove("d-none");

  var outputMessage = document.getElementById("python-output");
  outputMessage.classList.remove("d-none");
  let cdTotal = 0;
  let errors = [];
  localStorage.removeItem("errors")

  pyshell.on("message", function (message) {

    console.log(message);
    const [typeofmessage, messagecode] = message.split(":");

    if (typeofmessage == "sd") {
      sd = messagecode;
      if (sd==0){
        const defaultImage = document.getElementById('default-image');
        // defaultImage.classList.add('d-none');
      }
      // Read the file as a data URL
      console.log(files[sd]);
      // reader.readAsDataURL(files[sd]);
    }


    if (typeofmessage == "fd") {
      console.log(message);
      console.log("stitched image saved");
      let strippedPath = message.replace(/^fd:/, "");
      // let outputMessage = document.getElementById('file-directory');
      // outputMessage.innerHTML = "Stitched image will be saved at: " + strippedPath;
      // fd = path.join(strippedPath, 'image1.png');
      localStorage.setItem("finalImageFolder", strippedPath);
      historyFolder = strippedPath.replace(
        "result-images",
        "result-images-history"
      );
      localStorage.setItem("historyFolder", historyFolder);
    }

    if (typeofmessage == "tn") {
      tn = messagecode;
      var outputMessage = document.getElementById("python-output");
      // outputMessage.classList.remove("d-none");
      outputMessage.innerHTML =
        '<i class="bi bi-info-circle-fill"></i> ' +
        tn +
        " Image(s) Selected for Size Measurement";
    }

    if (typeofmessage == "cd") {
      cd = messagecode;
      cdTotal = cdTotal + parseFloat(cd);
      let percentageDone = (cdTotal / tn) * 100;
      console.log(percentageDone);
      var progressBar = document.getElementById("progress-bar");
      progressBar.setAttribute("aria-valuenow", percentageDone);
      progressBar.style.width = percentageDone + "%";
      // progressBar.value = percentageDone;
      outputMessage = document.getElementById("python-output");
      // outputMessage.classList.replace("alert-info", "alert-success");
      outputMessage.innerHTML =
        '<i class="bi bi-info-circle-fill"></i> ' +
        parseInt(cdTotal) +
        " of " +
        tn +
        " Images Processed";
    }

    if (typeofmessage == "er") {
      hasPythonCodeRun = true;
      if (messagecode == 0) {
        console.log(messagecode);
        console.log("no stitching needed");
        // console.log(fd);
        var fileOpenButton = document.getElementById("file-open-button");
        var fileCopyButton = document.getElementById("copy-path-button");
        var outputMessage = document.getElementById("python-output");
        var progressBar = document.getElementById("progress-bar");


        fileOpenButton.style.display = "block";
        fileCopyButton.style.display = "block";

        errors = localStorage.getItem("errors")

        if (localStorage.getItem("errors") !== null) {
          console.log("errors");
          errors = localStorage.getItem("errors").split(",");
          outputMessage.classList.replace("alert-info", "alert-warning");
          outputMessage.classList.replace("alert-danger", "alert-warning");
          outputMessage.innerHTML = '<i class="bi bi-exclamation-triangle"></i> All Images Processed, An Error Occured in ' + errors;
          progressBar.classList.add("bg-warning");
        }

        else {
          outputMessage.classList.replace("alert-info", "alert-success");
          outputMessage.innerHTML = '<i class="bi bi-check-lg"></i> All Images Measured Successfully!';
          progressBar.classList.add("bg-success");

        }

        percentageDone = 100;
        progressBar.setAttribute("aria-valuenow", percentageDone);
        progressBar.style.width = percentageDone + "%";
      }
    }

    if (typeofmessage == "er_msg") {
      hasPythonCodeRun = true;
      var outputMessage = document.getElementById("python-output");
      outputMessage.classList.replace("alert-info", "alert-danger");
      outputMessage.innerHTML = '<i class="bi bi-exclamation-triangle"></i> An Error Occured in ' + messagecode + '. Please Try Again.';

      errors.push(messagecode);
      localStorage.setItem("errors", errors);


    }

    if (typeofmessage == "finished") {
      let strippedPath = message.replace(/^finished:/, "");
      // shell.openPath(strippedPath);
      localStorage.setItem("finalImagePath", strippedPath);
    }
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err, code, signal) {
    if (err) {
      console.log(err);
      console.log("An error occured");
      var outputMessage = document.getElementById("python-output");
      outputMessage.classList.replace("alert-info", "alert-danger");
      outputMessage.innerHTML = '<i class="bi bi-exclamation-triangle"></i> An Error Occured. Please Try Again.';

      var fileOpenButton = document.getElementById("file-open-button");
      fileOpenButton.style.display = "block";

      percentageDone = 100;
      var progressBar = document.getElementById("progress-bar");
      progressBar.setAttribute("aria-valuenow", percentageDone);
      progressBar.style.width = percentageDone + "%";
      progressBar.classList.add("bg-danger");

    }
    hasPythonCodeRun = true;
    console.log("The exit code was: " + code);
    console.log("The exit signal was: " + signal);
    console.log("finished");
  });
}

openCSV = () => {
  var fileCopyButton = document.getElementById("copy-path-button");
  finalImagePath = localStorage.getItem("finalImagePath");
  const { shell } = require("electron"); // deconstructing assignment
  shell.openPath(finalImagePath);
  setTimeout(function () {
    fileCopyButton.innerHTML =
      '<i class="bi bi-file-check"></i> Open CSV File';
  }, 1000);
};

resetPage = () => {
  window.location.reload();
};