# streamlink 실시간 스트리밍 다운로드 및 유튜브 자동 업로드

__※ 제 환경이 아닌 다른 환경에서의 실사용은 어렵습니다. ※__

## 개요

__[ [streamlink](https://github.com/streamlink/streamlink)를 이용한 스트리밍 다운로드 및 유튜브 자동 업로드 ]__

스트리머의 방송 시작 및 종료를 주기적으로 확인하여 실시간으로 스트리밍 영상을 다운로드 받고

유튜브에 비공개로 업로드하는 파이썬 데몬 스크립트 (Twitch 방송을 위해 제작하였지만 Youtube도 사용 가능)

## 개발 및 사용 환경

- Ubuntu 20.04.4 LTS (Focal Fossa)
- Python 3.8.10
- Google Chrome 100.0.4896.127
- streamlink 3.2.0

## 설치 방법

1.  python 가상환경 구성

        python3 -m venv venv

2.  가상환경 진입

        source venv/bin/activate

3.  streamlink 설치
        
        pip install --upgrade streamlink
        
    - 설치 참고 : https://streamlink.github.io/install.html

4.  google-api-python-client 사용을 위한 모듈 설치

        # https://github.com/googleapis/google-api-python-client
        pip install httplib2 uritemplate pyopenssl WebTest wheel apiclient 
        pip install --upgrade oauth2client
        pip install --upgrade google-api-python-client

5. Google에 애플리케이션 등록 및 OAuth 2.0 사용을 위한 인증 정보 만들기

    참고1 : https://developers.google.com/youtube/registering_an_application?hl=ko

    참고2 : https://kminito.tistory.com/5


        # client_secrets.json 예시

        {
                "installed": {
                        "client_id":"123456-abcdefg.apps.googleusercontent.com",
                        "project_id":"example",
                        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                        "token_uri":"https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                        "client_secret":"ABCDE-ABC_DEF12345",
                        "redirect_uris":["http://localhost"]
                }
        }

6. oauth 인증(브라우저에서 클릭 필요)

7. 구글 크롬 및 채굴을 위한 트위치 자동 클릭 확장 프로그램 설치


## 실행 방법

1. [config.json](./config/config.json) 을 환경에 맞게 설정한다.

        {
                # 스트리밍 탐색 주기
                "INTERVAL": 5,
                # 파일시스템 사용량 경고 Usage(%)
                "WARN_USAGE": 85,
                # 다운로드할 영상의 퀄리티
                "QUALITY": "best",
                # 다운로드 경로
                "OUTPUT_DIR": "/home/ubuntu/mnt/Twitch/recordings",
                # 영상 파일명 규칙
                "FILE_RULE": "[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts",
                # 다운로드할 스트리머의 주소 목록
                "TARGET_URL": "/home/ubuntu/Documents/github/streamlink-live-download/target_url.txt",
                # streamlink 실행 파일 경로(pip로 install한 경로)
                "STREAMLINK_CMD": "/home/ubuntu/Documents/github/streamlink-live-download/venv/bin/streamlink",
                # streamlink 옵션
                "STREAMLINK_OPTIONS": "--force --twitch-disable-hosting --twitch-disable-ads --twitch-disable-reruns",
                # streamlink 로그 옵션
                "STREAMLINK_LOG_OPTIONS": "info",
                # streamlink 로그 경로
                "STREAMLINK_LOG_PATH": "/home/ubuntu/Documents/github/streamlink-live-download/logs/streamlink",
                # 유튜브 업로드 파이썬 스크립트 경로
                "UPLOAD_YOUTUBE_PY": "/home/ubuntu/Documents/github/streamlink-live-download/src/upload_youtube.py",
                # subprocess로 파이썬을 실행하기 위한 python 실행 경로
                "PYTHON_CMD": "/home/ubuntu/Documents/github/streamlink-live-download/venv/bin/python",
                # 영상 업로드 실패 시 임시 저장 경로
                "SAVED_DIR": "/home/ubuntu/mnt/Twitch/recordings/saved",
                # 업로드 완료된 영상 파일 저장 경로
                "UPLOADED_DIR": "/home/leeyw/mnt/Twitch/recordings/uploaded",
                # container로 기동 시 pipe를 통한 chrome 실행 기능 수행 여부
                "PIPE_FLAG": false
        }


2. 다운로드하고 싶은 스트리머의 url을 [target_url.txt](./target_url.txt)에 저장한다.

   ```
   $ cat target_url.txt

   https://www.twitch.tv/woowakgood
   https://www.twitch.tv/vo_ine
   ```

   - 주의사항 : 'url'만 한 줄씩 입력해야 합니다. 주석처리 없음

3.  python 스크립트를 실행한다.

        (venv) [UBUNTU-YW] ubuntu@ /home/ubuntu/Documents/github/streamlink-live-download/src # python main.py

4.  실행 로그를 확인한다.

    - 스크립트 실행 로그 : `./logs/pystreamlink.log`
    - streamlink 실행 로그 : `./logs/streamlink_{streamer}.log`

5.  영상이 정상적으로 저장되는지 확인한다.

    - 영상 저장 경로 :
        
        [config.json](./config/config.json) 에서 `OUTPUT_DIR` 을 변경하여 설정 가능
    
    - 영상 이름 규칙 : 
    
        [config.json](./config/config.json)에서 `FILE_RULE` 을 변경하여 설정 가능
        
        - Metadata variables [참고](https://streamlink.github.io/cli.html#metadata-variables)

6.  구글 크롬 실행 및 종료 확인
        
    스트리밍이 시작되면 해당 스트리머의 방송 url이 구글 크롬에서 새 창으로 열리며, 스트리밍이 종료되면 자동으로 크롬이 닫힙니다.

7. E-Mail, Slack 알림 설정

    `./config/secrets.json` 파일을 아래와 같이 설정하면 영상 업로드 실패, 파일 시스템 용량 경고와 같은 중요 에러 발생 시 이메일 및 Slack으로 해당 내용을 전송
    
    (미설정 시 전송하지 않음)

    ```
    {
        "FROM_EMAIL_ADDR": "abc@example.com",
        "TO_EMAIL_ADDR": "your_email@gmail.com",
        "SLACK_CHANNEL":"slack_channel_name",
        "SLACK_KEY":"xoxb-1234123412341-123412341234-KdozV41VqaIxcVLqwBgbvcdA"
    }
    ```

## 이슈

### 스트리머 author, title을 가져오지 못하는 이슈
- 스트리밍 시작 직후에는 metadata를 (title, author)을 제대로 가져오지 못하는 버그가 있음
- 스트리밍 시작하면 다시 조회해서 `영상 이름.txt` 파일을 동일 경로에 생성하도록 함 (이름 바꾸기 수동으로 해주어야됨)
- 스트리머가 방송 시작한 직후 title을 입력하기 때문인지 아니면 다른 이유인지 트위치 어플에서도 방송 시작과 동시에는 title이 뜨지 않음
- 그런데 author도 못가져오는 이유는 모르겠음.
- (결과)
    - streamlink의 문제가 아니라 twitch api의 문제 (https://github.com/streamlink/streamlink/issues/4411)
    - 약 10초 내외의 딜레이가 있는 것 같음 -> 30초 가량 딜레이가 생겨 그만큼 녹화가 누락되는 현상도 발견..
    - title, author 가 조회되면 영상 다운로드를 시작하는 방식으로 변경(초반 10초정도는 다운로드하지 못함)
    - 이렇게 하지 않으면 유투브 자동 업로드가 어려워짐..

### YouTube Data API v3의 quota(할당량)
- 일일 요청 한도는 10,000, 1분 요청 한도는 1,600 
- 유튜브 업로드(insert)의 비용은 1,600(https://developers.google.com/youtube/v3/determine_quota_cost?hl=ko)
- 1분에 최대 1개의 영상 업로드,
- 하루에 최대 6개의 영상 업로드가 가능함(6개 업로드 시 cost = 9,600)
- 일일 할당량은 태평양 표준시(PT) 자정에 재설정됨 (우리나라와 +17)
    - 즉, 매일 17시에 초기화가 된다. (서머타임 적용시 16시)
- 6개를 초과하는 영상들이 존재할 때, 어떻게 처리할지 고민해봐야함
    - 우선 quota를 확인하고 영상 업로드가 가능하면 업로드, 불가능하면 로그찍고 저장? 다음 날 초기화되면 다시 수행?
    - quota를 확인하는 api가 없는 것 같음(웹에서 확인, https://console.cloud.google.com/ 에서 [API 및 서비스]-[사용 설정된 API 및 서비스])
    - 403 에러 응답을 받으면 1분 뒤 재시도 해보고(1분 내 여러명의 스트리밍이 종료되었을 수 있으니)
    - 1분 뒤 재시도 해도 403 응답이라면 로그 찍고 saved 디렉토리에 저장
    - saved 디렉토리에 저장되어 있는 영상들은 매일 17시에 자동으로 업로드함
        - 여기서도 403 에러 응답을 받으면 1분 뒤 재시도 해보고 그래도 403 이라면 로그 찍고 saved 디렉토리에 그대로 유지 및 다음 날 17시까지 sleep

### Youtube API의 토큰 갱신 한도?
- Youtube API를 통해 영상을 Upload 하면 약 50회 정도에 한 번씩 웹 브라우저를 통해 토큰을 갱신하는 작업이 필요하다.
- 따로 구글에 promotion 신청을 하면 한도를 늘려주는 것 같은데 개인적인 프로젝트이므로 신청이 어려워보인다.
- 로컬에서 실행한다면 웹 브라우저를 통해 사용자가 직접 클릭해주는 방식으로, 컨테이너를 통해 실행한다면 `--noauth_local_webserver` 옵션을 이용해 외부 웹 브라우저에서 인증 후 코드를 Slack 메시지로 전달받아 갱신하는 방식을 사용했다.