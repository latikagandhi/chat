import json

from utils.common import generate_response
from utils.http_code import *
import datetime
import random
import os

from .models import MessageMedia, MessageRecipients, Message, ChatRoom


def get_rooms(input_data, user_id):
    rooms = ChatRoom.objects(participants__user_id__contains=user_id).order_by('-updated_at').select_related(3)

    for room in rooms:
        if not room['is_group']:
            if room['participants']:
                if user_id == room['participants'][0]['user_id']:
                    room['name'] = room['participants'][-1]['email']
                    room['image'] = room['participants'][-1]['profile_image']
                else:
                    room['name'] = room['participants'][0]['email']
                    room['image'] = room['participants'][0]['profile_image']
    return rooms


def get_messages(input_data):
    # import pdb;pdb.set_trace()
    page = input_data.get('page', 1)
    page_size = input_data.get('page_size', 10)
    # room = ChatRoom.objects(id=input_data['room']).get().to_json()
    room = ChatRoom.objects(id=input_data['room']).get().to_json()
    if not room['is_group']:
        if room['participants']:
            if input_data['user_id'] == room['participants'][0]['user_id']:
                room['name'] = room['participants'][-1]['email']
                room['image'] = room['participants'][-1]['profile_image']
            else:
                room['name'] = room['participants'][0]['email']
                room['image'] = room['participants'][0]['profile_image']
    # import pdb;
    # pdb.set_trace()
    # messages = Message.objects(recipients__room=input_data['room'])
    


    unread_count = Message.objects(recipients__room=room['id'], recipients__is_read=False,
                                   recipients__recipient__user_id=input_data['user_id']).count()
    
    if unread_count > 0:
        page_size = unread_count+20
    
    messages_pagination = Message.objects(recipients__room=input_data['room']).paginate(page=page, per_page=page_size)
    list_of_items = messages_pagination.items


    return generate_response(
        data={
            'room': room, 
            'messages': [message.to_json() for message in list_of_items], 
            'unread_count': unread_count,
            'paginate': {
                "page" : messages_pagination.page,
                "page_size" : messages_pagination.per_page,
                "total_pages" : messages_pagination.pages,
                "total_number_of_items" : messages_pagination.total
            },
            },
        status=HTTP_200_OK)
