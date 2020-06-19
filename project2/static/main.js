document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#add').onclick = count;
});
function count() {
  document.querySelector("#add").style.display="none";
  var f = document.createElement("form");
  f.setAttribute('id','form1');
  f.setAttribute('method',"post");
  f.setAttribute('style',"margin-top:20px;");

  var t=document.createElement("div");
  t.setAttribute('class',"form-group");

  var i = document.createElement("input");
  i.setAttribute('type',"text");
  i.setAttribute('name',"channelname");
  i.setAttribute('class',"form-control");
  i.setAttribute('placeholder',"Channel Name");
  i.setAttribute('style',"margin-bottom:20px;");
  i.setAttribute('required','');

  var s = document.createElement("button");
  s.setAttribute('type',"submit");
  s.setAttribute('class',"btn btn-primary");
  s.setAttribute('id','create');
  s.setAttribute('onclick','addchannel()');
  s.setAttribute('style',"margin-bottom:20px;");

  s.innerHTML="Create";

  f.appendChild(i);
  f.appendChild(s);

  var g=document.querySelector(".dropdown");
  g.parentNode.insertBefore(f,g);

  var h=document.querySelector(".dropdown-menu");
  var j=document.createElement("a");
  j.setAttribute('class','dropdown-item');
  j.innerHTML=" {{ cname }} ";
  h.options.add(j);
}

window.addEventListener('beforeunload', function () {
  if(localStorage.getItem('channel'))
  {
    localStorage.removeItem('channel');
  }
});
