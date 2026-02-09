## **COPILOT EXECUTION SCRIPT — FINAL AUTHORITY DOCUMENT**

This document governs execution order, edit permissions, and stopping conditions for an automated coding agent.

The purpose is to eliminate recursive edits, architectural drift, and speculative implementation.

---

## **0\. Execution Principles**

The agent operates under four rules:

1. Build only the currently authorized file.

2. Do not modify previously completed files.

3. Do not anticipate future steps.

4. Stop when the current step’s acceptance criteria are met.

If uncertainty exists, execution halts.

---

## **1\. Global Execution Constraints**

The agent must never:

* Refactor completed files.

* Introduce new dependencies.

* Rename directories or files.

* Merge responsibilities between layers.

* Introduce helper abstractions not explicitly required.

All logic must remain local to the file being built.

---

## **2\. Execution Sequence (Immutable Order)**

Each step is atomic. Completion locks the file.

---

### **STEP 1 — Repository Skeleton**

Create empty structure:

`config/`  
`services/`  
`models/`  
`ui/`  
`utils/`  
`app.py`  
`requirements.txt`

Acceptance condition:

* Directories exist.

* No implementation code written.

STOP.

---

### **STEP 2 — requirements.txt**

Add only:

`streamlit`  
`feedparser`  
`yt-dlp`  
`python-dateutil`

Acceptance condition:

* No version pinning required.

* No additional packages added.

STOP.

---

### **STEP 3 — Data Model (LOCK POINT A)**

File:

`models/video_item.py`

Create dataclass with fields defined in the build contract.

Acceptance condition:

* File imports only stdlib modules.

* No logic functions present.

After completion:

**This file becomes immutable.**

STOP.

---

### **STEP 4 — Configuration Layer (LOCK POINT B)**

File:

`config/channels.py`

Create:

`RSS_CHANNELS = {}`

Acceptance condition:

* Static dictionary only.

* No functions.

File locked.

STOP.

---

### **STEP 5 — RSS Fetcher**

File:

`services/rss_fetcher.py`

Requirements:

* Function `fetch_rss(channel_id: str)`

* Returns raw feedparser output

* No parsing or transformation

Acceptance condition:

* feedparser imported.

* Function returns feedparser.parse result directly.

STOP.

---

### **STEP 6 — yt-dlp Fetcher**

File:

`services/ytdlp_fetcher.py`

Requirements:

* subprocess execution

* stdout parsing only

* returns raw JSON objects

Forbidden:

* downloads

* temp files

* caching

Acceptance condition:

* command contains `--dump-json --flat-playlist`.

STOP.

---

### **STEP 7 — Normalization Layer (LOCK POINT C)**

File:

`services/normalizer.py`

Responsibilities:

* Convert raw data → VideoItem

* Construct embed URL

* Parse dates

* Sort descending by published

Acceptance condition:

* Output type is `List[VideoItem]`.

* No Streamlit imports.

File locked.

STOP.

---

### **STEP 8 — Cache Layer**

File:

`utils/cache.py`

Requirements:

* Wrap fetch calls only.

* Use:

`@st.cache_data(ttl=3600)`

Acceptance condition:

* Cache functions do not transform data.

STOP.

---

### **STEP 9 — CSS Injection**

File:

`ui/css.py`

Requirements:

* Single function `inject_css()`

* Inject style via st.markdown

* Hide header/footer/menu

* Rounded thumbnails

* Disable text selection

Acceptance condition:

* CSS only, no layout logic.

STOP.

---

### **STEP 10 — Video Grid**

File:

`ui/video_grid.py`

Requirements:

* Accept `List[VideoItem]`

* Determine column count from width threshold

* Render thumbnails and embedded players

Forbidden:

* data filtering

* sorting

* fetching

STOP.

---

### **STEP 11 — Layout Controller**

File:

`ui/layout.py`

Responsibilities:

* Channel selector

* Search filter (title \+ channel only)

* Focus Mode toggle

Acceptance condition:

* Search operates on provided list only.

STOP.

---

### **STEP 12 — Application Entry (FINAL BUILD STEP)**

File:

`app.py`

Execution order must be:

`inject_css()`  
`load_channels()`  
`select_channel()`  
`fetch_data()`  
`normalize()`  
`render_layout()`

Acceptance condition:

* Application runs without errors.

* Video playback functional.

STOP.

---

## **3\. Post-Build Restrictions**

After Step 12:

Only allowed edits:

* CSS styling adjustments

* Grid spacing adjustments

Forbidden edits:

* schema changes

* fetch logic changes

* normalization logic changes

---

## **4\. Completion Criteria**

Execution is complete when:

* Channel change updates grid deterministically.

* Metadata fetch occurs once per hour.

* Videos play inline on iOS.

* AirPlay available.

* No navigation to YouTube homepage exists.

