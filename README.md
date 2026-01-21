# School & Crypto Timing (Hex-a-thon 2026)

[![Hex](https://img.shields.io/badge/Built%20with-Hex-blueviolet?style=for-the-badge&logo=hex)](https://hex.tech) [![Live App](https://img.shields.io/badge/Live%20App-hex.tech-00d1b2?style=for-the-badge)](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest) [![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github)](https://github.com/Turbo31150/school-crypto-timing)

## Overview

An intelligent data application built with **Hex** that helps teacher-traders discover realistic crypto trading windows by combining school schedules with market signals and AI-powered coaching insights.

### Key Features
- 📊 **Heatmap Analysis**: Visualize optimal trading times (0-100 score) by day and hour
- 🎯 **Smart Filtering**: Filter by cryptocurrency, profitability, market activity, and minimum score
- 📈 **Market Integration**: Real-time analysis with ETL data pipeline
- 🤖 **AI Coaching**: Personalized trading insights based on school calendar constraints
- 💾 **SQLite Database**: Efficient storage with 45+ trading scenarios

## 🚀 Quick Start

### Live Demo
- **[Access Live Application](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/app/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/latest)**
- **[Open Editor (Draft)](https://app.hex.tech/019bce85-8714-7002-a7fc-e8078cad974e/hex/School-Crypto-Timing-032CAGPxUhxFTL3eU6LpRr/draft/logic)**

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Turbo31150/school-crypto-timing.git
   cd school-crypto-timing
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python exécuter.py
   ```

4. **Access in Hex**
   - Import `hex_notebook.py` into your Hex workspace
   - Run all cells sequentially
   - Navigate to the Application tab

## 📋 Project Structure

```
school-crypto-timing/
├── données/                    # Cleaned trading data (45 scenarios)
├── python/                     # Core Python modules
│   └── exécuter.py            # Database initialization script
├── SQL/                        # Database schema and queries
│   └── hackaton.db            # SQLite database (45 scores max 100)
├── hex_notebook.py            # Main Hex notebook
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── HACKATHON_GUIDE.md         # Detailed implementation guide
```

## 🎯 What It Does

1. **Trading Window Analysis**
   - Scores each available time window with a 0-100 "Trading Window Score"
   - Classifies windows into: RED (0-20), ORANGE (21-50), YELLOW (51-79), GREEN (80-100)

2. **Smart Filtering**
   - Filter by cryptocurrency (ETH, SOL, BTC, etc.)
   - Filter by profitability indicators
   - Adjust minimum score threshold
   - Real-time table updates without errors

3. **Interactive Dashboard**
   - Day × Hour heatmap showing trading scores
   - Detailed performance table (45+ rows)
   - Multi-select filter controls
   - Responsive UI for quick decision-making

## 🔧 Technology Stack

- **Hex**: Interactive data notebooks and apps
- **Python 3.x**: Data processing and analysis
- **SQLite**: Lightweight database (45 trading scenarios)
- **Pandas**: Data manipulation and filtering
- **GitHub**: Version control and collaboration

## 📊 Application Status

✅ **PRODUCTION READY**
- ✓ All 7 Hex cells execute without errors
- ✓ Application loads correctly and is responsive
- ✓ Heatmap displays accurate trading scores
- ✓ Filters update dynamically without stacktraces
- ✓ Database contains 45 verified scenarios (max score 100)
- ✓ Reload (Ctrl+F5) maintains state and responsiveness

## 📚 Documentation

- **[HACKATHON_GUIDE.md](HACKATHON_GUIDE.md)** - Complete implementation guide, checklist, video plan, and FAQ
- **[hex_app_improvements.md](hex_app_improvements.md)** - Technical improvements and optimization notes
- **[hex_cells_ready.py](hex_cells_ready.py)** - Minimal cell templates for quick setup
- **[HEX_QUICK_START.md](HEX_QUICK_START.md)** - Step-by-step Hex integration guide

## 🎥 Presentation & Demo

For the hackathon presentation:
1. Access the **Live App** link above
2. Show the heatmap with Thursday 10h-12h peak scores (~100 for ETH/SOL)
3. Demonstrate filter interactions (prof, cryptocurrencies, min_score)
4. Highlight the 45-line trading table with diverse scenarios
5. Reload the page to show stability and responsiveness

## 📝 License

Hackathon Hex 2026 - Educational & Competitive Use

## 👨‍💼 Author

**Turbo31150** - Teacher-Trader & Data Enthusiast

---

**Last Updated**: 2024  
**Status**: ✅ Production Ready for Hackathon Presentation
