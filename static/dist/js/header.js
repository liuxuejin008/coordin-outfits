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


auth0.createAuth0Client({
  domain: "dev-7t0ooaglcqz4tfqr.us.auth0.com",
  clientId: "RY0zAv7O3WYplPe1WKgslwQ8996oN6KK",
  authorizationParams: {
    redirect_uri: window.location.origin + window.location.pathname
  }
}).then(async (auth0Client) => {
  // login
  const authSm = document.querySelector('.auth-sm')
  const userSm = authSm.querySelector('.user')
  const loginSm = authSm.querySelector('.login-btn')

  const loginSmShowClass = 'inline-flex'
  const userSmShowClass = 'flex' 
  const showClass = 'md:flex'

  const userWarper = document.querySelector('.user-warper')
  const loginBtn = document.querySelector('.login-btn')
  const user = userWarper.querySelector('.user');

  function setNameAndAvatar(user, userProfile) {
    user.querySelector('img').src = userProfile.picture;
    user.querySelector('.user-name').textContent = userProfile.name;
  }

  function onAuth(e) {
    e.preventDefault();
    auth0Client.loginWithRedirect({
      authorizationParams: {
        redirect_uri: window.location.origin + window.location.pathname
      }
    });
  }

  loginSm.addEventListener('click', onAuth)
  loginBtn.addEventListener('click', onAuth)


  if (location.search.includes("state=") &&
    (location.search.includes("code=") ||
      location.search.includes("error="))) {
    try {
      await auth0Client.handleRedirectCallback();
      window.history.replaceState({}, document.title, location.pathname);
    } catch (e) {
      alert(e.message)
      console.error(e);
    }
  }


  const isAuthenticated = await auth0Client.isAuthenticated();
  const userProfile = await auth0Client.getUser();

  if (isAuthenticated) {
    loginSm.classList.add('hidden')
    loginBtn.classList.remove(showClass)
    userSm.classList.remove('hidden')
    userSm.classList.add(userSmShowClass)
    setNameAndAvatar(userSm, userProfile)
    setNameAndAvatar(user, userProfile)
    userWarper.classList.add(showClass)
  } else {
    debugger
    userSm.classList.add('hidden')
    userSm.classList.remove(userSmShowClass)
    loginSm.classList.remove('hidden')
    loginSm.classList.add(loginSmShowClass)
    loginBtn.classList.add(showClass)
    loginBtn.classList.remove('hidden')
  }
})