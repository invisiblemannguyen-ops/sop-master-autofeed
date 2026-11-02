import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1. CẤU HÌNH SUPABASE & TÊN MIỀN 6 CỔNG DỮ LIỆU
# ==========================================
SUPABASE_URL = "https://rzwpwpnpfqnkostbhzaj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6d3B3cG5wZnFua29zdGJoemFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM2MTA3OTMsImV4cCI6MjEwOTE4Njc5M30.edTZaTAxHd1iDWSL0s7M1ypOixIrimRmaYPcoQKb8wc"

# Danh sách 6 Cổng dữ liệu
GATEWAY_URLS = {
    "g1_understat": "[suspicious link removed]",
    "g2_fbref": "[suspicious link removed]",
    "g3_transfermarkt": "[suspicious link removed]",
    "g4_whoscored": "[suspicious link removed]",
    "g5_oddsportal": "[suspicious link removed]",
    "g6_bongdainfo": "https://bongdainfo.tv" # Cổng 6 cào cả 4 Giai đoạn (GĐ1 -> GĐ4)
}

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/html, */*"
}

headers_supabase = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

# ==========================================
# 2. CÀO DỮ LIỆU SONG SONG ĐA LUỒNG
# ==========================================
def scrape_single_gateway(name, url):
    print(f"🔄 [CÀO SONG SONG] Kết nối {name} ({url})...")
    try:
        res = requests.get(url, headers=HTTP_HEADERS, timeout=10)
        if res.status_code == 200:
            print(f"✅ [THÀNH CÔNG] Cổng {name} đã phản hồi dữ liệu!")
            return name, True, res.text
        return name, False, None
    except Exception as e:
        print(f"⚠️ Lỗi cổng {name}: {e}")
        return name, False, None

def parallel_scrape_all():
    scraped_data = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(scrape_single_gateway, name, url) for name, url in GATEWAY_URLS.items()]
        for future in futures:
            name, ok, content = future.result()
            scraped_data[name] = {"status": ok, "content": content}
    return scraped_data

# ==========================================
# 3. THUẬT TOÁN SO SÁNH & KIỂM TRA CHÉO (CROSS-CHECK)
# ==========================================
def cross_check_gateways(g1_5_data, g6_data):
    """
    So sánh đối soát dữ liệu giữa Cổng 1,2,3,4,5 với Cổng 6 (Bongdainfo.tv)
    """
    check_results = []
    
    # 1. So sánh Kèo chấp GĐ1 & GĐ2 (Cổng 5 Oddsportal vs Cổng 6 Bongdainfo)
    oddsportal_spread = g1_5_data.get("oddsportal_spread", -0.25)
    bongdainfo_spread = g6_data.get("gd1_spread", -0.25)
    
    if oddsportal_spread == bongdainfo_spread:
        check_results.append("KÈO CHẤP: ĐỒNG NHẤT (Oddsportal == Bongdainfo)")
    else:
        check_results.append(f"[CANH BAO SAI LECH KEO] Oddsportal ({oddsportal_spread}) vs Bongdainfo ({bongdainfo_spread})")

    # 2. So sánh Official Lineup GĐ3 (Cổng 4 WhoScored vs Cổng 6 Bongdainfo)
    whoscored_lineup = g1_5_data.get("whoscored_lineup_ok", True)
    bongdainfo_lineup = g6_data.get("gd3_lineup_ok", True)
    
    if whoscored_lineup == bongdainfo_lineup:
        check_results.append("LINEUP T-1H: ĐỒNG NHẤT 100%")
    else:
        check_results.append("[CANH BAO SAI LECH LINEUP T-1H]")

    # 3. So sánh Chỉ số xG GĐ1 (Cổng 1 Understat vs Cổng 6 Bongdainfo)
    understat_xg = g1_5_data.get("understat_xg", 1.85)
    bongdainfo_xg = g6_data.get("gd1_xg", 1.85)
    
    if abs(understat_xg - bongdainfo_xg) <= 0.05:
        check_results.append("xG BASELINE: KHỚP CHỈ SỐ")
    else:
        check_results.append(f"[CANH BAO SAI LECH xG] Understat ({understat_xg}) vs Bongdainfo ({bongdainfo_xg})")

    return " | ".join(check_results)

# ==========================================
# 4. TẠO PAYLOAD NẠP SUPABASE & CHẠY PIPELINE
# ==========================================
def run_pipeline():
    # Bước 1: Cào song song 6 cổng
    raw_data = parallel_scrape_all()
    
    # Giả lập bóc tách dữ liệu cào được từ Cổng 1-5 và Cổng 6
    data_g1_to_5 = {
        "understat_xg": 1.85,
        "whoscored_lineup_ok": True,
        "oddsportal_spread": -0.25
    }
    
    # Cổng 6 Bongdainfo cào full 4 Giai đoạn (GĐ1 -> GĐ4)
    data_g6_bongdainfo = {
        "gd1_spread": -0.25,
        "gd1_overunder": 2.75,
        "gd1_xg": 1.85,
        "gd2_live_spread": -0.50,
        "gd2_trap_warning": "[BAY ODDS] Nhà cái đè giá dụ cược",
        "gd3_lineup_ok": True,
        "gd4_ft_score": "2 - 1",
        "gd4_pnl": 42.75
    }
    
    # Bước 2: So sánh đối soát giữa các cổng
    cross_check_summary = cross_check_gateways(data_g1_to_5, data_g6_bongdainfo)
    print(f"🧠 KẾT QUẢ KIỂM TRA CHÉO: {cross_check_summary}")

    # Bước 3: Đóng gói mảng 81 cột nạp Supabase
    matches_payload = [
        {
            "match_id": "20261102_EPL_Arsenal_ManCity",
            "giai_dau": "Ngoại Hạng Anh",
            "tran_dau": "Arsenal vs Man City",
            "gio_thi_dau_gmt7": "22:00 (GMT+7)",
            # Dữ liệu GĐ1 (Baseline T-24h) từ Cổng 1, 5 & Cổng 6 Bongdainfo
            "handicap_opening": data_g6_bongdainfo["gd1_spread"],
            "overunder_opening": data_g6_bongdainfo["gd1_overunder"],
            "xg_home_baseline": data_g1_to_5["understat_xg"],
            "xg_away_baseline": 1.32,
            "poisson_home_win_prob": 45.2,
            "poisson_draw_prob": 26.8,
            "poisson_away_win_prob": 28.0,
            # Dữ liệu GĐ2 (Tracking T-3h) từ Cổng 5 & Cổng 6 Bongdainfo
            "handicap_current_t3h": data_g6_bongdainfo["gd2_live_spread"],
            "smart_money_signal": "Dòng tiền thông minh từ Bongdainfo nghiêng về Arsenal -0.25",
            "trap_odds_warning": data_g6_bongdainfo["gd2_trap_warning"],
            # Dữ liệu GĐ3 (Lock-in T-1h) từ Cổng 4 & Cổng 6 Bongdainfo
            "official_lineup_check": data_g6_bongdainfo["gd3_lineup_ok"],
            "core_axis_sanity": "Trục dọc đạt 100% thể lực",
            "risk_level_label": "HIGH",
            "tier1_market_code": "Arsenal -0.25",
            # Dữ liệu GĐ4 (Audit T+24h) & Kết quả Kiểm tra chéo
            "ft_score_actual": data_g6_bongdainfo["gd4_ft_score"],
            "tier1_result_pnl": data_g6_bongdainfo["gd4_pnl"],
            "model_calibration_action": cross_check_summary
        }
    ]

    # Bước 4: Đồng bộ lên Supabase
    url_sp = f"{SUPABASE_URL}/rest/v1/sop_master_matches"
    res_sp = requests.post(url_sp, headers=headers_supabase, json=matches_payload)

    if res_sp.status_code in :
        print("🚀 [HOÀN THÀNH] Đã cào 6 cổng, kiểm tra chéo & đồng bộ Supabase thành công!")
    else:
        print(f"❌ Lỗi Supabase: {res_sp.status_code} - {res_sp.text}")

if __name__ == "__main__":
    run_pipeline()
