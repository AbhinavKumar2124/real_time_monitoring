# 🚀 NODEX - Real-Time System Monitor

<div align="center">
  
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24.0-green)
![Flask](https://img.shields.io/badge/Flask-2.3.0-red)
![License](https://img.shields.io/badge/license-MIT-blue)

</div>

NODEX is a powerful, real-time system monitoring dashboard that provides live insights into your system's performance with a beautiful, modern interface. Built with Streamlit and Flask, NODEX offers comprehensive system monitoring capabilities with an intuitive user experience.

## ✨ Features

### 📊 Real-time Monitoring
- **CPU Usage**: Track processor performance with live-updating charts
- **Memory Usage**: Monitor RAM consumption and available memory
- **Disk Usage**: Keep an eye on storage space and I/O operations
- **Network Speed**: Real-time upload and download speed monitoring
- **Process Management**: Comprehensive process control and monitoring

### 🎨 Interactive Dashboard
- **Live Charts**: Beautiful, responsive charts that update in real-time
- **Process Control**: Intuitive interface for managing system processes
- **Custom Alerts**: Set personalized thresholds for system metrics
- **Theme Support**: Choose between dark and light themes for optimal viewing

### ⚙️ Process Management
- **Process Overview**: Detailed view of all running processes
- **Process Control**: 
  - Pause/Resume processes with a single click
  - Terminate unwanted processes safely
  - Sort processes by CPU or Memory usage
- **Resource Tracking**: Monitor process resource consumption

### 🔔 Smart Alert System
- **Custom Thresholds**: Set limits for CPU, Memory, and Disk usage
- **Flexible Controls**: Enable/Disable alerts as needed
- **Real-time Notifications**: Instant alerts when thresholds are exceeded
- **Visual Indicators**: Color-coded warnings for different alert levels

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start
1. **Clone the repository**:
   ```
   git clone https://github.com/AbhinavKumar2124/real_time_monitoring.git
   cd real_time_monitoring
   ```

2. **Set up virtual environment**:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## 🚀 Getting Started

1. **Start the backend server**:<br>(terminal 1)
   ```
   cd backend
   python app.py
   ```

2. **Launch NODEX**:<br>(terminal 2)
   ```
   cd frontend
   streamlit run dashboard.py
   ```

3. **Access NODEX Dashboard**:
   Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## 📁 Project Structure

```
real_time_monitoring/
├── backend/
│   └── app.py              # Flask backend server
├── frontend/
│   ├── dashboard.py        # NODEX Streamlit frontend
│   └── style.css          # Custom styling
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## 🤝 Contributing

We welcome contributions to NODEX! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing dashboard framework
- [Flask](https://flask.palletsprojects.com/) - For the robust backend server
- [psutil](https://psutil.readthedocs.io/) - For system monitoring capabilities
- [Plotly](https://plotly.com/) - For beautiful, interactive charts

## 📞 Support

For support, open an issue in the repository.

---

<div align="center">
  
Made with ❤️ by Team NODEX

</div> 