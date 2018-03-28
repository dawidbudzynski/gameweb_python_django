var cnt = 0,
  texts = [];

// save the texts in an array for re-use
$(".textContent").each(function() {
  texts[cnt++] = $(this).html();
});

function slide() {
  if (cnt >= texts.length) cnt = 0;
  $('#textMessage').html(texts[cnt++]);
  $('#textMessage')
    .fadeIn(3000)
    .fadeOut(5000, slide);
}
slide();