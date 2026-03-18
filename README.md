# 🤖 Hybrid Multi-Robot Planner (LaMMA-P Pivot)
### MSc Research Project: Natural Language to Symbolic Planning for Multi-Robot Coordination

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![ROS2](https://img.shields.io/badge/ROS2-Humble%20/%20Foxy-orange.svg)](https://docs.ros.org/en/humble/index.html)
[![LLM](https://img.shields.io/badge/LLM-OpenAI%20/%20DeepSeek-green.svg)](https://openai.com/)

This repository implements a **Hybrid Multi-Robot Planning Framework** that bridges the gap between High-Level Natural Language instructions and Low-Level ROS2 execution. 

---

## ⚡ Core Architecture

The system follows a three-layer "Think -> Allocate -> Execute" hierarchy:

1.  **Translation (LLM)**: Converts natural language into PDDL (Planning Domain Definition Language).
2.  **Symbolic Planning**: Uses the **Fast Downward** planner to solve the PDDL problem.
3.  **Execution (ROS2/Nav2)**: Generates and executes native `rclpy` scripts targeting LIMO robots in Gazebo.

---

## 🚀 Presentation Quick Start

To demonstrate the system logic without external API dependencies:

```bash
# Activate the environment
source venv/bin/activate

# Run the Mock Showcase
python scripts/pddlrun_llmseparate.py --floor-plan 6 --mock
```

To see the full narrated stack walkthrough:
```bash
python3 showcase_demo.py
```

---

## 📂 Project Structure

| Component | Path | Description |
| :--- | :--- | :--- |
| **Logic** | `scripts/pddlrun_llmseparate.py` | Main LLM-PDDL pipeline |
| **Coordination** | `scripts/resource_manager.py` | Multi-robot aisle lock mutex |
| **ROS2 Bridge** | `data/ros2_connect/` | Nav2/rclpy implementation templates |
| **Plans** | `data/pythonic_plans/` | Validated Warehouse domain structure |
| **Reports** | `logs/` | Performance logs and PDDL history |

---

## 🔧 Technical Features

- **Multi-Provider LLM Support**: Seamlessly switch between OpenAI, DeepSeek, and Local Ollama.
- **Conflict Resolution**: Real-time aisle reservation system for multi-robot safety.
- **Validation**: Automatic PDDL logical consistency checking using `Fast Downward`.
- **ROS2 Native**: Generates executable Python nodes using the **Nav2 Simple Commander**.

---

## 📝 Credentials
Store your API keys in `api_key.txt` (OpenAI format) or `api_key_deepseek.txt`. Keys are excluded from git via `.gitignore`.

---
*Developed as part of an MSc Research Project on Agentic Coding and Robotic Coordination.*
