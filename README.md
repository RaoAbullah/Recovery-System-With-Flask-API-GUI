# Recovery-System-With-Flask-API-GUI

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-brightgreen?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**Recovery-System-With-Flask-API-GUI** is a client-server systems management and recovery orchestration application. Combining a versioned RESTful **Flask API** backend with an interactive desktop **Tkinter GUI** client, it provides system administrators with real-time remote node registration, automated event logging, state tracking, and recovery reboot triggers.

---

## 📌 Project Overview

In enterprise server environments, administering recovery nodes and dispatching remote reboot commands often requires reliable, decoupled communication between a lightweight backend service and a user-friendly management console.

This project implements that architecture:
1. **Flask API Microservice (`server.py`):** Acts as the central command node. It manages system registrations, tracks active system states in memory, processes reboot signals, and maintains an append-only audit trail in `event_logs.txt`.
2. **Tkinter GUI Client (`gui recovery system.py`):** A desktop administrative dashboard providing point-and-click control over systems registration, live list updates, reboot dispatching, and real-time event log inspection.

---

## 🏗️ System Architecture & Communication Flow

```mermaid
flowchart LR
    subgraph Desktop Client [Tkinter Desktop Application]
        GUI[Tkinter GUI Window]
        TREE[Treeview Node Table]
        LOG_VIEW[Event Log Text Display]
        GUI --> TREE & LOG_VIEW
    end

    subgraph Backend Microservice [Flask REST API Server]
        ROUTER[Flask REST Router /v2]
        STATE[In-Memory Recovery Registry]
        LOGGER[Audit Logger Function]
        ROUTER <--> STATE
        ROUTER --> LOGGER
    end

    subgraph Storage [Persistent File Storage]
        FILE[(event_logs.txt)]
        LOGGER --> FILE
    end

    Desktop Client -- HTTP POST /v2/systems --> ROUTER
    Desktop Client -- HTTP GET /v2/systems --> ROUTER
    Desktop Client -- HTTP POST /v2/reboot --> ROUTER
    Desktop Client -- HTTP GET /v2/logs --> ROUTER
```

---

## 🌟 Key Features

* **Versioned REST API (`/v2/` Architecture):**
  * `/v2/systems` (`GET`): Returns JSON list of all active recovery nodes.
  * `/v2/systems` (`POST`): Registers a new recovery node with automated timestamping and active status assignment.
  * `/v2/reboot` (`POST`): Dispatches a remote reboot signal to put target nodes into recovery mode.
  * `/v2/logs` (`GET`): Reads and returns historical audit logs directly from disk.
* **Dual-Layer Event Logging:**
  * Appends timestamped events (`[%Y-%m-%d %H:%M:%S]`) to both in-memory arrays and the persistent `event_logs.txt` file on disk for non-repudiation.
* **Desktop Graphical Interface:**
  * **System Registry Treeview:** Displays registered node IDs and names in a structured multi-column table (`ttk.Treeview`).
  * **One-Click Node Creation:** Interactively registers new systems (`Recovery System 1`, `Recovery System 2`, etc.) via HTTP requests.
  * **Remote Reboot Trigger:** Issues recovery reboot signals to the active system cluster with confirmation popups.
  * **Integrated Log Monitor:** Dedicated text display widget fetching and rendering live server logs without needing terminal access.
* **Lightweight & Cross-Platform:**
  * Runs on Windows, macOS, and Linux without external database daemons or heavy background runtimes.

---

## 📡 REST API Reference

| Method | Endpoint | Description | Request Body | Response Status |
| :---: | :--- | :--- | :--- | :---: |
| `GET` | `/v2/systems` | Returns all registered recovery systems. | *None* | `200 OK` |
| `POST` | `/v2/systems` | Registers a new recovery node. | `{"id": 1, "name": "Recovery System 1"}` | `201 Created` |
| `POST` | `/v2/reboot` | Triggers recovery reboot on target node. | `{"name": "Recovery System 1"}` | `200 OK` |
| `GET` | `/v2/logs` | Retrieves full historical event log lines. | *None* | `200 OK` |

---

## 📂 Repository File Structure

```text
Recovery-System-With-Flask-API-GUI/
├── server.py                   # Flask REST API backend server with logging engine
├── gui recovery system.py      # Tkinter desktop GUI client for administrative control
├── event_logs.txt              # Persistent text-based audit trail generated at runtime
└── README.md                   # Comprehensive project documentation
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9 or higher
* `requests` and `flask` packages installed

### 1. Clone the Repository
```bash
git clone https://github.com/RaoAbullah/Recovery-System-With-Flask-API-GUI.git
cd Recovery-System-With-Flask-API-GUI
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install flask requests
```

### 3. Start the Flask Backend Server
In your first terminal:
```bash
python server.py
```
*The Flask REST API will start listening on `http://127.0.0.1:5000`.*

### 4. Launch the Tkinter Client GUI
In a second terminal window:
```bash
python "gui recovery system.py"
```
*The desktop window will open, allowing you to create systems, trigger reboots, and inspect event logs.*

---

## 👤 Author
* **Rao Abdullah Nasir** — [GitHub](https://github.com/RaoAbullah) · [LinkedIn](https://www.linkedin.com/in/rao-abdullah-rajput) · [Email](mailto:abdullahnasirrao7@gmail.com)
