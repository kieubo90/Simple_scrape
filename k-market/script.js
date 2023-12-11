const base_url = 'https://www.k-ruoka.fi/kauppa/tuotehaku/kala-ja-merenelavat';
let page_number = 1;
let max_pages = 3;
function addProductToTable(productName, productPrice) {
    const table = document.getElementById('productData');
    const row = document.createElement('tr');
    row.innerHTML = `<td>${productName}</td><td>${productPrice}</td>`;
    table.appendChild(row);
}

function scrapeData() {

    fetch(base_url)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');

            // Find product containers
            const productContainers = doc.querySelectorAll('li.HoverCard-sc-17t78cx-0.ProductCard__Container-sc-12u3k8m-0.gzzviz.cXoBjH');

            if (productContainers.length === 0) {
				console.log('No more products found.');
				document.getElementById('loading').style.display = 'none';
				document.getElementById('products').style.display = 'table';
				return;
            }
            productContainers.forEach(container => {
                const productNameTag = container.querySelector('div.ProductCard__Name-sc-12u3k8m-6.bWiPwy');
                const productPriceTag = container.querySelector('div.ProductPrice__PriceGrid-sc-u2ag1v-3.xCfNc');

                const productName = productNameTag ? productNameTag.textContent.trim() : 'No Name';
                const productPrice = productPriceTag ? productPriceTag.textContent.trim() : 'No Price';

                console.log(`Product Name: ${productName}, Product Price: ${productPrice}`);
				addProductToTable(productName, productPrice);
			});
			page_number++;
			if (page_number <= max_pages)
			{	
            	scrapeData(); // Recursively scrape the next page
			}
        })
		.catch(error => console.error('Error:', error));
}

scrapeData();

