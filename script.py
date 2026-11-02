import os
import requests

SUPABASE_URL = "https://rzwpwpnpfqnkostbhzaj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6d3B3cG5wZnFua29zdGJoemFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM2MTA3OTMsImV4cCI6MjEwOTE4Njc5M30.edTZaTAxHd1iDWSL0s7M1ypOixIrimRmaYPcoQKb8wc"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

sample_matches = [
    {
        "match_id": "match-001",
        "giai_dau": "Ngoại Hạng Anh",
        "tran_dau": "Arsenal vs Man City",
        "gio_thi_dau_gmt7": "22:00 (GMT+7)",
        "handicap_opening": -0.25,
        "overunder_opening": 2.75,
        "xg_home_baseline": 1.85,
        "xg_away_baseline": 1.32,
        "poisson_home_win_prob": 45.2,
        "poisson_draw_prob": 26.8,
        "poisson_away_win_prob": 28.0,
        "smart_money_signal": "Dòng tiền thông minh vào Arsenal -0.25",
        "trap_odds_warning": "Không có bẫy Odds",
        "official_lineup_check": True,
        "risk_level_label": "HIGH",
        "ft_score_actual": "2 - 1",
        "tier1_result_pnl": 42.75
    },
    {
        "match_id": "match-002",
        "giai_dau": "La Liga",
        "tran_dau": "Real Madrid vs Barcelona",
        "gio_thi_dau_gmt7": "22:15 (GMT+7)",
        "handicap_opening": -0.50,
        "overunder_opening": 3.00,
        "xg_home_baseline": 2.10,
        "xg_away_baseline": 1.60,
        "poisson_home_win_prob": 48.0,
        "poisson_draw_prob": 24.0,
        "poisson_away_win_prob": 28.0,
        "smart_money_signal": "Dòng tiền đè cửa Real Madrid",
        "trap_odds_warning": "Có bẫy Odds tài xỉu",
        "official_lineup_check": True,
        "risk_level_label": "HIGH",
        "ft_score_actual": "3 - 2",
        "tier1_result_pnl": 45.00
    }
]

url = f"{SUPABASE_URL}/rest/v1/sop_master_matches"
res = requests.post(url, headers=headers, json=sample_matches)

if res.status_code in [200, 201]:
    print("✅ Cập nhật Supabase tự động thành công!")
else:
    print(f"❌ Lỗi: {res.status_code} - {res.text}")
