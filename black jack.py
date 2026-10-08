# Python + Streamlit
import streamlit as st
import random

# 初期化
if 'player_cards' not in st.session_state:
    st.session_state.player_cards = []
if 'dealer_cards' not in st.session_state:
    st.session_state.dealer_cards = []
if 'player_total' not in st.session_state:
    st.session_state.player_total = 0
if 'dealer_total' not in st.session_state:
    st.session_state.dealer_total = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
st.session_rule = 0

# カードを引く関数（Aは1または11）
def deal_card(hand):
    card = random.choice(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
    hand.append(card)
    return hand

# 手札の合計を計算
def calculate_total(hand):
    total = 0
    aces = 0
    for card in hand:
        if card in ['J','Q','K']:
            total += 10
        elif card == 'A':
            aces += 1
            total += 11
        else:
            total += int(card)
    while total > 21 and aces > 0:
        total -= 10  # Aを1として使用
        aces -= 1
    return total

# ヒット処理
def player_hit():
    if not st.session_state.game_over:
        deal_card(st.session_state.player_cards)
        st.session_state.player_total = calculate_total(st.session_state.player_cards)
        if st.session_state.player_total > 21:  # バースト判定
            st.session_state.game_over = True

# スタンド（ディーラーのターン開始）
def stand():
    st.session_state.game_over = True
    # ディーラーが17以上になるまでカードを引く
    while st.session_state.dealer_total < 17:
        deal_card(st.session_state.dealer_cards)
        st.session_state.dealer_total = calculate_total(st.session_state.dealer_cards)

# リセット処理
def reset_game():
    st.session_state.player_cards = []
    st.session_state.dealer_cards = []
    st.session_state.player_total = 0
    st.session_state.dealer_total = 0
    st.session_state.game_over = False
    # 初期手札1枚ずつ配る
    player_hit()
    deal_card(st.session_state.dealer_cards)

#ルール
def rule():
    st.write("「一枚引く」を選択してカードを引く")
    st.write("21に近づける ピッタリを目指そう")
    st.write("「勝負」を押して相手よりも21に近かったら勝利")
# ゲーム開始時の初期手札
if st.session_state.player_total == 0 and not st.session_state.game_over:
    reset_game()

# タイトル表示
st.title("ブラックジャック")
st.write("21を超えず、なるべく近い値にしよう")
# プレイヤー操作ボタン
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("一枚引く"):
        player_hit()
with col2:
    if st.button("勝負"):
        stand()
with col3:
    if st.button("リセット"):
        reset_game()
if st.button("ルール"):
        rule()

# 現在の手札と合計表示
st.write("### あなたの手札:", st.session_state.player_cards)
st.write("### あなたの合計:", st.session_state.player_total)
st.write("### 相手の手札:", st.session_state.dealer_cards if st.session_state.game_over else [st.session_state.dealer_cards[0], '?'])
st.write("### 相手の合計:", st.session_state.dealer_total if st.session_state.game_over else '?')

# ゲーム終了判定
if st.session_state.game_over:
    if st.session_state.player_total > 21:
        st.write("21を超過してしまった！相手の勝ち！")
    elif st.session_state.dealer_total > 21:
        st.write("相手が21を超過した！あなたの勝ち！")
    elif st.session_state.player_total > st.session_state.dealer_total:
        if st.session_state.player_total == 21:
            st.write("ピッタリ21!あなたの勝利！")
        else:
            st.write("あなたの方が21に近い!あなたの勝ち！")
    elif st.session_state.player_total < st.session_state.dealer_total:
        if st.session_state.dealer_total == 21:
            st.write("相手がピッタリ21!相手の勝ち!")
        else:
            st.write("相手の方が21に近い!相手の勝ち！")
    else:
        st.write("引き分け！")
