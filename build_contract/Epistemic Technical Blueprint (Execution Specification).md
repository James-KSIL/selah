### **Epistemic Technical Blueprint (Execution Specification)**

---

## **0\. System Philosophy (Non-Negotiable Constraints)**

The system exists to aggregate and display YouTube content without introducing discovery mechanisms or behavioral manipulation.

The application:

* **Aggregates only**

* **Does not recommend**

* **Does not rank**

* **Does not personalize**

* **Does not mutate source data**

All outputs are direct transformations of retrieved feed metadata.

No inference layers exist.

---

## **1\. System Scope Definition**

### **1.1 Functional Objective**

Provide a mobile-first portal that:

1. Retrieves videos from predefined YouTube Channel IDs.

2. Displays videos in a clean grid layout.

3. Embeds videos without external navigation pathways.

4. Preserves native iOS playback features (AirPlay).

### **1.2 Non-Goals**

The system must not:

* Use YouTube API v3.

* Store user accounts or preferences.

* Provide recommendations.

* Provide comments or external links.

* Modify playback behavior beyond embed parameters.

---

## **2\. Architecture Overview**

### **2.1 High-Level Flow**

`RSS_CHANNELS`  
      `↓`  
`Fetch Layer`  
`(feedparser / yt-dlp)`  
      `↓`  
`Normalization Layer`  
`(dict schema)`  
      `↓`  
`Cache Layer`  
`(st.cache_data)`  
      `↓`  
`Presentation Layer`  
`(Streamlit UI)`

No cross-layer coupling is permitted.

---

## **3\. Data Model (Single Source of Truth)**

All video objects must conform to a single schema.

### **3.1 Video Object Schema**

`VideoItem = {`  
    `"video_id": str,`  
    `"title": str,`  
    `"channel_name": str,`  
    `"published": datetime,`  
    `"thumbnail": str,`  
    `"duration": int | None,   # seconds`  
    `"url": str,               # https://youtube.com/watch?v=`  
    `"embed_url": str          # https://www.youtube.com/embed/`  
`}`

Rules:

* Missing fields must be `None`.

* No derived ranking fields allowed.

* Sorting is strictly chronological (descending).

---

## **4\. Phase 1 — MVP ("Static Portal")**

### **4.1 Data Retrieval Logic**

RSS endpoint format:

`https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}`

Implementation rules:

* Use `feedparser`.

* Retrieve latest entries only.

* Limit to 15 items per channel.

* No pagination logic.

### **4.2 Channel Registry**

`RSS_CHANNELS = {`  
    `"Pastor Name": "CHANNEL_ID",`  
`}`

This dictionary is authoritative.

No dynamic channel discovery.

---

### **4.3 UI Behavior**

#### **Layout Rules**

| Device | Columns |
| ----- | ----- |
| iPhone | 2 |
| iPad | 3 |

Implementation:

* Use `st.columns()`

* Column count determined via viewport width heuristic.

#### **Video Rendering**

Embed format:

`https://www.youtube.com/embed/{VIDEO_ID}?rel=0&modestbranding=1`

Required parameters:

* `rel=0`

* `modestbranding=1`

* `playsinline=1`

---

### **4.4 Execution Requirements**

The UI must:

* Show thumbnail

* Show title

* Launch embedded player on click

* Never open youtube.com directly

---

## **5\. Phase 2 — Metadata Enhancement ("Archive")**

### **5.1 Problem Statement**

RSS feeds are limited to recent entries.

Solution: use yt-dlp for metadata expansion only.

### **5.2 Execution Rules**

yt-dlp is used strictly as a metadata extractor.

Allowed command:

`yt-dlp --dump-json --flat-playlist CHANNEL_URL`

Forbidden:

* Downloading video files

* Transcoding

* Media storage

---

### **5.3 Fetch Flow**

`Channel ID`  
    `↓`  
`Channel URL`  
    `↓`  
`yt-dlp subprocess`  
    `↓`  
`JSON output`  
    `↓`  
`Schema normalization`

---

### **5.4 Caching Rules**

All fetch operations must be wrapped with:

`@st.cache_data(ttl=3600)`

Cache key components:

* channel\_id

* fetch\_method ("rss" or "ytdlp")

---

### **5.5 Search Behavior**

Search operates only on:

* title

* channel\_name

Implementation:

* client-side filtering

* no fuzzy matching

* case-insensitive substring match

---

## **6\. Phase 3 — iOS Optimization ("App Feel")**

### **6.1 CSS Injection Rules**

Injected via:

`st.markdown("<style>...</style>", unsafe_allow_html=True)`

Required changes:

* Hide Streamlit header

* Hide footer

* Remove menu button

* Disable text selection

* Rounded thumbnail corners (12–16px)

* Reduce vertical padding

* Sidebar collapsed by default

---

### **6.2 Focus Mode**

Behavior:

* Clicking Focus Mode expands player container to viewport height.

* Grid hidden during playback.

* Exit returns to grid position.

No fullscreen JS hacks; rely on iframe/native controls.

---

### **6.3 iOS Playback Requirements**

Use:

`st.video(embed_url)`

Constraints:

* Must trigger native iOS playback controls.

* AirPlay icon must remain available.

* No custom video players.

---

## **7\. Performance Constraints**

* No fetch occurs on every rerun.

* Cached data reused within TTL.

* UI re-renders must not invalidate cache.

Expected load:

* \< 1 second UI rerender

* Metadata fetch only once per hour per channel.

---

## **8\. Deterministic Guardrails (Anti-Hallucination Rules)**

Execution agent must not:

* Introduce APIs.

* Introduce authentication.

* Add recommendation logic.

* Store persistent user state.

* Add analytics or tracking.

If a requirement is ambiguous:

* Default to omission, not invention.

---

## **9\. Definition of Done (Phase Complete)**

Phase is complete when:

* Videos load without navigating away from app.

* Mobile scrolling remains smooth.

* AirPlay works on iOS.

* No external YouTube navigation exists.

* Cache prevents repeated fetches.

