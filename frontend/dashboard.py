import streamlit as st
import requests
import time
import plotly.graph_objects as go
from collections import deque
import pandas as pd
import os
#---------------------------------------------------------------------------------------------
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from streamlit.components.v1 import html

# Load CSS
def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

API_URL = 'http://localhost:5000/api/system_stats'
PROCESS_URL = 'http://localhost:5000/api/processes'
MANAGE_URL = 'http://localhost:5000/api/process_manager'
API_ALERTS = "http://localhost:5000/api/set_alerts"
API_GET_ALERTS = "http://localhost:5000/api/get_alerts"
API_CHECK_ALERTS = "http://localhost:5000/api/check_alerts"
API_TOGGLE_ALERTS = "http://localhost:5000/api/toggle_alerts"

st.set_page_config(page_title='System Monitor', page_icon=':computer:', layout='wide', initial_sidebar_state='collapsed')

# Load CSS
load_css()

st.sidebar.image("logo name.png", width=300)
st.sidebar.title('Monitor. Analyze. Control.')
st.sidebar.divider()
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
page = st.sidebar.radio("Go to", ["Home", "Process Manager", "Alerts & Customization", "About Us (. ❛ ᴗ ❛.) (>'-'<) (◠‿◠✿)"], key="page_selector")

# Create empty containers for each page
home_container = st.empty()
process_container = st.empty()
alerts_container = st.empty()
about_container = st.empty()

if page == "Home":
#This is the home page of the system monitor, displaying the CPU, Memory, Disk, and Network usage alongwith their respective charts.
#-----------------------------------------------------------------------------------------------------------------------------------
    with home_container.container():
        st.divider()
        col1, col2, col3 = st.columns([4, 1.5, 2])
        with col1:
            # Custom title and description with HTML/CSS
            st.markdown("""
                <div style='text-align: left; padding: 1em 0;'>
                    <h1 style='
                        font-size: 3.5em; 
                        margin-bottom: 0.2em;
                        background: linear-gradient(120deg, #2cc012, #03ca66);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        text-fill-color: transparent;
                        font-weight: 600;
                        letter-spacing: -1px;
                        text-shadow: 2px 2px 10px rgba(44, 192, 18, 0.2);
                        font-family: "Poppins", sans-serif;
                    '>Real-Time<br>System Monitoring Solution</h1>
                    <p style='
                        font-size: 1.2em; 
                        margin-bottom: 2em;
                        background: linear-gradient(120deg, #03ca66, #2cc012);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        text-fill-color: transparent;
                        opacity: 0.9;
                        font-family: "Montserrat", sans-serif;
                    '>
                        Keep a real‑time pulse on your machine’s health with dynamic dashboards that track CPU, memory, disk, and network metrics through interactive visualizations and customizable alerts. Seamlessly control processes—pausing, resuming, or terminating them directly from your browser—and receive instant notifications whenever performance drifts beyond your defined thresholds. Crafted for both power users and IT professionals alike, this local‑first solution delivers deep insights and hands‑on control without ever leaving your desktop.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # if st.button("Execute Command"):
            #     page = "Process Manager"

        with col3:
            st.image("logo combined new.png", width=600)

        st.divider()

        st.title('Task Manager')

        # Placeholders for metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cpu_placeholder = st.metric(label='CPU', value='Loading...', delta=None)

        with col2:
            memory_placeholder = st.metric(label='Memory', value='Loading...', delta=None)

        with col3:
            disk_placeholder = st.metric(label='System Disk', value='Loading...', delta=None)
            #disk_placeholder = st.markdown('**System Disk**')

        with col4:
            network_placeholder = st.metric(label='Network', value='Loading...', delta=None)
            #network_placeholder = st.empty()

        st.divider()

        history_length = 30

        #cpu_history = deque(maxlen=history_length)
        cpu_history = deque([0] * history_length, maxlen=history_length)
        #memory_history = deque(maxlen=history_length)
        memory_history = deque([0] * history_length, maxlen=history_length)
        #disk_history = deque(maxlen=history_length)
        disk_history = deque([0] * history_length, maxlen=history_length)
        upload_speed_history = deque([0] * history_length, maxlen=history_length)
        download_speed_history = deque([0] * history_length, maxlen=history_length)

        #timestamps = deque(maxlen=history_length)
        timestamps = deque([""] * history_length, maxlen=history_length)

        global previous_sent, previous_recv
        previous_sent = None
        previous_recv = None
        x_labels = list(range(-history_length + 1, 1))

        # Placeholders for charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("CPU Usage")
            cpu_chart = st.empty()

        with col2:
            st.subheader("Memory Usage")
            memory_chart = st.empty()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("System Disk Usage")
            disk_chart = st.empty()

        with col2:
            st.subheader("Network Usage")
            network_chart = st.empty()

        st.divider()

        def fetch_data():
            try:
                response = requests.get(API_URL)
                return response.json()
            except:
                return None
            
        while True:
            data = fetch_data()
            #st.write(data)
            if data:
                # Updating placeholders
                cpu_placeholder.metric(label="CPU", value=f"{data['cpu']:.2f}% Used")

                memory_placeholder.metric(
                    label="Memory",
                    value=f"{data['memory']['used']} GB / {data['memory']['total']} GB",
                    delta=f"{data['memory']['percent']}% Used ({data['memory']['available']} GB available)"
                )

                disk_placeholder.metric(
                    label="System Disk",
                    value=f"{data['disk']['used']} GB / {data['disk']['total']} GB",
                    delta=f"{data['disk']['percent']}% Used ({data['disk']['free']} GB available)"
                )

                # Network Speed Calculation
                if previous_sent is not None and previous_recv is not None:
                    upload_speed = (data["network"]["bytes_sent"] - previous_sent) * 1024  # KBps
                    download_speed = (data["network"]["bytes_recv"] - previous_recv) * 1024 # KBps
                else:
                    upload_speed = 0
                    download_speed = 0

                previous_sent = data["network"]["bytes_sent"]
                previous_recv = data["network"]["bytes_recv"]

                network_placeholder.metric(
                    label="Network Speed (KBps)",
                    value=f"⬆ {upload_speed:.2f} | ⬇ {download_speed:.2f}"
                )

                # Updating histories
                timestamps.append(time.strftime("%H:%M:%S"))
                cpu_history.append(data['cpu'])
                memory_history.append(data['memory']['percent'])
                disk_history.append(data['disk']['percent'])
                upload_speed_history.append(upload_speed)
                download_speed_history.append(download_speed)

                # Updating charts
                cpu_fig = go.Figure()
                cpu_fig.add_trace(go.Scatter(
                    x=x_labels,
                    y=list(cpu_history),
                    mode='lines',
                    name="CPU Usage",
                    line=dict(color="#39FF14", width=2),
                    fill='tozeroy',
                    fillcolor='rgba(57, 255, 20, 0.1)'
                ))
                cpu_fig.update_xaxes(tickvals=x_labels, ticktext=list(timestamps), showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                cpu_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                cpu_fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False,
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        range=[0, 100]
                    ),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    yaxis_title='CPU Usage (%)'
                )
                cpu_chart.plotly_chart(cpu_fig, use_container_width=True)
                
                memory_fig = go.Figure()
                memory_fig.add_trace(go.Scatter(
                    x=x_labels,
                    y=list(memory_history),
                    mode='lines',
                    name="Memory Usage",
                    line=dict(color="#40E0D0", width=2),
                    fill='tozeroy',
                    fillcolor='rgba(64, 224, 208, 0.1)'
                ))
                memory_fig.update_xaxes(tickvals=x_labels, ticktext=list(timestamps), showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                memory_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                memory_fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False,
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        range=[0, 100]
                    ),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    yaxis_title='Memory Usage (%)'
                )
                memory_chart.plotly_chart(memory_fig, use_container_width=True)
                
                disk_fig = go.Figure()
                disk_fig.add_trace(go.Scatter(
                    x=x_labels,
                    y=list(disk_history),
                    mode='lines',
                    name="Disk Usage",
                    line=dict(color="#FF69B4", width=2),
                    fill='tozeroy',
                    fillcolor='rgba(255, 105, 180, 0.1)'
                ))
                disk_fig.update_xaxes(tickvals=x_labels, ticktext=list(timestamps), showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                disk_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                disk_fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False,
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        range=[0, 100]
                    ),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    yaxis_title='Disk Usage (%)'
                )
                disk_chart.plotly_chart(disk_fig, use_container_width=True)

                network_fig = go.Figure()
                network_fig.add_trace(go.Scatter(
                    x=x_labels,
                    y=list(upload_speed_history),
                    mode='lines',
                    name="Upload Speed",
                    line=dict(color="#E13F75", width=2),
                    fill='tozeroy',
                    fillcolor='rgba(225, 63, 117, 0.1)'
                ))
                network_fig.update_xaxes(tickvals=x_labels, ticktext=list(timestamps), showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                network_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#4F4C4D')
                network_fig.add_trace(go.Scatter(
                    x=x_labels,
                    y=list(download_speed_history),
                    mode='lines',
                    name="Download Speed",
                    line=dict(color="#8F26AB", width=2),
                    fill='tozeroy',
                    fillcolor='rgba(143, 38, 171, 0.1)'
                ))
                network_fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01,
                        font=dict(color='#ffffff'),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    yaxis_title='Speed (KBps)'
                )
                network_chart.plotly_chart(network_fig, use_container_width=True)

            time.sleep(0.5)

#Homepage completed.
#-----------------------------------------------------------------------------------------------------------------------------------


elif page == "Process Manager":
#This is the process manager page of the system monitor, displaying the list of processes running on the system.
#-----------------------------------------------------------------------------------------------------------------------------------
    with process_container.container():
        col1, col2 = st.columns([3.7, 2])
        with col1:
            st.markdown("""
                <div style='text-align: left; padding: 1em 0;'>
                    <h1 style='
                        font-size: 3.5em; 
                        margin-bottom: 0.2em;
                        background: linear-gradient(120deg, #2cc012, #03ca66);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        text-fill-color: transparent;
                        font-weight: 600;
                        letter-spacing: -1px;
                        text-shadow: 2px 2px 10px rgba(44, 192, 18, 0.2);
                        font-family: "Poppins", sans-serif;
                    '>Process Manager</h1>
                    <p style='
                        font-size: 1.2em; 
                        margin-bottom: 2em;
                        background: linear-gradient(120deg, #03ca66, #2cc012);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        text-fill-color: transparent;
                        opacity: 0.9;
                        font-family: "Montserrat", sans-serif;
                    '>
                        Gain complete visibility and control over all running system processes with real-time insights into process IDs, CPU and memory usage, execution states, and more. Effortlessly sort, search, and terminate processes from an intuitive interface designed for precision and performance—all without leaving your browser.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Initialize session state if not exists
        if 'selected_pid' not in st.session_state:
            st.session_state.selected_pid = None
        if 'selected_action' not in st.session_state:
            st.session_state.selected_action = "Pause"
        
        def fetch_processes():
            try:
                response = requests.get(PROCESS_URL)
                return response.json()
            except:
                return None

        process_data = processes_data = fetch_processes()

        # Callback functions to update session state
        def update_pid():
            st.session_state.selected_pid = st.session_state.pid_selectbox
        
        def update_action():
            st.session_state.selected_action = st.session_state.action_selectbox

        # Create two columns for the layout
        col1, col2 = st.columns([1, 5])

        with col1:
            st.title("Manage Processes")
            
            # Fetch current processes for the selectbox
            if process_data:
                df = pd.DataFrame(process_data)
                # Use session state for selectbox values
                st.selectbox(
                    "Select Process ID (PID):", 
                    df["pid"], 
                    key="pid_selectbox",
                    index=df["pid"].tolist().index(st.session_state.selected_pid) if st.session_state.selected_pid in df["pid"].tolist() else 0,
                    on_change=update_pid
                )
                st.selectbox(
                    "Action", 
                    ["Pause", "Resume", "Kill"],
                    key="action_selectbox",
                    index=["Pause", "Resume", "Kill"].index(st.session_state.selected_action),
                    on_change=update_action
                )
                
                if st.button("Execute"):
                    response = requests.post(MANAGE_URL, json={
                        "pid": st.session_state.selected_pid, 
                        "action": st.session_state.selected_action
                    })
                    if response.json().get("status") == "success":
                        st.success(response.json().get("message"))
                    else:
                        st.error(response.json().get("message"))
                st.button("Click \"if process is not in the list\"")
                st.divider()
            else:
                st.warning("No processes available to manage.")


        with col2:
            st.subheader('Running Processes')
            table_placeholder = st.empty()
            
            while True:
                if processes_data:
                    df = pd.DataFrame(processes_data)
                    df = df.sort_values(by='cpu_percent', ascending=False)
                    df_new = df[['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']]
                    df_new['pid'] = df_new['pid'].astype(str)
                    df_new['cpu_percent'] = df_new['cpu_percent'].round(2).astype(str) + '%'
                    df_new['memory_percent'] = df_new['memory_percent'].round(2).astype(str) + '%'
                    df_new.columns = ['Process ID', 'Process Name', 'User', 'CPU Usage', 'Memory Usage', 'Status']
                    table_placeholder.dataframe(df_new, hide_index=True, height=700, use_container_width=True)
                else:
                    table_placeholder.warning("No processes found on the system.")
                processes_data = fetch_processes()
                time.sleep(0.5)
#Process Manager page completed.
#-----------------------------------------------------------------------------------------------------------------------------------


elif page == "Alerts & Customization":
#This is the alerts and customization page of the system monitor, displaying the list of alerts and customization options.
#-----------------------------------------------------------------------------------------------------------------------------------
    with alerts_container.container():
        st.markdown("""
            <div style='text-align: left; padding: 1em 0;'>
                <h1 style='
                    font-size: 3.5em; 
                    margin-bottom: 0.2em;
                    background: linear-gradient(120deg, #2cc012, #03ca66);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    text-fill-color: transparent;
                    font-weight: 600;
                    letter-spacing: -1px;
                    text-shadow: 2px 2px 10px rgba(44, 192, 18, 0.2);
                    font-family: "Poppins", sans-serif;
                '>Alerts & Customization</h1>
                <p style='
                    font-size: 1.2em; 
                    margin-bottom: 2em;
                    background: linear-gradient(120deg, #03ca66, #2cc012);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    text-fill-color: transparent;
                    opacity: 0.9;
                    font-family: "Montserrat", sans-serif;
                '>
                    Implement real-time alert systems to notify users of critical events based on customizable triggers.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Fetch current alert settings
        def fetch_alert_settings():
            try:
                return requests.get(API_GET_ALERTS).json()
            except:
                return {"cpu": 90, "memory": 90, "disk": 90, "enabled": True}

        alert_settings = fetch_alert_settings()

        col1, col2, col3 = st.columns([7, 9, 2.25])
        with col1:
            # Alert Thresholds
            st.subheader("Set Alert Thresholds")
            cpu_threshold = st.slider("CPU Alert (%)", 10, 100, alert_settings["cpu"])
            memory_threshold = st.slider("Memory Alert (%)", 10, 100, alert_settings["memory"])
            disk_threshold = st.slider("Disk Alert (%)", 10, 100, alert_settings["disk"])

            # Save button
            if st.button("Save Alert Settings"):
                data = {
                    "cpu": cpu_threshold,
                    "memory": memory_threshold,
                    "disk": disk_threshold
                }
                response = requests.post(API_ALERTS, json=data)
                st.success(response.json()["message"])

        with col3:
            # Enable/Disable Alerts
            st.divider()
            st.subheader("Alert Status")
            alerts_enabled = st.checkbox("Enable Alerts", alert_settings["enabled"])
            if st.button("Update Alert Status"):
                response = requests.post(API_TOGGLE_ALERTS, json={"enabled": alerts_enabled})
                st.success(response.json()["message"])
            st.divider()

        st.divider()
        
        # Display Active Alerts
        st.subheader("Active Alerts")
        try:
            alerts = requests.get(API_CHECK_ALERTS).json()["alerts"]
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("✅ No active alerts!")
        except:
            st.error("❌ Error fetching alerts")
#Alerts and Customization page completed.
#-----------------------------------------------------------------------------------------------------------------------------------

elif page == "About Us (. ❛ ᴗ ❛.) (>'-'<) (◠‿◠✿)":
#This is the about us page of the system monitor, displaying the information about the developers of the system monitor.
#-----------------------------------------------------------------------------------------------------------------------------------
    with about_container.container():
        def image_to_base64(image):
            try:
                buffered = BytesIO()
                image.save(buffered, format="PNG", optimize=True)
                return base64.b64encode(buffered.getvalue()).decode()
            except Exception as e:
                st.error(f"Error converting image to base64: {str(e)}")
                return ""

        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Team member information
        team_members = {
            "abhinav": {
                "name": "ABHINAV",
                "image": "img2.jpg",
                "role": "Backend Developer"
            },
            "udit": {
                "name": "UDIT KATIYAR",
                "image": "img1.jpg",
                "role": "Frontend Developer"
            },
            "arshia": {
                "name": "ARSHIA SINGH",
                "image": "img3.jpg",
                "role": "UI/UX Designer"
            }
        }

        # Load team images with better error handling
        team_images = {}
        for member_id, member_info in team_members.items():
            try:
                img_path = os.path.join(base_dir, member_info["image"])
                if os.path.exists(img_path):
                    team_images[member_id] = Image.open(img_path)
                else:
                    raise FileNotFoundError(f"Image file not found: {member_info['image']}")
            except Exception as e:
                st.error(f"Error loading {member_info['image']}: {str(e)}")
                # Create a placeholder image with member's initial
                team_images[member_id] = Image.new('RGB', (400, 500), (0, 0, 0))
                # Add text to placeholder image
                draw = ImageDraw.Draw(team_images[member_id])
                font = ImageFont.truetype("arial.ttf", 100)
                draw.text((150, 200), member_info["name"][0], fill=(57, 255, 20), font=font)

        st.markdown("""
        <style>
            .team-container {
                display: flex;
                justify-content: center;
                gap: 30px;
                margin: 2rem 0;
                flex-wrap: wrap;
            }
            .team-card {
                width: 300px;
                background: rgba(44, 192, 18, 0.05);
                border-radius: 15px;
                padding: 0;
                margin: 0 auto;  /* Center the card */
                border: 1px solid rgba(44, 192, 18, 0.2);
                transition: all 0.3s ease;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                align-items: center;  /* Center content horizontally */
            }
            .team-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 0 20px rgba(57, 255, 20, 0.8);
            }
            .profile-img {
                width: 100%;
                height: 400px;
                object-fit: cover;
                display: block;
                transition: all 0.3s ease;
                margin: 0 auto;  /* Center the image */
            }
            .profile-img:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 0 20px rgba(57, 255, 20, 0.7) !important;
            }
            .team-name {
                text-align: center;
                font-size: 1.5rem;
                margin: 15px 0 5px 0;
                background: linear-gradient(120deg, #2cc012, #03ca66);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
                width: 100%;  /* Ensure full width for centering */
            }
            .team-role {
                text-align: center;
                font-size: 1rem;
                margin: 0 0 30px 0;
                color: rgba(44, 192, 18, 0.7);
                font-family: 'Montserrat', sans-serif;
                width: 100%;  /* Ensure full width for centering */
            }
            .main-heading {
                text-align: center;
                margin-bottom: 2rem;
            }
            @media (max-width: 768px) {
                .team-container {
                    flex-direction: column;
                    align-items: center;
                }
                .team-card {
                    width: 100%;
                    max-width: 300px;
                }
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="main-heading">
            <h1 style='
                font-size: 2.8rem;
                background: linear-gradient(120deg, #2cc012, #03ca66);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-family: "Poppins", sans-serif;
                font-weight: 600;
            '>Meet the Team</h1>
            <p style='
                font-size: 1.1rem; 
                color: rgba(44, 192, 18, 0.7);
                font-family: "Montserrat", sans-serif;
                margin-bottom: 2rem;
            '>
                The brilliant minds behind your monitoring experience
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)  # Add line gap

        # Create team member cards
        cols = st.columns(3)
        for idx, (member_id, member_info) in enumerate(team_members.items()):
            with cols[idx]:
                st.markdown(f"""
                <div class="team-card">
                    <img src="data:image/png;base64,{image_to_base64(team_images[member_id])}" class="profile-img">
                </div>
                <p class="team-name"><br>{member_info['name']}</p>
                <p class="team-role">{member_info['role']}</p>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)  # Add line gap after each card

        st.markdown("<br>", unsafe_allow_html=True)  # Add line gap before project section
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)  # Add line gap after divider

        st.markdown("""
        <div style='
            margin-top: 3rem; 
            padding: 1.5rem; 
            background: rgba(44, 192, 18, 0.03); 
            border-radius: 15px;
            border: 1px solid rgba(44, 192, 18, 0.1);
        '>
            <h2 style='
                color: #2cc012; 
                text-align: center;
                font-family: "Poppins", sans-serif;
                margin-bottom: 1.5rem;
            '>About the Project</h2>
            <p style='
                line-height: 1.6; 
                color: rgba(44, 192, 18, 0.8); 
                text-align: center;
                font-family: "Montserrat", sans-serif;
                margin-bottom: 1.5rem;
            '>
                Our Real-Time System Monitoring Dashboard provides instant insights into your computer's performance metrics.
                Built with passion and cutting-edge technology to deliver:
            </p>
            <ul style='
                color: rgba(44, 192, 18, 0.8); 
                line-height: 1.8; 
                max-width: 600px; 
                margin: 1.5rem auto;
                font-family: "Montserrat", sans-serif;
                margin-bottom: 1.5rem;
            '>
                <li> <strong>Live resource monitoring</strong> (CPU, Memory, Disk, Network)</li>
                <li> <strong>Interactive visualizations</strong> with historical data</li>
                <li> <strong>Process management</strong> capabilities</li>
                <li> <strong>Custom alert system</strong> for thresholds</li>
            </ul>
            <div style='
                margin-top: 2rem; 
                padding: 1.2rem; 
                background: rgba(44, 192, 18, 0.1); 
                border-radius: 10px; 
                max-width: 500px; 
                margin-left: auto; 
                margin-right: auto;
                border: 1px solid rgba(44, 192, 18, 0.2);
            '>
                <p style='
                    text-align: center; 
                    color: #2cc012; 
                    margin: 0; 
                    font-size: 1.1rem;
                    font-family: "Poppins", sans-serif;
                '>
                    <strong>Tech Stack:</strong> Python • Streamlit • Plotly • Flask • Pandas
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

#About Us page completed.
#-----------------------------------------------------------------------------------------------------------------------------------
