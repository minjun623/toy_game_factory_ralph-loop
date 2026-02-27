"""
게임 아이디어 시드 생성기
난수를 생성하여 Claude가 창의적으로 해석할 수 있는 시드를 제공한다.
"""

import random
import string
import json
from datetime import datetime


def generate_seed():
    """랜덤 시드 문자열 생성"""
    length = random.randint(8, 16)
    chars = string.ascii_lowercase + string.digits
    seed = ''.join(random.choice(chars) for _ in range(length))
    return seed


def generate_game_constraints():
    """게임에 적용할 랜덤 제약 조건 생성"""

    genres = [
        "아케이드", "퍼즐", "리듬", "슈팅", "플랫포머",
        "레이싱", "타워디펜스", "카드", "두뇌", "반응속도",
        "물리엔진", "생존", "수집", "탈출", "타이핑"
    ]

    themes = [
        "우주", "바다", "숲", "도시", "사막",
        "눈", "화산", "하늘", "지하", "미래",
        "고대", "음식", "음악", "수학", "동물"
    ]

    mechanics = [
        "클릭/탭으로 조작", "방향키로 이동", "마우스로 조준",
        "타이밍 맞추기", "패턴 기억하기", "빠른 반응",
        "자원 관리", "경로 찾기", "쌓기/배치", "회피하기",
        "매칭하기", "연쇄 반응", "중력 활용", "스와이프"
    ]

    difficulty_curves = [
        "시간이 갈수록 속도 증가",
        "레벨마다 새로운 장애물 추가",
        "점수가 높을수록 난이도 상승",
        "제한 시간이 점점 짧아짐",
        "적의 수가 점점 늘어남"
    ]

    visual_styles = [
        "미니멀 (단색 도형)",
        "레트로 픽셀 아트 스타일",
        "네온 글로우 스타일",
        "손그림 스케치 스타일",
        "이모지 기반"
    ]

    result = {
        "seed": generate_seed(),
        "genre": random.choice(genres),
        "theme": random.choice(themes),
        "primary_mechanic": random.choice(mechanics),
        "secondary_mechanic": random.choice(mechanics),
        "difficulty_curve": random.choice(difficulty_curves),
        "visual_style": random.choice(visual_styles),
        "generated_at": datetime.now().isoformat()
    }

    # secondary가 primary랑 같으면 다시 뽑기
    while result["secondary_mechanic"] == result["primary_mechanic"]:
        result["secondary_mechanic"] = random.choice(mechanics)

    return result


if __name__ == "__main__":
    constraints = generate_game_constraints()
    print(json.dumps(constraints, ensure_ascii=False, indent=2))