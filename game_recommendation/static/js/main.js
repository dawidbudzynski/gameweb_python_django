var limit = 7;
$('input[name="tags"]').on('change', function(evt) {
   if($('input[name="tags"]:checked').length >= limit) {
       this.checked = false;
   }
});