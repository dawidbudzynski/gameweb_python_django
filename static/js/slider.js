var cnt = 0,
  texts = [];

$(".textContent").each(function() {
  texts[cnt++] = $(this).html();
});

function slide() {
  if (cnt >= texts.length) cnt = 0;
  $('#textMessage').html(texts[cnt++]);
  $('#textMessage')
    .fadeIn(3000).delay(3000)
    .fadeOut(3000, slide);
}
slide();