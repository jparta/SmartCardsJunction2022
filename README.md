# Get to know your payment card!
Exploring the content of payment cards at [Junction2022](https://app.hackjunction.com/dashboard/junction-2022-1/challenge) 

![image](https://user-images.githubusercontent.com/45148109/200143564-febaff8e-0a6d-4258-8c6b-87ddef45029a.png)

## Table of Contents

- [Demo link](#demo_link)
- [What](#what)
- [Why](#why)
- [Installation](#installation)
- [Test](#tests)
- [Privacy](#privacy)
- [Team](#team)
- [Credits](#credits)
- [License](#license)

---

## Demo link

Try it out the [webapp](http://trojar.pythonanywhere.com/)! (Although we have limited credits, so the website might go offline any time :( )

## What

![image](https://user-images.githubusercontent.com/45148109/200143649-2a266a0d-a10e-4442-9af7-6950e61f69e5.png)


### The Evil Side: Data from the card
This repo contains all the data extracted from a **test** payment card via a smart reader (public keys for its security, as well!), and converted from bytes to human-readable text. You can find them [here](https://github.com/jparta/SmartCardsJunction2022/blob/main/all_card_data.txt).

![image](https://user-images.githubusercontent.com/45148109/200143693-bb13b614-a13f-40df-b20e-ad7700a019f8.png)


### The Good Side: Making users aware
We built an [app](https://github.com/jparta/SmartCardsJunction2022/blob/main/app.py) that runs in the browser and nicely translates the data from the card into text, tables, and charts. The app is able to provide timely notification regarding suspect anomalies, for example when offline verification becomes suspiciously frequent or when the approved amount for transactions seems too high compared with past behaviour.

![image](https://user-images.githubusercontent.com/45148109/200143655-4a559cd3-7ff9-4794-a81c-efae3683699f.png)

![image](https://user-images.githubusercontent.com/45148109/200143705-2ae7a7d2-4738-4d1b-918c-f6bf9c014351.png)


## Why

Uncover juicy information and find out how much our cards know about the world around them.

![image](https://user-images.githubusercontent.com/45148109/200143725-e3c18ba5-dd38-4607-8c6f-75f2ef1d0305.png)


## Installation

Note: we have saved the test card data as text. The app does not need to connect to a real card reader. We strongly recommend not to try what we did with your payment card.

### Local

1) You need to have python >= 3.8 installed.

2)  Clone this repo to your local machine using 
```shell
$ git clone https://github.com/jparta/SmartCardsJunction2022.git
```

3) Install required libraries
```shell
$ pip install -r requirements.txt
```
 
4) Run the app on you local machine from the root folder of the repository
 ```shell
$ python -m app
```
 
You will be redirected to a local address that can be opened in your favourite browser.

---


## Tests

No time for tests!

Data in the text files is actual data from the card.

Anomalies and historical behaviour are simulated.

---

## Privacy

We have not used our own card or anyone's card!

---

## Team

| <a>**Joonatan**</a> | <a>**Steven**</a> | <a>**Letizia**</a> |
| :---:| :---:| :---:| 
| [![Joonatan](https://avatars2.githubusercontent.com/u/25590558?s=400&v=4)](https://github.com/jparta) | [![Steven](https://avatars.githubusercontent.com/u/28678107?v=4)](https://github.com/thodoan) | [![Letizia](https://avatars1.githubusercontent.com/u/45148109?s=200&v=4)](https://github.com/letiziaia) |

---

## Credits

The project was developed during Junction 2022 and the challenge (together with test card and card reader) was provided by [Nexi](https://www.nexi.it/en.html).

---
## License
- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2022 © Joonatan, Steven, Letizia
