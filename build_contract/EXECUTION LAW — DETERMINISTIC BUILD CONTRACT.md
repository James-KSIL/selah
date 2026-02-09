## **EXECUTION LAW — DETERMINISTIC BUILD CONTRACT**

---

## **0\. Authority of This Document**

This document is authoritative.

If implementation conflicts with assumptions or convenience:

* The implementation changes.

* The specification does not.

The execution agent must not introduce new architecture, abstractions, or features unless explicitly added to this document.

Ambiguity resolution rule:

When unclear, omit behavior rather than invent behavior.

---

## **1\. System Identity**

### **1.1 System Type**

Read-only media aggregation interface.

### **1.2 Allowed Capabilities**

The system may only:

1. Retrieve metadata from YouTube RSS feeds.

2. Retrieve metadata via yt-dlp.

3. Normalize metadata into a fixed schema.

4. Display embedded video players.

### **1.3 Forbidden Capabilities**

The system must never:

* Recommend content

* Rank content

* Personalize content

* Store user data

* Introduce analytics

* Modify playback behavior

* Navigate users to youtube.com

---

## **2\. Architectural Law**

The system is composed of four immutable layers:

`CONFIGURATION`  
`FETCH`  
`NORMALIZATION`  
`PRESENTATION`

### **2.1 Layer Isolation Rules**

| Layer | May Access | May Not Access |
| ----- | ----- | ----- |
| Config | nothing | all others |
| Fetch | Config | UI |
| Normalization | Fetch | UI |
| Presentation | Normalized Models | Fetch |

Violation of layer boundaries is a structural error.

---

## **3\. Build Order (Mandatory)**

The execution agent must build in the following order.

No file created out of sequence.

---

### **STEP 1 — Repository Skeleton**

Create directories only:

`config/`  
`services/`  
`models/`  
`ui/`  
`utils/`

No logic written yet.

---

### **STEP 2 — Data Model (LOCK POINT 1\)**

Create:

`models/video_item.py`

Define:

`@dataclass`  
`class VideoItem:`

Fields:

* video\_id

* title

* channel\_name

* published

* thumbnail

* duration

* url

* embed\_url

After creation:

* This file becomes immutable.

* No fields added later.

---

### **STEP 3 — Configuration Layer (LOCK POINT 2\)**

Create:

`config/channels.py`

Define:

`RSS_CHANNELS = {}`

Rules:

* Static dictionary only.

* No runtime mutation.

File locked after creation.

---

### **STEP 4 — Fetch Layer**

Create:

`services/rss_fetcher.py`  
`services/ytdlp_fetcher.py`

Constraints:

#### **RSS Fetcher**

* Returns raw feedparser output only.

* No transformation.

#### **yt-dlp Fetcher**

* Uses subprocess.

* Uses `--dump-json --flat-playlist`.

* No downloads.

* No file writes.

Fetch layer must not import Streamlit.

---

### **STEP 5 — Normalization Layer (LOCK POINT 3\)**

Create:

`services/normalizer.py`

Responsibilities:

* Convert raw feed data → VideoItem

* Build embed URL

* Parse timestamps

* Handle missing fields

Sorting rule:

`published DESC ONLY`

No scoring logic permitted.

After verification, this file becomes immutable.

---

### **STEP 6 — Cache Layer**

Create:

`utils/cache.py`

Rules:

* Only wrapper functions allowed.

* Must use:

`@st.cache_data(ttl=3600)`

Cache key must include:

* channel\_id

* fetch\_method

---

### **STEP 7 — UI Layer**

Create:

`ui/css.py`  
`ui/video_grid.py`  
`ui/layout.py`

UI rules:

* No fetching logic.

* No normalization logic.

* UI receives only List\[VideoItem\].

---

### **STEP 8 — Application Entry**

Create:

`app.py`

Execution order must be:

`inject_css()`  
`select_channel()`  
`fetch_data()`  
`normalize()`  
`render()`

No branching workflows introduced.

---

## **4\. Deterministic UI Behavior**

### **4.1 Grid Rules**

| Width | Columns |
| ----- | ----- |
| \< 900px | 2 |
| ≥ 900px | 3 |

### **4.2 Video Embed Rules**

Embed URL format:

`https://www.youtube.com/embed/{id}?rel=0&modestbranding=1&playsinline=1`

Required outcomes:

* Inline playback

* Native iOS controls

* AirPlay available

---

## **5\. Cache Law**

Fetching must occur only when:

* cache expired

* channel changed

UI reruns must not trigger fetching.

---

## **6\. Focus Mode Law**

Focus Mode:

* Hides grid

* Expands video container

* Uses native iframe behavior only

No JavaScript fullscreen overrides allowed.

---

## **7\. Performance Boundaries**

Target constraints:

* Metadata fetch ≤ once per hour per channel

* UI rerender \< 1 second

* No background workers

---

## **8\. Anti-Hallucination Constraints**

Execution agent must not introduce:

* APIs

* databases

* authentication

* recommendation systems

* analytics

* ranking algorithms

* persistent state

If a requested behavior requires any of the above:

The behavior is rejected.

---

## **9\. Definition of Completion**

The system is complete when:

* Selecting a channel loads videos deterministically.

* Videos play inline on iOS.

* AirPlay is present.

* No external YouTube navigation exists.

* Metadata refresh occurs only via TTL.

---

## **10\. Iteration Law (Post-Build)**

After completion:

* Only presentation layer may change without approval.

* Fetch and normalization layers are frozen.

* Schema changes require specification revision.

