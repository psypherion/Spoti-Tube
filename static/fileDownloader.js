// Function to select or deselect all checkboxes
function selectAll() {
    // Get all checkboxes with the name "file"
    var checkboxes = document.getElementsByName("file");
    // Get the "Select All" checkbox
    var selectAllCheckbox = document.getElementById("select-all");

    // Loop through each checkbox and set its checked property
    // to match the state of the "Select All" checkbox
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = selectAllCheckbox.checked;
    }
}

// Function to download selected files
function downloadSelectedFiles() {
    // Get all checkboxes with the name "file"
    var checkboxes = document.getElementsByName("file");

    // Iterate through each checkbox using forEach
    checkboxes.forEach(function(checkbox) {
        // Check if the checkbox is checked
        if (checkbox.checked) {
            // Create a new anchor element
            var link = document.createElement('a');
            // Set the href attribute to the file path
            link.href = '/static/downloads/jazz_4_u/' + checkbox.value;
            // Set the download attribute to the file name
            link.download = checkbox.value;
            // Hide the anchor element
            link.style.display = 'none';
            // Append the anchor element to the document body
            document.body.appendChild(link);
            // Trigger a click event on the anchor element
            link.click();
            // Remove the anchor element from the document body
            document.body.removeChild(link);
        }
    });
}
