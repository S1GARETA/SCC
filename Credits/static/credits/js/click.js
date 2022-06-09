function GameSession() {
    this.coins = 0
    this.click_power = 1
    this.coins_per_second = 0
    //this.next_level_price = 10

    /** Метод для инициализации данных. Данные подгружаются с бэкенда. */
    this.init = function() {
        getCore().then(core => {
            this.coins = core.coins
            this.click_power = core.click_power
            this.coins_per_second = core.coins_per_second
            //this.next_level_price = core.next_level_price
            render()
        })
    }
    /** Метод для добавления монеток. */
    this.add_coins = function(coins) {
        this.coins += coins
        render()
    }
    /** Метод для добавления невероятной мощи. */
    this.add_power = function(power) {
        this.click_power += power
        render()
    }
    /** Метод для добавления дружинника в отряд автоматизированных кликуш. */
    this.add_auto_power = function(power) {
        this.coins_per_second += power
        render()
    }
}

let Game = new GameSession() // Экземпляр класса GameSession.

/** Функция обработки клика пользователя на какаши. */
function call_click() {
    const coinsNode = document.getElementById('coins')
    Game.add_coins(Game.click_power)
    check_boost()
}

/** Функция для обновления количества монет, невероятной мощи и дружинных кликуш в HTML-элементах. */
function render() {
    const coinsNode = document.getElementById('coins')
    //const clickNode = document.getElementById('click_power')
    const autoClickNode = document.getElementById('coins_per_second')
    coinsNode.innerHTML = Game.coins
    //clickNode.innerHTML = Game.click_power
    autoClickNode.innerHTML = Game.coins_per_second
}

/** Функция получения данных об игре пользователя с бэкенда. */
function getCore() {
    return fetch('core', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}

/** Функция отправки данных о количестве монет пользователя на бэкенд. */
function updateCoins(coins) {
    const csrftoken = getCookie('csrftoken')
    return fetch('update_coins', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            coins: coins
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}

// Покупка и обновление бустов
function buy_boost(boost_id) {
    const csrftoken = getCookie('csrftoken') // Забираем токен из кукесов

    fetch(`boosts/${boost_id}`, {
        method: 'PUT', // Теперь метод POST, потому что мы изменяем данные в базе
        headers: { // Headers - мета-данные запроса
            "X-CSRFToken": csrftoken, // Токен для защиты от CSRF-атак, без него не будет работать
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            coins: Game.coins
        })
    }).then(response => {
        if (response.ok) return response.json()
        else return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        const old_boost_stats = response.old_boost_values
        const new_boost_stats = response.new_boost_values

        const coinsElement = document.getElementById('coins')
        coinsElement.innerText = Number(coinsElement.innerText) - old_boost_stats.price
        //const powerElement = document.getElementById('click_power')
        //powerElement.innerText = Number(powerElement.innerText) + old_boost_stats.power

        Game.add_coins(-old_boost_stats.price)
        if (old_boost_stats.type === 1) {
            Game.add_auto_power(old_boost_stats.power)
        } else {
            Game.add_power(old_boost_stats.power)
        }

        update_boost(new_boost_stats) // Обновляем буст на фронтике
    }).catch(err => console.log(err))
}

function update_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)

    boost_node.querySelector('.product_count').innerText = boost.level
    //boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('.price_text').innerText = boost.price

    check_boost()
}

function check_boost() {
    coins = Number(document.getElementById("coins").innerText)

    miska_boost = document.querySelector(".miska_boost")
    help_old_boost = document.querySelector(".help_old_boost")
    charity_boost = document.querySelector(".charity_boost")

    if (coins >= Number(miska_boost.querySelector('.price_text').innerText)) {
        miska_boost.classList.remove("disabled");
        miska_boost.classList.add("enabled");
    } else {
        miska_boost.classList.remove("enabled");
        miska_boost.classList.add("disabled");
    }
    if (coins >= Number(help_old_boost.querySelector('.price_text').innerText)) {
        help_old_boost.classList.remove("disabled");
        help_old_boost.classList.add("enabled");
    } else {
        help_old_boost.classList.remove("enabled");
        help_old_boost.classList.add("disabled");
    }
    if (coins >= Number(charity_boost.querySelector('.price_text').innerText)) {
        charity_boost.classList.remove("disabled");
        charity_boost.classList.add("enabled");
    } else {
        charity_boost.classList.remove("enabled");
        charity_boost.classList.add("disabled");
    }

}

// Куки
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/** Функция обработки автоматического клика. */
function setAutoClick() {
    setInterval(function() {
        /** Этот код срабатывает раз в секунду. */
        Game.add_coins(Game.coins_per_second)
    }, 1000)
}

/** Функция обработки автоматического сохранения (отправки данных о количестве монет пользователя на бэкенд). */
function setAutoSave() {
    setInterval(function() {
        /** Этот код срабатывает раз в минуту. */
        updateCoins(Game.coins)
    }, 15000)
}

window.onload = function () {
    Game.init() // Инициализация игры.
    setAutoClick() // Инициализация автоклика.
    setAutoSave() // Инициализация автосейва.
    check_boost()
}
