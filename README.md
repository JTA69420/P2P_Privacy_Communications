# P2P Privacy Communications

A secure peer-to-peer communications program with end-to-end encryption, voice calling, text messaging, and secure link sharing.

## Features

- **End-to-End Encryption**: All messages are encrypted using industry-standard cryptography
- **Voice Calls**: Real-time voice communication between peers
- **Text Messaging**: Secure text messaging with timestamps
- **Link Sharing**: Share URLs securely with other users
- **Privacy Focused**: No central servers, direct peer-to-peer communication
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Security Features

- **PBKDF2 Key Derivation**: Password-based key derivation with 100,000 iterations
- **Fernet Encryption**: Symmetric encryption for all message content
- **Salt-based Security**: Each session uses unique salts for key derivation
- **No Data Logging**: No messages or calls are stored or logged

## Installation

### Prerequisites

- Python 3.7 or higher
- Microphone and speakers/headphones for voice calls

### Setup

1. **Clone or download the project**:
   ```bash
   cd p2p_comm
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note for Windows users**: If pyaudio installation fails, try:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```
   
   **Note for macOS users**: You may need to install portaudio first:
   ```bash
   brew install portaudio
   pip install pyaudio
   ```
   
   **Note for Linux users**: Install system dependencies:
   ```bash
   sudo apt-get install python3-pyaudio portaudio19-dev
   # or
   sudo yum install python3-pyaudio portaudio-devel
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Getting Started

1. **Launch the application** by running `python main.py`
2. **Enter your username and password**:
   - Username: Your display name (can be anything)
   - Password: Used for message encryption (must match between communicating peers)
3. **Click "Connect"** to start your P2P node

### Adding Peers

1. **Click "Add Peer"** in the main interface
2. **Enter peer details**:
   - Username: The other person's username
   - IP Address: Their computer's IP (use "localhost" for same machine testing)
   - Port: The port number shown in their status bar
3. **Both users must add each other** to establish communication

### Sending Messages

1. **Select a peer** from the peer list
2. **Click "Send Message"**
3. **Type your message** and press OK
4. **Messages appear** in the main message area with timestamps

### Voice Calls

1. **Select a peer** from the peer list
2. **Click "Start Call"** to initiate a call
3. **The recipient will see a dialog** asking to accept or reject
4. **Once accepted**, both parties can speak and hear each other
5. **Click "End Call"** to terminate the call

### Sharing Links

1. **Select a peer** from the peer list
2. **Click "Share Link"**
3. **Enter the URL** you want to share
4. **The link is sent encrypted** and appears in the recipient's message area

## Network Setup

### Same Computer Testing
- Use "localhost" as IP for both peers
- Each instance will use a different port automatically
- Note the port numbers shown in the status bar

### Local Network (LAN)
- Find your local IP address:
  - Windows: `ipconfig`
  - macOS/Linux: `ifconfig` or `ip addr`
- Use the local IP (e.g., 192.168.1.100)
- Ensure firewall allows the application

### Internet Communication
- **Port forwarding** required on router
- Use **external IP address** of the host
- **VPN or tunnel services** recommended for security
- Consider using **dynamic DNS** for changing IPs

## Security Considerations

### Password Security
- **Use strong, unique passwords** for each communication session
- **Both parties must use the same password** for successful decryption
- **Passwords are not transmitted** over the network

### Network Security
- **Communications are encrypted** but network metadata is visible
- **Use VPN** for additional network-level privacy
- **Avoid public networks** for sensitive communications

### Privacy Features
- **No central servers** - direct peer-to-peer communication
- **No message logging** - messages exist only in memory during session
- **No user tracking** - no analytics or telemetry

## Troubleshooting

### Audio Issues
- **Check microphone permissions** in your operating system
- **Verify audio devices** are working with other applications
- **Try different audio sample rates** if experiencing quality issues
- **Install alternative audio libraries** if pyaudio fails

### Connection Issues
- **Check firewall settings** - ensure the application can bind to ports
- **Verify IP addresses** are correct and reachable
- **Test with localhost first** before trying network connections
- **Check port availability** - ensure ports aren't blocked

### Message Delivery
- **Verify both peers are online** and connected
- **Check password matching** - different passwords prevent decryption
- **Monitor the message area** for error messages

## Technical Details

### Architecture
- **UDP-based networking** for low-latency communication
- **JSON message protocol** for structured data exchange
- **Threading model** for concurrent message handling
- **Tkinter GUI** for cross-platform interface

### Encryption Details
- **Algorithm**: Fernet (AES 128-bit in CBC mode)
- **Key Derivation**: PBKDF2 with SHA-256
- **Iterations**: 100,000 rounds
- **Salt**: 16 random bytes per session

### Audio Processing
- **Sample Rate**: 44.1 kHz
- **Bit Depth**: 16-bit
- **Channels**: Mono
- **Chunk Size**: 1024 samples
- **Encoding**: Base64 for network transmission

## Limitations

- **Same password required** for all participants in a session
- **No user discovery** - manual peer addition required  
- **No file transfer** - text and links only
- **No group calls** - only one-to-one voice communication
- **No persistent storage** - messages not saved between sessions

## Future Enhancements

- File transfer capability
- Group messaging and calls
- User discovery mechanisms
- Message history persistence
- Mobile app versions
- Video calling support
- Screen sharing
- Advanced peer management

## License

This project is provided as-is for educational and personal use. Please ensure compliance with local laws and regulations regarding encrypted communications.

## Support

For issues and questions:
1. Check the troubleshooting section above

_________________________________________________________________
HOW TO USE
1. Run P2P_Launcher.exe 
2. Have the installation directory as the working directory
3. Allow the launcher to find and load main.py successfully
4. Launch your P2P Privacy Communications application properly
3. Verify all dependencies are installed correctly
4. Test with localhost before network connections
5. Check system logs for detailed error messages

