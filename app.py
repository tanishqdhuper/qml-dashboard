import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Quantum Machine Learning for Network Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

theme = st.sidebar.radio("Appearance", ["Dark", "Light"], horizontal=True, key="theme_mode")
st.sidebar.caption("Theme changes appearance only — experiment data and analysis logic remain unchanged.")

BASE = Path(__file__).parent

@st.cache_data
def load_data():
    classical = pd.read_csv(BASE / "classical_results.csv")
    qml = pd.read_csv(BASE / "qml_results.csv")
    pegasos = pd.read_csv(BASE / "pegasos_results.csv")
    meta = pd.read_csv(BASE / "dataset_metadata.csv")
    return classical, qml, pegasos, meta

classical, qml, pegasos, meta = load_data()

# ---- Styling ----
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {{
  --bg: {'#f3f7fc' if theme == 'Light' else '#070b14'};
  --bg2: {'#e9f1fa' if theme == 'Light' else '#0a1020'};
  --border: {'rgba(76,105,140,.20)' if theme == 'Light' else 'rgba(111,139,177,.22)'};
  --text: {'#162235' if theme == 'Light' else '#f5f7fb'};
  --muted: {'#61748c' if theme == 'Light' else '#93a4bb'};
  --cyan: {'#0788b5' if theme == 'Light' else '#45d9ff'};
  --purple: {'#6852c9' if theme == 'Light' else '#9b7cff'};
  --green: {'#16865d' if theme == 'Light' else '#49e3a5'};
  --shadow: {'rgba(47,76,112,.12)' if theme == 'Light' else 'rgba(0,0,0,.28)'};
}}
.stApp {{
  background:
    radial-gradient(circle at 86% 4%, {'rgba(7,136,181,.12)' if theme == 'Light' else 'rgba(69,217,255,.11)'}, transparent 28%),
    radial-gradient(circle at 12% 12%, {'rgba(104,82,201,.09)' if theme == 'Light' else 'rgba(155,124,255,.10)'}, transparent 25%),
    linear-gradient(135deg, var(--bg) 0%, var(--bg2) 55%, var(--bg) 100%);
  color: var(--text); font-family: 'Inter', sans-serif;
}}
[data-testid="stSidebar"] {{
  background: {'linear-gradient(180deg, #eef5fc 0%, #e5eef8 100%)' if theme == 'Light' else 'linear-gradient(180deg, #080d18 0%, #0c1322 100%)'};
  border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] * {{ font-family: 'Inter', sans-serif; color: var(--text) !important; }}
.block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px; }}
.hero {{
  position: relative; overflow: hidden; padding: 34px 38px;
  border: 1px solid var(--border); border-radius: 24px;
  background: {'linear-gradient(120deg, rgba(255,255,255,.90), rgba(236,245,253,.84))' if theme == 'Light' else 'linear-gradient(120deg, rgba(15,27,48,.95), rgba(10,17,32,.88))'};
  box-shadow: 0 22px 70px var(--shadow); margin-bottom: 24px;
}}
.hero h1 {{
  margin: 2px 0 8px; font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2rem, 4vw, 3.25rem); line-height: 1.05; letter-spacing: -.045em;
  background: linear-gradient(90deg, {'#17263a' if theme == 'Light' else '#fff'}, {'#087da7' if theme == 'Light' else '#bceeff'} 48%, {'#6852c9' if theme == 'Light' else '#a99bff'});
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.hero p {{ margin: 0; color: {'#637790' if theme == 'Light' else '#9eafc4'}; font-size: 1rem; max-width: 850px; }}
.offline {{
  display: inline-flex; align-items: center; gap: 8px; padding: 7px 12px; border-radius: 999px;
  background: {'rgba(22,134,93,.09)' if theme == 'Light' else 'rgba(30,73,61,.38)'};
  color: {'#11704e' if theme == 'Light' else '#8ff0c2'};
  border: 1px solid {'rgba(22,134,93,.25)' if theme == 'Light' else 'rgba(73,227,165,.30)'};
  font-size: .73rem; font-weight: 800; letter-spacing: .10em;
}}
.offline:before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--green); }}
.section {{ font-family: 'Space Grotesk', sans-serif; font-size: 1.38rem; font-weight: 700; margin: 25px 0 12px; color: var(--text); }}
.subtle {{ color: var(--muted); font-size: .88rem; }}
[data-testid="stMetric"] {{
  background: {'linear-gradient(145deg, rgba(255,255,255,.92), rgba(236,244,252,.86))' if theme == 'Light' else 'linear-gradient(145deg, rgba(18,28,46,.92), rgba(11,18,32,.90))'};
  border: 1px solid var(--border); padding: 17px 18px; border-radius: 16px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.45), 0 12px 30px var(--shadow);
}}
[data-testid="stMetricLabel"] {{ color: var(--muted) !important; font-weight: 600; }}
[data-testid="stMetricValue"] {{ color: var(--text) !important; font-family: 'Space Grotesk', sans-serif; }}
div[data-baseweb="select"] > div {{
  background: {'rgba(255,255,255,.82)' if theme == 'Light' else 'rgba(13,21,36,.9)'};
  border-color: var(--border); border-radius: 10px;
}}
div[data-testid="stDataFrame"] {{ border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }}
.note, .research-card {{
  padding: 16px 18px; border: 1px solid var(--border);
  background: {'linear-gradient(145deg, rgba(255,255,255,.78), rgba(234,243,251,.78))' if theme == 'Light' else 'linear-gradient(145deg, rgba(17,27,45,.82), rgba(10,17,30,.72))'};
  color: {'#536a84' if theme == 'Light' else '#b9c7d8'}; border-radius: 14px;
}}
.research-card strong {{ color: var(--text); }}
.glow-line {{ height: 2px; width: 100%; background: linear-gradient(90deg, transparent, var(--cyan), var(--purple), transparent); opacity: .55; margin: 10px 0 22px; }}
[data-testid="stPlotlyChart"] {{
  border: 1px solid var(--border); border-radius: 16px;
  background: {'rgba(255,255,255,.48)' if theme == 'Light' else 'rgba(9,15,27,.45)'}; padding: 5px;
}}
hr {{ border-color: var(--border) !important; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="offline">OFFLINE EXPERIMENTAL MODE — KDD CUP 99</div>
  <h1>Quantum Machine Learning<br>for Network Intrusion Detection</h1>
  <p>Experimental research cockpit for classical ML, QSVC, VQC and PegasosQSVC results — designed for analysis, presentation and project demonstration.</p>
</div>
<div class="glow-line"></div>
""", unsafe_allow_html=True)

# ---- Sidebar ----
pages = [
    "Overview",
    "Classical vs QML",
    "Experiment Explorer",
    "PegasosQSVC C Analysis",
    "Metric Comparison",
    "Best-Model Summary",
]
page = st.sidebar.radio("Research Views", pages)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Research Console")
st.sidebar.caption("Experiment navigation")
st.sidebar.write("Source: provided experiment-results screenshot")
st.sidebar.write("Dataset: KDD Cup99")
st.sidebar.write("Encoding: OHE")
st.sidebar.write("PCA: 8 components in reported PCA experiments")
st.sidebar.markdown("---")
st.sidebar.markdown("**Analysis scope**")
st.sidebar.caption("Recorded experiments only. No live packet capture, live NIDS inference, or fabricated evaluation artifacts.")

metric_cols = ["accuracy","precision","recall","f1_score"]
pretty = {"accuracy":"Accuracy","precision":"Precision","recall":"Recall","f1_score":"F1-score"}

def fmt_df(df):
    out = df.copy()
    for c in metric_cols:
        if c in out:
            out[c] = out[c].map(lambda x: f"{x:.3f}".rstrip("0").rstrip("."))
    return out

# ---- Overview ----
if page == "Overview":
    st.markdown('<div class="section">Experimental Overview</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Dataset", "KDD Cup99")
    c2.metric("Original features", "41")
    c3.metric("Records", "311,029")
    c4.metric("Expanded features", "41 → 114")

    st.markdown('<div class="section">Research Snapshot</div>', unsafe_allow_html=True)
    x1, x2, x3 = st.columns(3)
    with x1:
        st.markdown('<div class="research-card"><strong>⚛️ Quantum Track</strong><br><span class="subtle">QSVC, VQC and PegasosQSVC experiments across recorded subset sizes.</span></div>', unsafe_allow_html=True)
    with x2:
        st.markdown('<div class="research-card"><strong>🧠 Classical Track</strong><br><span class="subtle">LR, Random Forest and XGBoost baselines with and without PCA.</span></div>', unsafe_allow_html=True)
    with x3:
        st.markdown('<div class="research-card"><strong>📊 Evaluation</strong><br><span class="subtle">Accuracy, precision, recall and F1-score from the supplied results.</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="section">Reported experiment groups</div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("Classical runs", len(classical))
    b.metric("QSVC / VQC runs", len(qml))
    c.metric("PegasosQSVC runs", len(pegasos))

    st.markdown('<div class="section">Best Reported F1 by Experiment Family</div>', unsafe_allow_html=True)
    overview_rows = [
        ["Classical ML", classical["f1_score"].max()],
        ["QSVC / VQC", qml["f1_score"].max()],
        ["PegasosQSVC", pegasos["f1_score"].max()],
    ]
    overview_df = pd.DataFrame(overview_rows, columns=["family", "f1_score"])
    fig_over = px.bar(overview_df, x="family", y="f1_score", text="f1_score",
                      title="Highest recorded F1-score within each supplied result group")
    fig_over.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_over.update_layout(yaxis_range=[0,1.05], height=360, margin=dict(l=20,r=20,t=55,b=20), template=("plotly_white" if theme == "Light" else "plotly_dark"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=("#162235" if theme == "Light" else "#f5f7fb"))
    st.plotly_chart(fig_over, width="stretch")

    st.markdown('<div class="section">Dataset & preprocessing record</div>', unsafe_allow_html=True)
    st.dataframe(meta, width="stretch", hide_index=True)
    st.markdown('<div class="note">No confusion matrices, ROC curves, training times, prediction times, loss histories, or additional results are fabricated here. Only values present in the supplied experiment table are displayed.</div>', unsafe_allow_html=True)

# ---- Classical vs QML ----
elif page == "Classical vs QML":
    st.markdown('<div class="section">Classical Baselines vs Quantum ML</div>', unsafe_allow_html=True)
    classical_long = classical.copy()
    classical_long["family"] = "Classical ML"
    classical_long["display_model"] = classical_long["model"]

    qml_long = qml.copy()
    qml_long["family"] = "QML"
    qml_long["display_model"] = qml_long["qml_model"] + " (subset " + qml_long["subset_size"].astype(str) + ")"

    pegasos_long = pegasos.copy()
    pegasos_long["family"] = "QML"
    pegasos_long["display_model"] = "PegasosQSVC (C=" + pegasos_long["c"].astype(str) + ", n=" + pegasos_long["subset_size"].astype(str) + ", steps=" + pegasos_long["num_steps"].astype(str) + ")"

    all_runs = pd.concat([
        classical_long[["display_model","family"] + metric_cols],
        qml_long[["display_model","family"] + metric_cols],
        pegasos_long[["display_model","family"] + metric_cols]
    ], ignore_index=True)

    selected_metric = st.selectbox("Metric", metric_cols, format_func=lambda x: pretty[x])
    fig = px.bar(all_runs, x="display_model", y=selected_metric, color="family",
                 title=f"{pretty[selected_metric]} across reported runs",
                 labels={"display_model":"Experiment", selected_metric:pretty[selected_metric], "family":"Family"})
    fig.update_layout(xaxis_tickangle=-45, height=500, template=("plotly_white" if theme == "Light" else "plotly_dark"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=("#162235" if theme == "Light" else "#f5f7fb"))
    st.plotly_chart(fig, width="stretch")

    st.markdown("**Classical baseline results**")
    st.dataframe(fmt_df(classical), width="stretch", hide_index=True)
    st.markdown("**QSVC / VQC results**")
    st.dataframe(fmt_df(qml), width="stretch", hide_index=True)
    st.markdown("**PegasosQSVC results**")
    st.dataframe(fmt_df(pegasos), width="stretch", hide_index=True)

# ---- Explorer ----
elif page == "Experiment Explorer":
    st.markdown('<div class="section">Interactive Experiment Explorer</div>', unsafe_allow_html=True)
    st.caption("Filter the recorded QML/PegasosQSVC experiments. Filters do not generate or infer new results.")

    source = st.radio("Experiment family", ["QSVC / VQC", "PegasosQSVC"], horizontal=True)
    if source == "QSVC / VQC":
        df = qml.copy()
        model_options = sorted(df["qml_model"].unique())
        models = st.multiselect("Model", model_options, default=model_options)
        subsets = st.multiselect("Subset size", sorted(df["subset_size"].unique()), default=sorted(df["subset_size"].unique()))
        view = df[df["qml_model"].isin(models) & df["subset_size"].isin(subsets)]
        st.dataframe(fmt_df(view), width="stretch", hide_index=True)
    else:
        df = pegasos.copy()
        model_options = sorted(df["qml_model"].unique())
        models = st.multiselect("Model", model_options, default=model_options)
        subsets = st.multiselect("Subset size", sorted(df["subset_size"].unique()), default=sorted(df["subset_size"].unique()))
        cvals = st.multiselect("C value", sorted(df["c"].unique()), default=sorted(df["c"].unique()))
        steps = st.multiselect("num_steps", sorted(df["num_steps"].unique()), default=sorted(df["num_steps"].unique()))
        view = df[df["qml_model"].isin(models) & df["subset_size"].isin(subsets) & df["c"].isin(cvals) & df["num_steps"].isin(steps)]
        st.dataframe(fmt_df(view), width="stretch", hide_index=True)

    if len(view):
        m = st.selectbox("Plot metric", metric_cols, format_func=lambda x: pretty[x])
        x = "subset_size" if "subset_size" in view.columns else "model"
        fig = px.line(view, x=x, y=m, markers=True, title=f"{pretty[m]} for selected experiments")
        fig.update_layout(height=430, template=("plotly_white" if theme == "Light" else "plotly_dark"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=("#162235" if theme == "Light" else "#f5f7fb"))
        st.plotly_chart(fig, width="stretch")

# ---- C Analysis ----
elif page == "PegasosQSVC C Analysis":
    st.markdown('<div class="section">PegasosQSVC C-Value Analysis</div>', unsafe_allow_html=True)
    subset = st.selectbox("Subset size", sorted(pegasos["subset_size"].unique()))
    steps = st.selectbox("num_steps", sorted(pegasos["num_steps"].unique()))
    df = pegasos[(pegasos["subset_size"] == subset) & (pegasos["num_steps"] == steps)].sort_values("c")

    if df.empty:
        st.warning("No reported run matches this subset size and num_steps combination.")
    else:
        metric = st.selectbox("Metric", metric_cols, format_func=lambda x: pretty[x])
        fig = px.line(df, x="c", y=metric, markers=True, title=f"{pretty[metric]} vs C (subset={subset}, steps={steps})",
                      log_x=True)
        fig.update_layout(height=450, template=("plotly_white" if theme == "Light" else "plotly_dark"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=("#162235" if theme == "Light" else "#f5f7fb"))
        st.plotly_chart(fig, width="stretch")
        st.dataframe(fmt_df(df), width="stretch", hide_index=True)

        best = df.loc[df[metric].idxmax()]
        st.metric(f"Best reported {pretty[metric]}", f"{best[metric]:.3f}", f"C = {best['c']}")

# ---- Metrics ----
elif page == "Metric Comparison":
    st.markdown('<div class="section">Metric Comparison</div>', unsafe_allow_html=True)
    family = st.selectbox("Results source", ["Classical ML", "QSVC / VQC", "PegasosQSVC"])
    df = {"Classical ML":classical, "QSVC / VQC":qml, "PegasosQSVC":pegasos}[family].copy()

    if family == "Classical ML":
        df["label"] = df["model"]
    elif family == "QSVC / VQC":
        df["label"] = df["qml_model"] + " — subset " + df["subset_size"].astype(str)
    else:
        df["label"] = "C=" + df["c"].astype(str) + " — n=" + df["subset_size"].astype(str) + " — steps=" + df["num_steps"].astype(str)

    long = df.melt(id_vars=["label"], value_vars=metric_cols, var_name="metric", value_name="score")
    long["metric"] = long["metric"].map(pretty)
    fig = px.bar(long, x="label", y="score", color="metric", barmode="group",
                 title=f"{family}: Accuracy, Precision, Recall and F1-score")
    fig.update_layout(xaxis_tickangle=-45, yaxis_range=[0,1.05], height=520, template=("plotly_white" if theme == "Light" else "plotly_dark"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=("#162235" if theme == "Light" else "#f5f7fb"))
    st.plotly_chart(fig, width="stretch")
    st.dataframe(fmt_df(df.drop(columns=["label"])), width="stretch", hide_index=True)

# ---- Best model ----
else:
    st.markdown('<div class="section">Best-Model Summary</div>', unsafe_allow_html=True)
    st.caption("Best means highest reported F1-score within the supplied results; ties are retained rather than broken arbitrarily.")

    candidates = []
    for _, r in classical.iterrows():
        candidates.append({
            "family":"Classical ML", "model":r["model"], "configuration":f"PCA={r['pca_applied']}, features={r['features']}",
            "accuracy":r["accuracy"], "precision":r["precision"], "recall":r["recall"], "f1_score":r["f1_score"]
        })
    for _, r in qml.iterrows():
        candidates.append({
            "family":"QML", "model":r["qml_model"], "configuration":f"subset={r['subset_size']}, PCA={r['pca_applied']}",
            "accuracy":r["accuracy"], "precision":r["precision"], "recall":r["recall"], "f1_score":r["f1_score"]
        })
    for _, r in pegasos.iterrows():
        candidates.append({
            "family":"QML", "model":"PegasosQSVC",
            "configuration":f"C={r['c']}, subset={r['subset_size']}, num_steps={r['num_steps']}",
            "accuracy":r["accuracy"], "precision":r["precision"], "recall":r["recall"], "f1_score":r["f1_score"]
        })

    best_df = pd.DataFrame(candidates)
    best_f1 = best_df["f1_score"].max()
    winners = best_df[best_df["f1_score"] == best_f1].copy()

    a,b,c,d = st.columns(4)
    a.metric("Highest reported F1", f"{best_f1:.2f}")
    a2 = best_df.loc[best_df["accuracy"].idxmax()]
    b.metric("Highest accuracy", f"{a2['accuracy']:.2f}")
    p2 = best_df.loc[best_df["precision"].idxmax()]
    c.metric("Highest precision", f"{p2['precision']:.2f}")
    r2 = best_df.loc[best_df["recall"].idxmax()]
    d.metric("Highest recall", f"{r2['recall']:.2f}")

    st.markdown("### Highest-F1 reported configuration(s)")
    st.dataframe(fmt_df(winners), width="stretch", hide_index=True)

    st.markdown("### Interpretation")
    st.write(
        "Among the supplied records, PegasosQSVC reaches an F1-score of 0.92 at C=100, "
        "subset size 200 and num_steps=200. The supplied classical baseline table also contains "
        "multiple 0.95 F1-score results. These are reported values only; this dashboard does not "
        "claim statistical significance or real-time deployment performance."
    )

st.markdown("---")
st.caption("Quantum Machine Learning for Network Intrusion Detection • Offline Experimental Mode • Results reproduced from the provided experiment table")
