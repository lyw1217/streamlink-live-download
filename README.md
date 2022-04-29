# streamlink 를 이용한 실시간 스트리밍 다운로드 및 유튜브 자동 업로드

## 개요

streamlink를 이용한 스트리밍 다운로드 및 유튜브 자동 업로드

target 스트리머의 방송 시작 및 종료를 주기적으로 확인하여 실시간으로 스트리밍 영상을 다운로드 받고

유튜브에 비공개로 업로드하는 파이썬 스크립트

## - 설치 방법

1.  ### python 가상환경 구성

        python3 -m venv venv

2.  ### 가상환경 진입

        source venv/bin/activate

3.  ### streamlink 설치
        
        pip install --upgrade streamlink
        
    - 설치 참고 : https://streamlink.github.io/install.html

4.  ### google-api-python-client 사용을 위한 모듈 설치

        # https://github.com/googleapis/google-api-python-client
        pip install httplib2 uritemplate pyopenssl WebTest wheel apiclient 
        pip install --upgrade oauth2client
        pip install --upgrade google-api-python-client

5. ### Google에 애플리케이션 등록 및 OAuth 2.0 사용을 위한 인증 정보 만들기

참고1 : https://developers.google.com/youtube/registering_an_application?hl=ko

참고2 : https://kminito.tistory.com/5


        # client_secrets.json 예시

        {
        "installed": {
                "client_id":"123456-abcdefg.apps.googleusercontent.com",
                "project_id":"pystreamlink",
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":"ABCDE-ABC_DEF12345",
                "redirect_uris":["http://localhost"]
                }
        }

6. ### oauth 인증(브라우저에서 클릭 필요)
첫 업로드할 때 필요한데, 어떻게 간단하게 처리할지 아직 모름

7. ### 구글 크롬 및 [auto-clicker 확장 프로그램](https://chrome.google.com/webstore/detail/twitch-channel-points-aut/jdpblpklojajpopllbckephjndibljbc) 설치


## - 실행 방법
1. ### 스트리머의 url 저장

   다운로드하고 싶은 스트리머의 url을 [target_url.txt](./target_url.txt)에 저장한다.

   ```
   $ cat target_url.txt

   https://www.twitch.tv/woowakgood
   https://www.twitch.tv/vo_ine
   ```

   - 주의사항 : 'url'만 한 줄씩 입력해야 합니다. 주석처리 없음

2.  ### python 스크립트 실행

        (venv) [UBUNTU-YW] ubuntu@ /home/ubuntu/Documents/github/streamlink-live-download/src # python main.py

3.  ### 로그 확인

    - 스크립트 실행 로그 : `./logs/pystreamlink.log`
    - streamlink 실행 로그 : `./logs/streamlink.log`

4.  ### 영상 저장 확인
    - 영상 저장 경로 :
      ```
        MOUNT_DIR="${HOME}/mnt"
        OUTPUT_DIR="${MOUNT_DIR}/Twitch/recordings`
      ```
    - 영상 이름 규칙 : `[{author}]_{time:%Y-%m-%d-%H%M%S}_{title}.ts`
      - config.json에서 `FILE_RULE` 을 변경하여 설정 가능
        - Metadata variables 참고 (https://streamlink.github.io/cli.html#metadata-variables)

5.  ### 구글 크롬 실행 및 종료 확인
        
    스트리밍이 시작되면 구글 크롬에서 해당 스트리머의 방송 url이 새 창에서 열리며, 스트리밍이 종료되면 자동으로 크롬이 닫힙니다.


## - 이슈

### 스트리머 author, title을 가져오지 못하는 이슈
- 스트리밍 시작 직후에는 metadata를 (title, author)을 제대로 가져오지 못하는 버그가 있음
- 스트리밍 시작하면 다시 조회해서 `영상 이름.txt` 파일을 동일 경로에 생성하도록 함 (이름 바꾸기 수동으로 해주어야됨)
- 스트리머가 방송 시작한 직후 title을 입력하기 때문인지 아니면 다른 이유인지 트위치 어플에서도 방송 시작과 동시에는 title이 뜨지 않음
- 그런데 author도 못가져오는 이유는 모르겠음.
- (결과)
    - streamlink의 문제가 아니라 twitch api의 문제 (https://github.com/streamlink/streamlink/issues/4411)
    - 약 10초 내외의 딜레이가 있는 것 같음
    - title, author 가 조회되면 영상 다운로드를 시작하는 방식으로 변경(초반 10초정도는 다운로드하지 못함)
    - 이렇게 하지 않으면 유투브 자동 업로드가 어려워짐..

### YouTube Data API v3의 quota(할당량)
- 일일 할당량은 10,000
- 유튜브 업로드(insert)의 비용은 1,600(https://developers.google.com/youtube/v3/determine_quota_cost?hl=ko)
- 즉, 하루에 최대 6개의 영상 업로드가 가능함(cost : 9,600)
- 일일 할당량은 태평양 표준시(PT) 자정에 재설정됨 (우리나라와 +17)
    - 즉, 매일 17시에 초기화가 된다.
- 6개 이상의 영상이 존재할 때, 어떻게 처리할지 고민해봐야함
    - 우선 quota를 확인하고 영상 업로드가 가능하면 업로드, 불가능하면 로그찍고 저장? 다음 날 초기화되면 다시 수행?