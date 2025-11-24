const apiKey = "CG-uzWUEcWBhZ63foqxctF6JRDE"
const url = 'https://api.coingecko.com/api/v3/coins/markets/?vs_currency=usd';
const urlCoinsId = 'https://api.coingecko.com/api/v3/coins/bitcoin';
const options = {
    method: 'GET',
    headers: {
        'x-cg-demo-api-key': `${apiKey}`
    },
    body: undefined
};

fetch(urlCoinsId, options)
    .then(response => response.json())
    .then(data => {
        const cryptoCurrencies = data.map(cryptoCurrency => ({
            id: cryptoCurrency.id,
            name: cryptoCurrency.name,
            current_price: cryptoCurrency['current_price'],
            symbol: cryptoCurrency.symbol
        }));
        console.log(cryptoCurrencies);
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        console.log('Request completed');
    });

fetch(urlCoinsId, options)
    .then(response => response.json())
    .then(data => {
        const cryptoCurrencyRates = data['market_data']['current_price'];
        console.log(cryptoCurrencyRates);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    