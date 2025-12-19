---
categories:
- Operations Maintenance
date: 2025-11-27 03:02:53
description: Compiled the most commonly used Vim shortcuts and techniques in Linux
  system administration, including cursor movement, text editing, and split-screen
  operations, essential skills.
draft: false
tags:
- command
title: Vim Tips
---

# vim Common Commands

## Cursor Movement
- **h** or **Backspace**: Move left by one character  
- **l** or **Space**: Move right by one character  
- **j**: Move down by one line  
- **k**: Move up by one line  
- **gj**: Move to the next line within a paragraph  
- **gk**: Move to the previous line within a paragraph  
- **+** or **Enter**: Move to the first non-blank character of the next line  
- **-**: Move to the first non-blank character of the previous line  
- **w**: Move forward by one word, stopping at the start of the next word  
- **W**: Move forward by one word (ignoring some punctuation)  
- **e**: Move forward by one word, stopping at the end of the next word  
- **E**: Move forward by one word, stopping at punctuation (if any)  
- **b**: Move backward by one word, stopping at the start of the previous word  
- **B**: Move backward by one word (ignoring some punctuation)  
- **(**: Move forward by 1 sentence  
- **)**: Move backward by 1 sentence  
- **{**: Move forward by 1 paragraph  
- **}**: Move backward by 1 paragraph  
- **gg**: Move to the beginning of the file  
- **G**: Move to the end of the file  
- **$**: Move to the end of the line  
- **0**: Move to the beginning of the line  

## Scrolling
- **Ctrl + f**: Scroll down one screen  
- **Ctrl + b**: Scroll up one screen  
- **Ctrl + d**: Scroll down half a screen  
- **Ctrl + u**: Scroll up half a screen  
- **Ctrl + e**: Scroll down one line  
- **Ctrl + y**: Scroll up one line  
- **n%**: Go to n% of the file  
- **zz**: Move the current line to the center of the screen  
- **zt**: Move the current line to the top of the screen  
- **zb**: Move the current line to the bottom of the screen  

## Insertion
- **I**: Insert at the first non-blank character of the current line  
- **gI**: Insert at the first column of the current line  
- **a**: Insert after the cursor  
- **A**: Insert at the end of the current line  
- **o**: Insert a new line below and move to it  
- **O**: Insert a new line above and move to it  
- **:r filename**: Insert the contents of another file at the current position  
- **:[n]r filename**: Insert the contents of another file at line n  

## Cutting and Copying
- **[n]x**: Cut n characters to the right of the cursor (equivalent to d[n]l)  
- **[n]X**: Cut n characters to the left of the cursor (equivalent to d[n]h)  
- **y**: Copy the text in visual mode  
- **yy** or **Y**: Copy the entire line  
- **y[n]w**: Copy n words  
- **y[n]l**: Copy n characters to the right of the cursor  
- **y[n]h**: Copy n characters to the left of the cursor  
- **y$**: Copy from the cursor to the end of the line  
- **y0**: Copy from the cursor to the beginning of the line  
- **:m,ny**: Copy lines m to n  
- **y1G** or **ygg**: Copy all lines above the cursor  
- **yG**: Copy all lines below the cursor  
- **d**: Delete (cut) the text in visual mode  
- **d$** or **D**: Delete to the end of the line  
- **d[n]w**: Delete n words  
- **d[n]l**: Delete n characters to the right of the cursor  
- **d[n]h**: Delete n characters to the left of the cursor  
- **d0**: Delete to the beginning of the line  
- **p**: Paste after the cursor  
- **P**: Paste before the cursor  

## Searching and Replacing
- **/something**: Search for "something" forward  
- **?something**: Search for "something" backward  
- **n**: Search for the next occurrence  
- **N**: Search for the previous occurrence  
- s/old/new: Replace the first occurrence of "old" in the current line  
- s/old/new/g: Replace all occurrences of "old" in the current line  
- **%s/old/new/g**: Replace all occurrences of "old" in the entire file  

## Tips
- **:set paste**: Solve the problem of formatting errors when pasting