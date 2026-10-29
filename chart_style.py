# Morinus 차트 스타일 설정 스크립트
# 흰 배경 + 검은 선 + 행성만 색 (태양·목성·토성 빨강 / 달·금성·화성 파랑 / 수성·노드·포르투나 검정)
# 사용법: Morinus 폴더에서  python chart_style.py  실행 (모리누스는 꺼둔 상태로)

import os, sys
sys.path.insert(0, os.getcwd())
import wx
app = wx.App(False)
import options

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 0, 0)
BLUE = (0, 0, 220)

o = options.Options()

# --- 표시 설정 (Appearance) ---
o.bw = False                          # 컬러 모드
o.aspects = False                     # 각(aspect) 선 숨기기
o.transcendental = [False, False, False]  # 천왕성·해왕성·명왕성 숨기기
o.shownodes = True                    # 노드 표시
o.showlof = True                      # 포르투나 표시
o.showterms = True                    # 바깥 링에 텀(bounds) 표시
o.showdecans = False                  # 데칸 링 숨기기
o.showfixstars = 0                    # 항성 이름 숨기기

# --- 하우스 시스템: Porphyrius ---
o.hsys = 'O'

# --- 색 설정 (Colors) ---
o.clrbackground = WHITE
o.clrframe = BLACK
o.clrsigns = BLACK
o.clrAscMC = BLACK
o.clrhouses = BLACK
o.clrhousenumbers = BLACK
o.clrpositions = BLACK
o.clrtable = BLACK
o.clrtexts = BLACK
o.clraspect = [BLACK] * len(o.clraspect)

# 순서: 태양, 달, 수성, 금성, 화성, 목성, 토성, 천왕성, 해왕성, 명왕성, 노드, 포르투나
o.clrindividual = [RED, BLUE, BLACK, BLUE, BLUE, RED, RED, BLACK, BLACK, BLACK, BLACK, BLACK]
o.useplanetcolors = True

o.saveAppearance1()
o.saveColors()
o.saveHouseSystem()
print("완료! 모리누스를 다시 실행하세요.")
