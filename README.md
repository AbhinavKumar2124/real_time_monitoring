# Real-Time System Monitor

A real-time system monitoring dashboard built with Streamlit and Flask that provides live insights into your system's performance.

## Features

- **Real-time Monitoring**
  - CPU Usage
  - Memory Usage
  - Disk Usage
  - Network Speed
  - Process Management

- **Interactive Dashboard**
  - Live-updating charts
  - Process management capabilities
  - Customizable alert thresholds
  - Dark/Light theme support

- **Process Management**
  - View all running processes
  - Pause/Resume processes
  - Kill processes
  - Sort by CPU/Memory usage

- **Alert System**
  - Set custom thresholds for CPU, Memory, and Disk usage
  - Enable/Disable alerts
  - Real-time alert notifications

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/real_time_monitoring.git
cd real_time_monitoring
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the backend server:
```bash
cd backend
python app.py
```

2. In a new terminal, start the frontend:
```bash
cd frontend
streamlit run dashboard.py
```

3. Open your web browser and navigate to:
```
http://localhost:8501
```

## Project Structure

```
real_time_monitoring/
├── backend/
│   └── app.py
├── frontend/
│   ├── dashboard.py
│   └── style.css
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/)
- [psutil](https://psutil.readthedocs.io/)
- [Plotly](https://plotly.com/) 