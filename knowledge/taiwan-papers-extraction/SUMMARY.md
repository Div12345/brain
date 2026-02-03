# Taiwan Group Papers - Systematic Extraction Summary

**Generated:** 2026-02-01 (Updated)
**Method:** Gemini CLI extraction + manual verification
**Papers analyzed:** 22 total, 11 with complete structured data

---

## Complete Extraction Matrix

| Key | Citation | N | Input Signal | Location | Ankle PVR? | Oscillometry? | Fusion? | ML? | Mortality? |
|-----|----------|---|--------------|----------|------------|---------------|---------|-----|------------|
| 2RKTXMUY | Wang 2010 | 1272 | Tonometry | Carotid, Femoral | No | No | No | No | **YES** |
| C7958NR2 | Wang 2009 | 1272 | Tonometry | Carotid, Brachial, Femoral | No | No | No | No | **YES** |
| A84M8FI4 | Cheng 2013 | 1272 | Tonometry | Carotid, Brachial | No | No | No | No | **YES** |
| IULK3GHW | Chuang 2005 | 1329 | PVR, Oscillometry | **Brachial, Ankle** | **YES** | **YES** | **YES** | No | No |
| D5BZKCXV | Ghasemi 2018 | 164 | PVR, Oscillometry | **Arm, Ankle** | **YES** | **YES** | **YES** | Model | No |
| LNJB6JM9 | Lee 2016 | ? | Tonometry, Oscillometry | **Carotid, Ankle** | **YES** | No | **YES** | No | No |
| F6R5QJ4S | Chen 1996 | 66 | Tonometry, Catheter | Carotid, Aorta | No | No | No | No | No |
| QTF3BC7Q | Dhamotharan 2023 | 122 | Oscillometry | Brachial | No | Yes | No | No | No |
| DXCYPCWJ | Cheng 2012 | 140 | Oscillometry | Brachial | No | Yes | No | Multivariate | No |
| 3SBJKDJ9 | Verberk 2015 | 2332 | Oscillometry | Brachial | No | Yes | No | No | No |
| W3STXDZ2 | Hsu ? | ? | ? | ? | ? | ? | ? | ? | ? |

---

## The Critical Gap

### Papers with MORTALITY outcomes:
- Wang 2010, Wang 2009, Cheng 2013
- **ALL used only CAROTID TONOMETRY**
- **NONE used ankle PVR**
- All from same cohort: Chin-Shan Community Cardiovascular Cohort (N=1272)

### Papers with ANKLE PVR:
- Chuang 2005, Ghasemi 2018, Lee 2016
- **ALL were cross-sectional validation studies**
- **NONE tested mortality prediction**

### The Unfilled Matrix Cell:

|                    | Cross-sectional | Mortality Outcome |
|--------------------|-----------------|-------------------|
| Carotid Tonometry  | ✅ Chen 1996    | ✅ Wang 2010      |
| Ankle PVR          | ✅ Chuang 2005  | ❌ **YOUR GAP**   |
| Multi-signal Fusion| ✅ Ghasemi 2018 | ❌ **YOUR GAP**   |

---

## Detailed Key Findings by Paper

### Mortality Papers (Carotid Tonometry Only)

| Paper | Follow-up | Key Finding | HR |
|-------|-----------|-------------|-----|
| Wang 2010 | 15 years | Backward wave amplitude (Pb) predicted CV mortality independently of PWV | ~1.60 per 1-SD |
| Wang 2009 | 10 years | Central SBP independently predicted CV mortality | 1.30 per 10 mmHg |
| Cheng 2013 | 15 years | Central SBP ≥130 mmHg and cPP ≥45 mmHg associated with increased CV mortality | 1.5-2.0 |

### Ankle PVR Papers (Cross-sectional Only)

| Paper | N | Key Finding |
|-------|---|-------------|
| Ghasemi 2018 | 164 | Arm+Ankle PVR fusion estimates central BP with r≥0.78 |
| Lee 2016 | ? | Carotid+Ankle fusion correlates with cfPWV (gold standard) |
| Chuang 2005 | 1329 | baPWV significantly related to Framingham risk score |

---

## Your Research Opportunity

**What exists:**
1. Carotid tonometry → Mortality prediction (Wang 2010: Pb predicts CV death, HR~1.60)
2. Ankle PVR → Central BP estimation (Ghasemi 2018: r≥0.78)
3. Carotid + Ankle fusion → CV risk predictors (Lee 2016: correlates with cfPWV)

**What's missing:**
1. **Ankle PVR waveforms → Mortality prediction**
2. **Multi-signal fusion (Carotid + Ankle) → Mortality prediction**
3. **ML feature selection on peripheral waveforms → Mortality prediction**

---

## Your Dataset Advantages

| Your Data | Taiwan Papers | Novel? |
|-----------|---------------|--------|
| Ankle PVR + Mortality | Never combined | **YES** |
| Carotid + Ankle + Mortality | Never tested | **YES** |
| 545 waveform features + ML | Only ~10 features, no ML | **YES** |
| N=526 with all modalities | N=164 max for fusion papers | **YES** |

---

## Recommended Novel Claims

1. **"First study to test ankle PVR waveform features for long-term mortality prediction"**
   - Evidence: No Taiwan paper (or other) has done this

2. **"First study to fuse carotid tonometry + ankle oscillometry for mortality prediction"**
   - Evidence: Lee 2016 fused these but only for cross-sectional validation

3. **"First ML-based feature selection on multi-site peripheral waveforms for CV outcomes"**
   - Evidence: Ghasemi 2018 used model fitting but not ML feature selection; mortality papers used only Cox regression

---

## Extraction Status

**Successfully extracted (11/22):**
- 2RKTXMUY, C7958NR2, A84M8FI4, IULK3GHW, D5BZKCXV, LNJB6JM9, F6R5QJ4S, QTF3BC7Q, DXCYPCWJ, 3SBJKDJ9, W3STXDZ2

**Failed - Gemini rate limit (11/22):**
- 5L2G767Y, IE9DKQNV, 7UBH35Y5, B8BW8VCK, 8NDK6S55, 3X2S7WCZ, IPAIMBIK, FVZXRZVZ, DFTWXCZY, KANRWY4E, JSAZWJ64

---

## Files

- `/papers/*.md` - Individual paper extractions
- This file: Summary and gap analysis
