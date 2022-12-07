console.log('hello world')

const copyBtn = [...document.getElementsByClassName('copy-btn')]
console.log(copyBtn)

copyBtn.forEach(btn=> btn.addEventListener('click', ()=>{
    console.log('click')
    const share = btn.getAttribute('share-link')
    console.log(share)
    navigator.clipboard.writeText(share)
    btn.textContent = 'Link copied!'
}))