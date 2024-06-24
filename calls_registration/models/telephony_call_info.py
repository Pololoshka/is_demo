from __future__ import annotations

import os
from typing import TYPE_CHECKING

import base64

import settings
from calls_registration.constants import Constants as c
from mutagen.mp3 import MP3
from django.db import models
from pathlib import Path

from calls_registration.models.choise_add_to_chat import NumberChoicesAddToChat
from calls_registration.models.choise_type_call import NumberChoicesType

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


class TelephonyCallInfo(models.Model):
    add_to_chat = models.IntegerField(null=True, blank=True,
                                      choices=NumberChoicesAddToChat.choices)
    call_date = models.DateTimeField(null=True, blank=True)
    call_id = models.CharField(max_length=255, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    file = models.FileField(upload_to=c.inner_media_path, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    type = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesType.choices)
    user_id = models.IntegerField(null=False, blank=False)
    user_phone_inner = models.CharField(max_length=20, null=False, blank=False)


    def telephony_externalcall_register(self, but: BitrixUserToken) -> None:
        call = but.call_api_method("telephony.externalcall.register", {
            "USER_PHONE_INNER": self.user_phone_inner,
            "USER_ID": self.user_id,
            "PHONE_NUMBER": self.phone_number,
            "CALL_START_DATE": self.call_date,
            "TYPE": self.type,
        })

        self.call_id = call['result']['CALL_ID']
        self.duration = int(MP3(self.file).info.length)

        self.save()

    def telephony_externalcall_finish(self, but: BitrixUserToken) -> None:
        but.call_api_method('telephony.externalcall.finish', {
            "CALL_ID": self.call_id,
            "USER_ID": self.user_id,
            "DURATION": self.duration,
            "ADD_TO_CHAT": self.add_to_chat,
        })

    def telephony_externalcall_attachrecord(self, but: BitrixUserToken) -> None:
        with open((Path(settings.MEDIA_ROOT) / self.file.name), 'rb') as fi:
            file_content = base64.b64encode(fi.read())
        but.call_api_method('telephony.externalCall.attachRecord', {
            "CALL_ID": self.call_id,
            "FILENAME": str(self.file)[len(c.inner_media_path):],
            "FILE_CONTENT": file_content,
        })
