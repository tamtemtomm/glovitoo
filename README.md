# Glovitoo 🤖🧤  
_Smart Glove for SIBI Sign Language Translation_



https://github.com/user-attachments/assets/6f9b31eb-4367-43be-8763-114381c41e3a



## 🧠 Overview
Glovitoo started as a **smart glove for deaf and mute individuals**, aimed at translating **SIBI (Indonesian Sign Language)** into recognizable output using sensors and machine learning. 
Initially designed as a simple translator in [Wangsaff-SIBI](https://github.com/tamtemtomm/Wangsaff-SIBI), the project evolved into a **Cyber-Physical System** focusing on real-time gesture recognition using an RNN model.

## 📎 Important Links

- 📄 [Documentation](https://drive.google.com/file/d/1ISDnVtjC2MA20bdEOr3JKySoP5kx42uR/view) 
- 📊 [Project Slides](https://docs.google.com/presentation/d/10LGEclmdnarD-AjiXiqrFo7ihP6nowSCaV8P8YabLRM/edit?usp=sharing)

## 📌 Project Info
- **Name**: Glovitoo  
- **Duration**: Sep 2023 – Mar 2025  
- **Type**: College Final Project  
- **Institution**: Airlangga University  
- **Thesis Topic**: Cyber-Physical System for Gesture Recognition in SIBI Sign Language

## ⚙️ System Architecture

The system is split into two core components:

1. **ESP Microcontroller**
   - Collects real-time data from:
     - **Flex sensors**
     - **IMU sensors**
   - Sends the collected data via serial or wireless to the Khadas board

2. **Khadas Mini Computer**
   - Receives sensor data from ESP
   - Runs a trained **RNN (Recurrent Neural Network)** model
   - Predicts the gesture in real-time

## 📚 Acknowledgements
This project is part of my undergraduate thesis at **Airlangga University**.

---
Feel free to contribute, raise issues, or reach out if you're interested in this kind of assistive tech!
