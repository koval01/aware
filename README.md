# awse.us

<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-%23FFD242?logo=python&logoColor=white">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</p>

****

<p align="center">
    <b>Stay in your private space</b>
</p>

****

**This is a closed repository in which the project / site is being developed - awse.us**

###### **Get started**

**Link** - **https://www.jetbrains.com/pycharm/download/#section=mac** or **https://code.visualstudio.com/docs/?dv=osx**

**Next you need to go to PyCharm, on the main page you will be prompted to create or download the project. You will need to select the download via git, you will need to log in via your GitHub account, then select this repository (_awse_site_), and wait until all the files are downloaded.**

**After that PyCharm will offer to download all dependencies, for successful execution VS Build Tools 2014 or higher is required, 2019 is recommended.**

**Build tools download link - https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019**

**You will need to select the C++ set from the installer menu. (Example in the photo - https://docs.microsoft.com/answers/storage/attachments/34873-10262.png)**

**Everything seems ready, but not yet.**

**If you are working on Frontend, here is the JS project code - https://github.com/koval01/awse_site/blob/master/core_orig/core.js**

## **The following is an example of code design:**

**For convenience, you can use Google Chrome Dev - https://www.google.com/intl/en/chrome/dev/**

**Also Microsoft Visual Studio Code - https://code.visualstudio.com/**

****

**Example of JS code:**

```javascript
function get_from_history_suggestions(search_text) {
    var his = new search_history_data();
    var x_data = his.items();
    var reversed_array = x_data.reverse();

    var result_array = [];
    var naked_data = [];

    for (let i = 0; i < reversed_array.length; i++) {
        var string = reversed_array[i].toLowerCase();

        if (string.indexOf(search_text.toLowerCase()) !== -1) {
            result_array.push(`
                <li class="search-el-a">
                <span class="ico_s_el" style="margin-right: 0.25em;">
                <i style="color: #9a9a9a;" class="far fa-clock"></i>
                </span><span class="text_s_el">${string}</span></li>
            `);
            naked_data.push(string);
        }

        if (result_array.length == 3) {
            break;
        }
    }

    return [result_array, naked_data];
}
```

**Templates posted at this address - https://github.com/koval01/awse_site/tree/master/awse/templates/awse**

**The CSS code of this site is located here - https://github.com/koval01/awse_site/blob/master/awse/static/awse/css/main_page.css**

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

**Also here is the code of the sync_time_server function.**

**You can view the code below:**

```python
@require_GET
@ratelimit(key=my_ip_key, rate='10/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def sync_time_server(request):
    return JsonResponse({"time_unix": round(time())})
```

****

Licensing Adjustment. If you want to use the design or all the code of this project, you must specify that your project is based on awse. And provide a link to this repository.
