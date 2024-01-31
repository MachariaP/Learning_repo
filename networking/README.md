   

## Networking basics

<div align="center">
  <img src="https://gifdb.com/images/thumbnail/setting-up-a-small-office-network-p14b4gj75vacsrdf.webp" alt="Setting Up a Small Office Network">
</div>



### OSI Model
1. **What it is:**
   - A conceptual framework that standardizes the functions of a telecommunication or computing system into seven abstraction layers.
   - **Explanation:** It helps in understanding and designing complex network architectures by breaking down the communication process into manageable layers.

2. **How many layers it has:**
   - 7 layers.
   - **Explanation:** Each layer has a specific role and contributes to the overall functionality of network communication.

3. **How it is organized:**
   - Divided into Physical, Data Link, Network, Transport, Session, Presentation, and Application layers.
   - **Explanation:** This organization allows for modular design and troubleshooting, as each layer performs a specific set of functions.

Let's highlight the key points for each layer:
### Layer 7: Application Layer

-   **Closest to User:** Interacts directly with end-user applications.
-   **Software Examples:** Web browsers, email programs.
-   **Functions:** File sharing, message handling, database access.
-   **Protocols:** HTTP, FTP, SMB/CIFS, TFTP, SMTP.
-   **Note:** Identifies and determines the availability of communication partners.

### Layer 6: Presentation Layer

-   **Function:** Handles data formatting, translation, and encryption.
-   **Tasks:** Protocol conversion, data encryption/decryption, data compression.
-   **Syntax Layer:** Converts data into the format accepted by the application layer.
-   **Example:** ASN.1 for syntax structure negotiation.

### Layer 5: Session Layer

-   **Function:** Manages session setup, control, and teardown.
-   **Operations:** User logon, name lookup, user logoff.
-   **Modes:** Full-duplex, half-duplex, or simplex operation.
-   **Example:** DNS, authentication protocols.

### Layer 4: Transport Layer

-   **Function:** Transfers data between hosts across a network with QoS.
-   **Protocols:** TCP (connection-oriented, reliable), UDP (connectionless).
-   **Segmentation:** Breaks data into segments for transmission.
-   **Flow Control:** Ensures reliable and orderly data transfer.

### Layer 3: Network Layer

-   **Function:** Transfers packets between nodes in different networks.
-   **Features:** Message delivery, fragmentation for large messages.
-   **Protocols:** Routing protocols, multicast group management.
-   **Note:** No guarantee of reliable message delivery.

### Layer 2: Data Link Layer

-   **Function:** Provides node-to-node data transfer and error detection.
-   **Sublayers:** MAC (controls device access) and LLC (identifies network layer protocols).
-   **Examples:** Ethernet, Wi-Fi, Zigbee.
-   **Protocol:** Point-to-Point Protocol (PPP) for various physical layers.

### Layer 1: Physical Layer

-   **Responsibility:** Handles raw data transmission between devices and the physical medium.
-   **Conversion:** Converts digital bits into electrical, radio, or optical signals.
-   **Specifications:** Defines characteristics like voltage levels, timing, data rates, etc.
-   **Examples:** Bluetooth, Ethernet, USB standards.
-   **Encoding:** Specifies how 1s and 0s are represented in the physical signal.

This arrangement provides a top-down perspective, starting with the layer closest to the user and descending to the layer responsible for raw data transmission.

### Types of Networks
1. **LAN (Local Area Network):**
   - **What it is:**
     - A network that is limited to a small geographic area.
   - **Typical Usage:**
     - Used for connecting devices within a home, office, or campus.
   - **Typical Geographical Size:**
     - Covers a small area, like a single building or a group of nearby buildings.
   - **Example:** The Wi-Fi network in your home connecting your devices.

2. **WAN (Wide Area Network):**
   - **What it is:**
     - Spans a large geographic area.
   - **Typical Usage:**
     - Connects LANs over long distances, often between cities or countries.
   - **Typical Geographical Size:**
     - Covers a broad area, potentially spanning countries or continents.
   - **Example:** The internet connecting networks globally.

3. **Internet:**
   - **What it is:**
     - A global network of networks, connecting billions of devices worldwide.
   - **Example:** Accessing websites, sending emails, or streaming videos over the internet.

### IP Addressing
1. **What is an IP Address:**
   - A numerical label assigned to each device participating in a computer network.
   - **Explanation:** It serves as an identifier for devices to communicate with each other on a network.

2. **Types of IP Addresses:**
   - **Private:**
     - Used within a private network.
   - **Public:**
     - Used on the public Internet.
   - **Example:** Private IP addresses are commonly used within a home network, while public IP addresses are assigned to web servers.

3. **IPv4 and IPv6:**
   - **IPv4:**
     - 32-bit address.
   - **IPv6:**
     - 128-bit address, created to address the exhaustion of IPv4 addresses.
   - **Example:** IPv4: 192.168.0.1, IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334.

4. **Localhost:**
   - **What it is:**
     - A reserved IP address used to refer to the current device.
   - **Example:** 127.0.0.1 - accessing services on your own machine without going through the network.

5. **Subnet:**
   - **What it is:**
     - A subdivision of an IP network, dividing it into smaller, more manageable parts.
   - **Example:** Dividing a large organization's network into subnets for different departments.

6. **Why IPv6 was created:**
   - **Reason:**
     - Due to the limited number of IPv4 addresses, IPv6 was introduced to provide a vast pool of unique addresses.
   - **Example:** The increasing number of internet-connected devices requiring unique IP addresses for proper communication.

### TCP/UDP and Ports
1. **TCP and UDP:**
   - **TCP (Transmission Control Protocol):**
     - Ensures reliable, ordered, and error-checked delivery of information.
   - **UDP (User Datagram Protocol):**
     - Faster but less reliable, used for real-time applications.
   - **Example:** TCP is used for file transfers, while UDP is suitable for live streaming.

2. **TCP/UDP Ports:**
   - **SSH (Secure Shell):** 22
   - **HTTP (Hypertext Transfer Protocol):** 80
   - **HTTPS (Hypertext Transfer Protocol Secure):** 443
   - **Example:** Accessing a website (HTTP/HTTPS) or securely connecting to a server (SSH) on specific port numbers.

3. **Ping / ICMP:**
   - **What it is:**
     - A tool/protocol used to check if a device is connected to a network.
   - **Example:** Running `ping google.com` in the command line to check connectivity with Google's servers.

4. **Positional Parameters:**
   - **Definition:**
     - Parameters passed to a script or command based on their position in the command line.
   - **Example:** Running a script with `./myscript.sh parameter1 parameter2`.
