from datetime import datetime
from jinja2 import Markup


class MomentJs(object):
    def __init__(self, timestamp=None, local=False):
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
        self.local = local

    def _timestamp_as_iso_8601(self, timestamp):
        tz = ''
        if not self.local:
            tz = 'Z'
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S' + tz)

    def _render(self, format, refresh=False):
        t = self._timestamp_as_iso_8601(self.timestamp)
        return Markup('<span class="flask-moment" data-timestamp="{}" data-format="{}" data-refresh="{:d}" style="display: none">{}</span>'.format(
            t, format, int(refresh) * 60000, t))

    def format(self, fmt=None, refresh=False):
        return self._render("format('%s')" % (fmt or ''), refresh)

    def fromNow(self, no_suffix=False, refresh=False):
        return self._render("fromNow(%s)" % int(no_suffix), refresh)

    def fromTime(self, timestamp, no_suffix=False, refresh=False):
        return self._render("from(moment('%s'),%s)" % (
            self._timestamp_as_iso_8601(timestamp), int(no_suffix)), refresh)

    def toNow(self, no_suffix=False, refresh=False):
        return self._render("toNow(%s)" % int(no_suffix), refresh)

    def toTime(self, timestamp, no_suffix=False, refresh=False):
        return self._render("to(moment('%s'),%s)" % (
            self._timestamp_as_iso_8601(timestamp), int(no_suffix)), refresh)

    def calendar(self, refresh=False):
        return self._render("calendar()", refresh)

    def valueOf(self, refresh=False):
        return self._render("valueOf()", refresh)

    def unix(self, refresh=False):
        return self._render("unix()", refresh)
