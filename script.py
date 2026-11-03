#!/usr/bin/env python3
import argparse
import datetime
import json
import logging
import sys
import urllib.request
import urllib.error

# CẤU HÌNH KẾT NỐI SUPABASE CHÍNH THỨC
SUPABASE_URL = "https://bmkpedahdtfeypetpvdo.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_zgzSQB_-KYmSDjloOX_HMA_7Yg9g9k4"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.endpoint = f"{url.rstrip('/')}/rest/v1/sop_master_matches"
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=representation"
        }

    def upsert(self, data: list):
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(data).encode("utf-8"),
            headers=self.headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                logging.info(f"✅ Upsert thành công {len(result)} trận đấu vào Supabase!")
                return result
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            logging.error(f"❌ Lỗi Supabase HTTP {e.code}: {err_body}")
            return None
        except Exception as e:
            logging.error(f"❌ Lỗi kết nối Supabase: {e}")
            return None

def generate_sample_fixtures():
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return [
        {
            "match_id": "20261102_EPL_Arsenal_ManCity",
            "stt_tran": 1,
            "giai_dau": "Ngoại Hạng Anh (Premier League)",
            "tran_dau": "Arsenal vs Man City",
            "gio_thi_dau_gmt7": "22:00 (GMT+7)",
            "handicap_opening": -0.25,
            "odds_home_opening": 1.95,
            "odds_away_opening": 1.95,
            "overunder_opening": 2.75,
            "odds_over_opening": 1.90,
            "odds_under_opening": 1.90,
            "xg_home_baseline": 1.85,
            "xg_away_baseline": 1.32,
            "poisson_home_win_prob": 45.2,
            "poisson_draw_prob": 26.8,
            "poisson_away_win_prob": 28.0,
            "handicap_current_t3h": -0.25,
            "overunder_current_t3h": 2.75,
            "smart_money_signal": "Dòng tiền thông minh vào Arsenal -0.25",
            "trap_odds_warning": "Không",
            "official_lineup_check": True,
            "tier1_market_code": "Arsenal -0.25",
            "tier2_market_code": "Tài 2.75 bàn",
            "risk_level_label": "LOW_RISK",
            "ft_score_actual": "2 - 1 (HT 1-0)",
            "tier1_result_pnl": 42.75,
            "tier2_result_pnl": 33.25
        },
        {
            "match_id": "20261102_LALIGA_RealMadrid_Barcelona",
            "stt_tran": 2,
            "giai_dau": "La Liga",
            "tran_dau": "Real Madrid vs Barcelona",
            "gio_thi_dau_gmt7": "22:15 (GMT+7)",
            "handicap_opening": -0.50,
            "odds_home_opening": 2.02,
            "odds_away_opening": 1.88,
            "overunder_opening": 3.00,
            "odds_over_opening": 1.90,
            "odds_under_opening": 1.90,
            "xg_home_baseline": 2.10,
            "xg_away_baseline": 1.60,
            "poisson_home_win_prob": 48.0,
            "poisson_draw_prob": 24.0,
            "poisson_away_win_prob": 28.0,
            "handicap_current_t3h": -0.50,
            "overunder_current_t3h": 3.00,
            "smart_money_signal": "Không",
            "trap_odds_warning": "Có BẪY Odds tài xỉu",
            "official_lineup_check": True,
            "tier1_market_code": "Real Madrid -0.5",
            "tier2_market_code": "Tài 3.0 bàn",
            "risk_level_label": "HIGH_RISK",
            "ft_score_actual": "3 - 2 (HT 1-1)",
            "tier1_result_pnl": 45.90,
            "tier2_result_pnl": 31.50
        }
    ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=SUPABASE_URL)
    parser.add_argument("--key", default=SUPABASE_ANON_KEY)
    parser.add_argument("--push-sample", action="store_true")
    args = parser.parse_args()
    
    client = SupabaseClient(args.url, args.key)
    fixtures = generate_sample_fixtures()
    client.upsert(fixtures)

if __name__ == "__main__":
    main()
