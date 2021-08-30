    var slider = tns({
    container: '.photos-slider-awse',
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
    function update_block_photos_awse() {
        $(".images_search_layer_awse_edit").css("max-width",
            document.getElementsByClassName("images_search_layer_awse")[0].clientWidth - 40
        );
    }
    function hide_hint_block_photos_awse() {
        $(".hint_text_images_scroll_awse").css(
        {'visibility': 'hidden', 'margin-bottom': '-3em'}
        );
    }
    $(window).resize(function() {
        update_block_photos_awse();
    });
    setInterval(update_block_photos_awse, 10);
    setTimeout(hide_hint_block_photos_awse, 5000);
});