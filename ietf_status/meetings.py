# Copyright (C) 2026 Colin Perkins
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from .datatracker import DataTracker

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


class Meetings:
    _curr_meeting : dict[str,any]
    _next_meeting : dict[str,any]

    def __init__(self, dt:DataTracker):
        today = datetime.now(ZoneInfo("America/Los_Angeles")) 
        self._curr_meeting = None
        self._next_meeting = None
        for meeting in dt.get_multi("/api/v1/meeting/meeting/?type=ietf"):
            meeting_start = date.fromisoformat(meeting["date"])
            meeting_end   = meeting_start + timedelta(days = meeting["days"] - 1)
            if meeting_start > date.today():
                if self._next_meeting is None or meeting["date"] < self._next_meeting["date"]:
                    self._next_meeting = meeting
            elif meeting_end < date.today():
                break
            else:
                self._curr_meeting = meeting


    def curr_meeting(self) -> dict[str,any] | None:
        return self._curr_meeting


    def next_meeting(self) -> dict[str,any]:
        return self._next_meeting


