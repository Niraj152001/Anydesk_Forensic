# Anydesk_Forensic
Here's a complete `README.md` template for your AnyDesk forensic tool project. This will include installation instructions, features, and usage details.

```markdown
# AnyDesk Forensics Tool

This tool is designed to help digital forensics investigators analyze AnyDesk artifacts, such as trace logs, configuration files, and thumbnails. It allows you to view, search, and export AnyDesk-related data for forensic analysis.

## Features

- **Log file parsing**: View and analyze important AnyDesk log files (`ad.trace`, `ad_svc.trace`, `connection_trace.txt`).
- **System configuration analysis**: Read and parse the `system.conf` file.
- **Thumbnails Viewer**: View AnyDesk-related thumbnails from the `thumbnails` folder.
- **Dark Mode**: Toggle between light and dark modes for better UI experience.

2. Install the dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can run the tool in two ways: via command-line interface (CLI) or through the graphical user interface (GUI).

### Running the Tool via GUI

1. Run the tool by executing:

   ```bash
   python anydesk_forensics_tool.py
   ```

2. The GUI will open with buttons for different features:
   - View the contents of `ad.trace`, `ad_svc.trace`, `connection_trace.txt`, and `system.conf`.
   - View AnyDesk-related thumbnails in the `thumbnails` folder.
   - Toggle between light and dark modes.
   - Export the parsed data to CSV or Excel.

### Running the Tool via CLI

You can use the CLI to directly show logs or export the data. Run the following commands:

```bash
python anydesk_forensics_tool.py --trace ad.trace
python anydesk_forensics_tool.py --trace ad_svc.trace
python anydesk_forensics_tool.py --trace connection_trace.txt
python anydesk_forensics_tool.py --system_conf
python anydesk_forensics_tool.py --export_csv
python anydesk_forensics_tool.py --export_excel
```

#### Available Arguments:
- `--trace`: Show specific AnyDesk trace log files (`ad.trace`, `ad_svc.trace`, `connection_trace.txt`).
- `--system_conf`: Show the contents of the `system.conf` configuration file.
- `--export_csv`: Export the parsed data to a CSV file.
- `--export_excel`: Export the parsed data to an Excel file.

## File Locations

The tool automatically looks for AnyDesk files in the following default location:

- **Windows**: `C:\Users\<Your-Username>\AppData\Roaming\AnyDesk`
  - Trace files like `ad.trace`, `ad_svc.trace`, `connection_trace.txt`
  - `system.conf`
  - Thumbnails folder (for images)

If the tool does not find the AnyDesk folder, it will display an error message.

## Troubleshooting

- **AnyDesk folder not found**: Ensure that AnyDesk is installed and the relevant logs are in the expected location (`AppData\Roaming\AnyDesk`).
- **Error parsing files**: The tool may fail to read corrupted or invalid files. Check for file integrity or access issues.
- **Export not working**: Ensure that `pandas` is properly installed and the script has write permissions to save files.

## Contributing

If you'd like to contribute to the project, feel free to open issues or submit pull requests. All contributions are welcome!

## License

This tool is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

### Contact

For any inquiries, you can reach me at [your-email@example.com].

```

### Explanation:

- **Installation Instructions**: Clear steps to install dependencies.
- **Feature Overview**: Describes the tool's main functionalities.
- **Usage**: Detailed instructions on how to run the tool via GUI and CLI, with the corresponding command arguments.
- **File Locations**: Specifies the default folder where the AnyDesk files should be located.
- **Troubleshooting**: Basic troubleshooting tips.
- **Contributing**: Encourages others to contribute to the tool.
- **License**: Open-source license (MIT in this case).
  
Feel free to customize any section (e.g., license, email) according to your project specifics!
