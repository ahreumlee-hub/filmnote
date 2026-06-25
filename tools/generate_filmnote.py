from __future__ import annotations

import csv
import html
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "film log" / "Film log 333ce94eb2668114ab48e7b1b02a9949_all.csv"
NOTE_DIR = ROOT / "film log" / "Film log"
HTML_DIR = ROOT / "html"
POSTER_MANIFEST = ROOT / "srcs" / "img" / "posters" / "manifest.json"


FILM_INFO: dict[str, dict[str, str]] = {
    "버닝": {"Director": "이창동", "Year": "2018", "Country": "대한민국", "Genre": "미스터리, 드라마", "Duration": "148분"},
    "블루 발렌타인": {"Director": "데릭 시엔프랜스", "Year": "2010", "Country": "미국", "Genre": "드라마, 로맨스", "Duration": "112분"},
    "릴리 슈슈의 모든 것": {"Director": "이와이 슌지", "Year": "2001", "Country": "일본", "Genre": "드라마", "Duration": "146분"},
    "하나와 앨리스": {"Director": "이와이 슌지", "Year": "2004", "Country": "일본", "Genre": "드라마, 로맨스", "Duration": "135분"},
    "세계의 주인": {"Director": "윤가은", "Year": "2025", "Country": "대한민국", "Genre": "드라마", "Duration": "119분"},
    "박화영": {"Director": "이환", "Year": "2018", "Country": "대한민국", "Genre": "드라마", "Duration": "112분"},
    "위대한 개츠비": {"Director": "바즈 루어만", "Year": "2013", "Country": "미국, 오스트레일리아", "Genre": "드라마, 로맨스", "Duration": "143분"},
    "라스트 홀리데이": {"Director": "웨인 왕", "Year": "2006", "Country": "미국", "Genre": "코미디, 드라마", "Duration": "112분"},
    "원 배틀 애프터 어나더": {"Director": "폴 토머스 앤더슨", "Year": "2025", "Country": "미국", "Genre": "액션, 스릴러", "Duration": "162분"},
    "세 가지 색: 블루": {"Director": "크지슈토프 키에슬로프스키", "Year": "1993", "Country": "프랑스, 폴란드", "Genre": "드라마", "Duration": "98분"},
    "시라트": {"Director": "올리버 라세", "Year": "2025", "Country": "스페인, 프랑스", "Genre": "드라마, 스릴러", "Duration": "120분"},
    "마이 선샤인": {"Director": "오쿠야마 히로시", "Year": "2024", "Country": "일본", "Genre": "드라마", "Duration": "90분"},
    "물에 빠진 나이프": {"Director": "야마토 유키", "Year": "2016", "Country": "일본", "Genre": "드라마, 로맨스", "Duration": "111분"},
    "혐오스런 마츠코의 일생": {"Director": "나카시마 테츠야", "Year": "2006", "Country": "일본", "Genre": "드라마, 뮤지컬", "Duration": "130분"},
    "문라이트킹덤": {"Director": "웨스 앤더슨", "Year": "2012", "Country": "미국", "Genre": "코미디, 드라마", "Duration": "94분"},
    "나이트 크롤러": {"Director": "댄 길로이", "Year": "2014", "Country": "미국", "Genre": "스릴러, 범죄", "Duration": "118분"},
    "부고니아": {"Director": "요르고스 란티모스", "Year": "2025", "Country": "미국", "Genre": "SF, 코미디", "Duration": "118분"},
    "만약에 우리": {"Director": "김도영", "Year": "2025", "Country": "대한민국", "Genre": "로맨스, 드라마", "Duration": "115분"},
    "퐁네프의 연인들": {"Director": "레오스 카락스", "Year": "1991", "Country": "프랑스", "Genre": "드라마, 로맨스", "Duration": "125분"},
    "셔터 아일랜드": {"Director": "마틴 스코세이지", "Year": "2010", "Country": "미국", "Genre": "미스터리, 스릴러", "Duration": "138분"},
    "시카리오": {"Director": "드니 빌뇌브", "Year": "2015", "Country": "미국", "Genre": "범죄, 스릴러", "Duration": "121분"},
    "세 가지 색: 화이트": {"Director": "크지슈토프 키에슬로프스키", "Year": "1994", "Country": "프랑스, 폴란드", "Genre": "코미디, 드라마", "Duration": "92분"},
    "씨너스: 죄인들": {"Director": "라이언 쿠글러", "Year": "2025", "Country": "미국", "Genre": "공포, 스릴러", "Duration": "138분"},
    "탑건: 매버릭": {"Director": "조셉 코신스키", "Year": "2022", "Country": "미국", "Genre": "액션, 드라마", "Duration": "130분"},
    "베놈": {"Director": "루벤 플레셔", "Year": "2018", "Country": "미국", "Genre": "액션, SF", "Duration": "112분"},
    "호퍼스": {"Director": "다니엘 총", "Year": "2026", "Country": "미국", "Genre": "애니메이션, 코미디", "Duration": "정보 없음"},
    "올빼미": {"Director": "안태진", "Year": "2022", "Country": "대한민국", "Genre": "스릴러, 사극", "Duration": "118분"},
    "아나콘다": {"Director": "루이스 로사", "Year": "1997", "Country": "미국", "Genre": "공포, 모험", "Duration": "89분"},
    "매트릭스2": {"Director": "워쇼스키", "Year": "2003", "Country": "미국", "Genre": "액션, SF", "Duration": "138분"},
    "매트릭스3": {"Director": "워쇼스키", "Year": "2003", "Country": "미국", "Genre": "액션, SF", "Duration": "129분"},
    "프로젝트 Y": {"Director": "이환", "Year": "2026", "Country": "대한민국", "Genre": "범죄, 누아르", "Duration": "110분"},
    "바비": {"Director": "그레타 거윅", "Year": "2023", "Country": "미국", "Genre": "코미디, 판타지", "Duration": "114분"},
    "세 가지 색: 레드": {"Director": "크지슈토프 키에슬로프스키", "Year": "1994", "Country": "프랑스, 폴란드", "Genre": "드라마, 미스터리", "Duration": "99분"},
    "핫스팟: 우주인 출몰 주의!": {"Director": "미즈노 카쿠", "Year": "2025", "Country": "일본", "Genre": "코미디, SF", "Duration": "10부작"},
    "모두가 자신의 무가치함과 싸우고 있다": {"Director": "박해영, 차영훈", "Year": "2026", "Country": "대한민국", "Genre": "드라마", "Duration": "리미티드 시리즈"},
    "우리들": {"Director": "윤가은", "Year": "2016", "Country": "대한민국", "Genre": "드라마", "Duration": "94분"},
}

TITLE_EN = {
    "버닝": "Burning",
    "블루 발렌타인": "Blue Valentine",
    "릴리 슈슈의 모든 것": "All About Lily Chou-Chou",
    "하나와 앨리스": "Hana and Alice",
    "세계의 주인": "The World of Love",
    "박화영": "Park Hwa-young",
    "위대한 개츠비": "The Great Gatsby",
    "라스트 홀리데이": "Last Holiday",
    "원 배틀 애프터 어나더": "One Battle After Another",
    "세 가지 색: 블루": "Three Colors: Blue",
    "시라트": "Sirat",
    "마이 선샤인": "My Sunshine",
    "물에 빠진 나이프": "Drowning Love",
    "혐오스런 마츠코의 일생": "Memories of Matsuko",
    "문라이트킹덤": "Moonrise Kingdom",
    "나이트 크롤러": "Nightcrawler",
    "부고니아": "Bugonia",
    "만약에 우리": "Once We Were Us",
    "퐁네프의 연인들": "The Lovers on the Bridge",
    "셔터 아일랜드": "Shutter Island",
    "시카리오": "Sicario",
    "세 가지 색: 화이트": "Three Colors: White",
    "씨너스: 죄인들": "Sinners",
    "탑건: 매버릭": "Top Gun: Maverick",
    "베놈": "Venom",
    "호퍼스": "Hoppers",
    "올빼미": "The Night Owl",
    "아나콘다": "Anaconda",
    "매트릭스2": "The Matrix Reloaded",
    "매트릭스3": "The Matrix Revolutions",
    "프로젝트 Y": "Project Y",
    "바비": "Barbie",
    "세 가지 색: 레드": "Three Colors: Red",
    "핫스팟: 우주인 출몰 주의!": "Hot Spot: Beware of Aliens!",
    "모두가 자신의 무가치함과 싸우고 있다": "Everyone Is Fighting Their Own Worthlessness",
    "우리들": "The World of Us",
}

VALUE_EN = {
    "이아름": "Lee Areum",
    "이 아름": "Lee Areum",
    "이창동": "Lee Chang-dong",
    "데릭 시엔프랜스": "Derek Cianfrance",
    "이와이 슌지": "Shunji Iwai",
    "윤가은": "Yoon Ga-eun",
    "이환": "Lee Hwan",
    "바즈 루어만": "Baz Luhrmann",
    "웨인 왕": "Wayne Wang",
    "폴 토머스 앤더슨": "Paul Thomas Anderson",
    "크지슈토프 키에슬로프스키": "Krzysztof Kieslowski",
    "올리버 라세": "Oliver Laxe",
    "오쿠야마 히로시": "Hiroshi Okuyama",
    "야마토 유키": "Yuki Yamato",
    "나카시마 테츠야": "Tetsuya Nakashima",
    "웨스 앤더슨": "Wes Anderson",
    "댄 길로이": "Dan Gilroy",
    "요르고스 란티모스": "Yorgos Lanthimos",
    "김도영": "Kim Do-young",
    "레오스 카락스": "Leos Carax",
    "마틴 스코세이지": "Martin Scorsese",
    "드니 빌뇌브": "Denis Villeneuve",
    "라이언 쿠글러": "Ryan Coogler",
    "조셉 코신스키": "Joseph Kosinski",
    "루벤 플레셔": "Ruben Fleischer",
    "다니엘 총": "Daniel Chong",
    "안태진": "An Tae-jin",
    "루이스 로사": "Luis Llosa",
    "워쇼스키": "The Wachowskis",
    "그레타 거윅": "Greta Gerwig",
    "미즈노 카쿠": "Kaku Mizuno",
    "박해영, 차영훈": "Park Hae-young, Cha Young-hoon",
    "대한민국": "South Korea",
    "한국": "South Korea",
    "미국": "United States",
    "일본": "Japan",
    "미국, 오스트레일리아": "United States, Australia",
    "프랑스, 폴란드": "France, Poland",
    "스페인, 프랑스": "Spain, France",
    "프랑스": "France",
    "미스터리, 드라마": "Mystery, Drama",
    "드라마, 로맨스": "Drama, Romance",
    "드라마": "Drama",
    "액션, 스릴러": "Action, Thriller",
    "드라마, 스릴러": "Drama, Thriller",
    "드라마, 뮤지컬": "Drama, Musical",
    "코미디, 드라마": "Comedy, Drama",
    "스릴러, 범죄": "Thriller, Crime",
    "SF, 코미디": "Sci-Fi, Comedy",
    "로맨스, 드라마": "Romance, Drama",
    "미스터리, 스릴러": "Mystery, Thriller",
    "범죄, 스릴러": "Crime, Thriller",
    "공포, 스릴러": "Horror, Thriller",
    "액션, 드라마": "Action, Drama",
    "액션, SF": "Action, Sci-Fi",
    "애니메이션, 코미디": "Animation, Comedy",
    "스릴러, 사극": "Thriller, Period Drama",
    "공포, 모험": "Horror, Adventure",
    "범죄, 누아르": "Crime, Noir",
    "코미디, 판타지": "Comedy, Fantasy",
    "드라마, 미스터리": "Drama, Mystery",
    "코미디, SF": "Comedy, Sci-Fi",
    "정보 없음": "Unknown",
    "리미티드 시리즈": "Limited Series",
    "10부작": "10 episodes",
    "완료": "Complete",
    "예정": "Planned",
    "아직 작성된 노트가 없습니다.": "No note has been written yet.",
}

NOTE_LINE_EN = {
    "피해자": "Victim.",
    "수시로 나오는 댓글 창": "Comment windows appear again and again.",
    "그들의 소통": "Their communication.",
    "흔들리고 정신없는 카메라 무빙": "Shaky, breathless camera movement.",
    "그들의 정신과 현장감을 오롯이 느끼게 해준 연출": "Direction that makes their state of mind and the immediacy of the scene fully felt.",
    "그리고 한줄기 빛과 같은 희망": "And hope like a single beam of light.",
    "에테르, 믿음": "Ether, faith.",
    "이제서야 가장 좋아하는 영화가 무엇인지 묻는 질문에 답할 수 있을 것 같다.": "Only now do I feel able to answer when someone asks what my favorite film is.",
    "릴리 슈슈의 모든 것.": "All About Lily Chou-Chou.",
    "이와이 슌지 감독의 연출법이 참 좋다.": "I really like Shunji Iwai's way of directing.",
    "보는 동안은 영화 속 소년들의 사춘기처럼 멋대로 정신없고 휘휘몰아쳐갔다.": "While watching, I was swept around wildly, just like the boys' adolescence in the film.",
    "그 폭룡 끝엔 잔잔한 피아노 음악과 무겁게 뭉글거리는 마음이 남아있었다.": "At the end of that storm, quiet piano music and a heavy, swelling feeling remained.",
    "예쁘게 찍느라 연출을 제대로 하지 못했다": "It feels so focused on looking pretty that the direction never quite settles.",
    "인물에 제대로 된 이유가 없고 서사가 잘 흐르지 않는다.": "The characters lack convincing reasons, and the narrative does not flow well.",
    "예쁘게 찍는것에만 집중한 듯한 작품.": "A work that seems focused almost entirely on making pretty images.",
    "아이 배우들의 연기도 서툴고, 감독이 디렉팅을 좀 못한 것 같다.": "The child actors feel awkward too; the direction seems weak.",
    "말을 더듬는 설정에도 ㅇ": "Even the stuttering setup feels unfinished.",
    "시험기간에 보는데 어찌나 재밌는지": "I watched it during exam season, and it was absurdly fun.",
    "나를 울게 만든건 장군이 로봇들을 향해 총을 난사하며 버티던 장면": "The scene that made me cry was the general holding out, firing at the machines.",
    "어찌보면 눈물 포인트로 누군가는 너무 노렸다할지 모르지만": "Some might say it was calculated as an obvious tearjerker, but still.",
    "극 중 황진만이 시는 외우면 이해 돼 라는 말이 기억에 남는다.": "I remember Hwang Jin-man saying that a poem makes sense once you memorize it.",
    "외우면 입 안에서 계속해서 되뇌이다가 어느 날 습관처럼 되뇌였을 때 상황에 적용해서 그 감정과 생각을 이해할 수 있게 되기 때문인걸까": "Maybe because, once memorized, it keeps repeating in your mouth until one day it returns by habit and helps you understand a situation, a feeling, a thought.",
    "그런 진만이 이런 날은 살기 좋은 날": "That Jin-man thinks, 'A day like this is a good day to live.'",
    "이라는 자신이 머릿속으로 떠올린 시구와 함께": "With that line of poetry rising in his mind,",
    "다시 한번 화장실에서 자살을 시도하는 것은": "he attempts suicide again in the bathroom.",
    "마치 따스한 봄철 자살률이 높은 것을 연상시킨다": "It recalls the strange fact that suicide rates rise in warm spring weather.",
    "왜일까.": "Why is that?",
    "새에게 땅콩을 건네는 그런 따스함을 지니고도,": "Even with the tenderness to hand peanuts to a bird,",
    "그런 생명에 대한 애착이 있으면서도 자신을 놓으려 하는 것은.": "even with that attachment to living things, he still tries to let himself go.",
    "아마 진만의 딸 영실을 잃은 것에 대한 죄책감일 것이다.": "Perhaps it is guilt over losing his daughter Young-sil.",
    "이 세상엔 햇빛이 있고, 나눌 땅콩이 있고, 사랑스러운 참새가 있지만 정작 자신이 그토록 아끼고 사랑했던 딸 영실을 허무하게 잃은 것에 대해 존재가치를 못 느끼는 것이겠지. 죄책감을 견디기 어려운 것이겠지.": "There is sunlight in the world, peanuts to share, and a lovely sparrow; yet after losing the daughter he loved so dearly, he cannot feel his own worth. The guilt must be unbearable.",
    "음악도, 눈빛도, 행동도 다 중 2병의 끝판왕이지만, 그들의 휘몰아치는 세계에 함께 빠져서 겪어볼 만하다.": "The music, gazes, and behavior are all peak adolescent melodrama, but it is worth falling into their stormy world with them.",
    "무엇보다도 고마츠 나나가 너무 아름다워서 계속 보게 되고, 배우 캐스팅이 성공적인 영화이다.": "Above all, Nana Komatsu is so beautiful that you keep watching; the casting is a success.",
    "중2병이라고 오글거려하며 보면 끝까지 보기 어렵지만, 그냥 같이 빠져서 봐야하는 영화이다.": "If you watch it while cringing at the melodrama, it is hard to finish; it is a film you have to sink into.",
    "고양이는 실재했을까.": "Did the cat really exist?",
    "버닝 Burning": "Burning",
    "블루 발렌타인 Blue Balentine": "Blue Valentine",
    "위대한 개츠비 The Great Gatsby": "The Great Gatsby",
    "한 줄 감상": "One-line Impression",
    "다음에 참고할 요소": "Elements to Revisit",
    "(개봉연도 / 감독 / 국가 - 선택)": "(Release year / director / country - optional)",
    "(이 영화가 남긴 감정 한 문장)": "(One sentence for the feeling this film left behind)",
    "(연출/촬영/음악/캐릭터 등 한 가지)": "(One element: direction, cinematography, music, character, etc.)",
    "(장면/대사/오브젝트 등 1~2개)": "(One or two scenes, lines, or objects)",
    "(이 영화로 알게 된 내 취향 / 느낀 점)": "(A taste or feeling I discovered through this film)",
    "감독 / 촬영감독 / 배우 / 주제 등": "Director / cinematographer / actor / theme, etc.",
    "2018 / 이창동 / 한국": "2018 / Lee Chang-dong / South Korea",
    "2012 / Derek Cianfrance / 미국": "2012 / Derek Cianfrance / United States",
    "2013 / 바즈 루어만 / 미국, 오스트레일리아": "2013 / Baz Luhrmann / United States, Australia",
    "고양이가 정말 있었는지, 우물은 정말 있었는지, 벤은 정말 비닐하우스를 태웠는지. 그럴듯한 추정을 가능하지만 무엇이 정답일지 누구도 알 수 없다. 정답을 원하는 시대에 이 오묘한, 어쩌면 감독도 정답을 모를 것 같은 이 영화는 매력적이다.": "Was there really a cat, was there really a well, did Ben really burn greenhouses? Plausible guesses are possible, but no one can know the answer. In an age that wants answers, this strange film, whose answer even the director may not know, is magnetic.",
    "아름이 이 영화를 가장 좋아하는 영화로 꼽은 이유는 명확하다. 모호하고, 묘하고, 아리송한 것을 좋아하기 때문이다. 이 영화는 끝까지 명확한 답을 알려주지 않는다. 쉽게 말해 모든 것이 열린 결말인 이 영화는 모호해서 매력적이다.": "The reason Areum names this as her favorite film is clear: she likes things that are ambiguous, odd, and elusive. The film never gives a definite answer. In short, everything remains open, and that ambiguity is what makes it compelling.",
    "민제가 이 영화를 가장 좋아하는 영화로 꼽은 이유는 명확하다. 모호하고, 묘하고, 아리송한 것을 좋아하기 때문이다. 이 영화는 끝까지 명확한 답을 알려주지 않는다. 쉽게 말해 모든 것이 열린 결말인 이 영화는 모호해서 매력적이다.": "The reason Minje names this as his favorite film is clear: he likes things that are ambiguous, odd, and elusive. The film never gives a definite answer. In short, everything remains open, and that ambiguity is what makes it compelling.",
    "인상적인 요소 하나": "One Striking Element",
    "기억에 남는 디테일": "Memorable Details",
    "나와의 연결": "Personal Connection",
    "잘 만든 영화는 예상되지 않는다. 잘 만든 영화는 관찰자가 아닌 그 현장에 있는 사람으로 관객을 끌어들인다. 잘 만든 영화는 마냥 뽐내기만 하지 않는다, 빠져들게 한다.": "A well-made film is not predictable. It pulls the viewer in as someone present in the scene, not merely an observer. A well-made film does not simply show off; it draws you in.",
    "16mm 필름 속 시간들이 무용지물이 되어버린 너와 나.": "You and I, whose time inside 16mm film has become useless.",
    "빛을 너무 아름다운 영화.": "A film whose light is so beautiful.",
    "줄리.": "Julie.",
    "지뢰, 충격적, 사운드!": "Land mines, shock, sound!",
    "난 레이브 파티는 잘 안 맞을 듯. 클럽도 안 맞을 듯..": "Rave parties probably are not for me. Clubs probably are not either.",
    "사랑스럽고도 괴팍한 거짓말과 두 소녀의 변함없는 우정": "A lovely, eccentric lie and the unchanging friendship of two girls.",
}


def norm(value: str) -> str:
    return unicodedata.normalize("NFC", value or "").strip()


def en_value(value: str) -> str:
    value = norm(value)
    if value in TITLE_EN:
        return TITLE_EN[value]
    if value in VALUE_EN:
        return VALUE_EN[value]
    if "분" in value and value.endswith("분"):
        return value.replace("분", " min")
    return value


def en_title(value: str) -> str:
    return TITLE_EN.get(norm(value), norm(value))


def en_note_text(value: str) -> str:
    value = clean_inline(value)
    if value in TITLE_EN:
        return TITLE_EN[value]
    return NOTE_LINE_EN.get(value, en_value(value))


def lang_text(ko: str, en: str | None = None) -> str:
    ko = norm(ko)
    en = norm(en if en is not None else en_value(ko))
    return f'<span data-ko="{html.escape(ko, quote=True)}" data-en="{html.escape(en, quote=True)}">{html.escape(ko)}</span>'


def page_name(index: int) -> str:
    return f"page{index:03d}.html"


def metadata_line(row: dict[str, str]) -> str:
    parts = [norm(row.get(key, "")) for key in ["Director", "Year", "Country", "Genre", "Duration"]]
    return " · ".join(part for part in parts if part)


def list_metadata_line(row: dict[str, str]) -> str:
    parts = [norm(row.get(key, "")) for key in ["Director", "Year", "Genre"]]
    return " · ".join(part for part in parts if part)


def list_metadata_line_en(row: dict[str, str]) -> str:
    parts = [en_value(row.get(key, "")) for key in ["Director", "Year", "Genre"]]
    return " · ".join(part for part in parts if part)


def read_notes() -> dict[str, str]:
    notes: dict[str, str] = {}
    for path in NOTE_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = norm(line[2:])
                break
        if title:
            notes[title] = text
    return notes


def clean_heading(value: str) -> str:
    value = re.sub(r"^[^\w가-힣]+", "", value).strip()
    return clean_inline(value)


def clean_inline(value: str) -> str:
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"^\s*[-+]\s*", "", value)
    value = value.replace("**", "").replace("__", "").replace("*", "").replace("_", "")
    value = value.replace("`", "")
    return value.strip()


def merge_info(row: dict[str, str]) -> dict[str, str]:
    title = norm(row["이름"])
    merged = dict(FILM_INFO.get(title, {}))
    for key, value in row.items():
        if norm(value):
            merged[key] = norm(value)
    merged["이름"] = title
    return merged


def load_posters() -> dict[str, str]:
    if not POSTER_MANIFEST.exists():
        return {}
    data = json.loads(POSTER_MANIFEST.read_text(encoding="utf-8"))
    return {title: poster["file"] for title, poster in data.get("posters", {}).items()}


def note_is_complete(markdown: str) -> bool:
    meaningful: list[str] = []
    for line in markdown.splitlines():
        stripped = clean_inline(re.sub(r"^#{1,6}\s+", "", line.strip()))
        if not stripped:
            continue
        if re.match(r"^[A-Za-z][A-Za-z ]+:", stripped):
            continue
        if stripped.startswith("(") and stripped.endswith(")"):
            continue
        if stripped in {"정보 없음", "아직 작성된 노트가 없습니다."}:
            continue
        meaningful.append(stripped)
    return len(meaningful) > 1


def markdown_to_html(markdown: str, fallback_title: str) -> tuple[str, list[tuple[str, str]], str]:
    title = fallback_title
    meta: list[tuple[str, str]] = []
    blocks: list[tuple[str, list[str]]] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            blocks.append(("paragraph", paragraph_lines))
            paragraph_lines = []

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = norm(stripped[2:])
            continue
        if re.match(r"^#{2,6}\s+", stripped):
            flush_paragraph()
            blocks.append(("heading", [re.sub(r"^#{2,6}\s+", "", stripped)]))
            continue
        match = re.match(r"^([A-Za-z][A-Za-z ]+):\s*(.+)$", stripped)
        if match:
            meta.append((match.group(1), match.group(2)))
            continue
        if not stripped:
            flush_paragraph()
            continue
        paragraph_lines.append(stripped)
    flush_paragraph()

    html_blocks: list[str] = []
    for kind, lines in blocks:
        if kind == "heading":
            text = clean_heading(lines[0])
            if text:
                html_blocks.append(f'<p class="note-heading">{lang_text(text, en_note_text(text))}</p>')
            continue
        cleaned_lines = [lang_text(clean_inline(part), en_note_text(part)) for part in lines if clean_inline(part)]
        if cleaned_lines:
            html_blocks.append(f"<p>{'<br>'.join(cleaned_lines)}</p>")

    if not html_blocks:
        html_blocks.append(f'<p class="empty-note">{lang_text("아직 작성된 노트가 없습니다.", "No note has been written yet.")}</p>')

    return title, meta, "\n".join(html_blocks)


def head(title: str, stylesheet: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" type="text/css" href="{stylesheet}">
    <link rel="stylesheet" type="text/css" href="{stylesheet.rsplit('/', 1)[0]}/reset.css">
    <link rel="icon" type="image/x-icon" href="{ '../' if stylesheet.startswith('../') else '' }srcs/img/favicon.ico">
    <script src="{ '../' if stylesheet.startswith('../') else '' }js/java.js"></script>
    <script src="{ '../' if stylesheet.startswith('../') else '' }js/i18n.js"></script>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha256-3edrmyuQ0w65f8gfBsqowzjJe2iM6n0nKciPUp8y+7E=" crossorigin="anonymous"></script>
    <script>
        (function (d) {{
            var config = {{ kitId: 'cho1mkp', scriptTimeout: 3000, async: true }},
                h = d.documentElement,
                t = setTimeout(function () {{ h.className = h.className.replace(/\\bwf-loading\\b/g, "") + " wf-inactive"; }}, config.scriptTimeout),
                tk = d.createElement("script"),
                f = false,
                s = d.getElementsByTagName("script")[0],
                a;
            h.className += " wf-loading";
            tk.src = 'https://use.typekit.net/' + config.kitId + '.js';
            tk.async = true;
            tk.onload = tk.onreadystatechange = function () {{
                a = this.readyState;
                if (f || a && a != "complete" && a != "loaded") return;
                f = true;
                clearTimeout(t);
                try {{ Typekit.load(config) }} catch (e) {{ }}
            }};
            s.parentNode.insertBefore(tk, s)
        }})(document);
    </script>
</head>"""


def list_links(rows: list[dict[str, str]], prefix: str, notes: dict[str, str]) -> str:
    links = []
    for index, row in enumerate(rows, 1):
        row = merge_info(row)
        title = row["이름"]
        description = list_metadata_line(row) or "정보 없음"
        description_en = list_metadata_line_en(row) or "Unknown"
        complete = note_is_complete(notes.get(title, f"# {title}\n"))
        hover = "완료" if complete else "예정"
        hover_en = "Complete" if complete else "Planned"
        status_class = "list-complete" if complete else "list-upcoming"
        links.append(
            f"""            <a class="{status_class}" href="{prefix}{page_name(index)}">
                <span class="number">{index:02d}</span>
                <span class="title">{lang_text(title, en_title(title))}</span>
                <span class="description" data-hover="{html.escape(hover)}" data-hover-ko="{html.escape(hover, quote=True)}" data-hover-en="{html.escape(hover_en, quote=True)}" data-ko="{html.escape(description, quote=True)}" data-en="{html.escape(description_en, quote=True)}">{html.escape(description)}</span>
            </a>"""
        )
    return "\n".join(links)


def lang_toggle() -> str:
    return """            <div class="lang-toggle" aria-label="Language">
                <button type="button" data-lang="ko" aria-pressed="true">KR</button>
                <button type="button" data-lang="en" aria-pressed="false">EN</button>
            </div>"""


def render_index(rows: list[dict[str, str]], notes: dict[str, str]) -> str:
    return f"""{head("필름노트", "css/style.css")}

<body>
    <div id="wrap">
        <div class="header">
            <h1 class="maintitle" id="box">{lang_text("필름노트", "filmnote")}</h1>
{lang_toggle()}
            <script src="js/scrollscript.js"></script>
        </div>
        <div class="dscr-container">
            <div class="dsc film-intro" id="dsc">
                <h3 class="dscrkr">
                    {lang_text("필름노트는 이아름이 영화를 보고 남긴 개인적인 분석 노트의 아카이브다. 감상과 장면, 인물의 움직임, 이미지가 남긴 잔상을 한 편씩 기록한다.", "filmnote is a personal archive of film analysis notes by Lee Areum. It records impressions, scenes, character movement, and the afterimages each film leaves behind.")}
                    <p class="indent">{lang_text("완성된 리뷰보다 다시 돌아갈 수 있는 메모에 가깝다. 영화가 남긴 질문과 생각들이 이곳에 쌓이고, 서로 다른 작품 사이의 작은 연결을 만든다.", "Rather than finished reviews, these entries are notes to revisit. The questions and thoughts left by each film gather here and form small connections between different works.")}</p>
                </h3>
                <h3 class="dscren">
                    {lang_text("영화의 세부 정보와 포스터, 작성된 노트와 앞으로 작성할 목록을 함께 보관한다.", "It keeps film details, posters, completed notes, and the list of notes still to be written.")}
                    <p class="indent">{lang_text("목록의 회색 정보는 감독, 연도, 장르를 보여주고, 마우스를 올리면 노트의 완료 여부를 확인할 수 있다.", "The gray line in the list shows director, year, and genre; hovering reveals whether the note is complete or planned.")}</p>
                </h3>
                <span class="date">{lang_text("필름노트", "filmnote")}<br>{lang_text("이 아름", "Lee Areum")}</span>
            </div>
        </div>
        <div class="list">
{list_links(rows, "html/", notes)}
        </div>
        <footer>
            <p>&copy; 2026 {lang_text("이아름", "Lee Areum")}.</p>
        </footer>
    </div>
</body>

</html>
"""


def render_page(rows: list[dict[str, str]], row: dict[str, str], index: int, note: str, notes: dict[str, str], posters: dict[str, str]) -> str:
    row = merge_info(row)
    title = row["이름"]
    note_title, note_meta, note_body = markdown_to_html(note, title)
    csv_meta = [(key, norm(row.get(key, ""))) for key in ["Director", "Year", "Country", "Genre", "Duration", "Rating", "Theme"] if norm(row.get(key, ""))]
    combined_meta = csv_meta[:]
    used_keys = {key for key, _ in csv_meta}
    for key, value in note_meta:
        normalized_value = norm(value)
        if normalized_value and key not in used_keys:
            combined_meta.append((key, normalized_value))
            used_keys.add(key)
    meta_html = "\n".join(
        f"""                        <p><span>{html.escape(key)}</span>{lang_text(value, en_value(value))}</p>"""
        for key, value in combined_meta
    )
    if not meta_html:
        meta_html = f'                        <p><span>Note</span>{lang_text("필름 로그에서 가져온 항목", "Imported from the film log")}</p>'
    poster = posters.get(title, "")
    poster_html = (
        f"""                <img class="film-poster" src="../{html.escape(poster)}" alt="{html.escape(title)} poster">"""
        if poster
        else ""
    )

    prev_button = f"""            <button id="prevPageBtn" onclick="location.href='{page_name(index - 1)}'">←</button>""" if index > 1 else ""
    next_button = f"""            <button id="nextPageBtn" onclick="location.href='{page_name(index + 1)}'">→</button>""" if index < len(rows) else ""

    return f"""{head(f"{note_title} - 필름노트", "../css/style_others.css")}

<body>
    <div id="wrap">
        <div class="header">
{prev_button}
            <a href="../index.html">
                <h1 class="maintitle" id="box">{lang_text("필름노트", "filmnote")}</h1>
            </a>
{lang_toggle()}
            <script src="../js/scrollscript_others.js"></script>
{next_button}
        </div>
        <div class="dscr-container">
            <div class="dsc film-detail" id="dsc">
                <div class="dsc-txt film-meta">
                    <p class="film-kicker">filmnote {index:03d}</p>
                    <h2>{lang_text(note_title, en_title(note_title))}</h2>
                    <div class="film-meta-list">
{meta_html}
                    </div>
                </div>
{poster_html}
            </div>
        </div>
        <main class="film-note-container">
            <article class="film-note">
{note_body}
            </article>
        </main>
        <div class="list">
{list_links(rows, "", notes)}
        </div>
        <footer>
            <p>&copy; 2026 {lang_text("이아름", "Lee Areum")}.</p>
        </footer>
    </div>
</body>

</html>
"""


def main() -> None:
    with DATA_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = [{key: norm(value) for key, value in row.items()} for row in csv.DictReader(handle)]

    notes = read_notes()
    posters = load_posters()
    HTML_DIR.mkdir(exist_ok=True)

    (ROOT / "index.html").write_text(render_index(rows, notes), encoding="utf-8")

    for index, row in enumerate(rows, 1):
        title = norm(row["이름"])
        note = notes.get(title, f"# {title}\n")
        (HTML_DIR / page_name(index)).write_text(render_page(rows, row, index, note, notes, posters), encoding="utf-8")

    for path in HTML_DIR.glob("page*.html"):
        match = re.fullmatch(r"page(\d{3})\.html", path.name)
        if match and int(match.group(1)) > len(rows):
            path.unlink()


if __name__ == "__main__":
    main()
