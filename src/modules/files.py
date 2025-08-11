#Command: files createDir [path\directory name]
#Command: files create [path\file name]
#Command: files createPdf [path\file name] [content] [title]
#Command: files createDoc [path\file name] [content] [doc_type]
#Command: files write [path\file name] [content]
#Command: files read [path\file name]
#Command: files delete [path\file name]
#Command: files copy [source path] [destination path]
#Command: files move [source path] [destination path]
#Command: files rename [path] [old name] [new name]
#Command: files list [path] [date_filter] [show_details]
#Command: files search [path] [file name]


import os
import shutil


def create_pdf(path, content, title="Document"):
    """Create a PDF file with the given content."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        
        # Ensure the path has .pdf extension
        if not path.lower().endswith('.pdf'):
            path += '.pdf'
        
        # Create the PDF document
        doc = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = styles['Title']
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Add content
        normal_style = styles['Normal']
        # Split content by paragraphs and add each as a separate paragraph
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), normal_style))
                story.append(Spacer(1, 6))
        
        # Build the PDF
        doc.build(story)
        return f"PDF created at {path}."
        
    except ImportError:
        return "Error: reportlab library not installed. Please install it with: pip install reportlab"
    except Exception as e:
        return f"Error creating PDF: {str(e)}"


def create_document(path, content, doc_type="txt"):
    """Create various document types."""
    doc_type = doc_type.lower()
    
    if doc_type == "pdf":
        return create_pdf(path, content)
    
    elif doc_type == "html":
        if not path.lower().endswith('.html'):
            path += '.html'
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Document</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #333; }}
        p {{ margin-bottom: 16px; }}
    </style>
</head>
<body>
    <h1>Document</h1>
    {content.replace(chr(10), '<br>')}
</body>
</html>"""
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(html_content)
            return f"HTML document created at {path}."
        except Exception as e:
            return f"Error creating HTML document: {str(e)}"
    
    elif doc_type == "md" or doc_type == "markdown":
        if not path.lower().endswith('.md'):
            path += '.md'
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"Markdown document created at {path}."
        except Exception as e:
            return f"Error creating Markdown document: {str(e)}"
    
    elif doc_type == "csv":
        if not path.lower().endswith('.csv'):
            path += '.csv'
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"CSV document created at {path}."
        except Exception as e:
            return f"Error creating CSV document: {str(e)}"
    
    elif doc_type == "json":
        if not path.lower().endswith('.json'):
            path += '.json'
        
        try:
            import json
            # Try to parse content as JSON to validate it
            if content.strip().startswith('{') or content.strip().startswith('['):
                json.loads(content)  # Validate JSON
            else:
                # If not JSON format, wrap it as a simple JSON object
                content = json.dumps({"content": content}, indent=2)
            
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"JSON document created at {path}."
        except json.JSONDecodeError:
            return "Error: Invalid JSON content provided."
        except Exception as e:
            return f"Error creating JSON document: {str(e)}"
    
    else:
        # Default to text file
        if not path.lower().endswith('.txt'):
            path += '.txt'
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"Text document created at {path}."
        except Exception as e:
            return f"Error creating text document: {str(e)}"


def parse_date_filter(date_filter):
    """Parse date filter into criteria for efficient filtering."""
    from datetime import datetime, timedelta
    import re
    
    try:
        if date_filter.startswith('>=') or date_filter.startswith('after:'):
            date_str = date_filter.replace('>=', '').replace('after:', '').strip()
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            return {'type': 'after', 'timestamp': target_date.timestamp()}
            
        elif date_filter.startswith('<=') or date_filter.startswith('before:'):
            date_str = date_filter.replace('<=', '').replace('before:', '').strip()
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            target_date = target_date.replace(hour=23, minute=59, second=59)
            return {'type': 'before', 'timestamp': target_date.timestamp()}
            
        elif date_filter.lower() == 'today':
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow = today + timedelta(days=1)
            return {'type': 'range', 'start': today.timestamp(), 'end': tomorrow.timestamp()}
            
        elif date_filter.lower() == 'yesterday':
            yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            today = yesterday + timedelta(days=1)
            return {'type': 'range', 'start': yesterday.timestamp(), 'end': today.timestamp()}
            
        elif date_filter.lower().startswith('last'):
            if 'days' in date_filter.lower():
                days_match = re.search(r'(\d+)', date_filter)
                if days_match:
                    days = int(days_match.group(1))
                    cutoff_date = datetime.now() - timedelta(days=days)
                    return {'type': 'after', 'timestamp': cutoff_date.timestamp()}
            elif 'week' in date_filter.lower():
                cutoff_date = datetime.now() - timedelta(weeks=1)
                return {'type': 'after', 'timestamp': cutoff_date.timestamp()}
            elif 'month' in date_filter.lower():
                cutoff_date = datetime.now() - timedelta(days=30)
                return {'type': 'after', 'timestamp': cutoff_date.timestamp()}
                
        else:
            # Exact date match
            target_date = datetime.strptime(date_filter, '%Y-%m-%d')
            start = target_date.timestamp()
            end = (target_date + timedelta(days=1)).timestamp()
            return {'type': 'range', 'start': start, 'end': end}
            
    except ValueError:
        return None


def check_date_match(file_timestamp, criteria):
    """Check if file timestamp matches the filter criteria."""
    if not file_timestamp or not criteria:
        return False
        
    if criteria['type'] == 'after':
        return file_timestamp >= criteria['timestamp']
    elif criteria['type'] == 'before':
        return file_timestamp <= criteria['timestamp']
    elif criteria['type'] == 'range':
        return criteria['start'] <= file_timestamp < criteria['end']
    
    return False


def filter_files_by_date(file_infos, date_filter):
    """Filter files by date. Supports various date formats and operators."""
    from datetime import datetime, timedelta
    import re
    
    try:
        # Parse different date filter formats
        if date_filter.startswith('>=') or date_filter.startswith('after:'):
            # Files modified on or after a specific date
            date_str = date_filter.replace('>=', '').replace('after:', '').strip()
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            target_timestamp = target_date.timestamp()
            return [f for f in file_infos if f["modified"] and f["modified"] >= target_timestamp]
            
        elif date_filter.startswith('<=') or date_filter.startswith('before:'):
            # Files modified on or before a specific date
            date_str = date_filter.replace('<=', '').replace('before:', '').strip()
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            # Add 24 hours to include the entire day
            target_date = target_date.replace(hour=23, minute=59, second=59)
            target_timestamp = target_date.timestamp()
            return [f for f in file_infos if f["modified"] and f["modified"] <= target_timestamp]
            
        elif date_filter.lower() == 'today':
            # Files modified today
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_timestamp = today.timestamp()
            tomorrow_timestamp = (today + timedelta(days=1)).timestamp()
            return [f for f in file_infos if f["modified"] and today_timestamp <= f["modified"] < tomorrow_timestamp]
            
        elif date_filter.lower() == 'yesterday':
            # Files modified yesterday
            yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            yesterday_timestamp = yesterday.timestamp()
            today_timestamp = (yesterday + timedelta(days=1)).timestamp()
            return [f for f in file_infos if f["modified"] and yesterday_timestamp <= f["modified"] < today_timestamp]
            
        elif date_filter.lower().startswith('last'):
            # Handle "last 7 days", "last week", "last month", etc.
            if 'days' in date_filter.lower():
                days_match = re.search(r'(\d+)', date_filter)
                if days_match:
                    days = int(days_match.group(1))
                    cutoff_date = datetime.now() - timedelta(days=days)
                    cutoff_timestamp = cutoff_date.timestamp()
                    return [f for f in file_infos if f["modified"] and f["modified"] >= cutoff_timestamp]
            elif 'week' in date_filter.lower():
                cutoff_date = datetime.now() - timedelta(weeks=1)
                cutoff_timestamp = cutoff_date.timestamp()
                return [f for f in file_infos if f["modified"] and f["modified"] >= cutoff_timestamp]
            elif 'month' in date_filter.lower():
                cutoff_date = datetime.now() - timedelta(days=30)
                cutoff_timestamp = cutoff_date.timestamp()
                return [f for f in file_infos if f["modified"] and f["modified"] >= cutoff_timestamp]
                
        else:
            # Exact date match (YYYY-MM-DD format)
            target_date = datetime.strptime(date_filter, '%Y-%m-%d')
            start_timestamp = target_date.timestamp()
            end_timestamp = (target_date + timedelta(days=1)).timestamp()
            return [f for f in file_infos if f["modified"] and start_timestamp <= f["modified"] < end_timestamp]
            
    except ValueError:
        # Invalid date format
        return None


def execute(args):
    if args is None or len(args) == 0:
        return("No command provided.")
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching


    if "createdir" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for directory creation.")
        try:
            # Create the directory
            os.makedirs(path)
            return(f"Directory created at: {path}")
        except FileExistsError:
            return(f"Error: Directory '{path}' already exists.")
        except PermissionError:
            return(f"Error: Permission denied to create directory at '{path}'.")
        except Exception as e:
            return(f"An error occurred: {e}")

    elif "createpdf" in command:
        path = args.get("path", None)
        content = args.get("content", "")
        title = args.get("title", "Document")
        
        if path is None:
            return("No path provided for PDF creation.")
        if not content:
            return("No content provided for PDF creation.")
        
        return create_pdf(path, content, title)

    elif "createdoc" in command:
        path = args.get("path", None)
        content = args.get("content", "")
        doc_type = args.get("doc_type", "txt")
        
        if path is None:
            return("No path provided for document creation.")
        if not content:
            return("No content provided for document creation.")
        
        return create_document(path, content, doc_type)

    elif "create" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for file creation.")
            return
        # Create the file
        open(f"{path}", "w").close()
        return(f"File created at {path}.")
        
    elif "write" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for file writing.")
        content  = args.get("content", None)  # Get the content from the arguments
        if content is None:
            return("No content provided for file writing.")
        
        # Write the content to the file
        with open(f"{path}", "w") as file:
            file.write(content)
        return(f"Content written to {path}.")

    elif "read" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for file reading.")
            return
        # Read the content of the file
        with open(f"{path}", "r") as file:
            content = file.read()
        return(f"Content of {path}:" f"\n{content}")

    elif "delete" in command:
       path = args.get("path", None)  # Get the path from the arguments
       if path is None:
            return("No path provided for file deletion.")
       # Delete the file
       try:
           os.remove(f"{path}")
       except FileNotFoundError:
            return(f"Error: File '{path}' not found.")
       except PermissionError:
            return(f"Error: Permission denied to delete file '{path}'.")
       return(f"File deleted from {path}.")

    elif "copy" in command:
        source_path = args.get("source_path", None)  # Get the source path from the arguments
        dest_path = args.get("destination_path", None)  # Get the destination path from the arguments
        if source_path is None or dest_path is None:
            return("Source or destination path not provided for file copying.")
        # Copy the file
        shutil.copy(f"{source_path}", f"{dest_path}")
        return(f"File copied from {source_path} to {dest_path}.")
    elif "move" in command:
        source_path = args.get("source_path", None)
        dest_path = args.get("destination_path", None)
        if source_path is None or dest_path is None:
            return("Source or destination path not provided for file moving.")        # Move the file
        shutil.move(f"{source_path}", f"{dest_path}")
        return(f"File moved from {source_path} to {dest_path}.")
    elif "rename" in command:
        path =  args.get("path", None)  # Get the path from the arguments
        old_name =  args.get("old_name", None)  # Get the old name from the arguments
        new_name =   args.get("new_name", None)  # Get the new name from the arguments
        if path is None or old_name is None or new_name is None:
            return("Path, old name or new name not provided for file renaming.")
        # Rename the file
        os.rename(f"{path}/{old_name}", f"{path}/{new_name}")
        return(f"File {old_name} renamed to {new_name} in {path}.")
    elif "list" in command:
        # Extract the path from the command
        path = args.get("path", None)
        date_filter = args.get("date_filter", None)  # Optional date filter
        show_details = args.get("show_details", True)  # Show creation/modification times
        
        if path is None:
            return("No path provided for listing files.")
        if not os.path.isdir(path):
            return(f"'{path}' is not a valid directory.")

        try:
            from datetime import datetime, timedelta
            import re
            
            files = os.listdir(path)
            total_files = len(files)
            
            # Parse date filter once if provided
            filter_criteria = None
            if date_filter:
                filter_criteria = parse_date_filter(date_filter)
                if filter_criteria is None:
                    return("Invalid date format. Please use YYYY-MM-DD format (e.g., 2025-07-23).")
            
            # Gather file info with smart filtering
            file_infos = []
            files_processed = 0
            matching_files = 0
            
            for file in files:
                file_path = os.path.join(path, file)
                try:
                    modified = os.path.getmtime(file_path)
                    is_dir = os.path.isdir(file_path)
                    
                    # If we have a date filter, check it immediately
                    if filter_criteria and not check_date_match(modified, filter_criteria):
                        continue  # Skip files that don't match date filter
                    
                    # File matches criteria, gather full info
                    if show_details:
                        created = os.path.getctime(file_path)
                        file_infos.append({
                            "name": file,
                            "created": created,
                            "modified": modified,
                            "is_dir": is_dir
                        })
                    else:
                        file_infos.append({
                            "name": file,
                            "created": None,
                            "modified": modified,
                            "is_dir": is_dir
                        })
                    
                    matching_files += 1
                        
                except Exception as e:
                    # If we can't get file info, still include it
                    file_infos.append({
                        "name": file,
                        "created": None,
                        "modified": None,
                        "is_dir": False
                    })

            # Sort by modified time, newest first (directories first)
            file_infos.sort(key=lambda x: (not x["is_dir"], -(x["modified"] if x["modified"] is not None else 0)))

            filter_text = f" (filtered by {date_filter})" if date_filter else ""
            result_lines = [f"Files in {path}{filter_text} (newest to oldest):"]
            
            if date_filter and matching_files < total_files:
                result_lines.append(f"Found {matching_files} files matching criteria out of {total_files} total files.")
            
            if not file_infos:
                result_lines.append("No files found matching the criteria.")
            else:
                for info in file_infos:
                    file_type = "[DIR]" if info["is_dir"] else "[FILE]"
                    if show_details and info["created"] is not None:
                        created_str = datetime.fromtimestamp(info["created"]).strftime('%Y-%m-%d %H:%M:%S')
                        modified_str = datetime.fromtimestamp(info["modified"]).strftime('%Y-%m-%d %H:%M:%S') if info["modified"] else "Unknown"
                        result_lines.append(f"- {file_type} {info['name']} (modified: {modified_str}, created: {created_str})")
                    else:
                        modified_str = datetime.fromtimestamp(info["modified"]).strftime('%Y-%m-%d %H:%M:%S') if info["modified"] else "Unknown"
                        result_lines.append(f"- {file_type} {info['name']} (modified: {modified_str})")
            
            return "\n".join(result_lines)
            
        except PermissionError:
            return(f"Error: Permission denied to access directory '{path}'.")
        except Exception as e:
            return(f"Error listing files: {str(e)}")

    elif "search" in command:
        # Extract the path and file name from the command
        path = args.get("path", None)
        file_name = args.get("file_name", None)
        if path is None or file_name is None:
            return("Path or file name not provided for file searching.")
        # Search for the file in the directory, and its subdirectories
        # return the path of the file if found or a message if not found
        for root, dirs, files in os.walk(path):
            if file_name in files:
                return(f"File found at: {os.path.join(root, file_name)}")
        else:
            return(f"File '{file_name}' not found in '{path}' or its subdirectories.")
    else:
        return("Files command not recognized.")

