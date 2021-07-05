    var slider = tns({
    container: '.photos-slider-aware',
    items: 2,
    speed: 500,
    loop: false,
    autoHeight: true,
    mouseDrag: true,
    autoWidth: false,
    swipeAngle: 20,
    preventScrollOnTouch: false,
    lazyload: false,
    controls: false,
    nav: false,
    edgePadding: 0,
    responsive: {
      320: {
        gutter: 5,
        items: 1
      },
      640: {
        gutter: 8,
        items: 2
      },
      700: {
        gutter: 12
      },
      900: {
        items: 3
      },
    }
});
$(document).ready(function() {
    function update_block_photos_aware() {
        $(".images_search_layer_aware_edit").css("max-width",
            document.getElementsByClassName("images_search_layer_aware")[0].clientWidth - 40
        );
    }
    function hide_hint_block_photos_aware() {
        $(".hint_text_images_scroll_aware").css(
        {'visibility': 'hidden', 'margin-bottom': '-4em'}
        );
    }
    $(window).resize(function() {
        update_block_photos_aware();
    });
    setInterval(update_block_photos_aware, 300);
    setTimeout(hide_hint_block_photos_aware, 5000);
});