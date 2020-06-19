document.addEventListener('DOMContentLoaded', () => {

var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', () => {
  var k = document.querySelector('#submit');
  document.querySelector('#submit').disabled = true;
  document.querySelector('#text').onkeyup = () => {
  if (document.querySelector('#text').value.length > 0)
      document.querySelector('#submit').disabled = false;
  else
      document.querySelector('#submit').disabled = true;
  };
  k.onclick = () => {
    var input =  document.querySelector('#text');
    var message = input.value;
    var cname = document.querySelector('h1').innerHTML;
    document.querySelector('#text').value='';
    document.querySelector('#submit').disabled = true;
    socket.emit('add message',{'message':message , 'cname':cname});

  }
  var s=document.getElementsByName('button');
  s.forEach(del);
  function del(item) {
    item.onclick = cut;
    function cut()  {
      var k=item.parentElement.parentElement.parentElement.querySelector("p");
      var username=k.querySelector('b').innerHTML;
      var msg=k.querySelectorAll('span')[0].innerHTML;
      var time=k.querySelectorAll('span')[1].innerHTML;
      var cname = document.querySelector('h1').innerHTML;
      socket.emit('delete message',{'username':username,'msg':msg,'time':time,'cname':cname});
    }

  }

});
socket.on('display message', data => {

    var div = document.createElement('div');
    div.innerHTML = `<li><p><b>${data.user}</b><br><span>${data.msg}</span><button type="button" style="float: right;" class="btn btn-primary" name="button" onclick="c(this)">Delete Message</button><br><span>${data.time}</span><br></p></li>`;
    var button = div.querySelector('button');
    var line = document.createElement('br');
    div.append(line);
    document.querySelector('#messages').append(div);
    button.onclick = () => {
      var k=button.parentElement.parentElement.parentElement.querySelector("p");
      var username=k.querySelector('b').innerHTML;
      var msg=k.querySelectorAll('span')[0].innerHTML;
      var time=k.querySelectorAll('span')[1].innerHTML;
      var cname = document.querySelector('h1').innerHTML;
      socket.emit('delete message',{'username':username,'msg':msg,'time':time,'cname':cname});
    }

});
socket.on('removed', data => {
  var all=document.querySelectorAll('p');
  all.forEach(one);
  function one(item) {
    if(item.querySelector('b').innerHTML == data['username'] && item.querySelectorAll('span')[0].innerHTML == data['msg'] && item.querySelectorAll('span')[1].innerHTML == data['time'])
    {
      console.log(item.parentElement.innerHTML);
      item.parentElement.parentElement.innerHTML='';
    }
  }
});





});
window.addEventListener('beforeunload', function () {
  console.log(window.location.href);
  localStorage.setItem('channel',window.location.href);
});
