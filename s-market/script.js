const base_url = 'https://www.s-kaupat.fi/tuotteet/makeiset-ja-naposteltavat-1/karkkipussit';
let page_number = 1;

function addProductToTable(productName, productPrice) {
    const table = document.getElementById('productData');
    const row = document.createElement('tr');
    row.innerHTML = `<td>${productName}</td><td>${productPrice}</td>`;
    table.appendChild(row);
}

function scrapeData() {
    const url = `${base_url}?page=${page_number}`;

    fetch(url)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');

            // Find product containers
            const productContainers = doc.querySelectorAll('div.sc-ddb02d9f-0.dHHZyS');

            if (productContainers.length === 0) {
				console.log('No more products found.');
				document.getElementById('loading').style.display = 'none';
				document.getElementById('products').style.display = 'table';
				return;
            }

            productContainers.forEach(container => {
                const productNameTag = container.querySelector('span.sc-4dcde147-0.egffZb');
                const productPriceTag = container.querySelector('span.sc-68088102-0.jusdFT');

                const productName = productNameTag ? productNameTag.textContent.trim() : 'No Name';
                const productPrice = productPriceTag ? productPriceTag.textContent.trim() : 'No Price';

                console.log(`Product Name: ${productName}, Product Price: ${productPrice}`);
				addProductToTable(productName, productPrice);
            });
			
            page_number++;
			scrapeData(); // Recursively scrape the next page
        })
        .catch(error => console.error('Error:', error));
}
window.scrollTo({
	top: document.body.scrollHeight,
	left: 0,
	behavior: 'smooth'
  });
  
scrapeData();
