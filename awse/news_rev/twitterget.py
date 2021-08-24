import logging, re, requests_cache
from datetime import datetime
from django.conf import settings
from ..news_utils.newsfilter import parse_text
from random import shuffle

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend="memory", namespace='twitter_api_cache', expire_after=1800)
bearer = settings.TWITTER_BEARER.replace(' ', '').split(',')
available_country = settings.AVAILABLE_COUNTRY


def replace_url_to_tag(string: str) -> str:
    """
    Replace text url to functional link
    :param string: Post text
    :return: formatted text (html)
    """
    regex = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
    url = re.findall(regex, string)

    for el in url:
        string = string.replace(el[0], '<a href="%s" target="_blank" style="color:#9c9c9c">%s&nbsp;</a>' % (
        el[0], el[0].replace('https://', '')))

    return string


def __main__(country="ua") -> list:
    """
    Function for search tweets by news
    :param country: country news need
    :return: list tweets
    """
    error_http = False
    error_json = False

    if country in available_country:
        users = dict(
            ua=[
                ['414630556', 15],  # @bbc_ua
                ['60030749', 15],  # @tsnua
                ['1454734730', 15],  # @hromadskeua
                ['47581890', 15],  # @5channel
                ['15827782', 15],  # @unian
                ['2613887972', 15],  # @apukraine
                ['331491073', 15],  # @kabmin_ua
                ['478598515', 15],  # @verkhovna_rada
                ['2777916078', 15],  # @gp_ukraine
                ['236466533', 15],  # @ukrpravda_news
                ['74224897', 15],  # @dw_ukrainian
                ['167317309', 15],  # @ukrinform
                ['2644527462', 15],  # @rnbo_gov_ua
                ['2827700719', 15],  # @servicessu
                ['2370200534', 15],  # @mineconomdev
                ['2340013831', 15],  # @minjust_gov_ua
                ['3293757682', 15],  # @nab_ukr
                ['55774975', 15],  # @zer0corruption_
                ['3547739837', 15],  # @cxemu
                ['4707444867', 15],  # @npu_gov_ua
                ['905645454', 15],  # @ng_ukraine
                ['630995607', 15],  # @defenceu
                ['4012126155', 15],  # @generalstaffua
                ['3002967393', 100],  # @history_ukraine
                ['1035241565596344321', 100],  # @istoriya_ua
                ['1178661064080269314', 15],  # @navalpages
                ['452900925', 15],  # @qirim_news
                ['17718831', 15],  # @radiosvoboda
                ['2423747006', 10],  # @poroshenko
                ['339521621', 20],  # @epravda
            ],
        )
        shuffle(users[country])
        data_array = []

        for bearer_token in bearer:
            for id_user in users[country]:
                url = f'https://api.twitter.com/2/users/{id_user[0]}/tweets'
                params = {
                    "max_results": id_user[1],
                    "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
                    "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
                    "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                    "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
                    "poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
                    "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics",
                }
                headers = {
                    "authorization": "Bearer " + bearer_token,
                }
                try:
                    http_response = session.get(url, params=params, headers=headers)
                    logger.info('Status code - %s' % http_response.status_code)
                except Exception as e:
                    logger.error(e)
                    error_http = True

                if not error_http:
                    try:
                        json_response = http_response.json()
                    except Exception as e:
                        logger.debug(e)
                        error_json = True

                    if not error_json:
                        try:
                            tweets = json_response['data']
                            includes = json_response['includes']

                            for i in tweets:
                                image = None
                                try:
                                    mediakey = i['attachments']['media_keys'][0]
                                    for media_search in includes['media']:
                                        if media_search['media_key'] == mediakey and media_search['type'] in ['photo',
                                                                                                              'animated_gif']:
                                            image = media_search['url']

                                except Exception as e:
                                    logger.debug(e)

                                time_ = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z').replace(
                                    tzinfo=None)

                                description = replace_url_to_tag(i['text']).replace('\'', '\\\'')
                                title = description.split('\n', 1)[0]

                                if len(includes['users'][0]['name']) > 20:
                                    includes['users'][0]['name'] = (includes['users'][0]['name'])[:17] + "..."

                                tweet = dict(
                                    time=round(time_.timestamp()) * 1000,
                                    description=description.replace('\n', '<br/>'),
                                    title=(re.sub(r'http\S+', '', title)[:35] + '... - Twitter'),
                                    image=image,
                                    url="https://twitter.com/%s/status/%s" % (i['author_id'], i['id']),
                                    name=includes['users'][0]['name'].replace('\'', '\\\''),
                                    profile_username=includes['users'][0]['username'],
                                    profile_link='https://twitter.com/%s' % includes['users'][0]['username'],
                                    source_mark=i['author_id'],
                                    desc_org=parse_text(i['text']).replace('\'', '\\\'')
                                )

                                if (datetime.now() - time_).days <= 3:
                                    data_array.append(tweet)

                        except Exception as e:
                            logger.error(e)

            if len(data_array) != 0:
                return data_array

    return []