// List of URLs to check
const urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3'
];

// String to search for
const searchString = "THIS PAGE DOESN’T EXIST. RETURN TO THE LAST PAGE YOU VISITED OR BROWSE OUR NEW ARRIVALS.";

// Function to check if a URL contains the specified string
async function checkUrl(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const text = await response.text();
        if (text.includes(searchString)) {
            console.log(url, true);
        } else {
            console.log(url, false);
        }
    } catch (error) {
        console.error('There was a problem with fetching the URL:', error);
    }
}

// Loop through each URL and check if it contains the specified string
urls.forEach(url => checkUrl(url));
