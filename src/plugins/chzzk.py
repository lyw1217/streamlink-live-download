"""
$description South Korean live-streaming platform for gaming, entertainment, and other creative content. Owned by Naver.
$url chzzk.naver.com
$type live, vod
"""

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.dash import DASHStream
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(
    name="live",
    pattern=re.compile(r"https?://chzzk\.naver\.com/live/(?P<channel_id>[^/?]+)"),
)
@pluginmatcher(
    name="video",
    pattern=re.compile(r"https?://chzzk\.naver\.com/video/(?P<video_id>[^/?]+)"),
)
class Chzzk(Plugin):
    _API_CHANNELS_LIVE_DETAIL = "https://api.chzzk.naver.com/service/v1/channels/{channel_id}/live-detail"
    _API_VIDEOS = "https://api.chzzk.naver.com/service/v1/videos/{video_id}"
    _API_VOD_PLAYBACK_URL = "https://apis.naver.com/neonplayer/vodplay/v1/playback/{video_id}?key={in_key}"

    def _query_api(self, url, *schemas):
        return self.session.http.get(
            url,
            acceptable_status=(200, 404),
            schema=validate.Schema(
                validate.parse_json(),
                validate.any(
                    validate.all(
                        {
                            "code": int,
                            "message": str,
                        },
                        validate.transform(lambda data: ("error", data["message"])),
                    ),
                    validate.all(
                        {
                            "code": 200,
                            "content": dict,
                        },
                        validate.get("content"),
                        *schemas,
                        validate.transform(lambda data: ("success", data)),
                    ),
                ),
            ),
        )

    def _api_channels_live_detail(self, channel_id):
        return self._query_api(
            self._API_CHANNELS_LIVE_DETAIL.format(channel_id=channel_id),
            {
                "status": str,
                "liveId": int,
                "liveTitle": validate.any(str, None),
                "liveCategory": validate.any(str, None),
                "channel": validate.all(
                    {"channelName": str},
                    validate.get("channelName"),
                ),
                "livePlaybackJson": validate.all(
                    str,
                    validate.parse_json(),
                    {
                        "media": [
                            validate.all(
                                {
                                    "mediaId": str,
                                    "protocol": str,
                                    "path": validate.url(),
                                },
                                validate.union_get(
                                    "mediaId",
                                    "protocol",
                                    "path",
                                ),
                            ),
                        ],
                    },
                    validate.get("media"),
                ),
            },
            validate.union_get(
                "status",
                "liveId",
                "channel",
                "liveCategory",
                "liveTitle",
                "livePlaybackJson",
            ),
        )

    def _api_videos(self, video_id):
        return self._query_api(
            self._API_VIDEOS.format(video_id=video_id),
            {
                "inKey": str,
                "videoId": str,
                "videoTitle": validate.any(str, None),
                "videoCategory": validate.any(str, None),
                "channel": validate.all(
                    {"channelName": str},
                    validate.get("channelName"),
                ),
            },
            validate.union_get(
                "inKey",
                "videoId",
                "channel",
                "videoCategory",
                "videoTitle",
            ),
        )

    def _get_live(self, channel_id):
        datatype, data = self._api_channels_live_detail(channel_id)
        if datatype == "error":
            log.error(data)
            return

        status, self.id, self.author, self.category, self.title, media = data
        if status != "OPEN":
            log.error("The stream is unavailable")
            return

        for media_id, media_protocol, media_path in media:
            if media_protocol == "HLS" and media_id == "HLS":
                return HLSStream.parse_variant_playlist(
                    self.session,
                    media_path,
                    ffmpeg_options={"copyts": True},
                )

    def _get_video(self, video_id):
        datatype, data = self._api_videos(video_id)
        if datatype == "error":
            log.error(data)
            return

        self.id = video_id
        in_key, vod_id, self.author, self.category, self.title = data

        for name, stream in DASHStream.parse_manifest(
            self.session,
            self._API_VOD_PLAYBACK_URL.format(video_id=vod_id, in_key=in_key),
            headers={"Accept": "application/dash+xml"},
        ).items():
            if stream.video_representation.mimeType == "video/mp2t":
                yield name, stream

    def _get_streams(self):
        if self.matches["live"]:
            return self._get_live(self.match["channel_id"])
        elif self.matches["video"]:
            return self._get_video(self.match["video_id"])


__plugin__ = Chzzk
