# streamlink 를 이용한 실시간 스트리밍 다운로드

## 개요

streamlink를 이용한 스트리밍 다운로드

target 스트리머의 방송 시작 및 종료를 주기적으로 확인하여 실시간으로 스트리밍 영상을 다운로드 받는 스크립트

## - 설치 방법

1.  ### python 가상환경 구성

        python3 -m venv venv

2.  ### 가상환경 진입

        source venv/bin/activate

3.  ### streamlink 설치

        pip install --upgrade streamlink

    - 설치 참고 : https://streamlink.github.io/install.html

## - 사전 준비 사항

1. ### 스트리머의 url 저장

   다운로드하고 싶은 스트리머의 url을 [target_url.dat](./target_url.txt)에 저장한다.

   ```
   # ./target_url.txt

   https://www.twitch.tv/woowakgood
   https://www.twitch.tv/vo_ine
   ```

   - 주의사항 : 'url'만 한 줄씩 입력해야 합니다. 주석처리 없음

## - 실행 방법

1.  ### python 스크립트 실행

        (venv) [UBUNTU-YW] ubuntu@ /home/ubuntu/Documents/github/streamlink-live-download/src # python3 main.py

2.  ### 로그 확인

    - 스크립트 실행 로그 : `./logs/pystreamlink.log`
    - streamlink 실행 로그 : `./logs/streamlink.log`

3.  ### 영상 저장 확인
    - 영상 저장 경로 :
      ```
        MOUNT_DIR="${HOME}/mnt"
        OUTPUT_DIR="${MOUNT_DIR}/Twitch/recordings`
      ```
    - 영상 이름 규칙 : `[{author}]_{time:%Y-%m-%d-%H%M}_{title}.ts`
      - config.json에서 `FILE_RULE` 을 변경하여 설정 가능
        - Metadata variables 참고 (https://streamlink.github.io/cli.html#metadata-variables)
      - 영상 이름을 제대로 가져오지 못하는 버그가 있음
        - 방송 시작하면 다시 조회해서 `영상 이름.txt` 파일을 동일 경로에 생성하도록 함 (이름 바꾸기 수동으로 해주어야됨)
        - 스트리머가 방송 시작한 직후 title을 입력하기 때문인지 아니면 다른 이유인지 트위치 어플에서도 방송 시작과 동시에는 title이 뜨지 않음
        - 그런데 author도 못가져오는 이유는 모르겠음.

## - 채굴까지 하고 싶다면?

구글 크롬 및 [auto-clicker 확장 프로그램](https://chrome.google.com/webstore/detail/twitch-channel-points-aut/jdpblpklojajpopllbckephjndibljbc)이 설치되어있어야 합니다.

1.  ### python mining 스크립트 실행

        (venv) [UBUNTU-YW] ubuntu@ /home/ubuntu/Documents/github/streamlink-live-download/src # python3 main_mining.py

2.  ### 구글 크롬 실행 확인
        
    구글 크롬에서 해당 스트리머의 방송 url이 자동으로 새 창에서 열리며, 방송이 종료되면 자동으로 크롬이 닫힙니다.