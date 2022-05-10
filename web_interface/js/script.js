// Function for randomly shuffling an array
function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

const inputElement = document.getElementById("uploadFile");
inputElement.addEventListener("change", handleFiles, false);

function handleFiles() {
  console.log("read files")
  const fileList = this.files; /* now you can work with the file list */
  console.log(fileList)
}
