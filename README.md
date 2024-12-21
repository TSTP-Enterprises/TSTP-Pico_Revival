# TSTP Pico Revival Tool

A powerful GUI utility for managing and flashing firmware on Raspberry Pi Pico devices. Built with PyQt5, this tool provides an intuitive interface for flashing MicroPython, CircuitPython, or custom firmware while handling device detection and error recovery.

## 🎯 Overview

The TSTP Pico Revival Tool simplifies the process of managing Raspberry Pi Pico firmware. Whether you're:

- Flashing new firmware
- Recovering bricked devices 
- Installing CircuitPython or MicroPython
- Testing custom firmware
- Managing multiple Pico devices

This tool provides a streamlined solution with comprehensive error handling.

## ✨ Key Features

- **Smart Device Detection**
  - Automatic Pico detection
  - Volume name identification
  - Real-time drive monitoring
  - Multiple device support
  - Drive refresh capabilities

- **Firmware Management**
  - MicroPython flashing
  - CircuitPython installation
  - Custom firmware support
  - Device recovery tools
  - Flash verification

- **User Interface**
  - Intuitive controls
  - Progress monitoring
  - Detailed console output
  - Status indicators
  - Error notifications

- **Error Recovery**
  - Flash nuke capability
  - Device reset options
  - Comprehensive logging
  - Timeout handling
  - Clear error messages

- **Safety Features**
  - Operation confirmation
  - Drive validation
  - Write verification
  - Safe disconnection
  - Error prevention

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- PyQt5
- rarfile (optional)
- win32api (Windows only)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TSTP-Enterprises/TSTP-Pico-Revival.git
   cd TSTP-Pico-Revival
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python pico_flasher.py
   ```

### Building from Source

1. **Install Build Dependencies**
   ```bash
   pip install pyinstaller
   ```

2. **Create Executable**
   ```bash
   pyinstaller --onefile --windowed --icon=assets/icon.ico pico_flasher.py
   ```

## 📖 Usage Tutorial

### Basic Operations

1. **Connecting Your Pico**
   - Hold BOOTSEL button while connecting USB
   - Release after connecting
   - Tool will auto-detect the device

2. **Flashing Firmware**
   - Select desired firmware type
   - Click corresponding Flash button
   - Wait for process to complete
   - Check console for progress

3. **Recovery Process**
   - Use Reset Pico for complete reset
   - Follow console instructions
   - Wait for device reconnection

### Advanced Features

1. **Custom Firmware**
   - Click "Select Firmware"
   - Choose .uf2 file
   - Use Flash button
   - Verify installation

2. **Multiple Devices**
   - Connect devices
   - Use drive selector
   - Manage independently
   - Check volume names

3. **Troubleshooting**
   - Check console output
   - Verify connections
   - Use reset options
   - Follow error messages

## 💝 Support Our Work

Your support helps us maintain and enhance this tool. Consider supporting us through:

### 🎁 One-Time Donations
- [PayPal](https://www.paypal.com/donate/?hosted_button_id=RAAYNUTMHPQQN)
- [Buy Me a Coffee](https://buymeacoffee.com/thesolutionstoproblems)
- [Ko-fi](https://ko-fi.com/thesolutionstoproblems)

### 🌟 Monthly Sponsorship
- [GitHub Sponsors](https://github.com/sponsors/TSTP-Enterprises)
- [Patreon](https://www.patreon.com/thesolutionstoproblems)

### 💎 Enterprise Support
- Custom feature development
- Priority support
- Training sessions
- Contact us at support@tstp.xyz

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

## 🔗 Quick Links

- [🌐 Official Website](https://tstp.xyz/)
- [💻 GitHub Repository](https://github.com/TSTP-Enterprises/TSTP-Pico-Revival)
- [👥 LinkedIn](https://www.linkedin.com/company/thesolutions-toproblems)
- [🎥 YouTube Channel](https://www.youtube.com/@yourpststudios)
- [📱 Facebook Page](https://www.facebook.com/profile.php?id=61557162643039)

## 📞 Contact & Support

- 📧 Email: support@tstp.xyz
- 🌐 Website: [tstp.xyz](https://tstp.xyz)

## 🏢 About TSTP Solutions

TSTP Solutions specializes in developing innovative tools for IT professionals. Our mission is to simplify complex administrative tasks through intelligent automation and user-friendly interfaces.

---
© 2024 TSTP Solutions. All rights reserved.
Made with ❤️ by the TSTP team
