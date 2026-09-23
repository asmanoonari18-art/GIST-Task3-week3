import pandas as pd
from app.services import analyze_csv, clean_csv, validate_csv

def test_validate_csv():
    validate_csv("students.csv")

def test_reject_non_csv():
    try:
        validate_csv("students.xlsx")
        assert False
    except ValueError:
        assert True

def test_analyze_csv():
    content = b"Name,Score\nAli,80\nSara,90\n"
    profile = analyze_csv(content)
    assert profile["shape"]["rows"] == 2
    assert profile["shape"]["columns"] == 2
    assert profile["missing_by_column"]["Score"] == 0

def test_clean_csv_removes_duplicates_and_missing_values():
    content = b"Name,Score\nAli,80\nAli,80\nSara,\n"
    cleaned, report = clean_csv(content)
    df = pd.read_csv(__import__("io").BytesIO(cleaned))
    assert report["duplicates_removed"] == 1
    assert len(df) == 2
    assert int(df["Score"].isna().sum()) == 0
