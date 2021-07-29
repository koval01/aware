# awse.us

<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-%23FFD242?logo=python&logoColor=white">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</p>

**This is a closed repository in which the project / site is being developed - awse.us**

###### **Get started**

**Link** - **https://www.jetbrains.com/pycharm/**

**Next you need to go to PyCharm, on the main page you will be prompted to create or download the project. You will need to select the download via git, you will need to log in via your GitHub account, then select this repository (_aware_site_), and wait until all the files are downloaded.**

**After that PyCharm will offer to download all dependencies, for successful execution VS Build Tools 2014 or higher is required, 2019 is recommended.**

**Build tools download link - https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019**

**You will need to select the C++ set from the installer menu. (Example in the photo - https://docs.microsoft.com/answers/storage/attachments/34873-10262.png)**

**Everything seems ready, but not yet.**

**If you are working on Frontend, here is the JS project code - https://github.com/koval01/aware_site/blob/master/core_orig/core.js**

## **The following is an example of code design:**

**For convenience, you can use Google Chrome Dev - https://www.google.com/intl/en/chrome/dev/**

**Also Microsoft Visual Studio Code - https://code.visualstudio.com/**

****

**Example of JS code:**

```javascript
function example(string) {
    /*
    This function is an example for README.md
    */
    
    const developers = [
        "John", "Alex", "Sandy"
    ];
    
    for (let i = 0; i < developers.length; i++) {
    
        if (string.toLowerCase().indexOf(words[i]) !== -1) {
            // Yeah, this developer in list
            return true;
        }
        
        // Or send false bool var
    }
}
```

**Templates posted at this address - https://github.com/koval01/aware_site/tree/master/awse/templates/awse**

**The CSS code of this site is located here - https://github.com/koval01/aware_site/blob/master/awse/static/awse/css/main_page.css**

## **Server code and structure queue::**

****

**An example of code that processes requests to the image generator:**

```python
@require_GET
@cache_page(60 * 180)
def image_generate_api(request):
    """
    Image to text api
    :param request: body request
    :return: raw image
    """
    salt = Fernet(sign_key)
    received_address = salt.decrypt(str.encode(str(request.GET['sign']))).decode('utf-8')
    
    try:
        original_address = request.headers['X-Forwarded-For'].replace(' ', '').split(',')[-1:][0]
    except Exception as e:
        original_address = '127.0.0.1'
        logger.error(e)

    if original_address == received_address:
        
        token = request.GET['token']
        salt = Fernet(image_proxy_key)
        
        token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8')) + 15
        control_time = round(time())
        
        if token_get > control_time:
            try:
                text = request.GET['text']
                author = request.GET['author']
                if 5 < len(text) <= 1000 and 2 < len(author) <= 64:
                    logger.warning('IMAGE GENERATOR: Check sentences')
                    
                    if not sentence_check(text):
                        return JsonResponse(
                            {
                                'code': 409, 'code_name': 'Conflict',
                                'error': 'This text does not seem to have any value.',
                            }
                        )
                    
                    logger.info('IMAGE GENERATOR: Generating image')
                    
                    img = text_to_image_api(text, author)
                    
                    return HttpResponse(
                        img['img'],
                        content_type=img['headers'],
                        status=img['status_code'],
                        reason=img['reason'],
                    )
                return JsonResponse(
                    {
                        'code': 411, 'code_name': 'Length Required',
                        'error': 'Text length cannot be less than 5 characters or more than 1000. The author\'s name / nickname \
                        cannot be shorter than 2 characters and longer than 64 characters.',
                    }
                )
            except Exception as e:
                logger.error(e)

    return error_400(request)
```

****

**Also here is the code of the load_more function at the time of writing this help. This feature handles requests to download search results, weather, news, calculator, translator, and more.**

**You can view the code below:**

```python
@require_POST
@cache_page(60 * 180)
@ratelimit(key=my_ip_key, rate='1/3s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def load_more(request):
    """
    Technical (load_more) page view
    :param request: request body
    :return: render template page
    """
    c_token = request.POST.get('c_t___kk_', '')
    sign_data = request.POST.get('sign', '')
    
    try:
        token = request.POST.get('validtoken', '')
        typeload = request.POST.get('typeload', '')
    except Exception as e:
        token = typeload = 0
        logging.error(e)

    salt = Fernet(sign_key)
    received_address = salt.decrypt(str.encode(sign_data)).decode('utf-8')

    try:
        original_address = request.headers['X-Forwarded-For'].replace(' ', '').split(',')[-1:][0]
    except Exception as e:
        original_address = '127.0.0.1'
        logger.error(e)

    if check_request__(c_token) and original_address == received_address:

        additions = int(request.POST.get('additions', ''))
        news_append = int(request.POST.get('news', ''))
        covid_stat_append = int(request.POST.get('covid_stat', ''))
        search = request.POST.get('search', '')
        len_c = request.POST.get('c', '')
        search_index = request.POST.get('search_index_', '')
        namaz = request.POST.get('namaz', '')
        mobile = request.POST.get('mobile', '')
        videos = request.POST.get('videos', '')

        if len(search) <= max_search_len:
            if not videos:
                # If the variable does not exist, then set its value - 0
                videos = 0

            try:
                user_address = request.headers['X-Forwarded-For'].replace(' ', '').split(',')[-1:][0]
            except Exception as e:
                user_address = '127.0.0.1'
                logger.error(e)

            user_agent = request.headers['User-Agent']
            user_request_method = request.method

            try:
                user_referer = request.headers['HTTP_REFERER']
            except Exception as e:
                logger.warning(e)
                user_referer = None

            if not search_index:
                search_index = 0
            else:
                search_index = int(search_index)

            if namaz:
                namaz = get_namaz_data(search)

            if videos:
                videos = tiktok_data_get()

            if token and typeload and len(search) == int(len_c):
                if typeload == 'newsession' and covid_stat_append:
                    covid_stat_ua = covid_stat('UA')
                    covid_stat_ru = covid_stat('RU')
                else:
                    covid_stat_ua = 0
                    covid_stat_ru = 0

                # token decrypt
                try:
                    salt = Fernet(load_more_encrypt_key)
                    token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8'))
                except Exception as e:
                    token_get = 0
                    logging.error(e)

                if token_get and (token_get + 72000) > round(time()):
                    # data collect
                    news = newsfeed(news_append)

                    # image proxy encrypt data
                    salt = Fernet(image_proxy_key)
                    data = str.encode(str(round(time())))
                    token_valid = salt.encrypt(data).decode("utf-8")

                    # calculator
                    c_result, c_input = calculator(search)

                    # news link append
                    news_link_add = news_search_in_str(search)

                    # Send data to InfoBot
                    if search:
                        if namaz:
                            search_type_data = 'namaz'
                        else:
                            search_type_data = 'search request'

                        Process(
                            target=infobot_send_data,
                            args=(
                                user_agent,
                                user_address,
                                search,
                                search_type_data,
                                user_request_method,
                                user_referer,
                                search_index,
                            )
                        ).start()

                    # Search API
                    search_send = search
                    if namaz:
                        search_send = ''

                    search_api = search_execute(search_send, search_index)
                    search_data = search_api['data']
                    search_array = search_api['array']

                    # Weather
                    weather = weather_get(search)

                    # DeepL API
                    translate_result = translate_simple(search)

                    # data pack
                    data = zip(news, search_array)

                    logger.info(f'function load_more: request {request}')

                    return render(request, 'awse/load_more.html', {
                        'data': data, 'token_image_proxy': token_valid, 'search_index': search_index,
                        'typeload': typeload, 'covid_ru': covid_stat_ru, 'covid_ua': covid_stat_ua,
                        'additions': additions, 'news_append': news_append, 'covid_stat_append': covid_stat_append,
                        'c_result': c_result, 'search': search, 'c_input': c_input,
                        'news_search_in_str': news_link_add, 'search_data': search_data,
                        'namaz_data': namaz, 'videos': videos, 'user_address_original': user_address,
                        'translate_result': translate_result, 'mobile': mobile, 'weather': weather,
                        'search_api_full_dict': search_api,
                        'check_bot_request_search': check_bot_request_search(search),
                        'check_info_request_search': check_info_request_search(search),
                    })

    return error_400(request)
```

****
