# MudraAI — Temporal Landmark Dataset Discovery & Audit Report

**Generated Date:** 2026-10-05  
**Project Location:** `D:\projects\MudraAI`  
**Integration Status:** Complete

---

## 1. Executive Summary

A comprehensive local filesystem scan across mounted drives (`C:\`, `D:\`, and `E:\`) was performed to discover candidate dynamic/temporal landmark datasets from prior project iterations. Three distinct candidate datasets were identified, audited, and evaluated against the technical requirements of the MudraAI Text → Sign pipeline.

The **WLASL-100 / ASL-Recognizer** dataset and **MudraAI_OLD_Backup** were selected as the primary sources of authentic temporal landmark data. **101 sign classes** with genuine temporal motion across 30–45 frames were verified, audited, and copied into `D:\projects\handsignai\temporal_data\`.

---

## 2. Discovered Candidate Datasets

| # | Dataset / Subproject | Absolute Path | Total Files | Sample Shape | Dtype | Feature Dim | Hand Count | Coordinate Format |
|---|----------------------|---------------|-------------|--------------|-------|-------------|------------|-------------------|
| **1** | **ASL-Recognizer (WLASL-100)** | `E:\COD\MACHLI\PROJECT EXHIBITION 1\MudraAI\asl-recognizer\data\landmarks` | 562 `.npy` files (100 folders) | `(30, 126)` | `float32` | 126 | 1 or 2 hands | Wrist-centered relative 3D coordinates (Left: 0..62, Right: 63..125) |
| **2** | **MudraAI_OLD_Backup** | `E:\COD\MACHLI\PROJECT EXHIBITION 1\MudraAI_OLD_Backup\data\landmarks` | 60 `.npy` files (2 folders: Hello, Yes) | `(45, 126)` | `float64` | 126 | 1 or 2 hands | Absolute MediaPipe normalized 3D coordinates |
| **3** | **SignSense** | `E:\COD\MACHLI\PROJECT EXHIBITION 1\MudraAI\SignSense\data\` | 647 `.npy` files | `(48..369, 130)` | `float64` | 130 | 2 hands + 4 avg features | Bounding-box normalized + avg x/y (63+63+2+2) |
| **4** | **Google ASL Competition** | `E:\COD\MACHLI\PROJECT EXHIBITION 1\MudraAI_Datasets\google_asl` | 2346 `.parquet` files | Variable | `float32` | 543 (Holistic) | Face, Pose, Hands | Raw parquet frames |

---

## 3. Detailed Audit & Mathematical Validation

### Candidate 1: ASL-Recognizer (WLASL-100) — **SELECTED**
- **Structure:** 100 sign vocabulary classes (`help`, `yes`, `no`, `what`, `who`, `want`, `need`, `like`, `time`, `walk`, `work`, `wrong`, `book`, `eat`, `drink`, `dance`, `play`, `fine`, `finish`, `give`, `go`, `hot`, `how`, `mother`, `family`, `right`, `table`, etc.).
- **Shape:** `(30, 126)` — 30 sequential frames per sample.
- **Feature Breakdown:**
  - Dimensions 0..62: Left Hand (21 landmarks × 3 coordinates: x, y, z).
  - Dimensions 63..125: Right Hand (21 landmarks × 3 coordinates: x, y, z).
  - Landmark 0 (wrist) is set to `(0, 0, 0)` as origin; Landmark 9 (middle MCP) scale-normalized.
- **Two-Hand Verification:** Verified on two-hand signs (e.g., `help`, `book`, `dance`, `basketball`, `clothes`, `change`) where both left and right hands are actively populated (120 non-zero values per frame) and naturally offset. For one-hand signs (e.g. `yes`, `no`, `what`), the inactive hand is cleanly zero-padded.
- **Temporal Motion Verification:** Mean frame-to-frame diff: `0.0527` to `0.2293` (distinct trajectories across all frames). No duplicate/static frames.

### Candidate 2: MudraAI_OLD_Backup — **SELECTED (Supplementary)**
- **Structure:** 2 classes (`Hello`, `Yes`), 30 files each.
- **Shape:** `(45, 126)` — 45 sequential frames showing a complete waving motion.
- **Feature Breakdown:** 21 landmarks × 3 coords × 2 hands in standard MediaPipe camera coordinates.
- **Temporal Motion:** Verified waving motion trajectory (`Hello_001.npy`, wrist transitions smoothly from `[0.86, 0.78]` to `[0.80, 0.82]`).

### Candidate 3: SignSense — **REJECTED**
- **Reason for Rejection:** Features are encoded as a 130-dimensional engineered vector (`63 + 63 + 2 + 2`), where each frame was independently min-max normalized (`(hand - low) / diff`). This causes independent spatial distortion per frame, making smooth kinematic skeleton reconstruction unstable compared to the raw geometric coordinates of WLASL-100.

### Candidate 4: Google ASL Parquet — **REJECTED**
- **Reason for Rejection:** Stored in tabular `.parquet` format with 543 holistic landmarks rather than clean hand landmark `.npy` sequences. Unnecessary complexity and excessive size.

---

## 4. Language & Domain Honesty

- **Language Identity:** The discovered temporal dataset originates from **American Sign Language (ASL / WLASL-100)**.
- **Technical Position:** It is **NOT** authentic Indian Sign Language (ISL).
- **Presentation Rule:** The UI and reports must explicitly label these as **"ASL Temporal Sequences"** or **"Sign Animation (ASL dataset)"** and must never claim they represent genuine ISL.

---

## 5. Summary of Selected & Copied Resources

- **Destination Directory:** `temporal_data/`
- **Web JSON Cache:** `static/temporal/`
- **Total Copied Classes:** **101 canonical signs**
- **Total `.npy` Files Copied:** 562 files (~8.2 MB)
- **Metadata Record:** `temporal_data/metadata.json`

---

## 6. Integration Architecture

```text
Text Input ("hey pls help me")
   │
   ▼
Deterministic Normalization & Greedy Longest-Phrase Matcher
   │
   ▼
[Hello] (Temporal ASL) ──> [Please] (Static Baseline) ──> [Help] (Temporal ASL) ──> [me] (Unsupported)
   │
   ├─► IF Temporal: Loads JSON sequence ──► Computes Global Bounding Box ──► requestAnimationFrame (30 FPS)
   │
   └─► IF Static: Loads representatives.json ──► Static 2D Skeleton Display with Hold State
```
