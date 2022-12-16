const menuCloseBtn = document.querySelector('.menu-close-btn')
const canvasSidebar = document.querySelector('.canvas-sidebar')
const canvasBackdrop = document.querySelector('.canvas-backdrop')
const menuOpen = document.querySelector('.menu-open')
const menuOpenDiv = document.querySelector('.menu-open-div')
const mainContent = document.querySelector('.main')
const mob = document.querySelector('.mob')
const bd = document.querySelector('.bd')


// bd.addEventListener('click', close)
menuCloseBtn.addEventListener('click', close)
function close(){
    console.log(canvasBackdrop)
    menuCloseBtn.classList.toggle('hidden')
    canvasSidebar.classList.remove("translate-x-0")
    canvasSidebar.classList.add("-translate-x-full")
    canvasBackdrop.classList.remove('opacity-100')
    canvasBackdrop.classList.add('opacity-0')
    menuOpenDiv.classList.remove('z-10')
    menuOpenDiv.classList.add('show')
    menuOpenDiv.classList.add('bg-green-200')
    // mainContent.classList.add('z-50')
    setTimeout(contentAppear, 1000)
    // setTimeout(mobMenuClose, 1000)
}
// mob.addEventListener('click', close)
menuOpen.addEventListener('click', open)
function open(){
    menuOpenDiv.classList.remove('show')
    menuOpenDiv.classList.add('z-10')
    canvasSidebar.classList.remove("-translate-x-full")
    canvasSidebar.classList.add("translate-x-0")
    canvasSidebar.classList.add("z-50")
    menuCloseBtn.classList.toggle('hidden')
    canvasBackdrop.classList.remove('opacity-0')
    canvasBackdrop.classList.add('opacity-100')
    // mainContent.classList.remove('z-50')
    setTimeout(contentAppear, 1)
    // mobMenuOpen()
}
function contentAppear(){
    mainContent.classList.toggle('show')
}
function contentDisappear(){
    mainContent.classList.remove('z-50')
}
canvasBackdrop.addEventListener('click', function(){
    console.log('backdrop clicked')
})
canvasSidebar.addEventListener('click', function(){
    console.log('canvasSidebar clicked')
})
function mobMenuClose(){
    // mob.classList.remove('relative')
    // mob.classList.add('hidden')
    mob.classList.remove('relative')
    mob.classList.add('hidden')
}
function mobMenuOpen(){
    mob.classList.remove('hidden')
    mob.classList.add('relative')
}

function handleClickOutside(event){
    console.log(event.target)
}
document.addEventListener('click', handleClickOutside)