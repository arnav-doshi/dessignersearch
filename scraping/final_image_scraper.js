// Function to transform thumb URL to high-resolution URL
function transformThumbToHighRes(thumbUrl) {
    // Example transformation
    // Replace the URL pattern according to your requirement
    return thumbUrl.replace('/c_scale,h_280/', '/');
}

// List of URLs
const urls = [

];

// Array to store the transformed data
const transformedData = [];

// Function to fetch and process each URL
async function fetchAndProcessURL(url) {
    try {
        const response = await fetch(url);
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const productTiles = doc.querySelectorAll('.plp-products__row .plp-products__product-tile');

        productTiles.forEach(tile => {
            // Extracting span text
            const brandName = tile.querySelector('.product-tile__description .s-row:nth-child(1) .s-text').textContent.trim();
            const productName = tile.querySelector('.product-tile__description .s-row:nth-child(2) .s-text').textContent.trim();
            const productPrice = tile.querySelector('.product-tile__description .s-row:nth-child(3) .s-text').textContent.trim();

            const imgSrc = tile.querySelector('img').dataset.srcset;
            const highResUrl = transformThumbToHighRes(imgSrc);

            // Extract href attribute
            const href = tile.querySelector('a').getAttribute('href');

            transformedData.push(`${brandName} : ${productName} : ${productPrice} : ${href} : ${highResUrl}`);
        });
    } catch (error) {
        console.error('Error fetching URL:', error);
    }
}

// Fetch and process each URL
Promise.all(urls.map(fetchAndProcessURL))
    .then(() => {
        // Create a Blob containing the data
        const blob = new Blob([transformedData.join('\n')], { type: 'text/plain' });
        
        // Create a temporary anchor element
        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = 'transformed_data.txt';
        
        // Trigger a click event to prompt the user to download the file
        a.click();
    });
