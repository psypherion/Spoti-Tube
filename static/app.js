// Wait for the DOM to be fully loaded before executing the code
document.addEventListener('DOMContentLoaded', function () {
    // Read the text file using the Fetch API
    fetch('songs.txt')
      .then(response => response.text())
      .then(data => parseAndDisplaySongs(data)) // Once the data is fetched, call the function to parse and display songs
      .catch(error => console.error('Error reading file:', error)); // Log an error if fetching fails
  });
  
  // Function to parse and display songs from the data
  function parseAndDisplaySongs(data) {
    // Get the HTML element where the song list will be displayed
    const songListElement = document.getElementById('songList');
    // Get the HTML element representing the "Select All" button
    const selectAllButton = document.getElementById('selectAll');
  
    // Split the data into individual songs based on the double line breaks
    const songs = data.split('\n\n');
    
    // Loop through each song and extract title and artist
    songs.forEach((song, index) => {
      // Use regular expressions to match the title and artist in the song data
      const titleMatch = song.match(/Title: (.+)/);
      const artistMatch = song.match(/Artist: (.+)/);
  
      // Check if both title and artist are found in the song data
      if (titleMatch && artistMatch) {
        // Extract the title and artist from the matched groups
        const title = titleMatch[1];
        const artist = artistMatch[1];
  
        // Create a list item for each song with a checkbox
        const listItem = document.createElement('li');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `song${index}`;
        listItem.appendChild(checkbox);
  
        // Create a label for the checkbox with the title and artist
        const label = document.createElement('label');
        label.htmlFor = `song${index}`;
        label.textContent = `${title} by ${artist}`;
        listItem.appendChild(label);
  
        // Append the list item to the song list element
        songListElement.appendChild(listItem);
      }
    });
  
    // Add an event listener to the "Select All" button
    selectAllButton.addEventListener('click', function () {
      // Select all checkboxes when the "Select All" button is clicked
      const checkboxes = document.querySelectorAll('input[type="checkbox"]');
      checkboxes.forEach(checkbox => (checkbox.checked = true));
    });
  }
  