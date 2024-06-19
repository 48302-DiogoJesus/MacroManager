from DesktopAutomationFramework import vars, keyboard, key, windows, files, gui, Macro, wait, end

@Macro(interval_s=2.5) # You can increase this while testing and decrease later
def macro():
    # GETTING INVOCATION VARIABLES #

    ## if script is called like: pythonw macro.py reports_number=10
    ## ! NOTE: decimal values are accepted. Ex: pythonw macro.py reports_number=2.3
    reports_number = vars.getNumber("reports_number")
    ## if script is called like: pythonw macro.py macro_variant="variant 1"
    ## ! NOTE: when calling the script use " " if your values have spaces, as shown in the comment above
    variant: str = vars.getString("macro_variant", accepted_values=["variant 1", "variant 2"])
    ## if script is called like: pythonw macro.py location=FA
    location: str = vars.getString("location", accepted_values=["LX", "FA", "PT"])

    # KEYBOARD OPERATIONS #

    keyboard.keys(key.win)
    keyboard.write("notepad")
    keyboard.keys(key.shift, key.right, repeat_times=5, repeat_interval_s=2)

    # INTERACT WITH WINDOWS #

    ## waits for a window containing the title "notepad" to be active within 2 seconds
    windows.wait("notepad", timeout_s=2)
    ## selects the window containing the title "notepad"
    windows.select("notepad")

    # FILE OPERATIONS #

    ## Show the output folder in Windows File Explorer 
    files.show(vars.output_folder)
    ## Opens "C:\users\<your_user>\my_file.csv" on Excel (default program)
    files.show(vars.user_dir + "\\my_file.csv")
    files.createFile(vars.output_folder + "\\file.txt")
    ## Create a file and write to it
    files.createFile(
        vars.output_folder + "\\file.txt", 
        "First line",
        "Second line"
    )
    files.createFolder(vars.output_folder + "\\CSV_Files")
    ## Delete a file/folder
    files.delete(vars.output_folder)
    files.delete(vars.output_folder + "\\file.txt")
    ## Check if file/folder exists
    output_folder_exists: bool = files.exists(vars.output_folder)
    file_content: str = files.read(vars.output_folder + "\\file.txt")
    ## Gets file content separated into lines
    file_lines: list[str] = files.readLines(vars.output_folder + "\\file.txt")

    # INPUT (USER INTERFACES) #

    ## Show a message
    gui.show("First Stage Complete")
    ## Ask user if he wants to proceed. If the answer is NO, end the macro
    should_proceed: bool = gui.confirm("First Stage Complete. Do you want to proceed?")
    if not should_proceed:
        end()
    name: str = gui.ask("What is your name?")
    option_selected: str = gui.options("Variant 1", "Variant 2", "Variant 3", "Variant 4")

    # OTHER OPERATIONS (MORE GENERIC) #

    ## Pause the execution for 4 seconds
    wait(4)
    ## Finish the macro execution earlier that the end of the function
    end()

macro()
