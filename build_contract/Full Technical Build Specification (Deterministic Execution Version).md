## **Full Technical Build Specification (Deterministic Execution Version)**

---

## **1\. System Objective**

Build a mobile-first web application that aggregates YouTube videos from predefined channels using RSS feeds and yt-dlp metadata extraction, presented in a distraction-free interface optimized for iPad and iPhone browsers.

The system is a **read-only aggregation layer**.

The application does not:

* recommend content

* personalize content

* rank content

* store users or preferences

* modify source data

All outputs are deterministic transformations of retrieved metadata.

---

## **2\. System Architecture**

### **2.1 Layer Separation (Mandatory)**

The application consists of four isolated layers:

`CONFIGURATION`  
      `↓`  
`FETCH LAYER`  
      `↓`  
`NORMALIZATION LAYER`  
      `↓`  
`PRESENTATION LAYER`

Rules:

* UI never fetches data directly.

* Fetch logic never formats UI.

* Normalization owns schema integrity.

* Only normalized objects reach the UI.

---

## **3\. Repository Structure (Fixed Layout)**

`refined_media_portal/`  
`│`  
`├── app.py`  
`│`  
`├── config/`  
`│   └── channels.py`  
`│`  
`├── services/`  
`│   ├── rss_fetcher.py`  
`│   ├── ytdlp_fetcher.py`  
`│   └── normalizer.py`  
`│`  
`├── ui/`  
`│   ├── layout.py`  
`│   ├── video_grid.py`  
`│   └── css.py`  
`│`  
`├── models/`  
`│   └── video_item.py`  
`│`  
`├── utils/`  
`│   └── cache.py`  
`│`  
`└── requirements.txt`

No additional directories introduced without specification change.

---

## **4\. Dependencies**

### **requirements.txt**

`streamlit`  
`feedparser`  
`yt-dlp`  
`python-dateutil`

No frontend frameworks.  
 No JS frameworks.

---

## **5\. Data Model (Single Source of Truth)**

### **models/video\_item.py**

`from dataclasses import dataclass`  
`from datetime import datetime`  
`from typing import Optional`

`@dataclass`  
`class VideoItem:`  
    `video_id: str`  
    `title: str`  
    `channel_name: str`  
    `published: datetime`  
    `thumbnail: str`  
    `duration: Optional[int]`  
    `url: str`  
    `embed_url: str`

Rules:

* All UI consumes this model only.

* No dictionaries passed to UI layer.

---

## **6\. Configuration Layer**

### **config/channels.py**

`RSS_CHANNELS = {`  
    `"Pastor Name": "CHANNEL_ID"`  
`}`

Constraints:

* Static dictionary only.

* No runtime editing.

* No external config loading.

---

## **7\. Fetch Layer**

---

## **7.1 RSS Fetcher**

### **services/rss\_fetcher.py**

Responsibilities:

* Fetch latest entries via RSS.

* Extract minimal metadata.

* Return raw entries only.

`import feedparser`

`def fetch_rss(channel_id: str):`  
    `url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"`  
    `return feedparser.parse(url)`

No transformation here.

---

## **7.2 yt-dlp Fetcher**

### **services/ytdlp\_fetcher.py**

Responsibilities:

* Metadata expansion beyond RSS limit.

* Subprocess execution only.

Command:

`yt-dlp --dump-json --flat-playlist CHANNEL_URL`

Implementation rules:

* stdout parsed line-by-line.

* No downloads permitted.

* No file writing.

---

## **8\. Normalization Layer**

### **services/normalizer.py**

This layer converts raw data into `VideoItem`.

Responsibilities:

* Schema enforcement.

* Timestamp parsing.

* Embed URL creation.

* Missing value handling.

Embed format:

`https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&playsinline=1`

Sorting:

`published DESC`

No ranking logic allowed.

---

## **9\. Cache Layer**

### **utils/cache.py**

All fetch functions wrapped with:

`@st.cache_data(ttl=3600)`

Cache key must include:

* channel\_id

* fetch method

Cache invalidation occurs only via TTL expiration.

---

## **10\. Presentation Layer**

---

## **10.1 CSS Injection**

### **ui/css.py**

Injected once at app startup.

Required rules:

* Hide Streamlit header

* Hide footer

* Remove menu

* Disable text selection

* Rounded thumbnails

* Reduced padding

* Sidebar collapsed by default

Example:

`def inject_css():`  
    `st.markdown("""`  
    `<style>`  
    `header {visibility: hidden;}`  
    `footer {visibility: hidden;}`  
    `.stApp {padding-top: 0rem;}`  
    `img {border-radius: 14px;}`  
    `* {user-select: none;}`  
    `</style>`  
    `""", unsafe_allow_html=True)`

---

## **10.2 Grid Rendering**

### **ui/video\_grid.py**

Responsibilities:

* Responsive grid rendering only.

* No data manipulation.

Rules:

| Device Width | Columns |
| ----- | ----- |
| \< 900px | 2 |
| ≥ 900px | 3 |

Implementation:

`cols = st.columns(n)`

Each item displays:

* thumbnail

* title

* embedded player on click

---

## **10.3 Layout Controller**

### **ui/layout.py**

Responsibilities:

* Sidebar channel selector

* Search input

* Focus Mode toggle

Focus Mode behavior:

* Grid hidden

* Player expands to viewport height

* Exit restores grid

---

## **11\. Application Entry Point**

### **app.py**

Execution order:

`1. Inject CSS`  
`2. Load channels`  
`3. Select channel`  
`4. Fetch data (cached)`  
`5. Normalize data`  
`6. Render grid`

No deviation permitted.

---

## **12\. iOS Playback Requirements**

The system must:

* Use iframe embed only.

* Preserve native controls.

* Allow AirPlay via iOS player.

Forbidden:

* custom JS players

* HLS manipulation

* overlay controls

---

## **13\. Performance Constraints**

Expected behavior:

* Initial load fetches once.

* Subsequent reruns use cache.

* UI updates do not trigger refetch.

Target:

* \<1 second UI rerender.

---

## **14\. Deterministic Guardrails**

Execution agent must not introduce:

* APIs

* authentication

* analytics

* recommendation systems

* ranking algorithms

* persistent databases

If implementation uncertainty exists:

Default action \= omit feature.

---

## **15\. Phase Completion Criteria**

The build is complete when:

* Channel selection updates grid instantly.

* Videos play inline on iPad/iPhone.

* AirPlay is available.

* No navigation to youtube.com occurs.

* Metadata refreshes hourly via cache.

