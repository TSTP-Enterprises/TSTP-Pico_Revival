import sys
import os
import shutil
import time
import logging
import threading
import requests  # For downloading files
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
                            QWidget, QLabel, QTextEdit, QFileDialog, QMessageBox, QMenuBar,
                            QMenu, QAction, QDialog, QTextBrowser, QComboBox, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, QUrl, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPalette, QColor, QDesktopServices

# Attempt to import for RAR extraction (if installed)
# You may need `pip install rarfile`
try:
    import rarfile
except ImportError:
    rarfile = None

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(600, 800)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextBrowser {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 16px;
                line-height: 1.6;
            }
            QTextBrowser a {
                color: #64b5f6;
            }
        """)
        
        layout = QVBoxLayout()
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setText("""
        <style>
            body { line-height: 1.6; }
            h1 { 
                color: #64b5f6;
                font-size: 28px;
                border-bottom: 2px solid #64b5f6;
                padding-bottom: 10px;
                margin: 20px 0;
            }
            .section {
                background-color: #333333;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
            }
            .highlight { 
                color: #81c784;
                background-color: #1f4a2c;
                padding: 10px;
                border-left: 4px solid #81c784;
                margin: 10px 0;
            }
            .mission { 
                color: #64b5f6;
                background-color: #1f314a;
                padding: 10px;
                border-left: 4px solid #64b5f6;
                margin: 10px 0;
            }
        </style>

        <h1>Pico Revival Tool</h1>

        <div class="mission">
            <h3>Building Solutions That Empower</h3>
            <p>Part of TSTP's mission to make innovative tools accessible to everyone, everywhere.</p>
        </div>

        <div class="section">
            <h3>About This Tool</h3>
            <p>The Pico Revival Tool exemplifies our commitment to practical, user-friendly solutions. It provides:</p>
            <ul>
                <li>Streamlined firmware management for Raspberry Pi Pico</li>
                <li>Intuitive interface for both beginners and experts</li>
                <li>Reliable recovery and update capabilities</li>
                <li>Time-saving automation features</li>
            </ul>
        </div>

        <div class="highlight">
            <h3>About TSTP (The Solutions To Problems)</h3>
            <p>We specialize in creating software that makes technology more accessible and useful:</p>
            <ul>
                <li>Desktop and mobile applications with clean, intuitive interfaces</li>
                <li>Automation tools that boost productivity</li>
                <li>Educational resources for technology learning</li>
            </ul>
        </div>

        <div class="section">
            <h3>Our Commitment</h3>
            <p>Every TSTP project reflects our core values:</p>
            <ul>
                <li>Practical solutions for real-world challenges</li>
                <li>Balance of simplicity and powerful features</li>
                <li>Focus on user education and empowerment</li>
                <li>Continuous improvement and innovation</li>
            </ul>
        </div>

        <div class="section">
            <h3>Connect With Us</h3>
            <p>Explore more of what TSTP has to offer:</p>
            <ul>
                <li><a href='https://tstp.xyz/about'>About TSTP</a> - Learn about our mission and values</li>
                <li><a href='https://tstp.xyz/portal'>TSTP Portal</a> - Access our full suite of tools</li>
                <li><a href='https://tstp.xyz/software'>Software Hub</a> - Discover our other applications</li>
            </ul>
        </div>

        <div class="section" style="font-size: 14px; color: #888888;">
            <p>Version 1.0.0 | MIT License</p>
            <p>Copyright © 2024 The Solutions To Problems, LLC</p>
            <p>Built with Python and PyQt5</p>
        </div>
        """)
        layout.addWidget(text)
        self.setLayout(layout)

class TutorialDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tutorial")
        self.setFixedSize(900, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextBrowser {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 16px;
                line-height: 1.6;
            }
            QTextBrowser a {
                color: #64b5f6;
            }
        """)
        
        layout = QVBoxLayout()
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setText("""
        <style>
            body { line-height: 1.6; }
            h1 { 
                color: #64b5f6;
                font-size: 28px;
                border-bottom: 2px solid #64b5f6;
                padding-bottom: 10px;
                margin: 20px 0;
            }
            h2 { 
                color: #81c784;
                font-size: 24px;
                margin-top: 30px;
                margin-bottom: 15px;
                border-bottom: 1px solid #81c784;
                padding-bottom: 5px;
            }
            h3 { 
                color: #fff176;
                font-size: 20px;
                margin-top: 25px;
                margin-bottom: 10px;
            }
            .section {
                background-color: #333333;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
            }
            .warning { 
                color: #ff8a65;
                background-color: #4a1f1f;
                padding: 10px;
                border-left: 4px solid #ff8a65;
                margin: 10px 0;
            }
            .tip { 
                color: #64b5f6;
                background-color: #1f314a;
                padding: 10px;
                border-left: 4px solid #64b5f6;
                margin: 10px 0;
            }
            .note { 
                color: #fff176;
                background-color: #4a461f;
                padding: 10px;
                border-left: 4px solid #fff176;
                margin: 10px 0;
            }
            .step { 
                font-weight: bold;
                color: #64b5f6;
            }
            li { margin: 12px 0; }
            ul, ol { margin: 15px 0; }
            .button {
                background-color: #0d47a1;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-family: monospace;
            }
            .keyboard {
                background-color: #424242;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-family: monospace;
            }
        </style>

        <h1>Pico Revival Tool Tutorial</h1>

        <div class="section">
            <h2>Quick Start Guide</h2>
            <ol>
                <li><span class="step">Connect Pico in Bootloader Mode:</span>
                    • Hold <span class="keyboard">BOOTSEL</span> button while connecting USB
                    • Release after connecting
                </li>
                <li><span class="step">Select Firmware:</span>
                    • Choose <span class="button">MicroPython</span> or <span class="button">CircuitPython</span>
                    • Click corresponding <span class="button">Flash</span> button
                </li>
                <li><span class="step">Wait for Completion:</span>
                    • Process takes about 30-60 seconds
                    • Watch console for progress updates
                </li>
            </ol>
        </div>

        <h2>Detailed Instructions</h2>

        <h3>1. Initial Setup</h3>
        <div class="section">
            <ul>
                <li><b>Drive Detection:</b>
                    • Tool automatically detects Pico drives
                    • "RPI-RP2" indicates bootloader mode
                    • "CIRCUITPY" indicates CircuitPython is installed
                </li>
                <li><b>Required Files:</b>
                    • Downloads automatically on first run
                    • Can be manually selected via <span class="button">File > Select Required Files</span>
                </li>
            </ul>
        </div>

        <h3>2. Flashing Options</h3>
        <div class="section">
            <ul>
                <li><b>MicroPython:</b>
                    • Standard Python implementation for Pico
                    • Best for general use and learning
                    • Compatible with most tutorials
                </li>
                <li><b>CircuitPython:</b>
                    • Adafruit's Python variant
                    • Excellent for USB devices and sensors
                    • Large library of pre-built drivers
                </li>
                <li><b>Custom Firmware:</b>
                    • Flash your own .uf2 files
                    • Supports any Pico-compatible firmware
                    • Use <span class="button">Select Firmware</span> to choose file
                </li>
            </ul>
        </div>

        <h3>3. Recovery Options</h3>
        <div class="section">
            <ul>
                <li><b>Reset Pico:</b>
                    • Completely erases the device
                    • Returns to factory state
                    • Use when device is unresponsive
                </li>
                <li><b>Reset CircuitPython:</b>
                    • Resets only CircuitPython installation
                    • Preserves bootloader
                    • Fixes corrupted CircuitPython installs
                </li>
            </ul>
        </div>

        <div class="warning">
            ⚠ <b>Important Safety Notes:</b>
            <ul>
                <li>Never disconnect Pico during flashing</li>
                <li>Always use a quality USB data cable</li>
                <li>Back up any important files before resetting</li>
            </ul>
        </div>

        <div class="tip">
            💡 <b>Pro Tips:</b>
            <ul>
                <li>Use <span class="keyboard">BOOTSEL</span> + connect for guaranteed bootloader mode</li>
                <li>Check console messages for detailed progress</li>
                <li>Keep firmware files for offline use</li>
            </ul>
        </div>

        <div class="note">
            📝 <b>Additional Resources:</b>
            <ul>
                <li>Visit <a href='https://tstp.xyz/docs'>our documentation</a> for advanced usage</li>
                <li>Join our community for support and updates</li>
                <li>Check GitHub for latest releases</li>
            </ul>
        </div>
        """)
        layout.addWidget(text)
        self.setLayout(layout)

class DonationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Support Development")
        self.setFixedSize(1000, 800)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                color: #ffffff;
                border: 2px solid;
                border-radius: 4px;
                padding: 12px 24px;
                font-size: 14px;
                margin: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
                padding-top: 13px;
                padding-bottom: 11px;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                line-height: 1.6;
                padding: 5px;
            }
            QLabel:hover {
                background-color: rgba(100, 181, 246, 0.1);
                border-radius: 4px;
            }
            QGroupBox {
                border: 1px solid #666666;
                border-radius: 4px;
                margin-top: 10px;
                padding: 15px;
                background-color: rgba(51, 51, 51, 0.5);
            }
            QGroupBox:hover {
                border-color: #64b5f6;
                background-color: rgba(51, 51, 51, 0.8);
            }
            QGroupBox::title {
                color: #64b5f6;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                background-color: #2b2b2b;
                font-weight: bold;
            }
            QGroupBox::title:hover {
                color: #90caf9;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title and Description
        title = QLabel("Support The Solutions To Problems")
        title.setStyleSheet("font-size: 24px; color: #64b5f6; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Why Support Section
        why_support = QLabel(
            "Your support helps us continue developing innovative tools and solutions that "
            "make technology more accessible to everyone. We're committed to creating "
            "high-quality, open-source software that solves real-world problems.\n\n"
            "With your support, we can:\n"
            "• Develop new features and tools\n"
            "• Maintain and improve existing software\n"
            "• Provide better documentation and tutorials\n"
            "• Offer faster support and bug fixes"
        )
        why_support.setWordWrap(True)
        why_support.setStyleSheet("margin: 10px 0; padding: 10px; background-color: #333333; border-radius: 4px;")
        layout.addWidget(why_support)

        # One-Time Donations
        one_time_group = QGroupBox("One-Time Donations")
        one_time_layout = QHBoxLayout()
        
        paypal_btn = QPushButton("Donate with PayPal")
        paypal_btn.setStyleSheet("background-color: #0070ba; border-color: #003087;")
        paypal_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.paypal.com/donate/?hosted_button_id=RAAYNUTMHPQQN')))
        
        coffee_btn = QPushButton("Buy Me a Coffee")
        coffee_btn.setStyleSheet("background-color: #FFDD00; color: #000000; border-color: #FFDD00;")
        coffee_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://buymeacoffee.com/thesolutionstoproblems')))
        
        kofi_btn = QPushButton("Support on Ko-fi")
        kofi_btn.setStyleSheet("background-color: #13C3FF; border-color: #0D8EBA;")
        kofi_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://ko-fi.com/thesolutionstoproblems')))
        
        one_time_layout.addWidget(paypal_btn)
        one_time_layout.addWidget(coffee_btn)
        one_time_layout.addWidget(kofi_btn)
        one_time_group.setLayout(one_time_layout)
        layout.addWidget(one_time_group)

        # Monthly Support
        monthly_group = QGroupBox("Monthly Support")
        monthly_layout = QHBoxLayout()
        
        github_btn = QPushButton("GitHub Sponsors")
        github_btn.setStyleSheet("background-color: #2EA44F; border-color: #22863A;")
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/sponsors/TSTP-Enterprises')))
        
        patreon_btn = QPushButton("Support on Patreon")
        patreon_btn.setStyleSheet("background-color: #FF424D; border-color: #E64248;")
        patreon_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.patreon.com/thesolutionstoproblems')))
        
        monthly_layout.addWidget(github_btn)
        monthly_layout.addWidget(patreon_btn)
        monthly_group.setLayout(monthly_layout)
        layout.addWidget(monthly_group)

        # Enterprise Support
        enterprise_group = QGroupBox("Enterprise Support")
        enterprise_layout = QHBoxLayout()
        
        enterprise_text = QLabel(
            "Need custom features or priority support? Our enterprise solutions include:\n"
            "• Custom feature development\n"
            "• Priority technical support\n"
            "• Training and implementation assistance\n"
            "• Direct access to our development team"
        )
        enterprise_text.setWordWrap(True)
        
        contact_btn = QPushButton("Contact Enterprise Support")
        contact_btn.setStyleSheet("background-color: #7B1FA2; border-color: #6A1B9A;")
        contact_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('mailto:support@tstp.xyz')))
        
        enterprise_layout.addWidget(enterprise_text)
        enterprise_layout.addWidget(contact_btn)
        enterprise_group.setLayout(enterprise_layout)
        layout.addWidget(enterprise_group)

        # Social Links
        social_group = QGroupBox("Connect With Us")
        social_layout = QHBoxLayout()
        
        website_btn = QPushButton("Official Website")
        website_btn.setStyleSheet("background-color: #1976D2; border-color: #1565C0;")
        website_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://tstp.xyz/')))
        
        github_repo_btn = QPushButton("GitHub")
        github_repo_btn.setStyleSheet("background-color: #24292E; border-color: #1B1F23;")
        github_repo_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/TSTP-Enterprises')))
        
        youtube_btn = QPushButton("YouTube")
        youtube_btn.setStyleSheet("background-color: #FF0000; border-color: #CC0000;")
        youtube_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.youtube.com/@yourpststudios')))
        
        social_layout.addWidget(website_btn)
        social_layout.addWidget(github_repo_btn)
        social_layout.addWidget(youtube_btn)
        social_group.setLayout(social_layout)
        layout.addWidget(social_group)

        self.setLayout(layout)

class WorkerSignals(QObject):
    """Signals for threading feedback."""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    message = pyqtSignal(str)

class DownloadWorker(threading.Thread):
    """Worker thread to download and extract the RAR file."""
    def __init__(self, url, dest_folder, signals):
        super().__init__()
        self.url = url
        self.dest_folder = dest_folder
        self.signals = signals

    def run(self):
        try:
            self.signals.message.emit("Downloading TSTP-Pico_Revival package...")
            rar_path = os.path.join(self.dest_folder, "TSTP-Pico_Revival.rar")
            
            # Download the file
            r = requests.get(self.url, stream=True, timeout=30)
            r.raise_for_status()
            
            with open(rar_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.signals.message.emit("Download complete. Extracting files...")

            # Check if we can extract
            if rarfile:
                try:
                    rf = rarfile.RarFile(rar_path)
                    rf.extractall(self.dest_folder)
                    rf.close()
                    self.signals.message.emit("Extraction complete.")
                except Exception as e:
                    raise RuntimeError(f"Error extracting RAR file: {str(e)}")
            else:
                raise RuntimeError(
                    "Cannot extract RAR file. The 'rarfile' module is not installed.\n"
                    "Please install with 'pip install rarfile' or use an external tool."
                )
            
            # Remove downloaded RAR to clean up
            if os.path.exists(rar_path):
                os.remove(rar_path)

            self.signals.finished.emit()

        except requests.exceptions.RequestException as e:
            self.signals.error.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.signals.error.emit(str(e))

class PicoFlasher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Pico Revival Tool")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {background-color: #2b2b2b;}
            QWidget {background-color: #2b2b2b; color: #ffffff;}
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {background-color: #1565c0;}
            QPushButton:disabled {background-color: #666666;}
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 4px;
            }
            QLabel {color: #ffffff;}
            QComboBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        # Logging setup (already includes timestamps)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('pico_flasher.log'),
                logging.StreamHandler()
            ]
        )

        # Initialize file paths
        self.flash_nuke_path = None
        self.micropython_path = None
        self.circuitpython_path = None
        self.adafruit_hid_path = None
        
        # For custom firmware
        self.custom_firmware_path = None

        # Download source and extraction folder
        self.download_url = "https://www.tstp.xyz/downloads/tools/TSTP-Pico_Revival.rar"
        self.extract_folder = r"C:\TSTP\TSTP-Pico_Revival"

        self.setup_menu()
        self.setup_ui()
        
        # Attempt to find or download the required files
        self.check_and_download_files()

        # Timer for drive checking
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_drive)
        self.check_timer.start(1000)  # Check drives every second

    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar {background-color: #333333;} QMenuBar::item:selected {background-color: #0d47a1;}")

        file_menu = menubar.addMenu('File')
        help_menu = menubar.addMenu('Help')

        # File menu actions
        select_files_action = QAction('Select Required Files', self)
        select_files_action.triggered.connect(self.select_all_files)
        file_menu.addAction(select_files_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu actions
        tutorial_action = QAction('Tutorial', self)
        tutorial_action.triggered.connect(self.show_tutorial)
        help_menu.addAction(tutorial_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        donate_action = QAction('Donate', self)
        donate_action.triggered.connect(self.show_donation)
        help_menu.addAction(donate_action)

        website_action = QAction('Visit Website', self)
        website_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://tstp.xyz")))
        help_menu.addAction(website_action)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Status label at top
        self.status_label = QLabel("Please connect your Raspberry Pi Pico")
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Drive selection row
        drive_container = QWidget()
        drive_layout = QHBoxLayout(drive_container)
        
        lbl_select_drive = QLabel("Select Drive:")
        lbl_select_drive.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        drive_layout.addWidget(lbl_select_drive)
        
        self.drive_combo = QComboBox()
        self.drive_combo.setMinimumWidth(200)
        drive_layout.addWidget(self.drive_combo)

        self.refresh_button = QPushButton("Refresh Drives")
        self.refresh_button.clicked.connect(self.refresh_drives)
        drive_layout.addWidget(self.refresh_button)

        main_layout.addWidget(drive_container)

        # Button container
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)

        ##
        # Row 1: Reset Buttons (dangerous = red, with confirmation)
        ##
        reset_container = QWidget()
        reset_layout = QHBoxLayout(reset_container)
        
        self.reset_pico_button = QPushButton("Reset Pico")
        self.reset_pico_button.clicked.connect(lambda: self.confirm_reset_device("RPI-RP2", "Reset Pico"))
        self.reset_pico_button.setEnabled(False)

        self.reset_circuitpy_button = QPushButton("Reset CircuitPython")
        self.reset_circuitpy_button.clicked.connect(lambda: self.confirm_reset_device("CIRCUITPY", "Reset CircuitPython"))
        self.reset_circuitpy_button.setEnabled(False)

        # Style for dangerous buttons (red when enabled)
        self.reset_pico_button.setStyleSheet("""
            QPushButton:enabled {
                background-color: #b71c1c;
            }
            QPushButton:enabled:hover {
                background-color: #c62828;
            }
        """)
        self.reset_circuitpy_button.setStyleSheet("""
            QPushButton:enabled {
                background-color: #b71c1c;
            }
            QPushButton:enabled:hover {
                background-color: #c62828;
            }
        """)

        reset_layout.addWidget(self.reset_pico_button)
        #reset_layout.addWidget(self.reset_circuitpy_button)
        button_layout.addWidget(reset_container)

        ##
        # Row 2: MicroPython (Select / Flash)
        ##
        micro_row = QWidget()
        micro_layout = QHBoxLayout(micro_row)

        self.select_micropython_button = QPushButton("Select MicroPython")
        self.select_micropython_button.clicked.connect(lambda: self.select_custom_firmware("micro"))
        micro_layout.addWidget(self.select_micropython_button)

        self.micropython_button = QPushButton("Flash MicroPython")
        self.micropython_button.clicked.connect(lambda: self.run_in_thread(self.flash_firmware, "micro"))
        self.micropython_button.setEnabled(False)
        micro_layout.addWidget(self.micropython_button)

        button_layout.addWidget(micro_row)

        ##
        # Row 3: CircuitPython (Select / Flash)
        ##
        circuit_row = QWidget()
        circuit_layout = QHBoxLayout(circuit_row)

        self.select_circuitpython_button = QPushButton("Select CircuitPython")
        self.select_circuitpython_button.clicked.connect(lambda: self.select_custom_firmware("circuit"))
        circuit_layout.addWidget(self.select_circuitpython_button)

        self.circuitpython_button = QPushButton("Flash CircuitPython")
        self.circuitpython_button.clicked.connect(lambda: self.run_in_thread(self.flash_firmware, "circuit"))
        self.circuitpython_button.setEnabled(False)
        circuit_layout.addWidget(self.circuitpython_button)

        button_layout.addWidget(circuit_row)

        ##
        # Row 4: Custom Firmware (Select / Flash)
        ##
        custom_row = QWidget()
        custom_layout = QHBoxLayout(custom_row)

        self.select_custom_fw_button = QPushButton("Select Firmware")
        self.select_custom_fw_button.clicked.connect(lambda: self.select_custom_firmware("custom"))
        custom_layout.addWidget(self.select_custom_fw_button)

        self.flash_custom_fw_button = QPushButton("Flash Firmware")
        self.flash_custom_fw_button.clicked.connect(lambda: self.run_in_thread(self.flash_firmware, "custom"))
        self.flash_custom_fw_button.setEnabled(False)
        custom_layout.addWidget(self.flash_custom_fw_button)

        button_layout.addWidget(custom_row)

        main_layout.addWidget(button_container)

        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        main_layout.addWidget(self.console)

        # Initial drive refresh
        self.refresh_drives()

    def run_in_thread(self, func, *args):
        """Runs a function in a separate thread to keep UI responsive."""
        thread = threading.Thread(target=func, args=args)
        thread.start()

    def confirm_reset_device(self, device_type, friendly_name):
        """Prompt user for confirmation before resetting (dangerous)."""
        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to {friendly_name}? This is a dangerous operation.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.run_in_thread(self.reset_device, device_type, friendly_name)

    def reset_device(self, device_type, friendly_name):
        try:
            drive = self.find_drive(self.get_available_drives(), device_type)
            if not drive:
                self.log_to_console(f"{device_type} not found!")
                return

            self.log_to_console(f"Resetting {friendly_name} using flash_nuke.uf2...")
            if not self.flash_nuke_path or not os.path.exists(self.flash_nuke_path):
                raise FileNotFoundError("Nuke firmware (flash_nuke.uf2) is missing.")
            
            # Ensure drive exists and is writable
            if not os.path.exists(drive):
                raise RuntimeError(f"Drive {drive} not found")
                
            dest_path = os.path.join(drive, "flash_nuke.uf2")
            
            # Try to open file for writing first to verify permissions
            try:
                with open(dest_path, 'wb') as _:
                    pass
            except PermissionError:
                raise RuntimeError(f"Cannot write to {drive}. Please check permissions.")
                
            # Copy the file with verification
            shutil.copy2(self.flash_nuke_path, dest_path)
            
            # Verify the file was copied
            if not os.path.exists(dest_path):
                raise RuntimeError("File transfer failed - file not found on destination drive")
                
            if os.path.getsize(self.flash_nuke_path) != os.path.getsize(dest_path):
                raise RuntimeError("File transfer failed - size mismatch")
                
            self.log_to_console("Reset file transferred successfully. Waiting for drive to reconnect...")

            # Give it a moment, then refresh
            time.sleep(10)
            self.refresh_drives()
            
            # Check if drive is still active
            if self.find_drive(self.get_available_drives(), device_type):
                self.log_to_console(f"Reset completed successfully - {device_type} drive detected")
                QTimer.singleShot(0, lambda: QMessageBox.information(self, "Success", f"{friendly_name} reset completed successfully!"))
            else:
                self.log_to_console(f"Warning: {device_type} drive not detected after reset")
                QTimer.singleShot(0, lambda: QMessageBox.warning(self, "Warning", f"{device_type} drive not detected after reset. Please check the connection."))

        except Exception as e:
            self.log_to_console(f"Error during {friendly_name} reset: {str(e)}")
            logging.error(f"Reset error: {str(e)}")

    def check_and_download_files(self):
        """
        Ensures required files/folders exist.
        If not, attempts to download from self.download_url
        and extract to self.extract_folder.
        """
        # First check if we already have what we need
        if os.path.exists(os.path.join(self.extract_folder, "flash_nuke.uf2")) \
           and os.path.exists(os.path.join(self.extract_folder, "RPI_PICO-20241129-v1.24.1.uf2")) \
           and os.path.exists(os.path.join(self.extract_folder, "adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.1.uf2")):
            self.log_to_console("All required firmware files found locally.")
            # Proceed to find them
            self.find_required_files()
            return

        # If we do NOT have internet or user refuses download, offer fallback
        try:
            # Quick check for internet
            requests.get("https://www.google.com", timeout=5)
        except:
            self.log_to_console("No internet connection detected.")
            self.log_to_console(f"Please visit: {self.download_url} to manually download later.")
            # Allow user to save link to desktop as text
            save_link = QMessageBox.question(
                self,
                "No Internet",
                "You have no internet. Would you like to save the download link on your desktop?",
                QMessageBox.Yes | QMessageBox.No
            )
            if save_link == QMessageBox.Yes:
                desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
                link_file = os.path.join(desktop, "TSTP-Pico_Revival_Download_Link.txt")
                try:
                    with open(link_file, "w") as f:
                        f.write(self.download_url + "\n")
                    self.log_to_console(f"Link saved to {link_file}.")
                except Exception as e:
                    self.log_to_console(f"Could not save link to desktop: {str(e)}")
            return

        # If we do have internet, try to download in a background thread
        if not os.path.exists(self.extract_folder):
            try:
                os.makedirs(self.extract_folder)
            except Exception as e:
                self.log_to_console(f"Error creating folder {self.extract_folder}: {str(e)}")
                return

        self.log_to_console("Downloading missing files from TSTP server...")
        # Create signals
        self.download_signals = WorkerSignals()
        self.download_signals.message.connect(self.log_to_console)
        self.download_signals.error.connect(self.on_download_error)
        self.download_signals.finished.connect(self.on_download_finished)

        worker = DownloadWorker(self.download_url, self.extract_folder, self.download_signals)
        worker.start()

    def on_download_error(self, msg):
        self.log_to_console(f"Download error: {msg}")

    def on_download_finished(self):
        self.log_to_console("Download and extraction finished. Finding required files...")
        self.find_required_files()
        self.refresh_drives()

    def setup_files(self):
        """(Deprecated) Moved logic to find_required_files()."""

    def find_required_files(self):
        """Locate the firmware files in self.extract_folder or script path."""
        search_paths = [
            os.path.dirname(os.path.abspath(__file__)),
            self.extract_folder,
        ]

        for path in search_paths:
            if os.path.exists(os.path.join(path, "flash_nuke.uf2")) and not self.flash_nuke_path:
                self.flash_nuke_path = os.path.join(path, "flash_nuke.uf2")

            if os.path.exists(os.path.join(path, "RPI_PICO-20241129-v1.24.1.uf2")) and not self.micropython_path:
                self.micropython_path = os.path.join(path, "RPI_PICO-20241129-v1.24.1.uf2")

            if os.path.exists(os.path.join(path, "adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.1.uf2")) and not self.circuitpython_path:
                self.circuitpython_path = os.path.join(path, "adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.1.uf2")

            if os.path.exists(os.path.join(path, "adafruit_hid")) and not self.adafruit_hid_path:
                self.adafruit_hid_path = os.path.join(path, "adafruit_hid")

        self.update_button_states()
        self.log_missing_files()

    def update_button_states(self):
        # Check if RPI-RP2 drive is selected
        current_drive = self.drive_combo.currentText()
        is_rp2_drive = "RPI-RP2" in current_drive

        # Only enable buttons if RPI-RP2 drive is selected AND required files exist
        can_flash_micro = bool(self.flash_nuke_path and self.micropython_path and is_rp2_drive)
        can_flash_circuit = bool(self.flash_nuke_path and self.circuitpython_path and is_rp2_drive)

        self.micropython_button.setEnabled(can_flash_micro)
        self.circuitpython_button.setEnabled(can_flash_circuit)

        # If custom_firmware_path is selected, enable flash button (only if RPI-RP2 drive present)
        self.flash_custom_fw_button.setEnabled(bool(self.custom_firmware_path and self.flash_nuke_path and is_rp2_drive))

    def log_missing_files(self):
        missing = []
        if not self.flash_nuke_path:
            missing.append("flash_nuke.uf2")
        if not self.micropython_path:
            missing.append("MicroPython firmware")
        if not self.circuitpython_path:
            missing.append("CircuitPython firmware")
        if not self.adafruit_hid_path:
            missing.append("adafruit_hid folder")

        if missing:
            self.log_to_console("Missing required files: " + ", ".join(missing))
            self.log_to_console("Please select or download required files.")

    def select_all_files(self):
        """Manual selection of required files (fallback if download fails)."""
        if not self.flash_nuke_path:
            self.flash_nuke_path = QFileDialog.getOpenFileName(self, "Select flash_nuke.uf2", "", "UF2 Files (*.uf2)")[0]
        if not self.micropython_path:
            self.micropython_path = QFileDialog.getOpenFileName(self, "Select MicroPython firmware", "", "UF2 Files (*.uf2)")[0]
        if not self.circuitpython_path:
            self.circuitpython_path = QFileDialog.getOpenFileName(self, "Select CircuitPython firmware", "", "UF2 Files (*.uf2)")[0]
        if not self.adafruit_hid_path:
            self.adafruit_hid_path = QFileDialog.getExistingDirectory(self, "Select adafruit_hid folder")

        self.update_button_states()

    def show_about(self):
        dialog = AboutDialog()
        dialog.exec_()

    def show_tutorial(self):
        dialog = TutorialDialog()
        dialog.exec_()

    def show_donation(self):
        dialog = DonationDialog()
        dialog.exec_()

    def log_to_console(self, message):
        """Prints and logs with timestamp (logging is already timestamped, but we also show text in console)."""
        timestamped = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}"
        self.console.append(timestamped)
        logging.info(message)

    def refresh_drives(self):
        """Refreshes the combo box with available drives and auto-selects if only one matches a name."""
        self.drive_combo.clear()
        drives = self.get_available_drives()

        # Collect possible RPI-RP2 or CIRCUITPY or others
        matched_rp2 = []
        matched_cpy = []
        
        for drive in drives:
            try:
                volume_name = self.get_volume_name(drive)
                if volume_name:
                    item_text = f"{drive} ({volume_name})"
                else:
                    item_text = drive
                self.drive_combo.addItem(item_text, drive)
                
                if volume_name == "RPI-RP2":
                    matched_rp2.append(drive)
                elif volume_name == "CIRCUITPY":
                    matched_cpy.append(drive)

            except Exception as e:
                logging.error(f"Error getting volume name for drive {drive}: {str(e)}")

        # If exactly one drive is RPI-RP2, auto-select it
        if len(matched_rp2) == 1:
            idx = drives.index(matched_rp2[0])
            self.drive_combo.setCurrentIndex(idx)

        # If exactly one drive is CIRCUITPY, auto-select it (only if RPI-RP2 not found)
        elif len(matched_cpy) == 1 and not matched_rp2:
            idx = drives.index(matched_cpy[0])
            self.drive_combo.setCurrentIndex(idx)

        self.check_drive()

    def get_volume_name(self, drive):
        if sys.platform == 'win32':
            import win32api
            try:
                return win32api.GetVolumeInformation(drive + "\\")[0]
            except:
                return None
        return None

    def check_drive(self):
        current_drive = self.drive_combo.currentData()
        if not current_drive:
            return

        volume_name = self.get_volume_name(current_drive)
        is_rp2 = (volume_name == "RPI-RP2")
        is_circuitpy = (volume_name == "CIRCUITPY")

        self.reset_pico_button.setEnabled(is_rp2)
        self.reset_circuitpy_button.setEnabled(is_circuitpy)

        if is_rp2:
            self.status_label.setText("Pico detected!")
            self.update_button_states()
        elif is_circuitpy:
            self.status_label.setText("CircuitPython device detected!")
        else:
            self.status_label.setText("Please select a valid drive")

            # Disable firmware buttons if not RPI-RP2
            self.micropython_button.setEnabled(False)
            self.circuitpython_button.setEnabled(False)
            self.flash_custom_fw_button.setEnabled(False)

    def get_available_drives(self):
        """Returns a list of available drives on Windows."""
        if sys.platform == 'win32':
            from ctypes import windll
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in range(65, 91):
                if bitmask & 1:
                    drives.append(chr(letter) + ":")
                bitmask >>= 1
            return drives
        return []

    def find_drive(self, drives, name):
        """Find a drive by volume name among the currently available drives."""
        for drive in drives:
            volume_name = self.get_volume_name(drive)
            if volume_name == name:
                return drive + "\\"
        return None

    def select_custom_firmware(self, firmware_type):
        """Select a custom .uf2 firmware file for micro, circuit, or a completely custom firmware."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Firmware File", "", "UF2 Files (*.uf2)")
        if file_path:
            if firmware_type == "micro":
                self.micropython_path = file_path
                self.log_to_console("MicroPython firmware selected.")
            elif firmware_type == "circuit":
                self.circuitpython_path = file_path
                self.log_to_console("CircuitPython firmware selected.")
            else:
                self.custom_firmware_path = file_path
                self.log_to_console("Custom firmware selected.")
            self.update_button_states()

    def flash_firmware(self, firmware_type):
        """Flashes MicroPython, CircuitPython, or a custom firmware onto the Pico."""
        try:
            rp2_drive = self.find_drive(self.get_available_drives(), "RPI-RP2")
            if not rp2_drive:
                self.log_to_console("Pico (RPI-RP2) not found!")
                return

            if not self.flash_nuke_path or not os.path.exists(self.flash_nuke_path):
                raise FileNotFoundError("Nuke firmware (flash_nuke.uf2) is missing. Cannot flash safely.")

            if firmware_type == "micro":
                firmware_path = self.micropython_path
                firmware_name = "MicroPython"
            elif firmware_type == "circuit":
                firmware_path = self.circuitpython_path
                firmware_name = "CircuitPython"
            else:
                # Custom firmware
                firmware_path = self.custom_firmware_path
                firmware_name = "Custom Firmware"

            if not firmware_path or not os.path.exists(firmware_path):
                raise FileNotFoundError(f"{firmware_name} .uf2 file not found.")

            self.log_to_console(f"Flashing {firmware_name} onto the Pico...")
            shutil.copy2(self.flash_nuke_path, os.path.join(rp2_drive, "flash_nuke.uf2"))
            self.log_to_console("Nuke UF2 transferred, waiting 10 seconds for device to reset...")
            time.sleep(10)

            # Refresh drives to see if still RPI-RP2 or it reconnected
            self.refresh_drives()
            rp2_drive = self.find_drive(self.get_available_drives(), "RPI-RP2")
            if not rp2_drive:
                raise RuntimeError("After nuke, the device didn't reappear as RPI-RP2. Can't flash new firmware.")

            shutil.copy2(firmware_path, os.path.join(rp2_drive, os.path.basename(firmware_path)))
            self.log_to_console(f"{firmware_name} copied successfully. Waiting 5 seconds for device to reconnect...")
            time.sleep(5)

            if firmware_type == "circuit":
                # Check for CIRCUITPY
                logging.info("Checking for CIRCUITPY drive...")
                self.log_to_console("Checking for CIRCUITPY drive...")
                if self.find_drive(self.get_available_drives(), "CIRCUITPY"):
                    logging.info("CircuitPython flashed successfully!")
                    self.log_to_console("CircuitPython flashed successfully!")
                    # Run message box in main thread
                    QTimer.singleShot(0, lambda: QMessageBox.information(self, "Success", "CircuitPython has been flashed successfully!"))
                else:
                    self.log_to_console("CIRCUITPY drive not detected. Please check the connection.")
                    QTimer.singleShot(0, lambda: QMessageBox.warning(self, "Warning", "CIRCUITPY drive not detected. Please check the connection."))
            else:
                self.log_to_console(f"{firmware_name} flashed successfully!")
                QTimer.singleShot(0, lambda: QMessageBox.information(self, "Success", f"{firmware_name} has been flashed successfully!"))

            # Finally refresh drives one more time
            self.refresh_drives()

        except Exception as e:
            self.log_to_console(f"Error during flashing: {str(e)}")
            logging.error(f"Flashing error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = PicoFlasher()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
