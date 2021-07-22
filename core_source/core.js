/*
|---------------------------------------|
| This file is the original kernel code |
|---------------------------------------|
*/

function imgError(o) {
    return (o.onerror = ""), (o.src = background_static__), !0;
}

function VideoError(o) {
    o.remove();
    $.notify("Video upload error.", {
        position: "bottom right",
        autoHideDelay: 3000
    });
    AOS.refresh();
}

function BannerError(o) {
    if (o.getAttribute('done') == 'yes') {
        o.remove();
        console.log("Banner load error!");
        AOS.refresh();
    }
}

function edit_query_string_q(data) {
    var queryParams = new URLSearchParams(window.location.search);
    queryParams.set("q", data);
    history.replaceState(null, null, "?" + queryParams.toString());
}

function makeid(length = 64) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(
            Math.floor(
                Math.random() * charactersLength
            ));
    }
    return result;
}

function search_title_set(title_text) {
    document.title = 'AWARE - ' + title_text;
}

function throttle(func, ms) {

    let isThrottled = false,
        savedArgs,
        savedThis;

    function wrapper() {

        if (isThrottled) {
            savedArgs = arguments;
            savedThis = this;
            return;
        }

        func.apply(this, arguments);

        isThrottled = true;

        setTimeout(function() {
            isThrottled = false;
            if (savedArgs) {
                wrapper.apply(savedThis, savedArgs);
                savedArgs = savedThis = null;
            }
        }, ms);
    }

    return wrapper;
}

function get__(enc_key_by_function) {
    var data = '';
    $.ajax({
        url: sync_time__by_server__,
        type: "GET",
        data: {},
        success: function(o) {
            // obfuscate this function before deploy
            var time_unix = new Date().getTime();
            var time_unix_string = time_unix.toString();

            function generator_local_get__(length, mode) {
                // only for function - get__
                var result = '';
                if (mode) {
                    var characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789-=+()*&^%$#@!<>:;|~\\/.,`\'"©®℗\
                    йцукенгшщзхъфывапролджэячсмитьбюїєіЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЇЄІ¢€£¥₮';
                } else {
                    // out num
                    var characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-=+()*&^%$#@!<>:;|~\\/.,\'"`©®℗\
                    йцукенгшщзхъфывапролджэячсмитьбюїєіЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЇЄІ¢€£¥₮';
                }
                var charactersLength = characters.length;
                for (var i = 0; i < length; i++) {
                    result += characters.charAt(Math.floor(Math.random() *
                        charactersLength));
                }
                return result;
            }

            function getRandomInt_local_get__(max) {
                return Math.floor(Math.random() * max);
            }

            function shuffle_local_get__(array) {
                var currentIndex = array.length,
                    temporaryValue, randomIndex;

                while (0 !== currentIndex) {

                    randomIndex = Math.floor(Math.random() * currentIndex);
                    currentIndex -= 1;

                    temporaryValue = array[currentIndex];
                    array[currentIndex] = array[randomIndex];
                    array[randomIndex] = temporaryValue;
                }

                return array;
            }

            var enc_key_local = enc_key_by_function;
            // var result = '';

            if (enc_key_local) {

                var array_date = time_unix_string.split('');
                var string_srv_time = o['time_unix'].toString();
                var array_server_time = string_srv_time.split('');

                var f_string = '';
                var b_string = '';

                for (let i = 0; i < time_unix_string.length; i++) {
                    f_string = f_string + generator_local_get__(getRandomInt_local_get__(48) + 32, false) + '\
                    ' + array_date[i] + generator_local_get__(getRandomInt_local_get__(48) + 32, false);
                }

                for (let x = 0; x < string_srv_time.length; x++) {
                    b_string = b_string + generator_local_get__(getRandomInt_local_get__(48) + 32, false) + '\
                    ' + array_server_time[x] + generator_local_get__(getRandomInt_local_get__(48) + 32, false);
                }

                data = "\
                " + generator_local_get__(getRandomInt_local_get__(256) + 256, true) + "_\
                " + f_string + "_\
                " + generator_local_get__(getRandomInt_local_get__(256) + 256, true) + "_\
                " + b_string + "_\
                " + generator_local_get__(getRandomInt_local_get__(256) + 256, true);
            }
        },
        error: function() {
            $.notify("Server side error.", {
                position: "bottom right",
                autoHideDelay: 3000
            });
        },
        async: false,
        cache: false,
        timeout: 2000,
    });

    return data;
}

function AOS_update_timer(time) {
    function upd() {
        AOS.refresh();
    }
    setTimeout(upd, time);
}

function getParameterByName(name, url = window.location.href) {
    try {
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    } catch {
        $.notify("Address bar parsing error.", {
            position: "bottom right",
            autoHideDelay: 3000
        });
    }
}

function etdd() {
    let i = !1;
    var a;
    return (
        (a = navigator.userAgent || navigator.vendor || window.opera),
        (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(
                a
            ) ||
            /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
                a.substr(0, 4)
            )) &&
        (i = !0),
        i
    );
};

function mob() {
    if (!etdd()) {
        return 1
    } else {
        return 0
    }
};
var search_index = 0;
var updated_search_text = '';
var comment_spin_global = '';
var timerId_global = '';
var timer_clear_update = '';
var timer_clear_is_active = true;
var get_ad_active_now = true;
var is_search_now = false;
var enc_key = enc_key_glb__; // for check request
// var token_recaptcha = '';

var temp_html_index_page = '';

// var hide_index_page_blocks = $.cookie('hide_block_index');

var error_block_space_design = '<div class="col-12 col-lg-12 padding-block-center-box">'+
    '<div class="user box aos-init aos-animate" data-aos="fade-up"><div class="box_aware_error">'+
    '<div class="box_aware_error__ghost"><div class="symbol"></div> <div class="symbol"></div> <div class="symbol"></div><div class="symbol"></div>'+
    '<div class="symbol"></div><div class="symbol"></div><div class="box_aware_error__ghost-container"><div class="box_aware_error__ghost-eyes">'+
    '<div class="box_aware_error__eye-left"></div><div class="box_aware_error__eye-right"></div></div><div class="box_aware_error__ghost-bottom">'+
    '<div></div><div></div><div></div><div></div><div></div></div></div><div class="box_aware_error__ghost-shadow"></div></div>'+
    '<div class="box_aware_error__description"><div class="box_aware_error__description-container"><div class="box_aware_error__description-title">'+
    'Oh!</div><div class="box_aware_error__description-text">'+
    'We could not find anything for your request... Please try again, or reformulate the question.</div></div></div></div></div></div>';

var pageX = $(document).width();
var pageY = $(document).height();
var mouseY = 0;
var mouseX = 0;

$(document).mousemove(function(event) {
    mouseY = event.pageY;
    yAxis = ((pageY / 2 - mouseY) / pageY) * 300;

    mouseX = event.pageX / -pageX;
    xAxis = -mouseX * 100 - 100;

    $(".box_aware_error__ghost-eyes").css({
        transform: "translate(" + xAxis + "%,-" + yAxis + "%)"
    });
});

function hide_hint_text_video() {
    var hint = $(".hint_text_video_play_yt");

    hint.css('margin-top', '-1em');
    hint.css('visibility', 'hidden');

    AOS.refresh();
}

function covid_anal(string) {
    /*
    Function to check whether the request is related to the coronavirus
    */
    const words = [
        'covid', 'covid-19', 'коронавирус', 'коронавірус',
        'коронавируса', 'коронавіруса', 'коронавірусу', 'коронавирусом', 'коронавірусом',
    ];

    for (let i = 0; i < words.length; i++) {
        if (string.toLowerCase().indexOf(words[i]) !== -1) {
            return 1;
        }
    }
    return 0;
}

function user_agent_anal(string) {
    /*
    The function decides whether the user needs to show information about his browser
    */
    const words = [
        'user agent', 'user-agent', 'user_agent', 'user+agent'
    ];

    for (let i = 0; i < words.length; i++) {
        if (string.toLowerCase().indexOf(words[i]) !== -1) {
            return 1;
        }
    }
    return 0;
}

function namaz_anal(string) {
    /*
    Function to check whether the request is related to the Prayer
    */
    const words = [
        'намаз', 'намаза', 'намазом', 'намазов',
    ];

    for (let i = 0; i < words.length; i++) {
        if (string.toLowerCase().indexOf(words[i]) !== -1) {
            return 1;
        }
    }
    return 0;
}

function get_namaz(string) {
    /*
    Function for obtaining information about Prayer
    */
    if (namaz_anal(string)) {
        // We make sure once again that this feature needs to be activated
        const string_split = string.split();
        var result = null;

        for (let i = 0; i < string_split.length; i++) {
            let c_b = string.length;
            $.ajax({
                url: load_more__,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val(),
                    validtoken: token_valid__,
                    typeload: 'newsession',
                    additions: 0,
                    c_t___kk_: get__(true),
                    news: 0,
                    sign: user_address__,
                    c: c_b,
                    gr_token: null,
                    covid_stat: 0,
                    search: string_split[i],
                    namaz: 1,
                    mobile: mob()
                },
                success: function(o) {
                    result = o;
                },
                async: false,
                timeout: 5000,
            });
        }
        return result;
    }
}

function load_ajax_end_page(o, type_loading) {
    const text_no = $(".no-more-results-text");

    const e = $(".load-more-end-butt"),
        n = e.find("span");

    const load_continue_footer = $(".load-more-end-butt-search-array"),
        n_con = load_continue_footer.find("span");

    var t = jQuery("[name=csrfmiddlewaretoken]").val();
    var search_data_text = o;
    var get = get__(true);
    var geted_c = o.length;
    var his = new search_history_data();
    var namaz_data = '';

    function move_error_block() {
        if (is_search_now) {
            $(".row-posts-end").css('margin-top', '-3em');
        } else {
            $(".row-posts-end").css('margin-top', '-12em');
        }
    }

    if (namaz_anal(search_data_text)) {
        namaz_data = get_namaz(search_data_text);
    }

    $.ajax({
        url: load_more__,
        type: "POST",
        data: {
            csrfmiddlewaretoken: t,
            validtoken: token_valid__,
            typeload: type_loading,
            additions: 0,
            c_t___kk_: get,
            news: 0,
            sign: user_address__,
            c: geted_c,
            gr_token: null,
            covid_stat: covid_anal(o),
            search: o,
            mobile: mob()
        },
        beforeSend: function() {
            if ($.cookie('hide_block_index') == 'no') {
                $('.row-posts-end').css('margin-top', '-3em');
            }

            $(".banner_ad_aware").css('width', '50%');
            $('.aware_hide_blocks_on_index_page').css('visibility', 'hidden');
            $(".clear_aware_search_string").css("margin-right", "2.5em");
            $(".search-input-aware").css("padding", "0 75px 0 20px");

            text_no.css('visibility', 'hidden'), e.attr("disabled", !0), n.addClass("d-inline-block"), AOS.refresh();
            text_no.css('display', 'none');

            // get_ad('con');

            error_search_no_text('ok');

            comment = document.createComment($(".icon_search_load_aware_one").get(0).outerHTML);
            $(".icon_search_load_aware_one").replaceWith(comment);

            e.css("top", "-5px");
            e.css("right", "10px");

            $('.spinner_search_load_aware').replaceWith(comment_spin_global);
            $(comment_spin_global).replaceWith(comment_spin_global.nodeValue);

            $(".row-posts-end").css("display", "");
        },
        success: function(o) {
            his.remove(search_data_text); // If it was already, then remove, then put again
            let long_word_search = false;

            splited_search_string = search_data_text.split(' ')

            for (let i = 0; i < splited_search_string.length; i++) {
                if (splited_search_string[i].length > 32) {
                    long_word_search = true;
                    break;
                }
            }

            if (!long_word_search) {
                his.add(search_data_text);
            }

            $(".clear_aware_search_string").css("margin-right", "2em");
            $(".search-aware-block-global").css("margin-bottom", "1em");
            $(".search-input-aware").css("padding", "0 65px 0 20px");

            updated_search_text = search_data_text;
            $(comment).replaceWith(comment.nodeValue);

            search_title_set(search_data_text);
            edit_query_string_q(search_data_text);

            e.removeAttr("style");
            $('.spinner_search_load_aware').replaceWith(comment_spin_global);
            load_continue_footer.css('visibility', 'visible');
            load_continue_footer.css('display', 'block');

            if (o.replace(/[^+\w]/g, '').length < 10) {
                load_continue_footer.css('visibility', 'hidden');
            }

            n_con.css('visibility', 'hidden');
            n_con.css('display', 'none');
            n_con.removeClass("d-inline-block");

            document.querySelector(".search-input").classList.remove("active");
            $(".float_bg").css("display", "none");
            AOS.refresh();

            if (type_loading == 'newsession') {
                $(".row-posts-end").empty();
                search_index = 21;
            }

            e.attr("disabled", !1),
                n.removeClass("d-inline-block"),
                "Ошибка валидации!" == o ? $.notify("Error. Reload the page.", {
                    position: "bottom right",
                    autoHideDelay: 3000
                }) : $(".row-posts-end").append(o),
                AOS.refresh(),
                $(document).ready(function() {
                    $('[data-toggle="tooltip"]').tooltip();
                });

            if ((o).length < 10) {
                e.removeAttr("style");
                $('.spinner_search_load_aware').replaceWith(comment_spin_global);
                $(".row-posts-end").empty(), $(comment).replaceWith(comment.nodeValue), $(".row-posts-end").append(error_block_space_design);
                // move_error_block();
                e.attr("disabled", !1), n.removeClass("d-inline-block");
            }

            // else {
            //     $(".wrapper").css("margin", "15px auto");
            // }
            $(".wrapper").css("margin", "15px auto");

            function update_AOS_blocks() {
                AOS.refresh();
            }

            setTimeout(update_AOS_blocks, 1200);
            setTimeout(hide_hint_text_video, 10000);

            if (namaz_data) {
                $(".row-posts-end").prepend(namaz_data);
                AOS.refresh();
            }

            if (user_agent_anal(search_data_text)) {
                let user_agent_data_block = '<div class="col-12 col-lg-12 padding-block-center-box"><div class="user box aos-init aos-animate" '+
                'data-aos="fade-up"><div style="float: left;"><label id="'+
                makeid(32)+
                '" class="username" style="margin-top: -0.5em;">'+
                'What\'s my user agent?</label><br><br><label id="'+
                makeid(32)+
                '" class="city user_agent_disp" style="font-weight: 900;">'+
                window.navigator.userAgent+
                '</label><br/><div style="background: #fff;border-radius: 0.5em;font-weight: 600;font-size: 0.9em;margin-top: 1em;display: inline-block;">'+
                '<span style="margin: 0.5em;">Special&nbsp;<i class="fas fa-hashtag"></i></span></div></div></div></div>';

                $(".row-posts-end").prepend(user_agent_data_block);
                AOS.refresh();
            }

            init_video_search_in_results();
            is_search_now = true;

            get_ad('con');
        },
        error: function() {
            $(".clear_aware_search_string").css("margin-right", "2em");
            $(".search-aware-block-global").css("margin-bottom", "1em");

            $(".wrapper").css("margin", "15px auto");
            $(".search-input-aware").css("padding", "0 65px 0 20px");
            e.removeAttr("style");

            $('.spinner_search_load_aware').replaceWith(comment_spin_global);
            $(".row-posts-end").empty(), $(comment).replaceWith(comment.nodeValue), $(".row-posts-end").append(error_block_space_design);
            // move_error_block();
            e.attr("disabled", !1), n.removeClass("d-inline-block");

            get_ad('new');
        },
        statusCode: {
            400: function() {
                $.notify("Something went wrong...", {
                    position: "bottom right",
                    autoHideDelay: 3000
                });
            },
            403: function() {
                $.notify("Too many requests.", {
                    position: "bottom right",
                    autoHideDelay: 3000
                });
            },
            500: function() {
                $.notify("Server side error.", {
                    position: "bottom right",
                    autoHideDelay: 3000
                });
            }
        },
    });
}

function load_continue_ajax_end_page(o, type_loading) {
    const text_no = $(".no-more-results-text");
    const e = $(".load-more-end-butt-search-array"),
        n = e.find("span");
    var t = jQuery("[name=csrfmiddlewaretoken]").val();
    var geted_c = o.length;
    $.ajax({
        url: load_more__,
        type: "POST",
        data: {
            csrfmiddlewaretoken: t,
            validtoken: token_valid__,
            typeload: type_loading,
            additions: 0,
            news: 0,
            c: geted_c,
            sign: user_address__,
            c_t___kk_: get__(true),
            gr_token: null,
            covid_stat: 0,
            search: o,
            mobile: mob(),
            search_index_: search_index
        },
        beforeSend: function() {
            text_no.css('visibility', 'hidden'), e.attr("disabled", !0), n.addClass("d-inline-block");
            text_no.css('display', 'none');
            error_search_no_text('ok'), n.css('visibility', 'visible'), n.css('display', 'inline-flex'), AOS.refresh();
        },
        success: function(o) {
            n.css('visibility', 'hidden');
            n.css('display', 'none');
            search_index = search_index + 10;

            if (search_index > 100) {
                e.css('visibility', 'hidden');
                text_no.css('visibility', 'visible');
                text_no.css('display', '');
            }

            e.attr("disabled", !1),
                n.removeClass("d-inline-block"),
                "Ошибка валидации!" == o ? $.notify("Error. Reload the page.", {
                    position: "bottom right",
                    autoHideDelay: 3000
                }) : $(".row-posts-end").append(o),
                AOS.refresh(),
                $(document).ready(function() {
                    $('[data-toggle="tooltip"]').tooltip();
                });

            if ((o).length < 10) {
                e.css('visibility', 'hidden'), e.attr("disabled", !1), n.css('visibility', 'hidden'), n.css('display', 'none');
                n.removeClass("d-inline-block"), text_no.css('visibility', 'visible');
                e.css('display', 'none');

                text_no.css('margin-bottom', '3em');
                text_no.css('display', '');
            }

            init_video_search_in_results();
            setTimeout(hide_hint_text_video, 10000);
        },
        error: function() {
            e.css('visibility', 'hidden'), e.attr("disabled", !1), n.css('visibility', 'hidden'), n.css('display', 'none');
            n.removeClass("d-inline-block"), text_no.css('visibility', 'visible');
            e.css('display', 'none');

            text_no.css('margin-bottom', '3em');
            text_no.css('display', '');
        },
        statusCode: {
            400: function() {
                $.notify("Something went wrong...", {
                    position: "bottom right",
                    autoHideDelay: 3000
                });
            },
            403: function() {
                $.notify("Too many requests.", {
                    position: "bottom right",
                    autoHideDelay: 3000
                });
            },
            500: function() {
                $.notify("Server side error.", {
                    position: "bottom right",
                    autoHideDelay: 3000
                });
            }
        },
    });
}

function onMenuClicked() {
    $(".menu_box").is(":hidden") ?
        ($(".menu_box").show(), $(".float_bg").show(), $(".search-input").attr("disabled", !1), $(".search-input").css("z-index", 1)) :
        ($(".menu_box").hide(), $(".float_bg").hide(), $(".search-input").attr("disabled", !0), $(".search-input").css("z-index", 106));
}

function get_from_history_suggestions(search_text) {
    var his = new search_history_data();
    var x_data = his.items();
    var reversed_array = x_data.reverse();

    var result_array = [];
    var naked_data = [];

    for (let i = 0; i < reversed_array.length; i++) {
        var string = reversed_array[i].toLowerCase();

        if (string.indexOf(search_text.toLowerCase()) !== -1) {
            result_array.push('\
            <li class="search-el-a">\
            <span class="ico_s_el" style="margin-right: 0.25em;">\
            <i style="color: #9a9a9a;" class="far fa-clock"></i>\
            </span><span class="text_s_el">' + string + '</span></li>\
            ');
            naked_data.push(string);
        }

        if (result_array.length == 3) {
            break;
        }
    }

    return [result_array, naked_data];
}

function modify_suggestions_from_server(history_sug, server_sug) {
    var el_server = $('<div></div>').html(server_sug);
    var el_server_j = $('li', el_server);

    for (let i = 0; i < history_sug.length; i++) {
        for (let y = 0; y < el_server_j.length; y++) {

            // console.log("--- \""+history_sug[i].toLowerCase()+"\" and \""+$(el_server_j.get(y)).children('.text_s_el').text().toLowerCase()+"\" ID I: "+i+" ID Y: "+y);

            if (history_sug[i].toLowerCase() == $(el_server_j.get(y)).children('.text_s_el').text().toLowerCase()) {
                el_server_j.get(y).remove();
            }
        }
    }

    return el_server.html();
}

function get_suggestions() {
    var text = $('.search-input-aware').val();
    $.ajax({
        url: search_suggestions_get__,
        type: "GET",
        data: {
            "q": text
        },
        success: function(o) {
            var his_data = get_from_history_suggestions(text);
            $(".autocom-box").empty()
            $(".autocom-box").append(his_data[0]);
            $(".autocom-box").append(modify_suggestions_from_server(his_data[1], o['data']));
        },
        async: true,
        timeout: 3000,
    });
}
$(".search-input-aware").on('keyup', function(e) {
    if (e.key === 'Enter' || e.keyCode === 13) {
        var search_text = $('.search-input-aware').val();
        if (search_text.length == 0) {
            error_search_no_text('error');
        } else {
            $('.row-posts-end').empty();
            load_ajax_end_page(search_text, 'newsession');
        }
    }
});

function run_remove_active() {
    document.querySelector(".search-input").classList.remove("active");
    $(".float_bg").css("display", "none");
    AOS.refresh();
    get_suggestions($('.search-input-aware').val());
}
$('.search-input-aware').on('input', function() {
    var search_text = $('.search-input-aware').val();
    edit_query_string_q(search_text);
    if (search_text.length == 0) {
        $('.clear_aware_search_string').css('visibility', 'hidden');
        $(".search-input-aware").css("padding", "0 60px 0 20px");
        setTimeout(run_remove_active, 200);

    } else {
        $('.clear_aware_search_string').css('visibility', 'visible');
        $(".search-input-aware").css("padding", "0 70px 0 20px");

        document.querySelector(".search-input").classList.add("active");
        $(".search-input").css("z-index", 106);
        $(".float_bg").removeAttr("style");

        AOS.refresh();
        let throttle_get_suggestions = throttle(get_suggestions, 150);

        throttle_get_suggestions(search_text);
    }
});
$('.search-input-aware').on('focus', function() {
    var search_text = $('.search-input-aware').val();
    if (search_text.length > 0) {
        document.querySelector(".search-input").classList.add("active");
        $(".search-input").css("z-index", 106);
        $(".float_bg").removeAttr("style");
        AOS.refresh();
    }
});
$('.search-input-aware').on('focusout', function() {
    function run_remove_active() {
        document.querySelector(".search-input").classList.remove("active");
        $(".float_bg").css("display", "none");
        AOS.refresh();
    }
    setTimeout(run_remove_active, 200);
});
$(".load-more-end-butt").on("click", function() {
    var search_text = $('.search-input-aware').val();
    if (search_text.length == 0) {
        error_search_no_text('error');
    } else {
        $('.row-posts-end').empty();
        load_ajax_end_page(search_text, 'newsession');
    }
});
$(".clear_aware_search_string").on("click", function() {
    var search_text_in_clear_func = $('.search-input-aware').val();

    function local_update_search_string() {
        $('.search-input-aware').attr("placeholder", search_template__);
    }
    // console.log('Text: ' + search_text_in_clear_func);

    if (search_text_in_clear_func.length > 0) {
        run_remove_active();
        $('.search-input-aware').val("");
        $('.clear_aware_search_string').css('visibility', 'hidden');
        let i = 0;

        function update_text_search_place() {
            var x_text = 'Ok...';
            i = i + 1;
            // console.log(i);
            $('.search-input-aware').attr("placeholder", x_text.slice(0, i));
        }
        let timerId = setInterval(() => update_text_search_place(), 150);
        timerId_global = timerId;
        setTimeout(() => {
            clearInterval(timerId);
            i = 0;
        }, 1400);
        if (timer_clear_is_active) {
            timer_clear_update = setTimeout(local_update_search_string, 1500);
        }
    }
});
$(".autocom-box").on("click", ".search-el-a", function(e) {
    var search_text = $(this).children(".text_s_el").text();
    $(".search-input-aware").val(search_text);
    load_ajax_end_page(search_text, 'newsession');
});

function error_search_no_text(mode) {
    if (mode == 'error') {
        clearInterval(timerId_global);
        clearInterval(timer_clear_update);
        $('.search-input-aware').attr("placeholder", "This field cannot be empty!");

    } else {
        $('.search-input-aware').attr("placeholder", search_template__);
    }
}
$(".load-more-end-butt-search-array").on("click", function() {
    // var search_text = $('.search-input-aware').val();
    var search_text = updated_search_text;
    if (search_text.length == 0) {
        error_search_no_text('error');
    } else {
        load_continue_ajax_end_page(search_text, search_index);
    }
});

function ready_news_search_button() {
    $(".news_search_button_aware_index_block").on("click", function() {
        var search_text = $(".aware_news_index_page_title").text();
        if (search_text.length > 0) {
            $('.row-posts-end').empty();
            $('.clear_aware_search_string').css('visibility', 'visible');
            $(".search-input-aware").val(search_text);
            load_ajax_end_page(search_text, 'newsession');
        } else {
            console.log('News search error!');
        }
    });
}

function append_ad_block(data) {
    var append_advertise_html_code_index_page_ad = '<div class="col-12 col-lg-12 padding-block-center-box ad_index_el"><div class="user box aos-init aos-animate" \
    data-aos="fade-up"><div style="float: left;"><label class="city" style="font-size: calc(14px + (18 - 14) * ( (100vw - 480px) / ( 1024 - 480) ));"\
    >' + String(data['text']).replace('\n', '<br>') + '</label></div></div></div>';

    $(".row-posts-end-ad").empty();
    $(".advertise-aware-block").append(append_advertise_html_code_index_page_ad);
    AOS.refresh();
}

function prepend_ad_block_to_search_results(data, ready = true) {
    var append_advertise_html_code_search_ad = '<div class="col-12 col-lg-12 padding-block-center-box ad_index_el"><div class="user box aos-init aos-animate" \
    data-aos="fade-up"><div style="float: left;"><label class="city" style="font-size: calc(14px + (18 - 14) * ( (100vw - 480px) / ( 1024 - 480) ));\
    ">' + String(data['text']).replace('\n', '<br>') + '</label><br/><div style="background: #fff;border-radius: 0.5em;font-weight: 600;font-size: 0.9em;\
    margin-top: 1em;display: inline-block;"><span style="margin: 0.5em;">Advertising&nbsp;<i class="fas fa-ad"></i></span></div></div></div></div>';

    // $(".advertise-aware-block").empty();
    // $(".row-posts-end-ad").empty();
    if ($.cookie('hide_block_index') == 'no') {
        $(".row-posts-end").prepend(append_advertise_html_code_search_ad);
    } else if ($.cookie('hide_block_index') == 'yes' && ready == false) {
        $(".row-posts-end").prepend(append_advertise_html_code_search_ad);
    }
    AOS.refresh();
}

function get_ad(mode) {
    if (get_ad_active_now) {
        $.ajax({
            url: get_ad__,
            type: "POST",
            data: {
                csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val(),
                c_t___kk_: get__(true),
                lang: "ru",
            },
            success: function(o) {
                $(".autocom-box").empty();
                if(o['text']){
                    if (mode == 'new') {
                        prepend_ad_block_to_search_results(o);
                    } else {
                        prepend_ad_block_to_search_results(o, false);
                    }
                }
            },
            async: true,
            timeout: 5000,
        });
    }
}

function get_footer_html() {
    $.ajax({
        url: footer_load__,
        type: "GET",
        data: {},
        success: function(o) {
            $(".footer-aware").append(o);

            let build_info = $(".build_info_footer").text();
            let user_agent = window.navigator.userAgent;

            if (user_agent.indexOf("AWARE Android ") != -1) {
                build_info = build_info.replace('awse-', 'awse_android-');
            } else if (!mob()) {
                build_info = build_info.replace('awse-', 'awse_mobile-');
            } else {
                build_info = build_info.replace('awse-', 'awse_web-');
            }

            $(".build_info_footer").text(build_info);
        },
        async: true,
        timeout: 5000,
    });
}

function check_banner_index(ready = false) {
    $.ajax({
        url: get_banner__,
        type: "POST",
        data: {
            csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val(),
            c_t___kk_: get__(true),
        },
        success: function(o) {
            init_banner(o['link'], o['ad_site'], o['title'], o['id'], results_ready = ready);
        },
        async: true,
        timeout: 3000,
    });
}

function hide_blocks_on_index_page_func(action_type, action_by_user = false) {
    if (action_type == 'yes') {
        $.cookie('hide_block_index', 'yes', {
            expires: 365
        });

        $(".ad_index_el").remove();
        $(".aware_hide_blocks_on_index_page_text").text('Show');
        $(".aware_hide_blocks_on_index_page").css('margin-bottom', '-5%');

        $(".row-posts-end").css("display", "none");
        // $(".row-posts-end").css("visibility", "hidden");
        temp_html_index_page = $(".row-posts-end").html();

        $(".row-posts-end").empty();
        $(".wrapper").css("margin-top", "");
        AOS.refresh();
        AOS_update_timer(500);

    } else if (action_type == 'no') {
        $.cookie('hide_block_index', 'no', {
            expires: 365
        });

        if (action_by_user) {
            $(".ad_index_el").remove();
            get_ad('new');
        }

        $(".aware_hide_blocks_on_index_page_text").text('Hide');
        $(".aware_hide_blocks_on_index_page").css('margin-bottom', '5%');

        $(".row-posts-end").css("display", "block");
        $(".row-posts-end").append(temp_html_index_page);

        ready_news_search_button();
        $(".wrapper").css("margin-top", "10px");

        AOS.refresh();
        AOS_update_timer(500);
    }
}
$(".aware_hide_blocks_on_index_page").on("click", function() {
    if ($.cookie('hide_block_index') == 'no') {
        hide_blocks_on_index_page_func('yes', true);
    } else {
        hide_blocks_on_index_page_func('no', true);
    }
});

function scrollToTop() {
    window.scrollTo(0, 0);
}

function init_banner(link, ad_link, title, id_ad, results_ready = false) {
    if (link) {
        var banner_el = $(".banner_ad_aware");
        var banner_div = $(".advertise-aware-block");
        var aware_search_input = $(".wrapper");
        var link_el = banner_el.parent('a');

        if (!title) {
            title = 'Advertising banner';
        }

        link = imageproxy__ + "?data=" + link + "&video_mode=1&token=" + token_valid__ + '&sign=' + user_address__;

        link_el.attr('id', id_ad);
        link_el.attr('href', ad_link);
        link_el.attr('target', '_blank');

        banner_el.attr('src', link);
        banner_el.attr('alt', title);
        banner_el.attr('title', title);
        banner_el.attr('done', 'yes');

        banner_el.css('display', 'inline-block');
        banner_el.css('width', '80%');

        banner_div.css("margin-top", "-3em");

        aware_search_input.css("margin-top", "10px");

        function init() {
            AOS.refresh();
            scrollToTop();
        }
        setTimeout(init, 1000);
    }
}

function set_video_volume_by_cookie(el_this) {
    var volume = $.cookie("video_volume");
    el_this.prop("volume", volume);
}

function detect_volume_change_by_user(id_el_this) {
    var vid = document.getElementById(id_el_this);
    vid.onvolumechange = function() {
        $.cookie('video_volume', vid.volume, {
            expires: 365
        });
    };
}

function init_video_search_in_results() {
    $(".view-container-youtube-video-aware").on("click", function() {
        var clickedEl = $(this);
        var video_id = clickedEl.children('.video_youtube_preview_image_aware').attr('data-youtube-id');
        var video_link = null;
        var parent = clickedEl.parent(".city").parent();
        var video_hint = parent.children(".youtube_video_info_div");
        var video_load_spin = video_hint.children("span").children(".youtube_video_load_wait_aware");

        if (video_id) {
            $.ajax({
                url: get_video_yt__,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val(),
                    c_t___kk_: get__(true),
                    video_id: video_id
                },
                beforeSend: function() {
                    video_load_spin.css("display", "inline-block");
                },
                success: function(o) {
                    video_link = o['link'];

                    if (video_link) {
                        clickedEl.empty();

                        clickedEl.append('<video id="yt_player" style="margin-top: 0%;margin-bottom: -2%;opacity: 1;width: 100%;transition: opacity\
                        0.5s linear, margin-bottom 1s, margin-top 1s;margin-right: 10px;max-height: 70vh;height: auto;-webkit-appearance: none;border-radius: \
                        2vh;padding: 0px;text-align:left;padding-bottom: 0px;box-shadow: 0 4px 15px 0 rgb(0 0 0 / 40%);" controls="controls" \
                        class="youtube_video_aware_search" data-youtube-id="' + video_id + '" src="' + video_link + '" onerror="VideoError(this);"></video>');

                        var video_loaded_yt_aware = clickedEl.children('.youtube_video_aware_search');

                        video_loaded_yt_aware.css('margin-top', '1%');
                        video_loaded_yt_aware.css('margin-bottom', '2%');

                        video_loaded_yt_aware.attr("id", makeid());

                        video_load_spin.css("display", "none");

                        AOS.refresh();

                        set_video_volume_by_cookie(video_loaded_yt_aware);
                        detect_volume_change_by_user(video_loaded_yt_aware.attr("id"));
                    } else {
                        video_load_spin.css("display", "none");
                        $.notify("Error. Failed to load video.", {
                            position: "bottom right",
                            autoHideDelay: 3000
                        });
                    }
                },
                error: function() {
                    // Error connection or not valid response
                    video_load_spin.css("display", "none");
                    $.notify("Error. Failed to load video.", {
                        position: "bottom right",
                        autoHideDelay: 3000
                    });
                },
                async: true,
                timeout: 12000,
            });
        }
        // console.log(video_link);
    });
}
var search_history_data = function() {
    var cookieName = 'search_history';
    var cookie = $.cookie(cookieName);
    var items = cookie ? cookie.split(/⊉/) : new Array();
    return {
        "add": function(val) {
            items.push(val);
            $.cookie(cookieName, items.join('⊉'), {
                expires: 365
            });
        },
        "remove": function(val) {
            indx = items.indexOf(val);
            if (indx != -1) items.splice(indx, 1);
            $.cookie(cookieName, items.join('⊉'), {
                expires: 365
            });
        },
        "clear": function() {
            items = null;
            $.cookie(cookieName, null, {
                expires: 365
            });
        },
        "items": function() {
            return items;
        }
    }
}
$(window).scroll(function() {
        $(window).scrollTop() == $(document).height() - $(window).height() &&
            setTimeout(function() {
                $(window).scrollTop() == $(document).height() - $(window).height();
            }, 150);
    }),
    AOS.init(),
    $(document).ready(function() {
        var hide_blocks_index = $.cookie('hide_block_index');
        get_footer_html();
        ready_news_search_button();
        if (!hide_blocks_index) {
            $.cookie('hide_block_index', 'no', {
                expires: 365
            });
            hide_blocks_on_index_page_func('no');
        } else {
            hide_blocks_on_index_page_func(hide_blocks_index);
        }
        $('[data-toggle="tooltip"]').tooltip();
        var question = getParameterByName('q');
        $(".row-posts-end").css('visibility', 'visible');
        if (!question && $.cookie('hide_block_index') == 'no') {
            get_ad('new');
            // console.log('Ad load...');
        }
        if (!question) {
            check_banner_index();
        } else {
            // add to search results page
            check_banner_index(true);
        }
        my_element_jq = $('.spinner_search_load_aware');
        elemnt_icon_aware = $(".icon_search_load_aware_one");
        my_element_jq.removeAttr("style");
        elemnt_icon_aware.removeAttr("style");
        comment_spin_global = document.createComment(my_element_jq.get(0).outerHTML);
        my_element_jq.replaceWith(comment_spin_global);
        if (question) {
            $('.row-posts-end').empty();
            $(".wrapper").css("margin", "15px auto");
            $(".search-aware-block-global").css("margin-bottom", "1em");
            $('input.search-input-aware').val(question);
            $('.clear_aware_search_string').css('visibility', 'visible');
            load_ajax_end_page(question, 'newsession');
        }
        $("#notify-bootstrap").empty();

        function local_AOS_upd() {
            AOS.refresh();
        }
        setInterval(local_AOS_upd, 1000); // update AOS per one second
    }),
    $("a.scroll-to").on("click", function() {
        scrollToTop();
        AOS.refresh();
    }),
    $(window).scroll(function() {
        (home_button = document.getElementById("h_butt")), 1e3 < $(window).scrollTop() ? (home_button.style.visibility = "visible") :
            (home_button.style.visibility = "hidden");
    }),
    $(document).on("click", function(o) {
        $(o.target).hasClass("float_bg") && ($(".menu_box").hide(), $(".float_bg").hide());
    });

/*

JQuery Cookies

*/
(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        factory(require('jquery'));
    } else {
        factory(jQuery);
    }
}(function($) {

    var pluses = /\+/g;

    function encode(s) {
        return config.raw ? s : encodeURIComponent(s);
    }

    function decode(s) {
        return config.raw ? s : decodeURIComponent(s);
    }

    function stringifyCookieValue(value) {
        return encode(config.json ? JSON.stringify(value) : String(value));
    }

    function parseCookieValue(s) {
        if (s.indexOf('"') === 0) {
            s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
        }
        try {
            s = decodeURIComponent(s.replace(pluses, ' '));
            return config.json ? JSON.parse(s) : s;
        } catch (e) {}
    }

    function read(s, converter) {
        var value = config.raw ? s : parseCookieValue(s);
        return $.isFunction(converter) ? converter(value) : value;
    }

    var config = $.cookie = function(key, value, options) {
        if (value !== undefined && !$.isFunction(value)) {
            options = $.extend({}, config.defaults, options);

            if (typeof options.expires === 'number') {
                var days = options.expires,
                    t = options.expires = new Date();
                t.setTime(+t + days * 864e+5);
            }
            return (document.cookie = [
                encode(key), '=', stringifyCookieValue(value),
                options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                options.path ? '; path=' + options.path : '',
                options.domain ? '; domain=' + options.domain : '',
                options.secure ? '; secure' : ''
            ].join(''));
        }

        var result = key ? undefined : {};
        var cookies = document.cookie ? document.cookie.split('; ') : [];

        for (var i = 0, l = cookies.length; i < l; i++) {
            var parts = cookies[i].split('=');
            var name = decode(parts.shift());
            var cookie = parts.join('=');

            if (key && key === name) {
                result = read(cookie, value);
                break;
            }
            if (!key && (cookie = read(cookie)) !== undefined) {
                result[name] = cookie;
            }
        }
        return result;
    };

    config.defaults = {};

    $.removeCookie = function(key, options) {
        if ($.cookie(key) === undefined) {
            return false;
        }
        $.cookie(key, '', $.extend({}, options, {
            expires: -1
        }));
        return !$.cookie(key);
    };
}));