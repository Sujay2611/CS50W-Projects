if(localStorage.getItem('channel'))
{
  window.location.href=localStorage.getItem('channel');
  localStorage.removeItem('channel');
}

window.addEventListener('beforeunload', function () {
  document.querySelector('input').value='';
});
