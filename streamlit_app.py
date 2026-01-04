import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import streamlit as st
import random
import time

# --- 1. INITIALIZE GAME STATE ---
if 'player' not in st.session_state:
    st.session_state.player = {
        "level": 1, "xp": 0, "gold": 0, "inventory": [], 
        "stone": 0, "iron": 0, "coal": 0, "obsidian": 0, "wheat": 0,
        "fairy_dust": 0, "hunger": 100,
        "current_island": "Starter Island",
        "cooldown_mod": 0, "dust_luck": 0, "hunger_mod": 1.0
    }

# Boss & Logic States
if 'boss_health' not in st.session_state: st.session_state.boss_health = 20
if 'last_mine_time' not in st.session_state: st.session_state.last_mine_time = 0
if 'hammer_hits' not in st.session_state: st.session_state.hammer_hits = 0
if 'active_recipe' not in st.session_state: st.session_state.active_recipe = None
if 'merchant_active' not in st.session_state: st.session_state.merchant_active = False

# --- 2. GAME LOGIC ---
if st.session_state.player['xp'] >= 100:
    st.session_state.player['level'] += 1
    st.session_state.player['xp'] = 0
    st.balloons()

if not st.session_state.merchant_active and random.random() < 0.15:
    st.session_state.merchant_active = True

# --- 3. SIDEBAR HUD ---
st.sidebar.header(f"👤 Level {st.session_state.player['level']}")
st.sidebar.progress(min(float(st.session_state.player['xp']) / 100.0, 1.0))
st.sidebar.subheader("🍖 Hunger Status")
st.sidebar.progress(st.session_state.player["hunger"] / 100.0)

if st.sidebar.button("♻️ Reset Game Data"):
    st.session_state.clear()
    st.rerun()

# --- 4. MERCHANT & RESOURCES ---
st.title("🏝️ Island Survival RPG")

if st.session_state.merchant_active:
    with st.expander("🕵️ A Merchant is here!", expanded=True):
        st.write("Trade **20 Obsidian** for a **Dragon Scale**?")
        if st.button("🤝 Accept Trade", key="merch_btn"):
            if st.session_state.player["obsidian"] >= 20:
                st.session_state.player["obsidian"] -= 20
                st.session_state.player["inventory"].append("Dragon Scale")
                st.success("Traded for Dragon Scale!")
            else: st.error("Not enough Obsidian!")
        if st.button("Dismiss Merchant"): 
            st.session_state.merchant_active = False
            st.rerun()

r1, r2, r3, r4 = st.columns(4)
r1.metric("🪨 Stone", st.session_state.player["stone"])
r2.metric("⛓️ Iron", st.session_state.player["iron"])
r3.metric("🔥 Coal", st.session_state.player["coal"])
r4.metric("💎 Obsidian", st.session_state.player["obsidian"])

# --- 5. PET SHOP ---
st.divider()
st.header("🐾 Pet Shop")
p1, p2 = st.columns(2)
with p1:
    st.write("**Baby Dino** (50 Gold)")
    if st.button("Adopt Dino", key="pet_dino"):
        if st.session_state.player["gold"] >= 50:
            st.session_state.player["gold"] -= 50
            st.session_state.player["hunger_mod"] = 0.5
            st.session_state.player["inventory"].append("Baby Dino")
            st.success("Hunger loss reduced!")
with p2:
    st.write("**Harvest Spirit** (30 Dust)")
    if st.button("Adopt Spirit", key="pet_spirit"):
        if st.session_state.player["fairy_dust"] >= 30:
            st.session_state.player["fairy_dust"] -= 30
            st.session_state.player["inventory"].append("Harvest Spirit")
            st.success("Double Wheat unlocked!")

# --- 6. TABS (FIXED VERSION) ---
st.divider()
tab1, tab2 = st.tabs(["🧚 Fairy Forest", "🌾 Farm & Kitchen"])

with tab1:
    st.subheader("Cloud Search")
    f_cols = st.columns(3)
    for i, col in enumerate(f_cols):
        if col.button(f"☁️ Cloud {i+1}", key=f"c_{i}"):
            if random.random() < 0.35:
                st.session_state.player["fairy_dust"] += 1
                st.success("Found Fairy Dust!")
            else: st.info("Nothing...")

with tab2:
    st.subheader("Harvesting & Cooking")
    if st.session_state.player["current_island"] == "Farm Island":
        if st.button("🧺 Harvest Wheat", key="harv_btn"):
            gain = 10 if "Harvest Spirit" in st.session_state.player["inventory"] else 5
            st.session_state.player["wheat"] += gain
            st.success(f"Harvested {gain} Wheat!")
    
    c_cook1, c_cook2 = st.columns(2)
    if c_cook1.button("🍞 Bake Bread (10 Wheat)"):
        if st.session_state.player["wheat"] >= 10:
            st.session_state.player["wheat"] -= 10
            st.session_state.player["hunger"] = min(100, st.session_state.player["hunger"] + 30)
            st.rerun()
    if c_cook2.button("🥩 Cook Meat (5 Coal)"):
        if st.session_state.player["coal"] >= 5:
            st.session_state.player["coal"] -= 5
            st.session_state.player["hunger"] = min(100, st.session_state.player["hunger"] + 50)
            st.rerun()

# --- 7. FORGE & COMBAT ---
st.divider()
st.subheader("⚒️ The Forge")
if st.session_state.active_recipe is None:
    if st.button("⚒️ Forge Steel Pickaxe (30 Stone, 15 Iron)"):
        if st.session_state.player["stone"] >= 30 and st.session_state.player["iron"] >= 15:
            st.session_state.active_recipe = "Steel Pickaxe"
            st.rerun()
else:
    st.write(f"🔨 Hammering: **{st.session_state.active_recipe}**")
    st.progress(st.session_state.hammer_hits / 8)
    if st.button("🔨 HIT ANVIL", key="forge_hit"):
        st.session_state.hammer_hits += 1
        if st.session_state.hammer_hits >= 8:
            st.session_state.player["cooldown_mod"] += 2
            st.session_state.active_recipe = None
            st.session_state.hammer_hits = 0
            st.balloons()

# --- 8. THE VOID BOSS ---
st.divider()
st.header("👹 Void Gate")
if st.session_state.player["level"] >= 10:
    if st.session_state.boss_health > 0:
        st.write(f"Void King HP: {st.session_state.boss_health}")
        st.progress(st.session_state.boss_health / 20)
        if st.button("🗡️ STRIKE THE KING", key="boss_atk"):
            st.session_state.boss_health -= 1
            if st.session_state.boss_health <= 0:
                st.balloons()
    else:
        st.title("🏆 THE VOID KING IS DEFEATED!")
else:
    st.info("Locked until Level 100 (Level 10 for testing).")

# --- 9. MAP & MINING ---
st.divider()
with st.expander("🗺️ World Map"):
    st.session_state.player["current_island"] = st.selectbox("Set Destination", 
        ["Starter Island", "Main Island", "Zombie Island", "Volcano Island", "Farm Island"])

if st.session_state.player["current_island"] == "Zombie Island":
    if st.button("⚔️ Fight Zombie", key="z_fight"):
        st.session_state.player["xp"] += 30
        st.session_state.player["iron"] += random.randint(2, 5)
        st.session_state.player["hunger"] -= 8 * st.session_state.player["hunger_mod"]

st.subheader(f"⛏️ Mining: {st.session_state.player['current_island']}")
if st.button("⛏️ Mine Ore", key="mine_master"):
    now = time.time()
    penalty = 2.0 if st.session_state.player["hunger"] < 30 else 1.0
    cd = max(1, (5 - st.session_state.player["cooldown_mod"]) * penalty)
    
    if now - st.session_state.last_mine_time < cd:
        st.error(f"Wait {int(cd - (now - st.session_state.last_mine_time))}s")
    else:
        island = st.session_state.player["current_island"]
        st.session_state.player["stone"] += 10
        st.session_state.player["xp"] += 15
        st.session_state.player["hunger"] -= 10 * st.session_state.player["hunger_mod"]
        if island == "Main Island": st.session_state.player["iron"] += 5
        elif island == "Volcano Island":
            st.session_state.player["obsidian"] += 4
            st.session_state.player["coal"] += 8
        st.session_state.last_mine_time = now
        st.success("Mined resources!")
