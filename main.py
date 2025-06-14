#!/usr/bin/env python3
"""
P2P Privacy-Based Communications Program
Features: Voice calling, text messaging, secure link sharing
"""

import asyncio
import json
import logging
import socket
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Audio libraries
try:
    import pyaudio
    import wave
except ImportError:
    print("Audio libraries not available. Install with: pip install pyaudio")
    pyaudio = None

# Encryption
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    import os
except ImportError:
    print("Cryptography library not available. Install with: pip install cryptography")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CryptoManager:
    """Handles encryption and decryption of messages"""
    
    def __init__(self, password: str):
        self.password = password.encode()
        self.salt = os.urandom(16)
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt(self, message: str) -> str:
        """Encrypt a message"""
        encrypted = self.cipher.encrypt(message.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_message: str) -> str:
        """Decrypt a message"""
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_message.encode())
            decrypted = self.cipher.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return "[DECRYPTION FAILED]"

class AudioManager:
    """Handles audio recording and playback for voice calls"""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio() if pyaudio else None
        self.chunk = 1024
        self.format = pyaudio.paInt16 if pyaudio else None
        self.channels = 1
        self.rate = 44100
        self.recording = False
        self.playing = False
    
    def start_recording(self, callback):
        """Start recording audio"""
        if not self.audio:
            return
        
        self.recording = True
        
        def record_audio():
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            while self.recording:
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    if callback:
                        callback(data)
                except Exception as e:
                    logger.error(f"Recording error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
        
        threading.Thread(target=record_audio, daemon=True).start()
    
    def stop_recording(self):
        """Stop recording audio"""
        self.recording = False
    
    def play_audio(self, audio_data: bytes):
        """Play received audio data"""
        if not self.audio:
            return
        
        def play():
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                output=True
            )
            
            stream.write(audio_data)
            stream.stop_stream()
            stream.close()
        
        threading.Thread(target=play, daemon=True).start()
    
    def __del__(self):
        if self.audio:
            self.audio.terminate()

class P2PNode:
    """Main P2P networking node"""
    
    def __init__(self, username: str, password: str, port: int = 0):
        self.username = username
        self.crypto = CryptoManager(password)
        self.audio = AudioManager()
        
        # Network setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', port))
        self.port = self.socket.getsockname()[1]
        
        # Peer management
        self.peers: Dict[str, Tuple[str, int]] = {}  # username -> (ip, port)
        self.active_connections: Dict[str, bool] = {}
        
        # Communication state
        self.in_call = False
        self.call_partner = None
        
        # Callbacks for UI updates
        self.message_callback = None
        self.call_callback = None
        self.peer_callback = None
        
        # Start listening
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen, daemon=True)
        self.listen_thread.start()
        
        logger.info(f"P2P Node started on port {self.port}")
    
    def add_peer(self, username: str, ip: str, port: int):
        """Add a peer to the network"""
        self.peers[username] = (ip, port)
        self.active_connections[username] = True
        logger.info(f"Added peer: {username} at {ip}:{port}")
        
        if self.peer_callback:
            self.peer_callback()
    
    def remove_peer(self, username: str):
        """Remove a peer from the network"""
        if username in self.peers:
            del self.peers[username]
            self.active_connections.pop(username, None)
            logger.info(f"Removed peer: {username}")
            
            if self.peer_callback:
                self.peer_callback()
    
    def send_message(self, recipient: str, message: str, msg_type: str = "text"):
        """Send an encrypted message to a peer"""
        if recipient not in self.peers:
            logger.error(f"Peer {recipient} not found")
            return False
        
        encrypted_msg = self.crypto.encrypt(message)
        
        packet = {
            "type": msg_type,
            "sender": self.username,
            "recipient": recipient,
            "message": encrypted_msg,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            ip, port = self.peers[recipient]
            self.socket.sendto(json.dumps(packet).encode(), (ip, port))
            logger.info(f"Sent {msg_type} message to {recipient}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message to {recipient}: {e}")
            return False
    
    def start_call(self, recipient: str):
        """Initiate a voice call"""
        if self.in_call:
            return False
        
        success = self.send_message(recipient, "call_request", "call")
        if success:
            self.call_partner = recipient
            logger.info(f"Call request sent to {recipient}")
        return success
    
    def accept_call(self, caller: str):
        """Accept an incoming call"""
        if self.in_call:
            return False
        
        self.in_call = True
        self.call_partner = caller
        self.send_message(caller, "call_accepted", "call")
        
        # Start audio streaming
        self.audio.start_recording(self._send_audio)
        logger.info(f"Call accepted with {caller}")
        return True
    
    def end_call(self):
        """End the current call"""
        if not self.in_call:
            return
        
        if self.call_partner:
            self.send_message(self.call_partner, "call_ended", "call")
        
        self.in_call = False
        self.call_partner = None
        self.audio.stop_recording()
        logger.info("Call ended")
    
    def _send_audio(self, audio_data: bytes):
        """Send audio data during a call"""
        if self.in_call and self.call_partner:
            # Encode audio data as base64 for JSON transmission
            audio_b64 = base64.b64encode(audio_data).decode()
            self.send_message(self.call_partner, audio_b64, "audio")
    
    def _listen(self):
        """Listen for incoming messages"""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(4096)
                packet = json.loads(data.decode())
                self._handle_packet(packet, addr)
            except Exception as e:
                logger.error(f"Error receiving data: {e}")
    
    def _handle_packet(self, packet: dict, addr: Tuple[str, int]):
        """Handle incoming packets"""
        msg_type = packet.get("type")
        sender = packet.get("sender")
        message = packet.get("message")
        
        if msg_type == "text":
            decrypted_msg = self.crypto.decrypt(message)
            if self.message_callback:
                self.message_callback(sender, decrypted_msg, "received")
        
        elif msg_type == "call":
            if message == "call_request":
                if self.call_callback:
                    self.call_callback("incoming", sender)
            elif message == "call_accepted":
                self.in_call = True
                self.audio.start_recording(self._send_audio)
                if self.call_callback:
                    self.call_callback("accepted", sender)
            elif message == "call_ended":
                self.in_call = False
                self.call_partner = None
                self.audio.stop_recording()
                if self.call_callback:
                    self.call_callback("ended", sender)
        
        elif msg_type == "audio":
            if self.in_call and sender == self.call_partner:
                try:
                    audio_data = base64.b64decode(message.encode())
                    self.audio.play_audio(audio_data)
                except Exception as e:
                    logger.error(f"Error playing audio: {e}")
        
        elif msg_type == "link":
            decrypted_link = self.crypto.decrypt(message)
            if self.message_callback:
                self.message_callback(sender, f"Shared link: {decrypted_link}", "link")
    
    def share_link(self, recipient: str, url: str):
        """Share a link with a peer"""
        return self.send_message(recipient, url, "link")
    
    def shutdown(self):
        """Shutdown the node"""
        self.running = False
        self.end_call()
        self.socket.close()
        logger.info("P2P Node shutdown")

class P2PCommApp:
    """Main GUI application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("P2P Privacy Communications")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.node = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Login frame
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        
        ttk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(self.login_frame, text="Connect", command=self.connect).pack(pady=10)
        
        # Main app frame (hidden initially)
        self.main_frame = ttk.Frame(self.root)
        
        # Peer management
        peer_frame = ttk.LabelFrame(self.main_frame, text="Peers")
        peer_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(peer_frame, text="Add Peer", command=self.add_peer).pack(side="left", padx=5)
        self.peer_listbox = tk.Listbox(peer_frame, height=3)
        self.peer_listbox.pack(fill="x", padx=5, pady=5)
        
        # Communication buttons
        comm_frame = ttk.Frame(self.main_frame)
        comm_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(comm_frame, text="Send Message", command=self.send_message).pack(side="left", padx=5)
        ttk.Button(comm_frame, text="Start Call", command=self.start_call).pack(side="left", padx=5)
        ttk.Button(comm_frame, text="End Call", command=self.end_call).pack(side="left", padx=5)
        ttk.Button(comm_frame, text="Share Link", command=self.share_link).pack(side="left", padx=5)
        
        # Messages display
        msg_frame = ttk.LabelFrame(self.main_frame, text="Messages")
        msg_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.messages_text = tk.Text(msg_frame, state="disabled")
        scrollbar = ttk.Scrollbar(msg_frame, orient="vertical", command=self.messages_text.yview)
        self.messages_text.configure(yscrollcommand=scrollbar.set)
        
        self.messages_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status bar
        self.status_var = tk.StringVar(value="Disconnected")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.pack(fill="x", side="bottom")
    
    def connect(self):
        """Connect to the P2P network"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        try:
            self.node = P2PNode(username, password)
            self.node.message_callback = self.on_message_received
            self.node.call_callback = self.on_call_event
            self.node.peer_callback = self.update_peer_list
            
            self.login_frame.pack_forget()
            self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            self.status_var.set(f"Connected as {username} on port {self.node.port}")
            self.add_message("System", "Connected to P2P network", "system")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
    
    def add_peer(self):
        """Add a new peer"""
        username = simpledialog.askstring("Add Peer", "Enter peer username:")
        if not username:
            return
        
        ip = simpledialog.askstring("Add Peer", "Enter peer IP:", initialvalue="localhost")
        if not ip:
            return
        
        port = simpledialog.askinteger("Add Peer", "Enter peer port:")
        if not port:
            return
        
        self.node.add_peer(username, ip, port)
        self.update_peer_list()
    
    def update_peer_list(self):
        """Update the peer list display"""
        self.peer_listbox.delete(0, tk.END)
        for username in self.node.peers:
            ip, port = self.node.peers[username]
            status = "Online" if self.node.active_connections.get(username, False) else "Offline"
            self.peer_listbox.insert(tk.END, f"{username} ({ip}:{port}) - {status}")
    
    def get_selected_peer(self):
        """Get the currently selected peer"""
        selection = self.peer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a peer")
            return None
        
        peer_info = self.peer_listbox.get(selection[0])
        username = peer_info.split(" ")[0]
        return username
    
    def send_message(self):
        """Send a text message"""
        recipient = self.get_selected_peer()
        if not recipient:
            return
        
        message = simpledialog.askstring("Send Message", f"Message to {recipient}:")
        if not message:
            return
        
        success = self.node.send_message(recipient, message)
        if success:
            self.add_message("You", f"To {recipient}: {message}", "sent")
        else:
            self.add_message("System", f"Failed to send message to {recipient}", "error")
    
    def start_call(self):
        """Start a voice call"""
        if not pyaudio:
            messagebox.showerror("Error", "Audio support not available. Install pyaudio.")
            return
        
        recipient = self.get_selected_peer()
        if not recipient:
            return
        
        success = self.node.start_call(recipient)
        if success:
            self.add_message("System", f"Calling {recipient}...", "system")
        else:
            self.add_message("System", "Failed to start call", "error")
    
    def end_call(self):
        """End the current call"""
        self.node.end_call()
        self.add_message("System", "Call ended", "system")
    
    def share_link(self):
        """Share a link with a peer"""
        recipient = self.get_selected_peer()
        if not recipient:
            return
        
        url = simpledialog.askstring("Share Link", f"Link to share with {recipient}:")
        if not url:
            return
        
        success = self.node.share_link(recipient, url)
        if success:
            self.add_message("You", f"Shared link with {recipient}: {url}", "sent")
        else:
            self.add_message("System", f"Failed to share link with {recipient}", "error")
    
    def on_message_received(self, sender: str, message: str, msg_type: str):
        """Handle received messages"""
        self.add_message(sender, message, msg_type)
    
    def on_call_event(self, event_type: str, peer: str):
        """Handle call events"""
        if event_type == "incoming":
            result = messagebox.askyesno("Incoming Call", f"Accept call from {peer}?")
            if result:
                self.node.accept_call(peer)
                self.add_message("System", f"Call started with {peer}", "system")
            else:
                self.node.send_message(peer, "call_rejected", "call")
        
        elif event_type == "accepted":
            self.add_message("System", f"Call accepted by {peer}", "system")
        
        elif event_type == "ended":
            self.add_message("System", f"Call ended by {peer}", "system")
    
    def add_message(self, sender: str, message: str, msg_type: str):
        """Add a message to the display"""
        self.messages_text.config(state="normal")
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if msg_type == "system":
            self.messages_text.insert(tk.END, f"[{timestamp}] {message}\n")
        elif msg_type == "error":
            self.messages_text.insert(tk.END, f"[{timestamp}] ERROR: {message}\n")
        elif msg_type == "link":
            self.messages_text.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        else:
            self.messages_text.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        
        self.messages_text.config(state="disabled")
        self.messages_text.see(tk.END)
    
    def on_closing(self):
        """Handle application closing"""
        if self.node:
            self.node.shutdown()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = P2PCommApp()
    app.run()

