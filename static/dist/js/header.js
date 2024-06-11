const openBtn = document.querySelector('#open-main-menu')
const mainMenu = document.querySelector('#headlessui-dialog-panel')
const closeMenu = document.querySelector('#close-menu')

openBtn.addEventListener('click', () => {
  mainMenu.classList.remove('hidden')
})

closeMenu.addEventListener('click', () => {
  mainMenu.classList.add('hidden')
})

window.addEventListener('resize', function () {
  if (window.innerWidth > 1024) {
    mainMenu.classList.add('hidden')
  }
})

const authSm = document.querySelector('.auth-sm')
const loginSm = authSm.querySelector('.login-btn')
const loginBtn = document.querySelector('.login-btn')

function onAuth(e) {
  location.href = '/login'
}
loginSm.addEventListener('click', onAuth)
loginBtn.addEventListener('click', onAuth)
