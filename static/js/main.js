const notifice = document.getElementById('message');

if (notifice) {
  setTimeout(() => { notifice.style.display = 'none'; }, 6000);
  notifice.addEventListener('click', () => {
    notifice.style.display = 'none';
  })
}

/**********************************************************/

const btn_delete = document.querySelectorAll('#delete');

if (btn_delete) {
   const btnArray = Array.from(btn_delete);
   btnArray.forEach((btn) => {
     btn.addEventListener('click',(e) => {
       if (!confirm('Are you sure, you want to delete it ??'))
       e.preventDefault();
     })
   })
}