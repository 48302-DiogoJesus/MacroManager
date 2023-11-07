import type { IMacroManager, InvocationVariableDetails, InvocationVariableName } from './IMacroManager';
import type { Folder } from './FileSystemTree';
import os from "os";
import { getLatestMacroLogs, getMacrosFlat } from './FileSystemUtils';
import { exec } from "child_process"
import path from 'path';
import fs from 'fs-extra';
import { macroTemplate } from './macro-template';
import { replaceMacroInterval } from './myUtils';

const MacrosPath = os.userInfo().homedir + '\\MacroManager';
const DEFAULT_MACRO_NAME = "macro.py"

export const MacroManager: IMacroManager = {
    // Returns the full path of the macro
    createMacro: function (macro_name: string): string {
        const folderFullPath = path.join(MacrosPath, macro_name);
        const pythonFilePath = path.join(folderFullPath, DEFAULT_MACRO_NAME);

        // Create the macro folder
        fs.mkdirSync(folderFullPath);

        // Create template macro file
        fs.writeFileSync(pythonFilePath, macroTemplate);

        return pythonFilePath;
    },

    openMacrosFolder: () => exec(`explorer "${MacrosPath}"`),
    openMacroInCodeEditor: (absoluteMacroPath: string) => exec(`code "${absoluteMacroPath}"`),
    openMacroInFileExplorer: (absoluteMacroPath: string) => exec(`explorer "${path.dirname(absoluteMacroPath)}"`),
    openTaskScheduler: () => exec(`taskschd.msc`),

    getMacrosFlat: () => getMacrosFlat(MacrosPath),

    getMacrosFolderTreeLike: function (): Promise<Folder> {
        throw new Error('Implement Later');
    },

    getLatestMacroLogs: getLatestMacroLogs,

    getMacroInvocationVariablesMetadata: (absoluteMacroPath: string) => {
        const usefulLines = fs.readFileSync(absoluteMacroPath, { encoding: 'utf-8' })
            .split('\n')
            .filter(line => line.includes('vars.getNumber(') || line.includes('vars.getString('));

        const invocationVariablesMetadata: { [key: InvocationVariableName]: InvocationVariableDetails } = {}

        for (const line of usefulLines) {
            let varname: InvocationVariableName
            let type: InvocationVariableDetails["type"]
            let accepted_values: InvocationVariableDetails["accepted_values"]

            const parts = line.split('(');
            const functionCall = parts[0].trim()
            if (functionCall.includes("vars.getNumber")) {
                type = "number"
            } else if (functionCall.includes("vars.getString")) {
                type = "string"
            }

            let args = parts[1].substring(1)
            varname = args.split("\"")[0]
            args = args.replace(`${varname}"`, "")

            let s: any = args.replace("\r", "").slice(0, -1)
            // Has a second parameter (accepted_values)
            if (s.charAt(0) == ",") {
                s = s.substring(1).trim()
                if (s.startsWith("accepted_values=")) {
                    s = s.replace("accepted_values=", "")
                }
                s = s.replace("[", "").replace("]", "")
                s = s.split(",").map((item: string) => item.trim().replaceAll("\"", ""))
                accepted_values = s
            }
            // Any value is accepted
            else {
                accepted_values = null
            }

            invocationVariablesMetadata[varname] = {
                type, accepted_values
            }
        };
        return invocationVariablesMetadata
    },

    runMacro: (
        absoluteMacroPath: string,
        invocationVariables: { [key: string]: string } = {},
        timeBetweenInstructionsS?: string
    ) => {
        if (timeBetweenInstructionsS) {
            // Change Python code
            const newMacroContent = fs.readFileSync(absoluteMacroPath, { encoding: "utf-8" })
                .split('\n')
                .map(line =>
                    line.startsWith("@Macro(")
                        ? replaceMacroInterval(line, timeBetweenInstructionsS)
                        : line).join("\n")

            fs.writeFileSync(absoluteMacroPath, newMacroContent, { encoding: "utf-8" })
        }

        const keyValuePairs = Object.entries(invocationVariables).map(([key, value]) => `${key}="${value}"`).join(' ');
        const command = `pythonw "${absoluteMacroPath}" ${keyValuePairs}`
        exec(command)
    },

    shouldUpdateFramework: function (): Promise<boolean> {
        throw new Error('Function not implemented.');
    },
    shouldUpdateManager: function (): Promise<boolean> {
        throw new Error('Function not implemented.');
    },

    updateFramework: function (): Promise<void> {
        throw new Error('Function not implemented.');
    },
    updateManager: function (): Promise<void> {
        throw new Error('Function not implemented.');
    }
}