import json
import re
import unicodedata
import ollama


# ============================================================
# CONFIG
# ============================================================

MODEL = "qwen3:1.7b"

REVIEWS_PER_RATING = 20
BATCH_SIZE = 5


# ============================================================
# CÁC PREFIX DÙNG ĐỂ TẠO 20 CÂU NỀN KHÁC NHAU
# ============================================================

PREFIXES = [
    "",
    "Nhìn chung, ",
    "Theo cảm nhận của tôi, ",
    "Với trải nghiệm này, ",
    "Ở góc độ người dùng, "
]


# ============================================================
# CÂU NỀN AN TOÀN
# 4 câu × 5 prefix = 20 câu / rating
# ============================================================

CORE_REVIEWS = {

    1: [
        "tôi rất thất vọng vì sản phẩm không đáp ứng được kỳ vọng.",
        "trải nghiệm với sản phẩm rất tệ và tôi hoàn toàn không hài lòng.",
        "sản phẩm không đạt mong đợi và khiến tôi cảm thấy rất thất vọng.",
        "chất lượng cảm nhận chưa đạt yêu cầu và trải nghiệm tổng thể rất tiêu cực."
    ],

    2: [
        "tôi chưa hài lòng vì sản phẩm vẫn còn nhiều điểm cần cải thiện.",
        "sản phẩm chưa đáp ứng tốt kỳ vọng và trải nghiệm còn khá hạn chế.",
        "trải nghiệm chưa tốt và sản phẩm cần cải thiện thêm để đáp ứng mong đợi.",
        "sản phẩm vẫn dùng được nhưng chưa khiến tôi cảm thấy hài lòng."
    ],

    3: [
        "sản phẩm dùng được, không quá tốt nhưng cũng không quá tệ.",
        "trải nghiệm ở mức bình thường và không có gì quá nổi bật.",
        "sản phẩm đáp ứng nhu cầu cơ bản nhưng chưa tạo được nhiều ấn tượng.",
        "sản phẩm ở mức trung bình và nhìn chung vẫn có thể chấp nhận được."
    ],

    4: [
        "tôi hài lòng vì sản phẩm nhìn chung đáp ứng tốt mong đợi.",
        "trải nghiệm khá tích cực và sản phẩm đáp ứng tốt nhu cầu của tôi.",
        "sản phẩm hoạt động ổn và mang lại trải nghiệm khá tốt.",
        "tôi có trải nghiệm tích cực và nhìn chung hài lòng với sản phẩm."
    ],

    5: [
        "tôi rất hài lòng vì sản phẩm đáp ứng rất tốt mong đợi của mình.",
        "trải nghiệm với sản phẩm rất tích cực và khiến tôi hoàn toàn hài lòng.",
        "sản phẩm đáp ứng rất tốt nhu cầu và mang lại trải nghiệm tuyệt vời.",
        "tôi rất hài lòng với chất lượng cảm nhận và trải nghiệm tổng thể."
    ]
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    text = text.lower()

    text = unicodedata.normalize(
        "NFD",
        text
    )

    return "".join(
        c
        for c in text
        if unicodedata.category(c) != "Mn"
    )


# ============================================================
# NHỮNG CHỦ ĐỀ OLLAMA KHÔNG ĐƯỢC TỰ BỊA
# ============================================================

FORBIDDEN = [
    "giao hang",
    "ship",
    "dich vu",
    "ho tro",
    "phuc vu",
    "hau mai",

    "gia",
    "bao hanh",

    "thiet ke",
    "mau sac",
    "chat lieu",
    "kich thuoc",
    "size",

    "mui",
    "bao bi",
    "dong goi",

    "thanh toan",
    "hoa don",

    "model",
    "tinh nang",
    "cong nang",
    "do ben"
]


# ============================================================
# KIỂM TRA SENTIMENT
# ============================================================

def valid_sentiment(review, rating):

    text = normalize_text(review)

    negative = [
        "that vong",
        "khong hai long",
        "khong tot",
        "khong dap ung",
        "chua dap ung",
        "tieu cuc",
        "chua tot",
        "han che"
    ]

    neutral = [
        "binh thuong",
        "dung duoc",
        "trung binh",
        "chap nhan",
        "khong qua tot",
        "khong qua te",
        "nhu cau co ban"
    ]

    positive = [
        "hai long",
        "tich cuc",
        "kha tot",
        "dap ung tot",
        "hoat dong on",
        "trai nghiem tot"
    ]

    strong_positive = [
        "rat hai long",
        "hoan toan hai long",
        "tuyet voi",
        "rat tich cuc",
        "dap ung rat tot"
    ]

    if rating == 1:
        return any(
            x in text
            for x in negative
        )

    if rating == 2:
        return any(
            x in text
            for x in negative
        )

    if rating == 3:
        return any(
            x in text
            for x in neutral
        )

    if rating == 4:
        return any(
            x in text
            for x in positive
        )

    if rating == 5:
        return any(
            x in text
            for x in strong_positive
        )

    return False


# ============================================================
# VALIDATE REVIEW DO OLLAMA SINH
# ============================================================

def is_valid_review(review, rating):

    if not isinstance(review, str):
        return False

    review = review.strip()

    if not review:
        return False

    word_count = len(
        review.split()
    )

    if word_count < 6 or word_count > 28:
        return False

    normalized = normalize_text(
        review
    )

    # Không cho số sao/rating
    if re.search(
        r"\b[1-5]\s*(sao|star)\b",
        normalized
    ):
        return False

    if re.search(
        r"\b[1-5]/5\b",
        normalized
    ):
        return False

    # Không cho chi tiết bị bịa
    for phrase in FORBIDDEN:

        if phrase in normalized:
            return False

    # Sentiment phải đúng rating
    if not valid_sentiment(
        review,
        rating
    ):
        return False

    return True


# ============================================================
# TẠO 20 CÂU NỀN CHO MỖI RATING
# ============================================================

def build_base_reviews(rating):

    reviews = []

    for prefix in PREFIXES:

        for core in CORE_REVIEWS[rating]:

            sentence = (
                prefix + core
            )

            # Viết hoa chữ đầu
            sentence = (
                sentence[0].upper()
                + sentence[1:]
            )

            reviews.append(
                sentence
            )

    assert len(reviews) == 20

    return reviews


# ============================================================
# OLLAMA PARAPHRASE 5 CÂU MỘT LẦN
# ============================================================

def paraphrase_batch(
    reviews,
    rating
):

    numbered_reviews = "\n".join(
        f"{i + 1}. {review}"
        for i, review
        in enumerate(reviews)
    )

    prompt = f"""
Bạn đang hỗ trợ tạo dữ liệu Customer Review giả lập
cho một dự án phân tích dữ liệu.

Dưới đây là {len(reviews)} câu review có Rating {rating}/5.

Hãy VIẾT LẠI từng câu bằng cách diễn đạt khác,
nhưng phải giữ nguyên ý nghĩa và mức độ hài lòng.

Các câu gốc:

{numbered_reviews}

Yêu cầu bắt buộc:

- Trả về đúng {len(reviews)} review.
- Giữ nguyên thứ tự tương ứng với câu gốc.
- Mỗi review chỉ gồm một câu.
- Văn phong tự nhiên bằng tiếng Việt.
- Không thêm thông tin mới.
- Không nhắc số sao hoặc rating.

TUYỆT ĐỐI KHÔNG tự thêm:

- giao hàng
- dịch vụ
- hỗ trợ
- giá cả
- bảo hành
- thiết kế
- màu sắc
- chất liệu
- kích thước
- tính năng
- thời gian sử dụng
- bao bì
- thanh toán

Chỉ trả JSON:

{{
    "reviews": [
        "review 1",
        "review 2"
    ]
}}

Không markdown.
Không giải thích.
"""

    try:

        response = ollama.chat(

            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            format="json",

            think=False,

            options={
                "temperature": 0.7
            }
        )

        data = json.loads(
            response["message"]["content"]
        )

        result = data.get(
            "reviews",
            []
        )

        if not isinstance(
            result,
            list
        ):
            return []

        return result

    except Exception:

        return []


# ============================================================
# TẠO REVIEW BANK CHO 1 RATING
# ============================================================

def generate_reviews(rating):

    base_reviews = build_base_reviews(
        rating
    )

    final_reviews = []

    for start in range(
        0,
        REVIEWS_PER_RATING,
        BATCH_SIZE
    ):

        batch = base_reviews[
            start:start + BATCH_SIZE
        ]

        generated = paraphrase_batch(
            batch,
            rating
        )

        for i, base_review in enumerate(batch):

            # Mặc định dùng câu nền
            selected = base_review

            # Nếu Ollama có sinh câu tương ứng
            if i < len(generated):

                candidate = (
                    generated[i]
                    .strip()
                )

                # Chỉ dùng output của Ollama
                # khi vượt validation
                if is_valid_review(
                    candidate,
                    rating
                ):
                    selected = candidate

            # Nếu bị duplicate
            # thì quay lại dùng câu nền
            existing = {
                normalize_text(x)
                for x in final_reviews
            }

            if (
                normalize_text(selected)
                in existing
            ):
                selected = base_review

            final_reviews.append(
                selected
            )

        print(
            f"Rating {rating}: "
            f"{len(final_reviews)}/20"
        )

    assert len(final_reviews) == 20

    return final_reviews


# ============================================================
# MAIN
# ============================================================

review_bank = {}

for rating in range(
    1,
    6
):

    print(
        f"\nĐang tạo Rating {rating}..."
    )

    reviews = generate_reviews(
        rating
    )

    review_bank[rating] = reviews

    print(
        f"\n=== RATING {rating} ==="
    )

    for review in reviews:
        print(review)


# ============================================================
# FINAL VALIDATION
# ============================================================

for rating, reviews in review_bank.items():

    if len(reviews) != 20:
        raise RuntimeError(
            f"Rating {rating} không đủ 20 review"
        )

    normalized = [
        normalize_text(x)
        for x in reviews
    ]

    if len(set(normalized)) != 20:

        raise RuntimeError(
            f"Rating {rating} có duplicate"
        )


total_reviews = sum(
    len(x)
    for x in review_bank.values()
)

if total_reviews != 100:

    raise RuntimeError(
        f"Tổng review sai: {total_reviews}"
    )


# ============================================================
# SAVE
# ============================================================

with open(
    "data/processed/review_bank.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        review_bank,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\n================================")
print("REVIEW BANK VALIDATION PASSED")
print(f"Tổng số review: {total_reviews}")
print(
    "Đã lưu: "
    "data/processed/review_bank.json"
)
print("================================")