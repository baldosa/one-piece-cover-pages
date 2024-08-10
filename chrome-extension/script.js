function loadBackground() {
    const imgs = JSON.parse(window.localStorage.getItem('data'))
    const randomElement = Math.floor(Math.random() * imgs.length)
    let baseUrl = `https://raw.githubusercontent.com/baldosa/one-piece-cover-pages/a6d45aeb8be1357bace3c8f4eea3f8abb77d0b78/images/${imgs[randomElement].replace(' ', '%20')}`
    document.body.style.backgroundImage = `url(${baseUrl})`;

}

// checks previous download date
const lastDw = window.localStorage.getItem('lastDownload')
const now = new Date()

// if older than 7 days download json to localstorage
if ((now - lastDw) / (1000 * 60 * 60 * 24) >= 7) {

    fetch('https://raw.githubusercontent.com/baldosa/one-piece-cover-pages/master/images.json')
        .then((response) => response.json())
        .then((json) => {
            window.localStorage.setItem('data', JSON.stringify(json.map((el) => el['filename'])))
            window.localStorage.setItem('lastDownload', Date.now())
            loadBackground()
        });
} else {
    loadBackground()
}





