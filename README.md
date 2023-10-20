# TLSv1.3 :: Full Handshake & Session Resumption

TLSv1.3에서 Full Handshake와 Session Resumption 과정을 시연하도록 작성된 /src/main.py를 이용하여 패킷을 발생시키고 그것을 Wireshark로 캡쳐해서 분석해보자.

사용되는 서버는 Self-Certificated 서버이다.

## 캡처된 패킷의 모습

![](/images/loopback.png)

---

![](/images/capture-options.png)

Localhost 주고받는 패킷을 캡처하기 위해 Loopback 채널을 선택하여 패킷을 캡처해야 한다.