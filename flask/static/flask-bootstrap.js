const textarea = document.querySelector('#inputText')

textarea.addEventListener('keydown', (e) => {
  if (e.keyCode === 9) {
    e.preventDefault()
    document.execCommand("insertText", false, "\t")
  }
})