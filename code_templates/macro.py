from DesktopAutomationFramework import vars, keyboard, key, windows, files, gui, Macro, wait, end, pause

@Macro()
def macro():
    # Write your macro code here. 
    # Use ctrl+space on the library objects to see the available functions
    
    vars.getNumber("num")
    vars.getNumber("num2", accepted_values=[1, 5, 2132])
    
    vars.getString("str")
    vars.getString("str2", accepted_values=["a", "b", "c", "d"])
    
    
    end()