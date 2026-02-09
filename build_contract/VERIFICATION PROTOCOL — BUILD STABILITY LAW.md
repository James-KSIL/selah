## **VERIFICATION PROTOCOL — BUILD STABILITY LAW**

---

## **0\. Purpose**

This protocol defines objective checks that must pass before execution proceeds to the next step.

The verification layer exists to prevent:

* silent schema drift

* cross-layer leakage

* unintended refactors

* behavioral changes during iteration

Verification is mechanical. No subjective judgment is permitted.

---

## **1\. Verification Model**

Each build step contains:

`INPUT STATE`  
`↓`  
`IMPLEMENTATION`  
`↓`  
`VERIFICATION CHECK`  
`↓`  
`LOCK OR HALT`

If verification fails:

* execution stops

* no auto-correction occurs

* previous files remain unchanged

---

## **2\. Global Invariants (Always True)**

These must remain true for the lifetime of the project.

### **2.1 Architectural Invariants**

The following imports are forbidden:

| Location | Forbidden Imports |
| ----- | ----- |
| services/\* | streamlit |
| models/\* | streamlit, feedparser, subprocess |
| ui/\* | feedparser, yt-dlp |
| config/\* | any runtime logic |

Verification rule:

`grep import violations`

If violated → halt.

---

### **2.2 Data Invariant**

Only one video schema exists:

`VideoItem`

Verification:

* Search for additional video structures.

* Any duplicate schema causes halt.

---

### **2.3 Navigation Invariant**

No link may navigate to:

`youtube.com/watch`  
`youtube.com/channel`  
`youtube.com/home`

Only embed URLs allowed.

---

## **3\. Lock Point Verification**

---

## **LOCK POINT A — Data Model**

File:

`models/video_item.py`

Verification checks:

* Contains only dataclass definition.

* No functions defined.

* Field names match specification exactly.

* No optional fields added later.

If modified after lock → halt execution.

---

## **LOCK POINT B — Configuration**

File:

`config/channels.py`

Verification checks:

* Contains only dictionary definition.

* No functions.

* No environment variables.

If dynamic loading introduced → halt.

---

## **LOCK POINT C — Normalization**

File:

`services/normalizer.py`

Verification checks:

* Returns List\[VideoItem\].

* Sorting only by published DESC.

* No ranking variables.

* No scoring logic.

If any derived ranking field exists → halt.

---

## **4\. Fetch Layer Verification**

### **RSS Fetcher**

Checks:

* Function returns raw feedparser output.

* No parsing logic.

### **yt-dlp Fetcher**

Checks:

* Command includes:

`--dump-json`  
`--flat-playlist`

* No file writes.

* No downloads.

---

## **5\. Cache Verification**

Checks:

* All fetch calls wrapped with:

`@st.cache_data(ttl=3600)`

* Cache functions do not modify data.

If transformation detected → halt.

---

## **6\. UI Verification**

### **Video Grid**

Checks:

* Accepts List\[VideoItem\] only.

* Does not sort or filter data internally.

### **Layout Controller**

Checks:

* Search operates on existing list only.

* No new data requests.

---

## **7\. Application Flow Verification**

Required execution order:

`inject_css`  
`↓`  
`select_channel`  
`↓`  
`fetch`  
`↓`  
`normalize`  
`↓`  
`render`

Verification:

* No alternate execution path exists.

---

## **8\. Performance Verification**

Manual validation:

* Reload page twice within one hour.

* Confirm fetch layer not re-executed.

* Confirm UI rerender only.

---

## **9\. Regression Guard (Future Iterations)**

Before any future change:

1. Run invariant checks.

2. Confirm lock point files unchanged.

3. Confirm no new dependencies introduced.

If any fail:

Change rejected.

---

## **10\. Completion State**

The system is considered stable when:

* All lock points verified.

* No invariant violations.

* App behavior unchanged across reloads.

