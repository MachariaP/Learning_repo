# Fabric Tutorial

This repository provides a comprehensive guide on how to use Fabric, a Python library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks.

## Table of Contents
1. [What is Fabric](#what-is-fabric)
2. [How to Deploy Code to a Server Easily](#how-to-deploy-code-to-a-server-easily)
3. [What is a tgz Archive](#what-is-a-tgz-archive)
4. [How to Execute Fabric Command Locally](#how-to-execute-fabric-command-locally)
5. [How to Execute Fabric Command Remotely](#how-to-execute-fabric-command-remotely)
6. [How to Transfer Files with Fabric](#how-to-transfer-files-with-fabric)
7. [How to Manage Nginx Configuration](#how-to-manage-nginx-configuration)
8. [What is the Difference Between Root and Alias in a Nginx Configuration](#what-is-the-difference-between-root-and-alias-in-a-nginx-configuration)

## What is Fabric
Fabric is a Python (2.7 or 3.4+) library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks.

## How to Deploy Code to a Server Easily
Fabric provides a suite of high-level operations that help you to perform common tasks such as running shell commands, downloading files, and deploying applications.

## What is a tgz Archive
A tgz archive, also known as tarball, is a collection of files bundled together using the tar (Tape Archive) command and then compressed using the gzip command. It's commonly used in Unix-based systems for data archiving and compression.

## How to Execute Fabric Command Locally
To execute a Fabric command locally, you can use the `fabric.local()` function. This function works similarly to the `fabric.run()` function, but it executes the command on the local system instead of a remote one.

## How to Execute Fabric Command Remotely
To execute a Fabric command remotely, you can use the `fabric.run()` function. This function takes a command as a string and runs it on the remote server.

## How to Transfer Files with Fabric
Fabric provides the `fabric.put()` and `fabric.get()` functions to upload and download files respectively. These functions use SFTP (SSH File Transfer Protocol), which is a secure file transfer protocol that provides file access, file transfer, and file management functionalities over any reliable data stream.

## How to Manage Nginx Configuration
Fabric can be used to manage Nginx configuration by running commands to start, stop, reload configuration, and other tasks. You can also use Fabric to upload new configuration files to the server.

## What is the Difference Between Root and Alias in a Nginx Configuration
In Nginx configuration, `root` and `alias` directives are used to define the filesystem path for the requested location. The main difference between them is how they handle the location part of the request. The `root` directive appends the location part to the path defined, while the `alias` directive replaces the location part with the path defined.
