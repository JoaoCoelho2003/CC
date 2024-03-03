# CC - Peer-to-Peer File Sharing Service

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Dependencies](#dependencies)
4. [Cloning the Repository](#cloning-the-repository)
5. [Compiling and Running](#compiling-and-running)
6. [Group's Report](#groups-report)
7. [Conclusion](#conclusion)
8. [Developed by](#developed-by)

## Overview

This project was developed as part of the `Comunicações por Computador` course, which is a subject offered in the third year, first semester of the Software Engineering Degree at the University Of Minho.

The project focuses on implementing a peer-to-peer file sharing service, utilizing both TCP and UDP protocols. It involves designing and implementing custom protocols for efficient communication between network elements, including a centralized tracker server and multiple file-sharing nodes. Additionally, the project integrates DNS platforms to enhance system functionality.

For further information about the project, including detailed design considerations, protocol specifications, implementation details, and test results, refer to the [project report](reports/CC-Enunciado-TP2-2023-2024.pdf).

## Key Features

Here are the key features of the project:

1. `Peer-to-Peer File Sharing:` The project implements a peer-to-peer file sharing system, allowing users to share files directly between their devices without relying on a central server.

2. `Utilization of TCP and UDP Protocols:` Custom protocols based on TCP and UDP were developed specifically for this project. TCP is used for reliable communication between nodes and the tracker server, while UDP is employed for efficient file transfer between nodes.

3. `Chunk-based File Transfer:` Files are divided into chunks to enable parallel downloading from multiple nodes, improving download speeds and overall system performance.

4. `Custom Communication Protocols:` Custom communication protocols were designed to facilitate efficient and secure communication between nodes and the tracker server, ensuring reliable file sharing and tracking.

5. `Dynamic Node Discovery:` The system utilizes dynamic node discovery techniques to efficiently locate nodes that possess specific file chunks, enabling faster file downloads and improved system scalability.

6. `Integration with DNS Platforms:` The project has been adapted to integrate with DNS platforms, enhancing system accessibility and reliability by utilizing domain names instead of direct IP addresses.

## Dependencies

- `Python:` The project is written in Python, so you need to have Python installed on your system to run the code. You can download Python from the [official Python website](https://www.python.org/downloads/).

- `Python Libraries/Modules:` Certain functionalities of the project may rely on specific Python libraries or modules. You can install these dependencies using the `pip` package manager. For example, to install a library named `example_lib`, you can use the following command:
  
```
pip install example_lib
```

Please refer to the project documentation or source code for more information on required dependencies.

## Cloning the Repository

To clone the repository, run the following command in your terminal:

```
$ git clone https://github.com/JoaoCoelho2003/CC.git
```

Once cloned, navigate to the repository directory using the cd command:

```
$ cd CC
```

## Compiling and Running

Before running the tracker and node components, it's essential to understand their roles in the system:

### Tracker

The tracker serves as a central server responsible for managing connections and coordinating file sharing among nodes in the network. It maintains information about available files and their respective nodes.

### Node

A node represents a client in the peer-to-peer network. Each node can act as both a client and a server, allowing it to request files from other nodes and share its own files.

To ensure proper functionality of the program, it's necessary to have the DNS (Domain Name System) running. The DNS resolves hostnames to IP addresses, facilitating communication between the tracker and nodes.

Now, follow the instructions below to compile and run the tracker and node components.


### Compile Tracker

To run the tracker component, follow these steps:

1. **Start Tracker**: Execute the `FS_tracker.py` script using Python 3 to start the tracker server.

```
$ python3 FS_tracker.py <port>
```


Replace `<port>` with the port number on which you want the tracker to listen for connections.

### Compile Node

To run the node component, follow these steps:

1. **Start Node**: Execute the `FS_node.py` script using Python 3 to start the node server and connect to the tracker.

```
$ python3 FS_node.py <path> <host> <port>
```

Replace `<path>` with the path to the folder containing files to be shared, `<host>` with the hostname or IP address of the tracker server, and `<port>` with the port number on which the tracker server is listening.

These instructions provide guidance on running both the tracker and node components using Python 3. No executable files are created; the Python scripts are executed directly using the Python interpreter.

## Group's Report

The group has prepared a comprehensive report detailing the design decisions, implementation strategies, and evaluation outcomes of the peer-to-peer file sharing system. In the report, every aspect of the project, including architecture, protocols, implementation details, and test results, is thoroughly explained.

For a deeper understanding of the project's intricacies and rationale behind various design choices, please refer to the [group's report](reports/CC-TP2-PL2-G6-Rel.pdf).

## Conclusion

Exploring the intricacies of peer-to-peer file sharing within the domain of distributed systems and cloud computing has been an enlightening and fulfilling experience. Throughout this project, we've delved into the nuances of custom protocol design, network communication optimization, and system scalability, gaining invaluable insights into the challenges and opportunities inherent in building such systems.

If you have any inquiries, recommendations, or feedback regarding our project, please don't hesitate to reach out. Your insights are crucial as we strive for continual improvement and innovation in our work. Happy coding!

## Developed by

**A100596** João Coelho

**A100692** José Rodrigues

**A100750** Duarte Araújo










