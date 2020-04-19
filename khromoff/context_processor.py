# file with static shit we need in processing


def static_context(request):
    # some basic stuff

    context = {'static': {
        # TODO: rename to https
        'HOSTNAME': 'https://' + request.META['HTTP_HOST'],
        'contact_urls': {'MY_VK': 'https://vk.com/id516131573',
                         'MY_TELEGRAM': 'https://t.me/Mikhail_Khromov',
                         'MY_GITHUB': 'https://github.com/mikhailkhromov'
                         }
    }}
    return context


def urls(request):
    # urls to different parts of the sitex

    context = {
        'urls': {
            'about_url': '/about',
            'login_url': '/l/ogin/',
            'logout_url': '/l/ougout',
            'personal_url': '/l/personal',
            'urlshortner_url': '/shorturl',

        }
    }
    return context
