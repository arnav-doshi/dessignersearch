// BUGGED. SEES IF 9 OR NOT

async function getNextPageNumber(url) {
    try {
        const response = await fetch(url);
        if (response.status === 404) {
            console.log(`${url} 1`);
            return;
        }
        const html = await response.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const lastPageElements = doc.querySelectorAll('li.pagination__last-page');

        if (lastPageElements.length > 1) {
            const nextPageHref = lastPageElements[lastPageElements.length - 2].querySelector('a').getAttribute('href');
            const pageNumber = nextPageHref.match(/\d+$/)[0]; // Extracting the last number
            console.log(`${url} ${pageNumber}`);
        } else if (lastPageElements.length === 1) {
            const nextPageHref = lastPageElements[0].querySelector('a').getAttribute('href');
            const pageNumber = nextPageHref.match(/\d+$/)[0]; // Extracting the last number
            console.log(`${url} ${pageNumber}`);
        } else {
            console.log(`${url} 1`);
        }
    } catch (error) {
        console.error(`Error fetching or parsing the HTML for ${url}:`, error);
    }
}

const websiteURLs = [
    'https://www.ssense.com/en-us/men/designers/rick-owens',
    // Add more URLs here
];

async function processURLs() {
    for (const url of websiteURLs) {
        await getNextPageNumber(url);
    }
}

processURLs();
