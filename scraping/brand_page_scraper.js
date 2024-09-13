const urls = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
console.log(urls.join('\n'));
