---
categories:
- Interview
date: 2025-12-03 02:56:44
draft: false
tags:
- Linux
title: SRE Interview Questions Summary | Linux
---

## 1. **Processes, Threads, and Coroutines**

- **Process**: The smallest unit of resource allocation in an operating system, including CPU, memory, and disk I/O. A process can have multiple threads.
- **Thread**: The execution unit within a process. A process can have multiple threads, and threads share the resources of the process.
- **Coroutine**: A lightweight user-space thread controlled by the user program, without the need for operating system support.

## 2. Process Priority in Linux and Setting Methods

The priority of a process determines the order in which it gets CPU time slices. Higher priority (lower numerical value) processes get CPU time slices first.

The priority of a process is represented by the Nice value, which ranges from -20 (highest priority) to 19 (lowest priority). By default, the Nice value of a process is 0.

- **nice command**: The nice command is used to start a process and set its Nice value. For example, `nice -n 10 command` starts the command with a Nice value of 10.
- **renice command**: The renice command is used to modify the Nice value of a running process. For example, `renice +5 -p 1234` increases the Nice value of the process with PID 1234 by 5. Note that only the root user can lower the Nice value of a process.
- **Calling nice() or setpriority() functions in code**: If you are writing a program, you can call the nice() or setpriority() functions in your code to change the priority of your process.

## 3. What is a Zombie Process

A zombie process is a process that has terminated but whose process descriptor (process descriptor) is still in memory.
The parent process has not yet reclaimed the resources of the child process.

## 4. What is Process Interrupt

An interrupt is a mechanism used by the system to respond to hardware device requests, which interrupts the normal scheduling and execution of a process, and then calls the kernel's interrupt handler to respond to the device request.
For example, in the case of ordering takeout food, instead of waiting, the action of calling is an interrupt.
Interrupts are an asynchronous processing mechanism that can improve the concurrency processing capability of the system.

### 4.1 Soft Interrupts, Hard Interrupts, and Uninterruptible Processes

Linux divides interrupts into two parts: the upper part and the lower part.
The upper part directly handles hardware requests and is characterized by fast execution (hard interrupt).
The lower part is triggered by the kernel and is characterized by delayed execution (soft interrupt).
An uninterruptible process indicates that the process and hardware are interacting, and to maintain consistency between process data and hardware, the system does not allow other processes or interrupts to interrupt this process. A process that remains in an uninterruptible state for a long time usually indicates that there is a problem with system I/O.

## 5. Ways of Inter-Process Communication and Their Use Cases

1. **Pipe (Pipe) and Named Pipe (Named pipe)**: A pipe is a half-duplex communication method, mainly used for inter-process communication between processes with parent-child relationships. A named pipe is a full-duplex communication method that can be used for communication between any two processes. They are mainly used for streaming data transmission.
2. **Message Queue (Message Queue)**: A message queue is a list structure that can store messages to be sent. A process can add messages to a message queue and also read messages from it. Message queues are often used for data exchange and synchronization between different processes.
3. **Shared Memory (Shared Memory)**: Shared memory is the fastest IPC method, allowing two or more processes to access the same memory area. This method is often used for exchanging large amounts of data.
4. **Signal (Signal)**: Signals are an asynchronous communication method used to notify the receiving process that an event has occurred. For example, when a process ends, it sends a SIGCHLD signal to its parent process.
5. **Socket (Socket)**: Sockets can be used for inter-process communication between processes on different machines, as well as on the same machine. It supports TCP, UDP, and other protocols and is often used for network communication.
6. **Semaphore (Semaphore)**: Semaphores are mainly used to solve race conditions and protect the access to critical resources. When multiple processes need to access the same resource, they can use semaphores for synchronization.
7. **File Locking (File Locking)**: File locks can be used to control access to the same file by multiple processes. When a process is accessing a file, other processes must wait until the process releases the file lock.

## 6. Ways to Limit CPU in cgroup

cgroups, short for control groups, is a feature of the Linux kernel that is used to limit, control, and isolate the resources of a process (such as CPU, memory, disk, etc.).

In cgroup, there are two ways to limit CPU:

1. **CPU Time Slice Limitation**: By setting the cpu.cfs_quota_us and cpu.cfs_period_us parameters, the CPU time that a process can use in each time period is limited.
2. **CPU Core Limitation**: By setting the cpu.shares parameter, the running time proportion of a process on multiple CPU cores is limited.

## 7. The Difference Between Buffers and Cached in Memory

**Design Purpose**: To improve system I/O performance

- **Buffers**: The memory used by kernel buffers, corresponding to the Buffers value in /proc/meminfo.
- **Cache**: The memory used by kernel page cache and Slab, corresponding to the sum of Cached and SReclaimable in /proc/meminfo.

**Buffers** are used to temporarily store data to be written to the hard disk, while **Cached** is used to store data that has been read from the hard disk for quick access.
**Buffer** is a cache for disk data. **Cache** is a cache for file data, which is used in both read and write requests.

Linux follows the principle of using as much memory as possible, and memory will allocate the remaining space as cache, while cache does not belong to free. When the system runs for a long time, we will find that the cache is very large.

When we see that the system memory usage is very high and free is almost 0, it does not mean that the system memory capacity has a bottleneck! It just means that the system has fully utilized the memory. When a process needs to apply for a large file memory, the kernel will reclaim some cache space, and the reclaimed memory will be allocated to the process program.

## 8. The Difference Between Stack Memory and Heap Memory

1. **Stack Memory (Stack)**
   - **Characteristics**: Stack memory is automatically allocated and released, and has the Last In First Out (LIFO) characteristic. Variables in stack memory are created when a function is called and are automatically destroyed when the function returns. Its management is controlled by the compiler, so it is efficient.
   - **Usage**: It is usually used to store temporary data such as local variables and function parameters.
   - **Advantages**: Memory allocation and release are fast, and it is not easy to produce memory fragmentation.
   - **Disadvantages**: The size of stack memory is usually limited, and it cannot be used to store a large amount of data or data that needs to be used for a long time.

2. **Heap Memory (Heap)**
   - **Characteristics**: Heap memory is dynamically allocated, and its size is not fixed. It needs to be manually allocated and released by the programmer. If it is forgotten to release, it may cause memory leaks. It does not have a strict LIFO order and can request memory allocation at any location in the program.
   - **Usage**: It is used to store a large amount of data that needs to be dynamically allocated, such as objects and global data. It is allocated through malloc() or new and released through free() or delete.
   - **Advantages**: Suitable for long-term use of data or large data structures, such as linked lists and trees. The size of heap memory is almost infinite compared to the stack (subject to physical memory and system limitations).
   - **Disadvantages**: Since it needs to be manually managed, the allocation and release of heap memory is slower, and it is easy to cause memory fragmentation.

**Difference Summary**:
- **Lifecycle**: The data in stack memory is valid during the function call period, while the data in heap memory is valid until it is manually released.
- **Allocation Method**: The stack is automatically allocated and managed by the system, while the heap is dynamically allocated and managed by the programmer.
- **Efficiency**: Stack memory is efficient, while heap memory allocation and release is slower.

## 9. How to Adjust the Maximum Number of Processes, Maximum Number of Threads, and Maximum Number of Open Files

### Checking Current Limits

```shell
ulimit -a
ulimit -u      # Maximum number of processes/threads
ulimit -n      # Maximum number of file handles
```

### Adjusting Maximum File Number

- **Temporary Effect**
  ```shell
  ulimit -n 65535
  ```

- **Permanent Effect**
  ```shell
  sudo vim /etc/security/limits.conf
  ```
  Add the following content:
  ```
  * soft nofile 65535
  * hard nofile 65535
  ```

### Adjusting Maximum Process Number / Maximum Thread Number

- **Temporary Effect**
  ```shell
  ulimit -u 65535
  ```

- **Permanent Effect**
  ```shell
  sudo vim /etc/security/limits.conf
  ```
  Add the following content:
  ```
  * soft nproc 65535
  * hard nproc 65535
  ```

### Notes
- **Soft Limit**: Users can exceed this value, but cannot exceed the hard limit.
- **Hard Limit**: Users cannot exceed this value, nor can they be lower than the soft limit.

The `/etc/sysctl.conf` file belongs to system-level kernel parameters and requires a restart to take effect.
The `/etc/security/limits.conf` file belongs to user-level or process-level parameters and requires a re-login to take effect.

## 10. The Difference Between Load and CPU Usage

- **Load**: The average load refers to the average number of processes in the system that are in a state of runnable (R) and uninterruptible (D) (average active process count) within a unit of time.
- **CPU Usage**: The CPU usage refers to the proportion of the total time that the CPU is processing tasks within a unit of time.

The ideal situation: the average load is equal to the number of CPU cores, and there is a process on each core.

```shell
Check the number of CPU cores
grep 'model name' /proc/cpuinfo | wc -l

uptime
 06:44:50 up 190 days, 22:44,  4 users,  load average: 0.42, 0.14, 0.04
```

### Relationship Between the Two

- **CPU-Intensive Processes**: Using a lot of CPU will cause the average load to rise, and these two are consistent.
- **I/O-Intensive Processes**: Waiting for I/O will also cause the average load to rise, but the CPU usage may not be very high.
- **A Large Number of Waiting CPU Processes**: Scheduling processes will also cause the average load to rise, and the CPU usage will also be relatively high.

## 11. Why du and df Show Different Disk Usage Results

In the system, there may be a large number of deleted files (zombie files), and there are running processes using these file handles.

When a file is deleted, if a process is still using the file, du will not count this part of the space because the file has been removed from the directory structure; however, df will count this part of the space because the disk space is actually still being occupied.

### Solution

- **Reboot the system**: Rebooting the system can clear all unused file handles, including zombie files.
- **Find and close the process**: Use tools like lsof or fuser to find and close the process using the zombie file.
  ```shell
  lsof | grep deleted
  ```
- **Manually delete the file**: If the process cannot be closed, the file must be manually deleted. However, be careful that all processes using the file will not work normally after the file is deleted.
- **Kill the process**

## 12. The Difference Between Hard Links and Soft Links

Hard links and soft links are two different types of file system links used to share files between directories.

### Hard Links

- **a.** Multiple files with the same inode node number are mutually hard linked files;
- **b.** Hard linked files are another entry point for the file;
- **c.** Hard links can be set up for files to prevent important files from being deleted by mistake;
- **d.** Deleting a hard link file or deleting the source file will not delete the file entity, and it will only take effect when both are deleted.

### Soft Links

- **a.** Similar to the shortcut in Windows systems;
- **b.** Soft links store the path to the source file, pointing to the source file;
- **c.** Deleting the source file, the soft link still exists, but cannot access the content of the source file;
- **d.** Soft links and source files are different files, and the file types are also different, and the inode number is also different;

## 13. How to Partition LVM

- **Create Physical Volume (PV)**
- **Create Volume Group (VG)**
- **Create Logical Volume (LV)**
- **Format Logical Volume (LV)**
- **Mount Logical Volume (LV)**

In public cloud operations, it is rare to see LVM partitioning disks, which is actually completely normal and is an industry trend.
- Cloud disks can be expanded directly, so there is no need for LVM's PV/VG/LV.
- Traditional LVM is often used for RAID1 (mirroring) and RAID0 (performance enhancement). However, cloud disks at the bottom are already multi-replicated and provide high performance through SSD.
- K8s weakens the use of LVM, with the root disk running the system and data stored in PVC.

## 14. How to Create and Manage Custom systemd Services

The location of the custom service configuration file is `/etc/systemd/system/`.

After creating or modifying the unit file, you need to reload the configuration to take effect.
```shell
sudo systemctl daemon-reload
```

## 15. What is /proc in the Linux System

/proc is an interface for user and kernel interaction, and the source of performance tool data (top, free, ps).

```shell
The complete command to start the current process
/proc/进程号/cmdline

The list of environment variables of the current process
/proc/2422772/environ
```

The output of /proc files is generated in C language and its derivatives, and needs to be separated to output normally.
```shell
cat /proc/3824/cmdline | tr '\0' '\n'
```

## 16. Use Cases of lsof Command

- **View the files opened by a process**
  ```shell
  lsof -p 1234
  ```
- **View which process is using a specific port**
  ```shell
  lsof -i :80
  ```
- **View all network connections**
  ```shell
  lsof -i
  ```
- **View the files opened by a user**
  ```shell
  lsof -u username
  ```
- **File has been deleted, but still occupied by a process**
  ```shell
  lsof | grep deleted
  ```