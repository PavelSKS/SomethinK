# CHANNEL/ROLE
WHITE_LIST_OF_CHANNEL = __list_of_channel__
HISTORY_CHANNEL_ID = __history_id_channel__
MODER_ROLE_ID = __moderator_id__
REPORT_CHANNEL_ID = __report_id_channel__

# CHECK URL
TWITCH_LINK_CHECK = 'twitch.tv'
YOUTUBE_LINK_CHECK = 'youtube.com'

# PREFIX
PREFIX = '__predix__'


# BAN WORD
ban_word_msg = ''
ban_word_list = open('banword.txt', encoding='utf-8').read().split('\n')

for word in ban_word_list:
    ban_word_msg += word + ', '
