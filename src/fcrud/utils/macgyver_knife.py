def sort_and_extract(data: list[dict], order: str = "ASC", sort="id", start=0, end=10) -> list[dict]:
    """
    JSON 데이터를 정렬하고 특정 인덱스의 항목을 추출합니다.

    Args:
    data: 정렬할 JSON 데이터 (List[dict])
    order: 정렬 순서 (DESC, ASC)
    sort: 정렬 기준
    start: 추출 시작
    end : 추출 끝

    Returns:
    정렬된 데이터의 특정 인덱스의 항목 (List[dict])
    """

    # 정렬
    sorted_data = sorted(
        data, key=lambda item: item[sort], reverse=(order == "DESC"))

    # 추출
    extracted_data = sorted_data[start:end]

    return extracted_data
