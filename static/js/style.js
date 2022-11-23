const btn_x = document.getElementById('btn-x')
const hamburger = document.getElementById('hamburger')
const menu_btn = document.getElementById('menu-btn')
const mobile_menu = document.getElementById('mobile-menu')
const mob_items = document.querySelectorAll('.mob-item')


// btn_x.addEventListener('click', navToggle)
// menu_btn.addEventListener('click', navToggle)

hamburger.addEventListener('click', hamburger_open)
btn_x.addEventListener('click', hamburger_close)
// mob_item.addEventListener('click', hamburger_close)
function navToggle() {
    console.log('you clicked me')
    // alert('you clicked me bruh')
}
function hamburger_open() {
    hamburger.classList.remove('block')
    hamburger.classList.add('hidden')
    btn_x.classList.remove('hidden')
    btn_x.classList.add('block')
    mobile_menu.classList.remove('hidden')
}

function hamburger_close(){
    btn_x.classList.remove('block')
    btn_x.classList.add('hidden')
    hamburger.classList.remove('hidden')
    hamburger.classList.add('block')
    mobile_menu.classList.add('hidden')
}

mob_items.forEach(item => {
    item.addEventListener('click', hamburger_close)
})
