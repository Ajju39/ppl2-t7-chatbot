import streamlit as st
import pandas as pd
import re
from pathlib import Path
st.set_page_config(page_title="PPL2 T7 Chatbot", page_icon="🏏", layout="wide")

@st.cache_data
def load_data():
    data = [
        {"player_name":"KIRAN","matches":10,"t7_runs":18,"t7_wickets":10,"balls_faced":94,"balls_bowled":87,"runs_conceded":11},
        {"player_name":"KRANTHI","matches":9,"t7_runs":11,"t7_wickets":1,"balls_faced":74,"balls_bowled":12,"runs_conceded":5},
        {"player_name":"VARMA","matches":9,"t7_runs":11,"t7_wickets":10,"balls_faced":74,"balls_bowled":84,"runs_conceded":8},
        {"player_name":"PAVAN","matches":9,"t7_runs":9,"t7_wickets":11,"balls_faced":79,"balls_bowled":83,"runs_conceded":6},
        {"player_name":"GIRISH","matches":9,"t7_runs":9,"t7_wickets":13,"balls_faced":72,"balls_bowled":73,"runs_conceded":12},
        {"player_name":"ARUN","matches":9,"t7_runs":8,"t7_wickets":0,"balls_faced":32,"balls_bowled":6,"runs_conceded":2},
        {"player_name":"RK","matches":9,"t7_runs":8,"t7_wickets":2,"balls_faced":52,"balls_bowled":20,"runs_conceded":1},
        {"player_name":"RUSHI","matches":10,"t7_runs":7,"t7_wickets":6,"balls_faced":55,"balls_bowled":28,"runs_conceded":1},
        {"player_name":"GANESH POKALA","matches":9,"t7_runs":7,"t7_wickets":5,"balls_faced":58,"balls_bowled":30,"runs_conceded":6},
        {"player_name":"PRASANTH","matches":10,"t7_runs":7,"t7_wickets":10,"balls_faced":31,"balls_bowled":67,"runs_conceded":6},
        {"player_name":"LPD","matches":10,"t7_runs":7,"t7_wickets":15,"balls_faced":53,"balls_bowled":110,"runs_conceded":10},
        {"player_name":"RAMESH","matches":9,"t7_runs":7,"t7_wickets":1,"balls_faced":57,"balls_bowled":6,"runs_conceded":4},
        {"player_name":"SANJAY","matches":9,"t7_runs":6,"t7_wickets":7,"balls_faced":56,"balls_bowled":43,"runs_conceded":7},
        {"player_name":"MADHU","matches":10,"t7_runs":6,"t7_wickets":9,"balls_faced":75,"balls_bowled":51,"runs_conceded":5},
        {"player_name":"SRINIVAS KATTA","matches":8,"t7_runs":5,"t7_wickets":8,"balls_faced":19,"balls_bowled":54,"runs_conceded":11},
        {"player_name":"NANDA","matches":9,"t7_runs":4,"t7_wickets":10,"balls_faced":40,"balls_bowled":47,"runs_conceded":10},
        {"player_name":"VAMSHI","matches":10,"t7_runs":3,"t7_wickets":7,"balls_faced":38,"balls_bowled":31,"runs_conceded":2},
        {"player_name":"SURAJ","matches":9,"t7_runs":3,"t7_wickets":1,"balls_faced":36,"balls_bowled":6,"runs_conceded":0},
        {"player_name":"ARJUN","matches":9,"t7_runs":3,"t7_wickets":9,"balls_faced":38,"balls_bowled":96,"runs_conceded":3},
        {"player_name":"CM","matches":10,"t7_runs":3,"t7_wickets":13,"balls_faced":37,"balls_bowled":102,"runs_conceded":11},
        {"player_name":"SUDHEER","matches":8,"t7_runs":2,"t7_wickets":2,"balls_faced":17,"balls_bowled":9,"runs_conceded":2},
        {"player_name":"AMIT","matches":9,"t7_runs":2,"t7_wickets":5,"balls_faced":23,"balls_bowled":19,"runs_conceded":4},
        {"player_name":"KASI","matches":10,"t7_runs":2,"t7_wickets":13,"balls_faced":25,"balls_bowled":84,"runs_conceded":7},
        {"player_name":"RAJIV","matches":10,"t7_runs":1,"t7_wickets":4,"balls_faced":33,"balls_bowled":24,"runs_conceded":3},
        {"player_name":"PRAMOD","matches":9,"t7_runs":1,"t7_wickets":2,"balls_faced":23,"balls_bowled":12,"runs_conceded":2},
        {"player_name":"RAMU","matches":10,"t7_runs":1,"t7_wickets":19,"balls_faced":23,"balls_bowled":84,"runs_conceded":11},
        {"player_name":"HARSHA","matches":9,"t7_runs":12,"t7_wickets":7,"balls_faced":74,"balls_bowled":62,"runs_conceded":11},
        {"player_name":"VENKY","matches":10,"t7_runs":5,"t7_wickets":0,"balls_faced":68,"balls_bowled":0,"runs_conceded":0},
    ]
    df = pd.DataFrame(data)
    df["all_rounder_score"] = df["t7_runs"] + (df["t7_wickets"] * 10)
    df["batting_runs_per_ball"] = (df["t7_runs"] / df["balls_faced"]).round(3)
    df["batting_balls_per_run"] = df.apply(
        lambda row: round(row["balls_faced"] / row["t7_runs"], 2) if row["t7_runs"] > 0 else None,
        axis=1,
    )
    df["bowling_runs_conceded_per_ball"] = df.apply(
        lambda row: round(row["runs_conceded"] / row["balls_bowled"], 3) if row["balls_bowled"] > 0 else 0,
        axis=1,
    )
    df["bowling_balls_per_run_conceded"] = df.apply(
        lambda row: round(row["balls_bowled"] / row["runs_conceded"], 2) if row["runs_conceded"] > 0 else None,
        axis=1,
    )
    return df


DEFAULT_RULES_TEXT = '''
1. Team & Player Rules
- 4 teams total
- 7 players per team
- 2 players per team are flexible players (decided by captain)
- Flexible players can only substitute within their own team (not opponents)
- Impact player can bat, bowl, and field (not required to be a flexible player)

2. Availability and Substitutions
- When someone in the team is injured or unavailable, captain can ask any of the other 4 flexible players to play in their team.
- Flexible players from the opposition are not allowed to play.
- Team players can replace flexible players at any point of time in the match.
- If someone is not available to bat, they will be considered retired out.
- No batsman is allowed to bat twice in an innings.

3. Match Setup
- 5 fielders + 1 keeper + 1 bowler will be on field.
- Batting team will have 7 wickets.
- Minimum 5 bowlers mandatory.
- Maximum limit for a bowler is 2 overs.

4. Tournament Rules
- Average of win margin (4s) will be used as net run rate.
- Top 2 teams will play finals.
- Formal scoring will be done through Stumps app.

5. Umpire Rules
- Umpire can be chosen by both captains, someone from the group not part of the given match.
- Every match will have 2 umpires: 1 straight and 1 off/leg between keeper and side boundary.
- Umpires will have the final call.
- Captains can decide who will be the main and leg umpire.
- Same umpires for both teams. No side changes.

6. Boundary and Ground Rules
- On a given day, cones placed by umpire define the boundary.
- Any obstruction by tree near iron grill or by umpire will not be counted as a four.
- Ball going to boundary after touching the fielder in a non-boundary area will be considered not a boundary.
- If ball touches or is on the boundary line, it will be considered a boundary.

7. Batting Rules
- No batting changes in between an over unless the player is declared injured by both umpires.
- Batsman can retire after the end of an over but needs to come back only as the last batsman in the team. Limited 1 per team.
- If batsman is injured as decided by umpires, batsman can retire but can come back anytime.

8. Bowling Rules
- No bowling changes in between an over unless the player is declared injured by both umpires.
- Only 1 over foot warning per bowler in a match.
- Wide will not extend if batsman moves towards wide crease. On the line is legal delivery.
- Above shoulder delivery according to batsman initial stance is first warning and above head is a wide. One warning allowed per over.
- Pitching the ball outside of pitch (wide crease) and spinning inward is a wide.
- Bowler walk length is restricted as per rear crease.
- Beamers or above-waist full toss as decided by umpire is a no ball.
- 2 beamers by a bowler in an over disqualify the bowler from bowling further in the match.
- Multiple bounce before reaching batsman is a no ball.
- Any ball bowled over stumps within legal height as decided by umpire is a legal delivery.
- On the wide line delivery while bowling is considered a legal ball.

9. No Ball Effects
- Any boundaries scored on a no ball will count.
- Follow-up legal delivery must be bowled.
- Any form of dismissal during a no ball will be discarded and batsman can continue playing.

10. Conduct Rules
- No shouting or fielder distraction allowed while a fielder is collecting the ball.
- Distracting batsman through comments, shouts, or bowler encouragement at the time of delivery is restricted.
- 2 such instances will be awarded a demerit point as decided by umpires.
- If someone disagrees or argues aggressively and both umpires think it is unnecessary, they can award demerit points.
- Each demerit point will cut short a boundary from their total score in the given match.

11. Other Rules
- All other rules will be same as that we are playing currently.
'''

RULE_KEYWORDS = {
    "team": ["team", "teams", "player", "players", "flexible", "impact"],
    "substitution": ["injured", "unavailable", "replace", "replacement", "substitute", "substitution", "retired out", "retire"],
    "match": ["wickets", "fielder", "keeper", "bowler mandatory", "overs", "over limit"],
    "tournament": ["final", "finals", "net run rate", "nrr", "win margin", "stumps app", "scoring"],
    "umpire": ["umpire", "umpires", "main umpire", "leg umpire", "final call"],
    "boundary": ["boundary", "four", "cone", "cones", "tree", "grill", "touches line", "fielder touch"],
    "batting": ["bat", "batsman", "batting", "retire", "retired", "bat twice"],
    "bowling": ["bowl", "bowler", "bowling", "wide", "no ball", "beamer", "beamers", "foot warning", "full toss", "multiple bounce", "rear crease"],
    "conduct": ["shouting", "distraction", "distract", "demerit", "argues", "aggressively", "comments"],
}

STAT_KEYWORDS = [
    "runs", "wickets", "top scorer", "highest runs", "most runs", "most wickets", "top wicket",
    "best player", "all-rounder", "best bowler", "best batter", "compare", "leaderboard",
    "balls faced", "balls bowled", "runs conceded", "player", "tell me about", "score"
]

def load_rules_text():
    rules_path = Path("rules.txt")
    if rules_path.exists():
        return rules_path.read_text(encoding="utf-8")
    return DEFAULT_RULES_TEXT


def split_rules_into_chunks(rules_text: str):
    chunks = []
    current_heading = "General Rules"
    current_lines = []

    for raw_line in rules_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if re.match(r"^\d+\.", line):
            if current_lines:
                chunks.append({
                    "heading": current_heading,
                    "text": "\n".join(current_lines)
                })
            current_heading = line
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        chunks.append({
            "heading": current_heading,
            "text": "\n".join(current_lines)
        })

    return chunks


def retrieve_rule_chunks(question: str, chunks, top_k: int = 2):
    words = re.findall(r"[a-zA-Z0-9']+", question.lower())
    stop_words = {
        "the", "is", "a", "an", "and", "or", "to", "of", "in", "on", "for",
        "if", "it", "be", "are", "what", "how", "many", "can", "do", "does",
        "with", "will", "by", "at", "from"
    }
    query_terms = [w for w in words if w not in stop_words]

    scored = []
    for chunk in chunks:
        text_lower = chunk["text"].lower()
        score = sum(text_lower.count(term) for term in query_terms)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
def answer_stats_question(q: str, df: pd.DataFrame) -> str:
    q = q.lower().strip()

    if "top scorer" in q or "most runs" in q or "highest runs" in q:
        top = df.sort_values(["t7_runs", "t7_wickets"], ascending=False).iloc[0]
        return f"Top T7 run scorer is {top['player_name']} with {top['t7_runs']} runs."

    if "most wickets" in q or "highest wickets" in q or "top wicket" in q:
        top = df.sort_values(["t7_wickets", "t7_runs"], ascending=False).iloc[0]
        return f"Top T7 wicket taker is {top['player_name']} with {top['t7_wickets']} wickets."

    if "best player" in q or "best all rounder" in q or "all-rounder" in q:
        top = df.sort_values("all_rounder_score", ascending=False).iloc[0]
        return (
            f"Best overall player is {top['player_name']} with an all-rounder score of "
            f"{top['all_rounder_score']} ({top['t7_runs']} runs, {top['t7_wickets']} wickets)."
        )

    if "best bowler" in q or "bowling control" in q or "balls per run conceded" in q:
        bowlers = df[df["runs_conceded"] > 0].sort_values("bowling_balls_per_run_conceded", ascending=False)
        top = bowlers.iloc[0]
        return (
            f"Best bowling control is by {top['player_name']}: 1 run conceded every "
            f"{top['bowling_balls_per_run_conceded']} balls."
        )

    if "best batter" in q or "runs per ball" in q:
        batters = df[df["t7_runs"] > 0].sort_values("batting_runs_per_ball", ascending=False)
        top = batters.iloc[0]
        return (
            f"Best batting efficiency is by {top['player_name']}: {top['batting_runs_per_ball']} runs per ball "
            f"across {top['balls_faced']} balls."
        )

    if "top 5" in q and "runs" in q:
        top5 = df.sort_values(["t7_runs", "t7_wickets"], ascending=False).head(5)
        return "Top 5 by runs: " + ", ".join([f"{row.player_name} ({row.t7_runs})" for row in top5.itertuples()])

    if "top 5" in q and "wickets" in q:
        top5 = df.sort_values(["t7_wickets", "t7_runs"], ascending=False).head(5)
        return "Top 5 by wickets: " + ", ".join([f"{row.player_name} ({row.t7_wickets})" for row in top5.itertuples()])

    if "compare" in q:
        matches = [player for player in df["player_name"] if player.lower() in q]
        if len(matches) >= 2:
            row1 = df[df["player_name"] == matches[0]].iloc[0]
            row2 = df[df["player_name"] == matches[1]].iloc[0]
            return (
                f"{row1['player_name']}: {row1['t7_runs']} runs, {row1['t7_wickets']} wickets. "
                f"{row2['player_name']}: {row2['t7_runs']} runs, {row2['t7_wickets']} wickets."
            )

    for player in df["player_name"]:
        if player.lower() in q:
            row = df[df["player_name"] == player].iloc[0]
            return (
                f"{row['player_name']} played {row['matches']} matches, scored {row['t7_runs']} runs from {row['balls_faced']} balls "
                f"({row['batting_runs_per_ball']} runs/ball), and took {row['t7_wickets']} wickets while conceding "
                f"{row['runs_conceded']} runs in {row['balls_bowled']} balls. "
                f"That is {row['bowling_runs_conceded_per_ball']} runs conceded per ball."
            )

    return "I could not match that to player stats. Try asking about runs, wickets, best player, or a player name."


def detect_rule_section(q: str):
    q = q.lower()
    scores = {}
    for section, keywords in RULE_KEYWORDS.items():
        scores[section] = sum(1 for kw in keywords if kw in q)
    best_section = max(scores, key=scores.get)
    return best_section if scores[best_section] > 0 else None


def answer_rules_question(q: str) -> str:
    q_lower = q.lower().strip()
    section = detect_rule_section(q_lower)

    rules_text = load_rules_text()
    chunks = split_rules_into_chunks(rules_text)
    retrieved_chunks = retrieve_rule_chunks(q, chunks, top_k=2)

    direct_answers = [
        (lambda x: "how many teams" in x or ("teams" in x and "total" in x), "There are 4 teams in the tournament."),
        (lambda x: "how many players" in x or "players per team" in x or ("team" in x and "7 players" in x), "Each team has 7 players."),
        (lambda x: "flexible" in x and "how many" in x, "Each team has 2 flexible players, decided by the captain."),
        (lambda x: "impact player" in x, "The impact player can bat, bowl, and field, and does not need to be a flexible player."),
        (lambda x: "injured" in x or "unavailable" in x, "If someone is injured or unavailable, the captain can use one of their own team's flexible players. Opposition flexible players are not allowed."),
        (lambda x: "retired out" in x or ("not available to bat" in x), "If someone is not available to bat, they are considered retired out. A batsman cannot bat twice in an innings."),
        (lambda x: "wickets" in x and "how many" in x, "The batting team has 7 wickets."),
        (lambda x: "minimum bowlers" in x or ("min" in x and "bowlers" in x), "A minimum of 5 bowlers is mandatory."),
        (lambda x: "maximum" in x and "overs" in x, "The maximum limit for a bowler is 2 overs."),
        (lambda x: "net run rate" in x or "nrr" in x, "Net run rate is based on the average win margin in 4s."),
        (lambda x: "finals" in x or "top 2" in x, "The top 2 teams will play the finals."),
        (lambda x: "umpire" in x and "how many" in x, "Each match has 2 umpires: 1 straight umpire and 1 off/leg umpire."),
        (lambda x: "wide" in x and "line" in x, "On the line is a legal delivery, and a ball on the wide line is considered legal."),
        (lambda x: "beamer" in x or "full toss" in x, "A beamer or above-waist full toss is a no ball. Two beamers by the same bowler in an over disqualify that bowler from bowling further in the match."),
        (lambda x: "multiple bounce" in x, "A ball that bounces multiple times before reaching the batsman is a no ball."),
        (lambda x: "no ball" in x and "dismissal" in x, "Any dismissal on a no ball is discarded, and the batsman can continue playing."),
        (lambda x: "boundary" in x and "line" in x, "If the ball touches or is on the boundary line, it is a boundary."),
        (lambda x: "tree" in x or "grill" in x, "Any obstruction by the tree near the iron grill or by the umpire will not count as a four."),
        (lambda x: "demerit" in x, "Two conduct violations can lead to a demerit point, and each demerit point cuts one boundary from the team's total score in that match."),
        (lambda x: "scoring" in x or "stumps app" in x, "Formal scoring will be done through the Stumps app."),
    ]

    for condition, answer in direct_answers:
        if condition(q_lower):
            if retrieved_chunks:
                return f"{answer}\n\nRelevant rule section: {retrieved_chunks[0]['heading']}"
            return answer

    if retrieved_chunks:
        combined = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
        return f"Based on rules.txt, these are the most relevant rule sections:\n\n{combined}"

    if section:
        section_explanations = {
            "team": "Team rules: 4 teams total, 7 players per team, 2 flexible players per team, and the impact player can bat, bowl, and field.",
            "substitution": "Substitution rules: injured or unavailable players can be replaced only by their own team's flexible players. If a player is unavailable to bat, they are retired out.",
            "match": "Match setup: 5 fielders, 1 keeper, and 1 bowler are on the field, the batting side has 7 wickets, at least 5 bowlers are required, and each bowler can bowl a maximum of 2 overs.",
            "tournament": "Tournament rules: average win margin in 4s is used as net run rate, top 2 teams play the finals, and formal scoring is done in the Stumps app.",
            "umpire": "Umpire rules: 2 umpires per match, chosen by captains from people not playing that match, and their decision is final.",
            "boundary": "Boundary rules: cones define the boundary, touching the line is a boundary, but obstruction by the tree, grill area, or umpire does not count as a four.",
            "batting": "Batting rules: no batting change in the middle of an over unless injured, one voluntary retire per team allowed after an over, and an injured batter may return anytime if allowed by umpires.",
            "bowling": "Bowling rules: no bowling changes mid-over unless injured, one foot warning per bowler in a match, wide and no-ball rules apply, and two beamers in an over disqualify the bowler.",
            "conduct": "Conduct rules: shouting, distraction, or aggressive arguing can lead to demerit points decided by umpires, and each demerit point removes one boundary from the score.",
        }
        return section_explanations[section]

    return "I could not find a clear rules match in rules.txt. Ask about team size, flexible players, wickets, overs, umpires, wide, no ball, boundaries, demerit points, or finals."

def detect_question_type(q: str, df: pd.DataFrame) -> str:
    q_lower = q.lower().strip()

    player_names = [p.lower() for p in df["player_name"].tolist()]
    stat_hits = sum(1 for kw in STAT_KEYWORDS if kw in q_lower)
    rule_hits = sum(1 for kws in RULE_KEYWORDS.values() for kw in kws if kw in q_lower)
    player_hit = any(name in q_lower for name in player_names)

    if player_hit:
        return "stats"
    if rule_hits > stat_hits:
        return "rules"
    if stat_hits > 0:
        return "stats"
    return "rules"


def smart_answer(q: str, df: pd.DataFrame):
    question_type = detect_question_type(q, df)
    if question_type == "stats":
        return question_type, answer_stats_question(q, df)
    return question_type, answer_rules_question(q)


def metric_card(label: str, value):
    st.markdown(
        f"""
        <div style='padding:16px;border-radius:18px;border:1px solid #2d2d2d;background:#111827;'>
            <div style='font-size:14px;color:#9ca3af'>{label}</div>
            <div style='font-size:30px;font-weight:700;color:white'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    df = load_data()

    st.title("🏏 PPL2 T7 Cricket Intelligence Bot")
    st.caption("T10 + Club combined into a single T7 format")

    top_run = df.sort_values(["t7_runs", "t7_wickets"], ascending=False).iloc[0]
    top_wkt = df.sort_values(["t7_wickets", "t7_runs"], ascending=False).iloc[0]
    best = df.sort_values("all_rounder_score", ascending=False).iloc[0]

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Top Scorer", f"{top_run['player_name']} ({top_run['t7_runs']})")
    with c2:
        metric_card("Top Wicket Taker", f"{top_wkt['player_name']} ({top_wkt['t7_wickets']})")
    with c3:
        metric_card("Best Player", best["player_name"])

    st.divider()

    sidebar = st.sidebar
    sidebar.header("Filters")
    min_matches = sidebar.slider("Minimum matches", 0, int(df["matches"].max()), 0)
    filtered_df = df[df["matches"] >= min_matches].copy()

    tab1, tab2, tab3, tab4 = st.tabs(["Smart AI Chatbot", "Leaderboard", "Compare Players", "Data Table"])

    with tab1:
        st.subheader("Ask one question for both stats and rules")
        sample_questions = [
            "Who scored most runs?",
            "Who took most wickets?",
            "Who is the best player?",
            "Tell me about KIRAN",
            "Top 5 by wickets",
            "How many players are there in each team?",
            "What is the no ball rule?",
            "What happens if someone is injured?",
            "How many overs can one bowler bowl?",
            "What are demerit points?",
        ]
        selected = st.selectbox("Try a sample question", [""] + sample_questions)
        question = st.text_input("Type your question", value=selected)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        col_a, col_b = st.columns([1, 1])
        with col_a:
            ask_clicked = st.button("Ask Smart Bot", use_container_width=True)
        with col_b:
            clear_clicked = st.button("Clear Chat", use_container_width=True)

        if clear_clicked:
            st.session_state.chat_history = []

        if ask_clicked:
            if question.strip():
                qtype, response = smart_answer(question, filtered_df)
                st.session_state.chat_history.append({
                    "question": question,
                    "type": qtype,
                    "response": response,
                })
            else:
                st.warning("Please enter a question.")

        if st.session_state.chat_history:
            st.markdown("### Conversation")
            for item in reversed(st.session_state.chat_history):
                st.markdown(f"**You:** {item['question']}")
                label = "Stats Answer" if item["type"] == "stats" else "Rules Answer"
                st.info(f"{label}: {item['response']}")
        else:
            st.caption("The bot automatically decides whether your question is about player statistics or tournament rules. Rules answers now read from rules.txt in your app folder.")

    with tab2:
        st.subheader("Leaderboards")
        metric = st.radio(
            "Choose leaderboard",
            ["Runs", "Wickets", "All-Rounder Score", "Batting Runs per Ball", "Bowling Balls per Run Conceded"],
            horizontal=True,
        )

        if metric == "Runs":
            leaderboard = filtered_df.sort_values(["t7_runs", "t7_wickets"], ascending=False)
            st.bar_chart(leaderboard.set_index("player_name")["t7_runs"])
        elif metric == "Wickets":
            leaderboard = filtered_df.sort_values(["t7_wickets", "t7_runs"], ascending=False)
            st.bar_chart(leaderboard.set_index("player_name")["t7_wickets"])
        elif metric == "All-Rounder Score":
            leaderboard = filtered_df.sort_values("all_rounder_score", ascending=False)
            st.bar_chart(leaderboard.set_index("player_name")["all_rounder_score"])
        elif metric == "Batting Runs per Ball":
            leaderboard = filtered_df[filtered_df["t7_runs"] > 0].sort_values("batting_runs_per_ball", ascending=False)
            st.bar_chart(leaderboard.set_index("player_name")["batting_runs_per_ball"])
        else:
            leaderboard = filtered_df[filtered_df["runs_conceded"] > 0].sort_values("bowling_balls_per_run_conceded", ascending=False)
            st.bar_chart(leaderboard.set_index("player_name")["bowling_balls_per_run_conceded"])

        st.dataframe(leaderboard.reset_index(drop=True), use_container_width=True)

    with tab3:
        st.subheader("Compare two players")
        players = sorted(filtered_df["player_name"].tolist())
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox("Player 1", players, index=0)
        with col2:
            p2 = st.selectbox("Player 2", players, index=1 if len(players) > 1 else 0)

        row1 = filtered_df[filtered_df["player_name"] == p1].iloc[0]
        row2 = filtered_df[filtered_df["player_name"] == p2].iloc[0]

        comp = pd.DataFrame(
            {
                "Metric": [
                    "Matches",
                    "Runs",
                    "Balls Faced",
                    "Batting Runs/Ball",
                    "Wickets",
                    "Balls Bowled",
                    "Runs Conceded",
                    "Bowling Balls/Run Conceded",
                    "All-Rounder Score",
                ],
                p1: [
                    row1["matches"],
                    row1["t7_runs"],
                    row1["balls_faced"],
                    row1["batting_runs_per_ball"],
                    row1["t7_wickets"],
                    row1["balls_bowled"],
                    row1["runs_conceded"],
                    row1["bowling_balls_per_run_conceded"],
                    row1["all_rounder_score"],
                ],
                p2: [
                    row2["matches"],
                    row2["t7_runs"],
                    row2["balls_faced"],
                    row2["batting_runs_per_ball"],
                    row2["t7_wickets"],
                    row2["balls_bowled"],
                    row2["runs_conceded"],
                    row2["bowling_balls_per_run_conceded"],
                    row2["all_rounder_score"],
                ],
            }
        )
        st.dataframe(comp, use_container_width=True)

        st.caption("Simple scoring formula: runs + (wickets × 10). T7 = T10 + Club. Bowling control is shown as balls per run conceded.")

    with tab4:
        st.subheader("Full T7 dataset")
        st.dataframe(filtered_df.sort_values("all_rounder_score", ascending=False), use_container_width=True)
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "players_t7.csv", "text/csv", use_container_width=True)


if __name__ == "__main__":
    main()
