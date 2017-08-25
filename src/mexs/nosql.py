#--coding:utf-8--


# from bson.objectid import ObjectId

# database = None

import base64
import binascii


class KoalaCollection(object):
    MESSAGE = "message"
    APPLICATION = "application"

    @staticmethod
    def getUserMessageCollection(user_id):
        # user_id = base64.b64encode(user_id)
        user_id = binascii.b2a_hex(user_id)
        return "{}_{}".format( KoalaCollection.MESSAGE,user_id)

class UserMessageStatus(object):
    FIELD = 'status'

    Sendable = 1        # 消息可被传递
    Confirmed = 2       # 消息已确认不能被传递


"""
    m = Message_t()
    m.meta.realm = row.get('realm','')
    m.meta.seq = row.get('_id')
    m.meta.sender = row.get('sender_id')
    m.meta.stime = row.get('send_time')
    m.title = row.get('title','')
    m.content = row.get('content','')
    m.props = Properties_t(row.get('props',{}))
"""

